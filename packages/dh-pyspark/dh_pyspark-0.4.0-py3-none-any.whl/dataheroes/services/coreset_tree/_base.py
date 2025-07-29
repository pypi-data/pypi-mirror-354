import copy
import inspect
import io
import itertools
import json
import os
import pathlib
import time
import warnings
from collections import defaultdict
from concurrent import futures
from datetime import datetime
from functools import reduce
from typing import Dict, Union, Iterable, Iterator, Callable, Any, Tuple, Optional, List
from concurrent.futures import wait
import joblib
import numpy as np
import pandas as pd
from numpy import ndarray
from scipy.sparse import csr_matrix, vstack
from sklearn.base import BaseEstimator
from sklearn.exceptions import FitFailedWarning
from sklearn.metrics import get_scorer
from threadpoolctl import threadpool_limits
from threading import Event

from dataheroes.core.coreset.common import is_percent

from dataheroes.data.storage.storage_manager import StorageManager

from .._coreset_service_base import CoresetServiceBase, DataManagerT
from ..common import (
    CoresetParams,
    DataTuningParamsClassification,
    FoldIterator,
    CategoricalEncoding,
    PreprocessingParams,
    CATEGORICAL_INFREQUENT,
    DataTuningParams,
)
from ..common import PreprocessingStage
from ..helpers import get_model_name
from ...configuration import DataHeroesConfiguration
from ...core.numpy_extra import filter_missing_and_inf
from ...core.tree.tree import DATA_MIX_THRESHOLD_DEFAULT, Node
from ...core.tree.utils import evaluate_max_batch_size
from ...data import helpers
from ...core.helpers import unpack_params
from ...core.common import weight_processing
from ...core.tree import CoresetTree, TreeOptimizedFor, utils
from ...core.tree import utils as tree_utils
from ...core.tree.manager import TreeManager
from ...data import DataParams
from ...data.utils import serialize_function, deserialize_function
from ...data.common import Dataset
from ...data.data_auto_processor import DataAutoProcessor
from ...data.helpers import file_path_to_files, resolve_reader_chunk_size_param_name, iter_first, file_path_to_iterable, \
    df_to_iterable, joblib_dumps, jsonobj_to_bytes, np_to_bytes
from ...data.manager import get_min_data_cells_for_parallel_build
from ...utils import add_telemetry_attribute, telemetry, check_feature_for_license, _allow, _deny, _is_allowed
from ...common import can_use_threadpool_limits, get_parallel_executor

warnings.simplefilter('always', DeprecationWarning)


def _prepare_data_and_categories(X,
                                 ohe_cat_features_idxs, ohe_categories,
                                 te_cat_features_idxs, te_categories,
                                 replacement_for_infrequent):
    """
    For categories that after OHE have "infrequent" column, we should do
        1) replace in category [1, 3, 'infrequent'] -> [1, 3, non_existing_encoded_value]
        2) replace all values that are not in [1, 3] with non_existing_encoded_value
    non_existing_encoded_value = any numeric value that is does not exist in encoded data, we could use -2
    all this done to have both in categories and X only numeric data

    X - data either as DataFrame or numpy array
    categories[i] - array of categorical values, for example
         [array(['infrequent']),
         array([0, 1]),
         array([1, 2, 'infrequent']
         ]
    replacement_for_infrequent - what numeric value will be used for "infrequent" replacement
    categorical_features_idxs - indexes of categorical features in X (X can include not only categorical features).
        Therefore, len(categorical_features_idxs) = len(categories)
    """
    assert len(ohe_cat_features_idxs) == len(ohe_categories)
    assert len(te_cat_features_idxs) == len(te_categories)

    # OHE
    # we should not change input categories
    ohe_categories_prepared = [c.copy() for c in ohe_categories]
    # list of indexes of categories that include "infrequent" value
    ohe_categories_infrequent = [i for i, cat in enumerate(ohe_categories) if
                                 len(cat) > 0 and cat[-1] == CATEGORICAL_INFREQUENT]
    # replace "infrequent" value with non-existing index (in data and ohe_categories_prepared)
    for idx in ohe_categories_infrequent:
        # [1, 2, infrequent] -> [1, 2, replacement_for_infrequent] =[1, 2, -2]
        ohe_categories_prepared[idx][-1] = replacement_for_infrequent
        # index corresponding feature in X
        index_of_feature = ohe_cat_features_idxs[idx]
        # replace all values that are not in list by replacement_for_infrequent value
        if type(X) == pd.DataFrame:
            mask = np.isin(X.iloc[:, index_of_feature], ohe_categories_prepared[idx])
            X.iloc[:, index_of_feature] = np.where(mask, X.iloc[:, index_of_feature],
                                                   replacement_for_infrequent)
        else:
            mask = np.isin(X[:, index_of_feature], ohe_categories_prepared[idx])
            X[:, index_of_feature] = np.where(mask, X[:, index_of_feature], replacement_for_infrequent)
    for idx, _ in enumerate(ohe_categories_prepared):
        ohe_categories_prepared[idx] = np.sort(ohe_categories_prepared[idx])

    # TE
    # we should not change input categories
    te_categories_prepared = [c.copy() for c in te_categories]
    for idx, _ in enumerate(te_categories_prepared):
        te_categories_prepared[idx] = np.sort(te_categories_prepared[idx])

    return X, ohe_categories_prepared, te_categories_prepared


def requires_tree(func):
    def requires_tree_wrapper(self, *args, **kwargs):
        if not self.trees:
            raise RuntimeError("Invalid operation. Coreset tree must be built prior to using this operation.")
        return func(self, *args, **kwargs)

    return requires_tree_wrapper


def _xgboost_user_mode():
    import xgboost
    if xgboost.__version__ >= '2.0.0':
        return True


def _catboost_user_mode():
    import catboost
    if catboost.__version__ >= '1.1.1':
        return True


def calc_blas_limits(n_jobs: Optional[int]) -> int:
    limits = os.cpu_count() // n_jobs if n_jobs else os.cpu_count()
    assert isinstance(limits, int)
    return limits


class CoresetTreeService(CoresetServiceBase):
    """
    A service class for creating a coreset tree and working with it.
    optimized_for is a required parameter defining the main usage of the service: 'training', 'cleaning' or both,
    optimized_for=['training', 'cleaning'].
    The service will decide whether to build an actual Coreset Tree or
    to build a single Coreset over the entire dataset, based on the quadruplet:
    n_instances, n_classes, max_memory_gb and the 'number of features' (deduced from the dataset).
    The chunk_size and coreset_size will be deduced based on the above quadruplet too.
    In case chunk_size and coreset_size are provided, they will override all above mentioned parameters (less recommended).

    Parameters:
        data_manager: DataManagerBase subclass, optional.
            The class used to interact with the provided data and store it locally.
            By default, only the sampled data is stored in HDF5 files format.

        data_params: <a href="../../../data/common">DataParams</a>, optional. Data preprocessing information.

        n_instances: int.
            The total number of instances that are going to be processed (can be an estimation).
            This parameter is required (unless chunk_size and coreset_size are provided)
            and the only one from the above-mentioned quadruplet, which isn't deduced from the data.

        max_memory_gb: int, optional.
            The maximum memory in GB that should be used.
            When not provided, the server's total memory is used.
            In any case only 80% of the provided memory or the server's total memory is considered.

        optimized_for: str or list
            Either 'training', 'cleaning' or both ['training', 'cleaning'], by default 'training'.
            The main usage of the service.

        chunk_size: int, optional.
            The number of instances to be used when creating a coreset node in the tree.
            When defined, it will override the parameters of optimized_for, n_instances, n_classes and max_memory_gb.
            chunk_size=0:  Nodes are created based on input chunks.
            chunk_size=-1: Force the service to create a single coreset from the entire dataset (if it fits into memory).

        chunk_by: function, label, or list of labels, optional.
            Split the data according to the provided key.
            When provided, chunk_size input is ignored.

        data_tuning_params: <a href="https://data-heroes.github.io/dh-library/reference/services/data_tuning_params/">DataTuningParams</a> or dict, optional. Data tuning information.

        coreset_params: CoresetParams or dict, optional.
            Coreset algorithm specific parameters.

        node_train_function: Callable, optional.
            method for training model at tree node level.

        node_train_function_params: dict, optional.
            kwargs to be used when calling node_train_function.

        node_metadata_func: callable, optional.
            A method for storing user meta data on each node.

        working_directory: str, path, optional.
            Local directory where intermediate data is stored.

        cache_dir: str, path, optional.
            For internal use when loading a saved service.

        chunk_sample_ratio: float, optional.
            Indicates the size of the sample that will be taken and saved from each chunk on top of the Coreset for the validation methods.
            The values are from the range [0,1].
            For example, chunk_sample_ratio=0.5, means that 50% of the data instances from each chunk will be saved.

        model_cls: A Scikit-learn compatible model class, optional.
            The model class used to train the model on the coreset, in case a specific model instance wasn't passed to fit or the validation methods.
    """
    _tree_cls = CoresetTree
    _data_tuning_params_cls = DataTuningParams

    @telemetry
    def __init__(
            self,
            *,
            data_manager: DataManagerT = None,
            data_params: Union[DataParams, dict] = None,
            data_tuning_params: Union[DataTuningParams, dict] = None,
            n_instances: int = None,
            max_memory_gb: int = None,
            n_classes: Optional[int] = None,
            optimized_for: Union[list, str] = TreeOptimizedFor.training,
            chunk_size: Union[dict, int] = None,
            chunk_by: Union[Callable, str, list] = None,
            coreset_params: Union[CoresetParams, dict] = None,
            working_directory: Union[str, os.PathLike] = None,
            cache_dir: Union[str, os.PathLike] = None,
            node_train_function: Callable[[np.ndarray, np.ndarray, np.ndarray], Any] = None,
            node_train_function_params: dict = None,
            node_metadata_func: Callable[
                [Tuple[np.ndarray], np.ndarray, Union[list, None]], Union[list, dict, None]
            ] = None,
            chunk_sample_ratio: float = None,
            model_cls: Any = None,
    ):

        # Transform the parmas to the proper DataTuning params class. _data_tuning_params_cls is overwritten in child classes
        optimized_for = TreeOptimizedFor.check(optimized_for)
        if data_tuning_params is None:
            data_tuning_params = self._data_tuning_params_cls()
        elif isinstance(data_tuning_params, dict):
            data_tuning_params = self._data_tuning_params_cls(**(copy.deepcopy(data_tuning_params)))
        else:
            data_tuning_params = self._data_tuning_params_cls(**data_tuning_params.to_dict())
        if "cleaning" in optimized_for:
            data_tuning_params.check_for_cleaning()
        super().__init__(
            data_manager=data_manager,
            data_params=data_params,
            data_tuning_params=data_tuning_params,
            chunk_by=chunk_by,
            working_directory=working_directory,
            cache_dir=cache_dir,
        )

        if not getattr(self, 'user_set_model', False):
            self.user_set_model = True if model_cls is not None else False

        if model_cls is not None:
            self.model_cls = model_cls

        # set coreset params
        coreset_params = unpack_params(coreset_params, optimized_for, params_class=self.coreset_params_cls)
        self.coreset_params = coreset_params

        if n_instances:
            self.data_manager.data_params.n_instances = n_instances
        if n_classes:
            self.data_manager.data_params.n_classes = n_classes

        self.data_manager.data_params.is_classification = self.is_classification
        is_training = True if 'training' in optimized_for else False
        new_chunk_sample_ratio = self._validate_and_set_default_chunk_sample_ratio(chunk_sample_ratio, is_training)
        self.save_all = True if new_chunk_sample_ratio >= 1.0 else False
        self.chunk_sample_ratio = new_chunk_sample_ratio
        if node_metadata_func:
            self.data_manager.schema.node_metadata_func = node_metadata_func

        self.params.update(
            {
                "data_tuning_params": data_tuning_params,
                "coreset_params": coreset_params,
                "chunk_size": chunk_size,
                "optimized_for": optimized_for if isinstance(optimized_for, list) else [optimized_for],
                "max_memory_gb": max_memory_gb,
                "chunk_sample_ratio": new_chunk_sample_ratio,
            }
        )

        self.node_train_function = node_train_function
        self.node_train_function_params = node_train_function_params

        self.tree_group_manager = None

        self._DH_DEBUG_MODE = os.getenv("_DH_DEBUG_MODE", False)

        # If for at least one tree the coreset size is provided, chunk size must also be provided
        if isinstance(data_params, dict):
            seq_col_chunk_by = data_params.get('seq_column', {}).get('chunk_by')
        elif isinstance(data_params, DataParams):
            seq_col_chunk_by = getattr(data_params, 'seq_column', None)
        else:
            seq_col_chunk_by = getattr(data_manager.data_params_internal, 'seq_chunk_by',
                                       False) if data_manager else None

        # flag that indicates that there is some kind of chunking set
        chunking_set = chunk_size is not None or chunk_by is not None or seq_col_chunk_by is not None

        # this covers the case when only n_instances and coreset_size are specified
        # for example n_instaces = 100_000, coreset_size = 0.2, [chunk_size,chunk_by]=None
        # in this case we need to verify that the coreset size is a relative value
        for size in data_tuning_params.coreset_size:
            if not chunking_set and size is not None and n_instances is not None:
                # check that the coreset size is a relative value (a float value < 1)
                if not is_percent(size):
                    raise ValueError(
                        "When chunk_size is not provided, the coreset_size argument must be a float smaller than 1,"
                        " representing the ratio between the chunk_size and the resulting coreset."
                    )
            # this covers the case where the coreset size is specified alone, without any chunk param or n_instances
            if size is not None and n_instances is None and not chunking_set:
                raise RuntimeError(
                    "When `coreset_size` is provided, a valid `chunk_size` or `chunk_by` or `n_instances`"
                    " argument must also be provided."
                )

        # If chunk_by is provided, the coreset size should also be provided
        if any(size is None for size in data_tuning_params.coreset_size) and (chunk_by is not None):
            raise RuntimeError("When `chunk_by` is provided, a valid `coreset_size` argument must also be provided.")

    @property
    def trees(self) -> List[CoresetTree]:
        return self.tree_group_manager.trees if self.tree_group_manager else []

    @property
    def _cleaning_tree_idx(self) -> int:
        return 0

    @property
    def data_tuning_params(self):
        return self.params["data_tuning_params"]

    @property
    def optimized_for(self):
        return self.params['optimized_for']

    @property
    def chunk_size(self):
        return self.params['chunk_size']

    @property
    def max_memory_gb(self):
        return self.params['max_memory_gb']

    @property
    def chunk_layer(self):
        return self.tree_group_manager.chunk_layer

    @property
    def buffer(self):
        """
        Mask for testing purposes
        """
        return self.tree_group_manager.chunk_layer.get_buffer()

    @telemetry
    def set_model_cls(self, model_cls: Any):
        """
        Set the model class used to train the model on the coreset, in case a specific model instance wasn't passed to fit or the validation methods.

        Parameters:
            model_cls: A Scikit-learn compatible model class.
        """
        self.model_cls = model_cls
        self.user_set_model = True

    def _get_dtype(self) -> str:
        try:
            for optimized_for in self.optimized_for:
                return self.coreset_params[optimized_for].dtype
        except Exception:
            pass
        return 'float32'

    @telemetry
    def build_from_file(
            self,
            file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]],
            target_file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]] = None,
            *,
            reader_f: Callable = pd.read_csv,
            reader_kwargs: dict = None,
            reader_chunk_size_param_name: str = None,
            local_copy_dir: str = None,
            seq: Any = None,
            n_jobs: int = None,
            verbose: int = 1,
    ) -> 'CoresetTreeService':
        """
        Create a coreset tree based on data taken from local storage.
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions. Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            file_path: file, list of files, directory, list of directories.
                Path(s) to the place where data is stored.
                Data includes features, may include targets and may include indices.
                The paths can be local or on AWS S3, Google Cloud Platform Storage, Azure Storage

            target_file_path: file, list of files, directory, list of directories, optional.
                Use when the dataset files are split to features and target.
                Each file should include only one column.
                The target will be ignored when the Coreset is built.
                The paths can be local or on AWS S3, Google Cloud Platform Storage, Azure Storage

            reader_f: pandas like read method, optional, default pandas read_csv.
                For example, to read excel files use pandas read_excel.

            reader_kwargs: dict, optional.
                Keyword arguments used when calling reader_f method.

            reader_chunk_size_param_name: str, optional.
                reader_f input parameter name for reading file in chunks.
                When not provided we'll try to figure it out our self.
                Based on the data, we decide on the optimal chunk size to read
                and use this parameter as input when calling reader_f.
                Use "ignore" to skip the automatic chunk reading logic.

            local_copy_dir: str, optional
                If provided, files are copied to this folder.
                Useful when the files are stored in the cloud and it's desired
                to keep a local copy of them.
                The local_copy_dir acts like a cache and files already there are
                not downloaded from the cloud.

            seq: Default: None. Assign a sequence to the data passed to the function.
                This option is available only if a seq_column has been defined with chunk_by=every_build.

            n_jobs: Default: number of CPUs. Number of jobs to run in parallel during build.

            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.

        Returns:
            self
        """

        reader_kwargs = (reader_kwargs or dict()).copy()
        first, file_path = iter_first(file_path_to_iterable(file_path))
        self._set_reader_chunk_size_param(first, reader_f, reader_kwargs, reader_chunk_size_param_name)
        return self._build_from_file(
            file_path, target_file_path,
            reader_f=reader_f,
            reader_kwargs=reader_kwargs,
            local_copy_dir=local_copy_dir,
            seq=seq,
            partial=False,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def partial_build_from_file(
        self,
        file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]],
        target_file_path: Union[
            Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]
        ] = None,
        *,
        reader_f: Callable = pd.read_csv,
        reader_kwargs: dict = None,
        reader_chunk_size_param_name: str = None,
        local_copy_dir: str = None,
        seq: Any = None,
        n_jobs: int = None,
        verbose: int = 1,
    ) -> "CoresetTreeService":
        """
        Add new samples to a coreset tree based on data taken from local storage.
        Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            file_path: file, list of files, directory, list of directories.
                Path(s) to the place where data is stored.
                Data includes features, may include targets and may include indices.
                The paths can be local or on AWS S3, Google Cloud Platform Storage, Azure Storage

            target_file_path: file, list of files, directory, list of directories, optional.
                Use when files are split to features and target.
                Each file should include only one column.
                The target will be ignored when the Coreset is built.
                The paths can be local or on AWS S3, Google Cloud Platform Storage, Azure Storage

            reader_f: pandas like read method, optional, default pandas read_csv.
                For example, to read excel files use pandas read_excel.

            reader_kwargs: dict, optional.
                Keyword arguments used when calling reader_f method.

            reader_chunk_size_param_name: str, optional.
                reader_f input parameter name for reading file in chunks.
                When not provided we'll try to figure it out our self.
                Based on the data, we decide on the optimal chunk size to read
                and use this parameter as input when calling reader_f.
                Use "ignore" to skip the automatic chunk reading logic.

            local_copy_dir: str, optional
                If provided, files are copied to this folder.
                Useful when the files are stored in the cloud and it's desired
                to keep a local copy of them.
                The local_copy_dir acts like a cache and files already there are
                not downloaded from the cloud.

            seq: Default: None. Assign a sequence to the data passed to the function.
                This option is available only if a seq_column has been defined with chunk_by=every_build.

            n_jobs: Default: number of CPUs. Number of jobs to run in parallel during build.

            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.

        Returns:
            self
        """
        reader_kwargs = (reader_kwargs or dict()).copy()
        first, file_path = iter_first(file_path_to_iterable(file_path))
        self._set_reader_chunk_size_param(first, reader_f, reader_kwargs, reader_chunk_size_param_name)
        return self._build_from_file(
            file_path, target_file_path,
            reader_f=reader_f,
            reader_kwargs=reader_kwargs,
            local_copy_dir=local_copy_dir,
            seq=seq,
            partial=True,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def build_from_df(
            self,
            datasets: Union[Iterator[pd.DataFrame], pd.DataFrame],
            target_datasets: Union[Iterator[Union[pd.DataFrame, pd.Series]], pd.DataFrame, pd.Series] = None,
            *,
            seq: Any = None,
            copy: bool = False,
            n_jobs: int = None,
            verbose: int = 1
    ) -> 'CoresetTreeService':
        """
        Create a coreset tree from pandas DataFrame(s).
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions. Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            datasets: pandas DataFrame or a DataFrame iterator.
                Data includes features, may include labels and may include indices and sample weights.

            target_datasets: pandas DataFrame or a DataFrame iterator, optional.
                Use when data is split to features and target.
                Should include only one column.
                The target will be ignored when the Coreset is built

            copy: boolean, default False.
                False (default) - Input data might be updated as result of this function and functions such as update_targets or update_features.
                True - Data is copied before processing (impacts memory).

            seq: Default: None. Assign a sequence to the data passed to the function.
                This option is available only if a seq_column has been defined with chunk_by=every_build.
                
            n_jobs: Default: number of CPUs. Number of jobs to run in parallel during build.

            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.

        Returns:
            self
        """
        return self._build_from_df(
            datasets,
            target_datasets,
            partial=False,
            seq=seq,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose
        )

    @telemetry
    def partial_build_from_df(
            self,
            datasets: Union[Iterator[pd.DataFrame], pd.DataFrame],
            target_datasets: Union[Iterator[pd.DataFrame], pd.DataFrame] = None,
            *,
            seq: Any = None,
            copy: bool = False,
            n_jobs: int = None,
            verbose: int = 1
    ) -> 'CoresetTreeService':
        """
        Add new samples to a coreset tree based on the pandas DataFrame iterator.
        Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            datasets: pandas DataFrame or a DataFrame iterator.
                Data includes features, may include targets and may include indices.

            target_datasets: pandas DataFrame or a DataFrame iterator, optional.
                Use when data is split to features and target.
                Should include only one column.
                The target will be ignored when the Coreset is built

            copy: boolean, default False.
                False (default) - Input data might be updated as result of this function and functions such as update_targets or update_features.
                True - Data is copied before processing (impacts memory).

            seq: Default: None. Assign a sequence to the data passed to the function.
                This option is available only if a seq_column has been defined with chunk_by=every_build.
                
            n_jobs: Default: number of CPUs. Number of jobs to run in parallel during build.

            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.
        Returns:
            self
        """
        return self._build_from_df(
            datasets,
            target_datasets,
            seq=seq,
            partial=True,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose
        )

    @telemetry
    def build(
            self,
            X: Union[Iterable, Iterable[Iterable]],
            y: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            sample_weight: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            indices: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            props: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            *,
            seq: Any = None,
            copy: bool = False,
            n_jobs: int = None,
            verbose: int = 1,
    ) -> "CoresetTreeService":
        """
        Create a coreset tree from the parameters X, y, indices and props (properties).
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions. Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            X: array like or iterator of arrays like.
                An array or an iterator of features. Categorical features are automatically encoded and missing values
                are automatically handled.

            y: array like or iterator of arrays like, optional.
                An array or an iterator of targets.
                The target will be ignored when the Coreset is built.

            sample_weight: array like or iterator of arrays like, optional.
                An array or an iterator of instance weights.

            indices: array like or iterator of arrays like, optional.
                An array or an iterator with indices of X.

            props: array like or iterator of arrays like, optional.
                An array or an iterator of properties.
                Properties, won’t be used to compute the Coreset or train the model, but it is possible to
                filter_out_samples on them or to pass them in the select_from_function of get_cleaning_samples.

            copy: boolean, default False.
                False (default) - Input data might be updated as result of this function and functions such as update_targets or update_features.
                True - Data is copied before processing (impacts memory).

            seq: Default: None. Assign a sequence to the data passed to the function.
                This option is available only if a seq_column has been defined with chunk_by=every_build.
                
            n_jobs: Default: number of CPUs. Number of jobs to run in parallel during build.

            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.

        Returns:
            self
        """
        datasets = self._convert_build_params(X, y, indices, sample_weight, props)

        return self._build(
            datasets,
            seq=seq,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose
        )

    @telemetry
    def partial_build(
            self,
            X: Union[Iterable, Iterable[Iterable]],
            y: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            sample_weight: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            indices: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            props: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            *,
            seq: Any = None,
            copy: bool = False,
            n_jobs: int = None,
            verbose: int = 1,
    ) -> "CoresetTreeService":
        """
        Add new samples to a coreset tree from parameters X, y, indices and props (properties).
        Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            X: array like or iterator of arrays like.
                An array or an iterator of features. Categorical features are automatically encoded and missing values
                are automatically handled.

            y: array like or iterator of arrays like, optional.
                An array or an iterator of targets.
                The target will be ignored when the Coreset is built.

            sample_weight: array like or iterator of arrays like, optional.
                An array or an iterator of instance weights.

            indices: array like or iterator of arrays like, optional.
                An array or an iterator with indices of X.

            props: array like or iterator of arrays like, optional.
                An array or an iterator of properties.
                Properties, won’t be used to compute the Coreset or train the model, but it is possible to
                filter_out_samples on them or to pass them in the select_from_function of get_cleaning_samples.

            copy: boolean, default False
                False (default) - Input data might be updated as result of this function and functions such as update_targets or update_features.
                True - Data is copied before processing (impacts memory).

            seq: Default: None. Assign a sequence to the data passed to the function.
                This option is available only if a seq_column has been defined with chunk_by=every_build.
                
            n_jobs: Default: number of CPUs. Number of jobs to run in parallel during build.

            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.

        Returns:
            self
        """
        datasets = self._convert_build_params(X, y, indices, sample_weight, props)

        return self._build(
            datasets,
            seq=seq,
            partial=True,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose
        )

    @telemetry
    def build_from_tensorflow_dataset(
            self,
            dataset: (Any, Any),
            *,
            seq: Any = None,
            verbose: int = 1
    ) -> 'CoresetTreeService':
        """
        Create a coreset tree based on the tf.data.Dataset.
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions.

        Parameters:
            dataset: tuple (tf.data.Dataset, tfds.core.DatasetInfo)
            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.
        """
        return self._build_from_tensorflow_dataset(
            dataset,
            seq=seq,
            verbose=verbose
        )

    @telemetry
    def partial_build_from_tensorflow_dataset(
            self,
            dataset: (Any, Any),
            *,
            seq: Any = None,
            verbose: int = 1
    ):
        """
        Add new samples to a coreset tree based on the tf.data.Dataset.

        Parameters:
            dataset: tuple (tf.data.Dataset, tfds.core.DatasetInfo)
            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.
        """
        return self._partial_build_from_tensorflow_dataset(
            dataset,
            seq=seq,
            verbose=verbose
        )

    @telemetry
    def build_from_tensor(
            self,
            dataset: Any,
            *,
            seq: Any = None,
            verbose: int = 1
    ):
        """
        Create a coreset tree based on the torch.Tensor.
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions.

        Parameters:
            dataset: torch.Tensor
            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.
        """
        return self._build_from_tensor(
            dataset,
            seq=seq,
            verbose=verbose
        )

    @telemetry
    def partial_build_from_tensor(
            self,
            dataset: Any,
            *,
            seq: Any = None,
            verbose: int = 1
    ):
        """
        Add new samples to a coreset tree based on the torch.Tensor.

        Parameters:
            dataset: torch.Tensor
            verbose: optional
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.
        """
        return self._partial_build_from_tensor(
            dataset,
            seq=seq,
            verbose=verbose
        )

    @telemetry
    def trees_data_tuning_params(self, as_df: bool = False) -> Union[pd.DataFrame, dict]:
        """
        Returns the specific data tuning params for each tree as a dictionary `{tree_idx: {param_name: param_value}}`.

        Parameters:
            as_df : bool, default=False
                True - Returns the data tuning params a dataframe with each param as a column

        Returns:
            Union[pd.DataFrame, dict]
        """
        self._requires_tree()
        tree_idx_to_param = {
            i: self._data_tuning_params_cls._filter(sample_params=tree.sample_params) for (i, tree) in
            enumerate(self.trees)
        }
        if as_df:
            return pd.DataFrame.from_dict(tree_idx_to_param, orient="index")
        else:
            return tree_idx_to_param

    @telemetry
    def build_from_databricks(
        self,
        query: Union[str, List[str]],
        target_query: Union[str, List[str]] = None,
        *,
        catalog: str = None,
        schema: str = None,
        http_path: str = None,
        seq: Any = None,
        local_copy_dir: pathlib.Path = None,
        n_jobs: int = None,
        verbose: int = 1,
    ):
        """
        Create a coreset tree from a Databricks SQL query.
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions. Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            query: Union[str, List[str]]
                A SQL query or a list of SQL queries.

            target_query: Union[str, List[str]], default=None
                A SQL query or a list of SQL queries. Use when the target is separate from the features. The target will be ignored when the Coreset is built.

            catalog: str, default=None
                The catalog to use for the query. If not passed, the one from the configuration file will be used

            schema: str, default=None
                The schema to use for the query. If not passed, the one from the configuration file will be used

            http_path: str, default=None
                The connector url to use for the query. Can be either an sql warehouse or a spark cluster. If not passed, the one from the configuration file will be used

            seq: Any, default=None
                The sequence to use for the query.

            local_copy_dir: pathlib.Path, default=None
                 The directory to save a local copy of the query or to load the local copy if it exists

            n_jobs: int, default=None
                The number of jobs to run in parallel.

            verbose: int, default=1
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.

        Returns:
            CoresetTreeService
                The coreset tree service.
        """

        return self._build_from_databricks(
            query,
            target_query=target_query,
            catalog=catalog,
            schema=schema,
            http_path=http_path,
            seq=seq,
            local_copy_dir=local_copy_dir,
            chunk_size=self.chunk_size,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    def partial_build_from_databricks(
        self,
        query: Union[str, List[str]],
        target_query: Union[str, List[str]] = None,
        *,
        catalog: str = None,
        schema: str = None,
        http_path: str = None,
        seq: Any = None,
        local_copy_dir: pathlib.Path = None,
        n_jobs: int = None,
        verbose: int = 1,
    ):
        """
        Add new samples to a coreset tree from a Databricks SQL query.
        Categorical features are automatically one-hot encoded or target encoded and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            query: Union[str, List[str]]
                A SQL query or a list of SQL queries.

            target_query: Union[str, List[str]], default=None
                A SQL query or a list of SQL queries. Use when the target is separate from the features. The target will be ignored when the Coreset is built.

            catalog: str, default=None
                The catalog to use for the query. If not passed, the one from the configuration file will be used

            schema: str, default=None
                The schema to use for the query. If not passed, the one from the configuration file will be used

            http_path: str, default=None
                The connector url to use for the query. Can be either an sql warehouse or a spark cluster. If not passed, the one from the configuration file will be used

            seq: Any, default=None
                The sequence to use for the query.

            local_copy_dir: pathlib.Path, default=None
                 The directory to save a local copy of the query or to load the local copy if it exists

            n_jobs: int, default=None
                The number of jobs to run in parallel.

            verbose: int, default=1
                The verbose level for printing build progress, 0 - silent, 1 - (default) print.

        Returns:
            CoresetTreeService
                The coreset tree service.
        """

        return self._build_from_databricks(
            query,
            target_query=target_query,
            catalog=catalog,
            schema=schema,
            http_path=http_path,
            seq=seq,
            local_copy_dir=local_copy_dir,
            chunk_size=self.chunk_size,
            partial=True,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def save(
            self,
            dir_path: Union[str, os.PathLike] = None,
            name: str = None,
            save_buffer: bool = True,
            override: bool = False,
            allow_pickle: bool = True,
    ) -> Union[str, os.PathLike]:
        """
        Save service configuration and relevant data to a local directory.
        Use this method when the service needs to be restored.

        Parameters:
            dir_path: string or PathLike, optional, default self.working_directory.
                A directory for saving service's files. Can be a local path or a path 
                to AWS S3, Google Cloud Platform Storage, Azure Storage.

            name: string, optional, default service class name (lower case).
                Name of the subdirectory where the data will be stored.

            save_buffer: boolean, default True.
                Save also the data in the buffer (a partial node of the tree)
                along with the rest of the saved data.

            override: bool, optional, default False.
                False: add a timestamp suffix so each save won’t override the previous ones.
                True: The existing subdirectory with the provided name is overridden.

            allow_pickle: bool, optional, default True.
                True: Saves the Coreset tree in pickle format (much faster).
                False: Saves the Coreset tree in JSON format.

        Returns:
            Save directory path.
        """
        self._requires_tree()
        check_feature_for_license("tree_save")
        # Assume we save all trees
        trees_params = [tree.get_params() for tree in self.trees]
        coreset_params = [tree.coreset_params for tree in self.trees]
        for tree, tree_param in zip(self.trees, trees_params):
            node_train_function = tree_param.pop("model_train_function", None)
            if self.service_params and self.service_params.get('node_train_function'):
                node_train_function = self.service_params['node_train_function']
            elif node_train_function:
                node_train_function = serialize_function(node_train_function)
            tree_param["model_train_function"] = node_train_function

        # IMPORTANT: since saving is done to JSON, and JSON dumping doesn't support ndarrays, some of the objects are
        # converted to lists. Upon their future retrieval, some code may rely on the fact that these objects are
        # ndarrays, and won't be able to work with lists. We need to take care of it upon retrieval.
        preprocessing_info = getattr(self, "preprocessing_info", None)
        if preprocessing_info is not None:
            preprocessing_info["ohe_used_categories"] = [e.tolist() for e in preprocessing_info["ohe_used_categories"]]
            preprocessing_info["te_used_categories"] = [e.tolist() for e in preprocessing_info["te_used_categories"]]
            preprocessing_info["te_encodings"] = [e.tolist() for e in preprocessing_info["te_encodings"]]
            if isinstance(preprocessing_info["te_classes"], np.ndarray):
                preprocessing_info["te_classes"] = preprocessing_info["te_classes"].tolist()

        service_params = {
            "tree_params": trees_params,
            "coreset_params": coreset_params,
            "node_train_function": node_train_function,
            "save_all": self.save_all,
            "chunk_index": self.chunk_layer.chunk_index,
            "preprocessing_info": preprocessing_info,
        }

        save_dir = self._save(dir_path, name, override, service_params=service_params, is_tree=True)

        tree_models, tree_data = [], []
        for tree in self.trees:
            data = tree.get_tree_data(allow_pickle=allow_pickle)
            assert isinstance(data, dict)
            model = data.pop('models', None)  # models are stored separately
            tree_data.append(data)
            tree_models.append(model)

        for i, tree in enumerate(self.trees):
            tree_name = f"tree_{i}"
            if allow_pickle:
                tree_data_path = self.storage_manager.joinpath(save_dir, f'{tree_name}.pkl')
                self.storage_manager.dump_bytes(joblib_dumps(tree_data), tree_data_path)
            else:
                tree_data_path = self.storage_manager.joinpath(save_dir, f'{tree_name}.json')
                self.storage_manager.dump_bytes(jsonobj_to_bytes(tree_data, tree_data_path))

            if tree_models:
                tree_nodes_models_dir = self.storage_manager.joinpath(save_dir, f'{tree_name}_nodes_models')
                self.storage_manager.mkdir(tree_nodes_models_dir, exist_ok=True)
                for model_data in tree_models:
                    if model_data:
                        model_id, model = model_data
                        path = self.storage_manager.joinpath(tree_nodes_models_dir, f"{model_id}")
                        self.storage_manager.dump_bytes(joblib_dumps(model), path)

        if save_buffer:
            buffer_path = self.storage_manager.joinpath(save_dir, 'buffer.npz')
            assert self.tree_group_manager is not None
            buffer = self.tree_group_manager.chunk_layer.get_buffer()
            if buffer:
                self.storage_manager.dump_bytes(np_to_bytes(buffer), buffer_path)

        save_dir = pathlib.Path(save_dir) if self.storage_manager.is_local(save_dir) else save_dir
        return save_dir

    @classmethod
    @telemetry
    def load(
            cls,
            dir_path: Union[str, os.PathLike],
            name: str = None,
            *,
            data_manager: DataManagerT = None,
            load_buffer: bool = True,
            working_directory: Union[str, os.PathLike] = None,
    ) -> 'CoresetTreeService':
        """
        Restore a service object from a local directory.

        Parameters:
            dir_path: str, path.
                A directory where service data is stored. Can be a local path or a path 
                to AWS S3, Google Cloud Platform Storage, Azure Storage.

            name: string, optional, default service class name (lower case).
                The name prefix of the subdirectory to load.
                When several subdirectories having the same name prefix are found, the last one, ordered by name, is selected.
                For example when saving with override=False, the chosen subdirectory is the last saved.

            data_manager: DataManagerBase subclass, optional.
                When specified, input data manger will be used instead of restoring it from the saved configuration.

            load_buffer: boolean, optional, default True.
                If set, load saved buffer (a partial node of the tree) from disk and add it to the tree.

            working_directory: str, path, optional, default use working_directory from saved configuration.
                Local directory where intermediate data is stored.

        Returns:
            CoresetTreeService object
        """
        storage_manager = StorageManager()

        service_params, load_dir = cls._load_params(
            dir_path,
            name,
            data_manager=data_manager,
            working_directory=working_directory,
        )

        class_params = service_params['class_params']

        # Load and prepare data
        model_path = storage_manager.joinpath(load_dir, "model.pickle")
        model = (
            joblib.load(storage_manager.read_bytes(model_path))
            if storage_manager.exists(model_path)
            else None
        )

        # init service
        service_obj = cls(**class_params, data_params=class_params['data_manager'].data_params)
        service_obj.model = model
        node_train_function_str = service_params['node_train_function']
        trees = []
        trees_params = service_params["tree_params"]
        # backward compatibility, replace sample_size with chunk_size
        if "sample_size" in trees_params:
            trees_params["chunk_size"] = trees_params["sample_size"]

        for i, tree_params in enumerate(trees_params):
            tree_name = f"tree_{i}"
            # load the tree data
            tree_data_path = storage_manager.joinpath(load_dir, f'{tree_name}.json')
            if storage_manager.exists(tree_data_path):
                tree_data = json.load(storage_manager.read_bytes(tree_data_path))
            else:
                tree_data_path = storage_manager.joinpath(load_dir, f'{tree_name}.pkl')
                tree_data = joblib.load(storage_manager.read_bytes(tree_data_path))

            # load node level models
            tree_nodes_models_dir = storage_manager.joinpath(load_dir, f'{tree_name}_nodes_models')
            if storage_manager.exists(tree_nodes_models_dir):
                models = []
                for model_path in storage_manager.iterdir(tree_nodes_models_dir):
                    if storage_manager.is_file(model_path):
                        model_name = storage_manager.stem(model_path)
                        model_data = storage_manager.read_bytes(model_path)
                        models.append((model_name, joblib.load(model_data)))
                tree_data[i]["models"] = models

            # load node train function
            if node_train_function_str:
                service_obj.service_params = dict(node_train_function=node_train_function_str)
                service_obj.node_train_function = deserialize_function(node_train_function_str)

            # init the tree with data
            # TODO Daci: better solution?
            which_params = "cleaning" if "cleaning" in class_params["optimized_for"] else "training"
            tree = service_obj._init_tree(tree_data=tree_data[i], which_params=which_params, sample_params=tree_params)
            trees.append(tree)

        # Initialise the TreeGroupManager
        service_obj._init_tree_group_manager(
            trees=trees, chunk_index=service_params.get("chunk_index")
        )  # will take chunk_size from the first tree
        assert service_obj.tree_group_manager is not None
        # load and set buffer
        buffer_path = storage_manager.joinpath(load_dir, 'buffer.npz')
        if load_buffer and storage_manager.exists(buffer_path):
            # TODO Razvan: is absolute path needed here for local?
            container = np.load(
                storage_manager.read_bytes(buffer_path), allow_pickle=True
            )
            buffer = [a if len(a.shape) > 0 else None for a in container.values()]
            service_obj.tree_group_manager.chunk_layer.set_buffer(buffer)
        service_obj.preprocessing_info = service_params["preprocessing_info"]
        return service_obj

    @telemetry
    def auto_preprocessing(self,
                           X: Union[Iterable, Iterable[Iterable]] = None,
                           sparse_output: bool = False,
                           copy: bool = False):
        """
        Apply auto-preprocessing on the provided prediction test data, similarly to the way it is done by the fit or
        get_coreset methods. Preprocessing includes handling missing values amd categorical encoding.

        Parameters:
            X: array like or iterator of arrays like.
                An array or an iterator of features.
            sparse_output: boolean, default False. When set to True, the function will create a sparse matrix
                after preprocessing.
            copy: boolean, default False.
                False (default) - Input data might be updated as result of this function.
                True - Data is copied before processing (impacts memory).

        Returns:
            A DataFrame of the preprocessed data.
        """
        self._requires_tree()

        orig_feature_names = [f.name for f in self.data_manager.data_params.features]
        features_out = self.preprocessing_info['features_out']
        preprocessing_params = PreprocessingParams.from_dict(self.preprocessing_info)

        # Get removed columns
        removed_features = preprocessing_params.missing_values_params.get('removed_features', [])
        removed_features_names = [orig_feature_names[i] for i in removed_features]

        array_features_names = [orig_feature_names[i] for i in
                                self.data_manager.data_params_internal.array_features_
                                if orig_feature_names[i] not in removed_features_names]

        # data_manager.data_params_internal.categorical_features_ retains the original feature names, including
        # the removed ones.
        categorical_column_names = [orig_feature_names[i] for i in
                                    self.data_manager.data_params_internal.categorical_features_
                                    if orig_feature_names[i] not in removed_features_names]

        # From orig to category-encoded
        if copy:
            X = X.copy()
        if isinstance(X, np.ndarray):
            # make sure that the columns are named
            X = pd.DataFrame(X, columns=orig_feature_names)
            # When loading from numpy and array features are preset all columns will be type O
            # we need to set the numeric values to type float
            if array_features_names is not None and len(array_features_names) > 0:
                convert_dict = {c: float for c in X.columns if
                                c not in array_features_names and c not in categorical_column_names}
                X = X.astype(convert_dict)

        # replace inf with NaN
        if len(array_features_names) > 0:
            not_arr_columns = [c for c in X.columns if c not in array_features_names]
            X.loc[:, not_arr_columns] = X[not_arr_columns].replace([np.inf, -np.inf], np.nan)
        else:
            X.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Compute missing values replacements
        missing_values_replacements = self.data_manager.data_params_internal.aggregated_missing_replacements
        for col_idx, replacement in preprocessing_params.missing_values_params['features'].items():
            missing_values_replacements[int(col_idx)] = replacement

        final_replacements = {}
        for col_idx, replacement in enumerate(missing_values_replacements):
            if replacement:
                # Numerical feature with a non-numerical replacement:
                if col_idx not in self.data_manager.data_params_internal.categorical_features_ \
                        and not isinstance(replacement, (int, float)):
                    raise ValueError(
                        f"Replacement for feature index {col_idx} is not numeric."
                    )
                final_replacements[X.columns[col_idx]] = replacement
            else:
                final_replacements[X.columns[col_idx]] = np.nan

        # As per pandas v2.1.0 silent upcasting for setitem-like operations is deprecated (see issue #1163)
        #   consequently, the call to fillna() is preceded by a call to convert_dtypes() with argument "dtype_backend='numpy_nullable'".
        #   The mentioned argument was added in pandas v2.0.0 (see https://pandas.pydata.org/pandas-docs/version/2.0/reference/api/pandas.DataFrame.convert_dtypes.html)
        if pd.__version__ >= "2.0":
            X = X.convert_dtypes(infer_objects=False, convert_string=False, convert_integer=False,
                                 convert_boolean=False, convert_floating=False, dtype_backend='numpy_nullable')
        X.fillna(value=final_replacements, inplace=True)

        if removed_features:
            X.drop(columns=removed_features_names, inplace=True)

        for col in categorical_column_names:
            X[col] = X[col].astype(str).where(X[col].notna(), pd.NA)

        all_orig_cats_without_removed = sorted(
            [k for k in self.data_manager.data_params_internal.categorical_features_ if k not in removed_features])
        all_curr_cats = sorted(
            preprocessing_params.ohe_cat_features_idxs + preprocessing_params.te_cat_features_idxs)  # flat list
        # all_orig_cats_without_removed and all_curr_cats are expected to be of exactly the same length.
        # todo Remove this assert in a later phase.
        assert len(all_orig_cats_without_removed) == len(all_curr_cats)
        all_curr_to_orig_cat_idx = {curr: all_orig_cats_without_removed[i] for i, curr in enumerate(all_curr_cats)}
        categorical_column_names_ohe = [orig_feature_names[all_curr_to_orig_cat_idx[i]] for i in
                                        preprocessing_params.ohe_cat_features_idxs]
        categorical_column_names_te = [orig_feature_names[all_curr_to_orig_cat_idx[i]] for i in
                                       preprocessing_params.te_cat_features_idxs]

        # Handle TE and array, if applicable.
        X_prep_te_ae = self._encode_te_ae_features(X, categorical_column_names_te, array_features_names,
                                                   orig_feature_names, preprocessing_params, sparse_output)

        # Handle OHE, if applicable.
        X_prep_ohe = self._encode_ohe_features(X_prep_te_ae, categorical_column_names_ohe, preprocessing_params,
                                               sparse_output)

        # add missing columns
        for col in features_out:
            if col not in X_prep_ohe.columns:
                X_prep_ohe[col] = 0

        # Verify the order after all transformations were done.
        # arrange columns according the features_out order
        X_prep_ohe = X_prep_ohe[features_out]
        return X_prep_ohe

    def _encode_te_ae_features(self, X, categorical_column_names_te, array_features_names,
                               orig_feature_names, preprocessing_params, sparse_output):

        if (self.data_manager.data_params.cat_encoding_method in (CategoricalEncoding.TE, CategoricalEncoding.MIXED)
                or array_features_names):

            cat_encoding_config = self.data_manager.cat_encoding_config_with_categories(
                preprocessing_params=preprocessing_params,
                ohe_categories=preprocessing_params.ohe_used_categories,  # This value won't be used eventually.
                te_categories=preprocessing_params.te_used_categories,
            )

            array_encoding_config = self.data_manager.array_encoding_config(preprocessing_params=preprocessing_params)

            # replace None values with an empty array
            for arr_feature in array_features_names:
                # replace None and nan values with array([])
                X.loc[X[arr_feature].isna(), arr_feature] = X.loc[
                    X[arr_feature].isna(), arr_feature].apply(lambda x: np.array([]))

            # Even if features were removed, we don't mind that, since in this case, the dap handles only the
            # categorical encoding (and not missing values), hence removed features are irrelevant, and therefore
            # the original feature names and categorical features indices are passed to the DAP. In any case,
            # any removed features are filtered out at the end of this method.
            dap = DataAutoProcessor(
                X=X,
                categorical_features=self.data_manager.data_params_internal.categorical_features_,
                array_features=self.data_manager.data_params_internal.array_features_,
                feature_names=orig_feature_names,
                cat_encoding_config=cat_encoding_config,
                array_encoding_config=array_encoding_config
            )

            # Although we set the value of sparse_threshold below, it actually has no effect whatsoever on TE-only
            # encoding, because TE always returns dense; so we might as well pass sparse_threshold=0 (to only
            # *symbolically* indicate that a dense output is expected), or simply omit this param.
            sparse_threshold = 1.0 if sparse_output else 0.01
            X_prep_te_ae = dap.handle_feature_encoding(sparse_threshold=sparse_threshold,
                                                       predict_context=True)

            array_generated_columns = dap.get_generated_array_feature_names()
            # Fuse the two processed sets, TE-related columns are replaced inside, and add the array features.
            # X_prep_te_ae encodes only TE and array features (no OHE),
            # and returns them first, before the numerical columns.
            for prep_te_ae_column_idx, column_name_te_ae in enumerate(
                    categorical_column_names_te + array_generated_columns):
                X[column_name_te_ae] = X_prep_te_ae[:, prep_te_ae_column_idx].astype(np.float32)
            if array_features_names is not None:
                # remove the original (un encoded) array columns:
                X = X[[c for c in X.columns if c not in array_features_names]]
        return X

    def _encode_ohe_features(self, X_prep_ae, categorical_column_names_ohe, preprocessing_params, sparse_output):

        if self.data_manager.data_params.cat_encoding_method in (CategoricalEncoding.OHE, CategoricalEncoding.MIXED):

            for idx, col in enumerate(categorical_column_names_ohe):
                X_prep_ae[col] = X_prep_ae[col].where(
                    X_prep_ae[col].isin(preprocessing_params.ohe_used_categories[idx]),
                    CATEGORICAL_INFREQUENT)

            # Apply OHE
            X_prep_ohe = pd.get_dummies(data=X_prep_ae, columns=categorical_column_names_ohe, dummy_na=True, dtype=int,
                                        sparse=sparse_output)
            X_prep_ohe = X_prep_ohe.loc[:, (X_prep_ohe != 0).any(axis=0)]
            return X_prep_ohe
        else:
            return X_prep_ae

    @telemetry
    def get_coreset(
            self,
            tree_idx: int = 0,
            level: int = 0,
            preprocessing_stage: Union[str, None] = "user",
            sparse_threshold: float = 0.01,
            as_df: bool = False,
            with_index: bool = False,
            seq_from: Any = None,
            seq_to: Any = None,
            save_path: Union[str, os.PathLike] = None,
    ) -> dict:
        """
        Get tree's coreset data in one of the preprocessing_stage(s) in the data preprocessing workflow.
        Use the level parameter to control the level of the tree from which samples will be returned.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional, default 0.
                Defines the depth level of the tree from which the coreset is extracted.
                Level 0 returns the coreset from the head of the tree with around coreset_size samples.
                Level 1 returns the coreset from the level below the head of the tree with around twice of the samples compared to level 0, etc.
                If the passed level is greater than the maximal level of the tree, the maximal available level is used.
            preprocessing_stage: string, optional, default `user`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **original** - Return the data as it was handed to the Coreset’s build function
                (The data_params.save_orig flag should be set for this option to be available).<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01.
                Returns the features (X) as a sparse matrix if the data density after preprocessing is below sparse_threshold,
                otherwise, will return the data as an array (Applicable only for preprocessing_stage=`auto`).
            as_df: boolean, optional, default False.
                When True, returns the X as a pandas DataFrame.
            with_index: boolean, optional, default False.
                Relevant only when preprocessing_stage=`auto`. Should the returned data include the index column.
            seq_from: string or datetime, optional, default None.
                The start sequence to filter samples by.
            seq_to: string or datetime, optional, default None.
                The end sequence to filter samples by.
            save_path: str, optional, default None.
                If provided, the coreset will be saved to the path which can be local or a path to AWS S3,
                Google Cloud Platform Storage, Azure Storage.
                If provided, as_df should be True. Otherwise, the coreset is generated a second time with as_df=True

        Returns:
            A dictionary representing the Coreset:
                ind: A numpy array of indices.
                X: A numpy array of the feature matrix.
                y: A numpy array of the target values.
                w: A numpy array of sample weights.
                n_represents: The number of instances represented by the coreset.
                features_out: A list of the output features, if preprocessing_stage=auto, otherwise None.
                props: A numpy array of properties, or None if not available.

        """
        if not _is_allowed():
            # get_coreset_size should work without license
            check_feature_for_license("get_coreset")
        self._requires_tree()
        coreset_data = self._get_tree_coreset(
            tree_idx=tree_idx,
            level=level,
            seq_from=seq_from,
            seq_to=seq_to,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            as_df=as_df,
            with_index=with_index,
            inverse_class_weight=True,
        )
        if save_path:
            # If as_df is False, _save_coreset must recompute the coreset
            save_coreset_data = coreset_data if as_df else None
            self._save_coreset(
                save_path,
                tree_idx=tree_idx,
                level=level,
                preprocessing_stage=preprocessing_stage,
                with_index=with_index,
                coreset_data=save_coreset_data,
            )
        return coreset_data

    @telemetry
    def get_coreset_size(
            self, tree_idx: int = 0, level: int = 0, seq_from: Any = None, seq_to: Union[str, datetime] = None
    ) -> int:
        """
        Returns the size of the tree's coreset data.
        Use the level parameter to control the level of the tree from which samples will be returned.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional, default 0.
                Defines the depth level of the tree from which the coreset is extracted.
                Level 0 returns the coreset from the head of the tree with around coreset_size samples.
                Level 1 returns the coreset from the level below the head of the tree with around twice of the samples compared to level 0, etc.
                If the passed level is greater than the maximal level of the tree, the maximal available level is used.
            seq_from: string or datetime, optional, default None.
                The start sequence to filter samples by.
            seq_to: string or datetime, optional, default None.
                The end sequence to filter samples by.

        Returns:
            int: coreset size
        """
        try:
            _allow()
            coreset = self.get_coreset(tree_idx=tree_idx, level=level, seq_from=seq_from, seq_to=seq_to)
        finally:
            _deny()
        return len(coreset.get('ind'))

    @telemetry
    def _save_coreset(
        self,
        file_path: Union[str, os.PathLike],
        tree_idx: int = 0,
        level: int = 0,
        preprocessing_stage: Union[str, None] = "user",
        with_index: bool = True,
        coreset_data: dict = None,
    ):
        """
        Get the coreset from the tree and save it to a file.
        Use the level parameter to control the level of the tree from which samples will be returned.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            file_path: string or PathLike.
                Local file path to store the coreset.
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional, default 0.
                Defines the depth level of the tree from which the coreset is extracted.
                Level 0 returns the coreset from the head of the tree with around coreset_size samples.
                Level 1 returns the coreset from the level below the head of the tree with around twice of the samples compared to level 0, etc.
                If the passed level is greater than the maximal level of the tree, the maximal available level is used.
            preprocessing_stage: string, optional, default `user`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **original** - Return the data as it was handed to the Coreset’s build function
                (The data_params.save_orig flag should be set for this option to be available).<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            with_index: boolean, optional, default False.
                Relevant only when preprocessing_stage=`auto`. Should the returned data include the index column.
            coreset_data: dict, optional, default False.
                If provided, the value of this parameter is saved.
                Otherwise, the coreset is computed on the spot.

        """
        check_feature_for_license("get_coreset")
        self._requires_tree()

        if TreeOptimizedFor.training not in self.optimized_for:
            raise ValueError("save_coreset is only supported when the coreset service is optimized_for 'training'")

        data = coreset_data or self.get_coreset(
            tree_idx=tree_idx,
            level=level,
            preprocessing_stage=preprocessing_stage,
            as_df=True,
        )
        export_data = data["X"]
        y = data.get("y", None)
        props = data.get("props", None)
        if with_index:
            export_data['index_column'] = data['ind']
        if y is not None:
            export_data['y'] = y
        export_data['weights'] = data['w']
        if props is not None:
            # props can be either a numpy array with multiple cols or a dataframe, add them to X
            if isinstance(props, np.ndarray):
                props_names = [prop.name for prop in self.data_manager.data_params.properties]
                props = pd.DataFrame(props, columns=props_names)
            export_data = pd.concat([export_data, props], axis=1)
        if with_index:
            # move the index column to the first position
            cols = ['index_column'] + [col for col in export_data.columns if col != 'index_column']
            export_data = export_data[cols]
        buffer = io.StringIO()
        export_data.to_csv(buffer, index=False)
        self.storage_manager.dump_bytes(buffer.getvalue().encode(), file_path)

    @telemetry
    def get_important_samples(
            self,
            size: int = None,
            class_size: Dict[Any, Union[int, str]] = None,
            ignore_indices: Iterable = None,
            select_from_indices: Iterable = None,
            select_from_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]] = None,
            ignore_seen_samples: bool = True,

    ) -> Union[ValueError, dict]:

        self._requires_tree()
        # Raise exception saying that the functionality now is called get_cleaning_samples
        warnings.warn("get_important_samples() is deprecated and will be removed in the future. "
                      "Use get_cleaning_samples() instead.", DeprecationWarning)
        return self._get_cleaning_samples(
            size=size,
            class_size=class_size,
            ignore_indices=ignore_indices,
            select_from_indices=select_from_indices,
            select_from_function=select_from_function,
            ignore_seen_samples=ignore_seen_samples,
        )

    @telemetry
    def get_cleaning_samples(
            self,
            size: int = None,
            ignore_indices: Iterable = None,
            select_from_indices: Iterable = None,
            select_from_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]] = None,
            ignore_seen_samples: bool = True,

    ) -> Union[ValueError, dict]:
        """
        Returns indices of samples in descending order of importance.
        Useful for identifying mislabeled instances and other anomalies in the data.
        size must be provided. Function must be called after build.
        This function is only applicable in case the coreset tree was optimized_for 'cleaning'.
        This function is not for retrieving the coreset (use get_coreset in this case).

        Parameters:
            size: required, optional.
                Number of samples to return.

            ignore_indices: array-like, optional.
                An array of indices to ignore when selecting cleaning samples.

            select_from_indices: array-like, optional.
                 An array of indices to consider when selecting cleaning samples.

            select_from_function: function, optional.
                 Pass a function in order to limit the selection of the cleaning samples accordingly.
                 The function should accept 4 parameters as input: indices, X, y, props.
                 and return a list(iterator) of the desired indices.

            ignore_seen_samples: bool, optional, default True.
                 Exclude already seen samples and set the seen flag on any indices returned by the function.

        Returns:
            Dict:
                idx: array-like[int].
                    Cleaning samples indices.
                X: array-like[int].
                    X array.
                y: array-like[int].
                    y array.
                importance: array-like[float].
                    The importance property. Instances that receive a high Importance in the Coreset computation,
                    require attention as they usually indicate a labeling error,
                    anomaly, out-of-distribution problem or other data-related issue.
        """
        self._requires_tree()
        return self._get_cleaning_samples(
            size=size,
            ignore_indices=ignore_indices,
            select_from_indices=select_from_indices,
            select_from_function=select_from_function,
            ignore_seen_samples=ignore_seen_samples
        )

    def _get_cleaning_samples(
            self,
            size: int = None,
            class_size: Dict[Any, Union[int, str]] = None,
            ignore_indices: Iterable = None,
            select_from_indices: Iterable = None,
            select_from_function: Callable[[Iterable, Iterable, Iterable], Iterable[Any]] = None,
            ignore_seen_samples: bool = True,
    ) -> Union[ValueError, dict]:
        self._requires_tree()
        size, class_size, classes, sample_all = self.validate_cleaning_samples_arguments(
            is_classification=self.is_classification,
            size=size,
            class_size=class_size
        )
        assert self.trees is not None and len(self.trees) > 0
        result = self.trees[self._cleaning_tree_idx].get_cleaning_samples(
            size=size,
            class_size=class_size,
            classes=classes,
            sample_all=sample_all,
            ignore_indices=ignore_indices,
            select_from_indices=select_from_indices,
            select_from_function=select_from_function,
            ignore_seen_samples=ignore_seen_samples,
        )
        return result

    @telemetry
    def set_seen_indication(self,
                            seen_flag: bool = True,
                            indices: Iterable = None,
                            ):
        """
        Set samples as 'seen' or 'unseen'. Not providing an indices list defaults to setting the flag on all samples.
        This function is only applicable in case the coreset tree was optimized_for 'cleaning'.

        Parameters:
            seen_flag: bool, optional, default True.
                Set 'seen' or 'unseen' flag

            indices: array like, optional.
                Set flag only for the provided list of indices. Defaults to all indices.
        """
        self._requires_tree()
        if TreeOptimizedFor.cleaning not in self.optimized_for:
            raise ValueError(
                "set_seen_indication is only supported when the coreset service is optimized_for 'cleaning'")
        return self.trees[self._cleaning_tree_idx].set_seen_indication(seen_flag, indices)

    @telemetry
    def remove_samples(
            self,
            indices: Iterable,
            force_resample_all: Optional[int] = None,
            force_sensitivity_recalc: Optional[int] = None,
            force_do_nothing: Optional[bool] = False
    ):
        """
        Remove samples from the coreset tree.
        The coreset tree is automatically updated to accommodate to the changes.

        Parameters:
            indices: array-like.
                An array of indices to be removed from the coreset tree.

            force_resample_all: int, optional.
                Force full resampling of the affected nodes in the coreset tree, starting from level=force_resample_all.
                None - Do not force_resample_all (default), 0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_sensitivity_recalc: int, optional.
                Force the recalculation of the sensitivity and partial resampling of the affected nodes,
                based on the coreset's quality, starting from level=force_sensitivity_recalc.
                None - If self.chunk_sample_ratio<1 - one level above leaf node level. If self.chunk_sample_ratio=1 - leaf level
                0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_do_nothing: bool, optional, default False.
                When set to True, suppresses any update to the coreset tree until update_dirty is called.
        """
        self._requires_tree()
        self._check_sensi_recalc(force_sensitivity_recalc)

        check_feature_for_license("update_remove")
        self.tree_group_manager.remove_samples(indices=indices,
                                               force_resample_all=force_resample_all,
                                               force_sensitivity_recalc=force_sensitivity_recalc,
                                               force_do_nothing=force_do_nothing)

    def _check_sequence_window(self) -> Optional[datetime]:
        # Check if window_size is defined
        seq_column = self.data_manager.data_params.seq_column
        if seq_column is None or seq_column.get("sliding_window") is None:
            return None

        # Determine seq_to needed to preserve window_size
        return self._get_window_pruning_point(seq_column["sliding_window"])

    def _get_window_pruning_point(self, sliding_window: int) -> Optional[datetime]:
        # We start checking the sequence step from the last leaf
        # If for the leaf before, the sequence step changes, we decrement the sliding_window size
        # TODO Daci: Multi Tree?
        seq_step = self.trees[0].tree[0][-1].statistics["seq"].item()
        for leaf in self.trees[0].tree[0][::-1]:
            # We don't count empty leaves towards the sliding window size
            if leaf.is_empty():
                continue
            if leaf.statistics["seq"].item() != seq_step:
                seq_step = leaf.statistics["seq"].item()
                sliding_window -= 1
                if sliding_window == 0:
                    break

        return seq_step if sliding_window == 0 else None

    @telemetry
    def remove_by_seq(self,
                      seq_from: Optional[Union[str, datetime]] = None,
                      seq_to: Optional[Union[str, datetime]] = None
                      ) -> None:
        """
        Remove nodes within a given sequence.

        Parameters:
            seq_from: string or datetime, optional, default None.
                The start sequence to filter samples by.
            seq_to: string or datetime, optional, default None.
                The end sequence to filter samples by.
        """
        check_feature_for_license("sequence_features")

        # Check which nodes must be removed
        node_idxs = self._find_leaves_by_seq(seq_from, seq_to)

        # check that we don't remove the entire tree
        # TODO Daci: Multi tree approach
        if len(node_idxs) == len(self.trees[0].get_leaves()):
            raise ValueError(f"remove_by_seq() with seq_from = {seq_from} and seq_to = {seq_to} would remove the entire tree") 

            # Tell the TreeManager to remove the nodes
        self.tree_group_manager.remove_nodes(node_idxs)

    def _find_leaves_by_seq(self, seq_from, seq_to) -> List[tuple]:
        # Identify all nodes belonging to a sequence
        # Can return either as list of nodes or list of (level_idx, node_idx) tuples

        if seq_from is None and seq_to is None:
            raise ValueError("At least one of `seq_from` or `seq_to` must not be None")
        # TODO Daci: Multi tree approach
        seq_from, seq_to = self.trees[0]._transform_seq_params(seq_from, seq_to)

        nr_leaves = len(self.trees[0].tree[0])
        root_zero_leaf_level = len(self.trees[0].tree) - 1
        leaf_idxs = zip([root_zero_leaf_level] * nr_leaves, range(nr_leaves))

        nodes = self.trees[0].compute_seq_nodes(
            nodes=leaf_idxs,
            seq_params=[seq_from, seq_to],
            seq_operators=[False, False],
            # we can't have data mix at leaf level, this value is meaningless
            data_mix_threshold=0,
            purpose=None,
        )
        return [self.trees[0]._where_is_node(node.node_id, root_zero=False) for node in nodes]

    @telemetry
    def update_sliding_window(self, sliding_window: int) -> None:
        """
            Update the size of the sliding window

            Parameters:
                sliding_window: int
                    Size of the new sliding window. If it is smaller than before, nodes will be removed
                    so that the tree fits in the new window size.
        """
        check_feature_for_license("sequence_features")

        if self.data_manager.data_params.seq_column is None:
            raise ValueError("`seq_column` must be defined in order to set the value `sliding_window`")
        self.data_manager.data_params.validate_sliding_window(sliding_window)
        self.data_manager.data_params.seq_column["sliding_window"] = sliding_window

        # See if nodes must be removed
        seq_to = self._check_sequence_window()
        if seq_to:
            self.remove_by_seq(seq_from=None, seq_to=seq_to)

    @telemetry
    def update_targets(
            self,
            indices: Iterable,
            y: Iterable,
            force_resample_all: Optional[int] = None,
            force_sensitivity_recalc: Optional[int] = None,
            force_do_nothing: Optional[bool] = False
    ):
        """
        Update the targets for selected samples on the coreset tree.
        The coreset tree is automatically updated to accommodate to the changes.

        Parameters:
            indices: array-like.
                An array of indices to be updated.

            y: array-like.
                An array of classes/labels. Should have the same length as indices.

            force_resample_all: int, optional.
                Force full resampling of the affected nodes in the coreset tree, starting from level=force_resample_all.
                None - Do not force_resample_all (default), 0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_sensitivity_recalc: int, optional.
                Force the recalculation of the sensitivity and partial resampling of the affected nodes,
                based on the coreset's quality, starting from level=force_sensitivity_recalc.
                None - If self.chunk_sample_ratio<1 - one level above leaf node level. If self.chunk_sample_ratio=1 - leaf level
                0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_do_nothing: bool, optional, default False.
                When set to True, suppresses any update to the coreset tree until update_dirty is called.
        """
        self._requires_tree()
        self._check_sensi_recalc(force_sensitivity_recalc)

        check_feature_for_license("update_remove")
        self.tree_group_manager.update_targets(
            indices=np.array(indices),
            y=np.array(y),
            force_resample_all=force_resample_all,
            force_sensitivity_recalc=force_sensitivity_recalc,
            force_do_nothing=force_do_nothing)

    @telemetry
    def update_features(
            self,
            indices: Iterable,
            X: Iterable,
            feature_names: Iterable[str] = None,
            force_resample_all: Optional[int] = None,
            force_sensitivity_recalc: Optional[int] = None,
            force_do_nothing: Optional[bool] = False
    ):
        """
        Update the features for selected samples on the coreset tree.
        The coreset tree is automatically updated to accommodate to the changes.

        Parameters:
            indices: array-like.
                An array of indices to be updated.

            X: array-like.
                An array of features. Should have the same length as indices.

            feature_names:
                If the quantity of features in X is not equal to the quantity of features in the original coreset,
                this param should contain list of names of passed features.

            force_resample_all: int, optional.
                Force full resampling of the affected nodes in the coreset tree, starting from level=force_resample_all.
                None - Do not force_resample_all (default), 0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_sensitivity_recalc: int, optional.
                Force the recalculation of the sensitivity and partial resampling of the affected nodes,
                based on the coreset's quality, starting from level=force_sensitivity_recalc.
                None - If self.chunk_sample_ratio<1 - one level above leaf node level. If self.chunk_sample_ratio=1 - leaf level
                0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_do_nothing: bool, optional, default False.
                When set to True, suppresses any update to the coreset tree until update_dirty is called.
        """
        self._requires_tree()
        self._check_sensi_recalc(force_sensitivity_recalc)

        check_feature_for_license("update_remove")
        self.tree_group_manager.update_features(indices=np.array(indices),
                                                X=np.array(X),
                                                feature_names=feature_names,
                                                force_resample_all=force_resample_all,
                                                force_sensitivity_recalc=force_sensitivity_recalc,
                                                force_do_nothing=force_do_nothing)

    @telemetry
    def filter_out_samples(
            self,
            filter_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]],
            force_resample_all: Optional[int] = None,
            force_sensitivity_recalc: Optional[int] = None,
            force_do_nothing: Optional[bool] = False
    ):
        """
        Remove samples from the coreset tree, based on the provided filter function.
        The coreset tree is automatically updated to accommodate to the changes.

        Parameters:
            filter_function: function, optional.
                A function that returns a list of indices to be removed from the tree.
                The function should accept 4 parameters as input: indices, X, y, props
                and return a list(iterator) of indices to be removed from the coreset tree.
                For example, in order to remove all instances with a target equal to 6, use the following function:
                filter_function = lambda indices, X, y, props : indices[y = 6].

            force_resample_all: int, optional.
                Force full resampling of the affected nodes in the coreset tree, starting from level=force_resample_all.
                None - Do not force_resample_all (default), 0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_sensitivity_recalc: int, optional.
                Force the recalculation of the sensitivity and partial resampling of the affected nodes,
                based on the coreset's quality, starting from level=force_sensitivity_recalc.
                None - If self.chunk_sample_ratio<1 - one level above leaf node level. If self.chunk_sample_ratio=1 - leaf level
                0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_do_nothing: bool, optional, default False.
                When set to True, suppresses any update to the coreset tree until update_dirty is called.
        """
        self._requires_tree()
        self._check_sensi_recalc(force_sensitivity_recalc)

        check_feature_for_license("update_remove")
        self.tree_group_manager.filter_out_samples(
            filter_function=filter_function,
            force_resample_all=force_resample_all,
            force_sensitivity_recalc=force_sensitivity_recalc,
            force_do_nothing=force_do_nothing)

    @telemetry
    def update_dirty(
            self,
            force_resample_all: Optional[int] = None,
            force_sensitivity_recalc: Optional[int] = None
    ):
        """
        Calculate the sensitivity and resample the nodes that were marked as dirty,
        meaning they were affected by any of the methods:
        remove_samples, update_targets, update_features or filter_out_samples,
        when they were called with force_do_nothing.

        Parameters:
            force_resample_all: int, optional.
                Force full resampling of the affected nodes in the coreset tree, starting from level=force_resample_all.
                None - Do not force_resample_all (default), 0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.

            force_sensitivity_recalc: int, optional.
                Force the recalculation of the sensitivity and partial resampling of the affected nodes,
                based on the coreset's quality, starting from level=force_sensitivity_recalc.
                None - If self.chunk_sample_ratio<1 - one level above leaf node level. If self.chunk_sample_ratio=1 - leaf level
                0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.
        """
        self._requires_tree()
        self._check_sensi_recalc(force_sensitivity_recalc)
        check_feature_for_license("update_remove")
        self.tree_group_manager.update_dirty(
            force_resample_all=force_resample_all,
            force_sensitivity_recalc=force_sensitivity_recalc
        )

    @telemetry
    def is_dirty(self) -> bool:
        """
            Returns:
                Indicates whether the coreset tree has nodes marked as dirty, meaning they were affected by any of the methods: remove_samples, update_targets, update_features or filter_out_samples, when they were called with force_do_nothing.
        """
        self._requires_tree()
        check_feature_for_license("update_remove")
        return self.tree_group_manager.is_dirty()

    @telemetry
    def get_max_level(self) -> int:
        """
        Return the maximal level of the coreset tree. Level 0 is the head of the tree.
        Level 1 is the level below the head of the tree, etc.
        """
        # Here it seems acceptable to use the first tree because we assume that all trees have the same structure
        self._requires_tree()
        if self.trees[0]:
            return self.trees[0].get_max_level()
        return 0

    @telemetry
    def fit(
        self,
        tree_idx: int = 0,
        level: Optional[int] = 0,
        seq_from: Any = None,
        seq_to: Any = None,
        model: Any = None,
        preprocessing_stage: Union[str, None] = "auto",
        sparse_threshold: float = 0.01,
        model_fit_params: Optional[dict] = None,
        **model_params,
    ):
        """
        Fit a model on the coreset tree. This model will be used when predict and predict_proba are called.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: Defines the depth level of the tree from which the coreset is extracted.
                Level 0 returns the coreset from the head of the tree with around coreset_size samples.
                Level 1 returns the coreset from the level below the head of the tree with around twice of the samples compared to level 0, etc.
                If the passed level is greater than the maximal level of the tree, the maximal available level is used.
            seq_from: string/datetime, optional
                The starting sequence of the training set.
            seq_to: string/datetime, optional
                The ending sequence of the training set.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                Default: instantiate the service model class using input model_params.
            preprocessing_stage: string, optional, default `auto`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            model_fit_params: dict, optional, default None.
                Parameters passed to the model's fit function.
            model_params: Model hyperparameters kwargs.
                Input when instantiating default model class.

        Returns:
            Fitted estimator.
        """
        check_feature_for_license("fit")
        self._requires_tree()
        self._print_model_warning(model)

        return self._fit(
            model=model,
            model_fit_params=model_fit_params,
            model_params=model_params,
            tree_idx=tree_idx,
            level=level,
            seq_from=seq_from,
            seq_to=seq_to,
            coreset_params=self.coreset_params["training"],
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
        )

    @telemetry
    def predict(self, X: Union[Iterable, Iterable[Iterable]], sparse_output: bool = False, copy: bool = False):
        """
        Run prediction on the trained model.
        This function is only applicable in case the coreset tree was optimized_for 'training' and
        in case fit() or grid_search(refit=True) where called before.
        The function automatically preprocesses the data according to the preprocessing_stage used to train the model.

        Parameters:
            X: An array of features.
            sparse_output: boolean, optional, default False.
                When set to True, the function will create a sparse matrix after preprocessing and pass it to the predict function.
            copy: boolean, default False.
                False (default) - Input data might be updated as result of this function.
                True - Data is copied before processing (impacts memory).

        Returns:
            Model prediction results.
        """
        check_feature_for_license("predict")
        X_prepared = self._prepare_data_before_predict(X=X, method_name="predict", sparse_output=sparse_output,
                                                       copy=copy)
        return self._predict(X_prepared)

    @telemetry
    def predict_proba(self, X: Union[Iterable, Iterable[Iterable]], sparse_output: bool = False, copy: bool = False):
        """
        Run prediction on the trained model.
        This function is only applicable in case the coreset tree was optimized_for 'training' and
        in case fit() or grid_search(refit=True) where called before.
        The function automatically preprocesses the data according to the preprocessing_stage used to train the model.

        Parameters:
            X: An array of features.
            sparse_output: boolean, optional, default False.
                When set to True, the function will create a sparse matrix after preprocessing and pass it to the predict_proba function.
            copy: boolean, default False.
                False (default) - Input data might be updated as result of this function.
                True - Data is copied before processing (impacts memory).

        Returns:
            Returns the probability of the sample for each class in the model.
        """
        check_feature_for_license("predict")
        X_prepared = self._prepare_data_before_predict(X=X, method_name="predict_proba", sparse_output=sparse_output,
                                                       copy=copy)
        return self._predict_proba(X_prepared)

    def _prepare_data_before_predict(self, X, method_name, sparse_output: bool = False, copy: bool = False):
        self._requires_tree()

        if TreeOptimizedFor.training not in self.optimized_for:
            raise ValueError(f"{method_name} is only supported when the coreset service is optimized_for 'training'")
        if self.data_manager.data_params_internal.last_fit_preprocessing_stage is None:
            raise ValueError(f"{method_name} must be called after fit or grid_search(refit=True)")

        if self.data_manager.data_params_internal.last_fit_preprocessing_stage == PreprocessingStage.AUTO:
            X_prepared = self.auto_preprocessing(X=X, sparse_output=sparse_output, copy=copy)
        else:
            X_prepared, _ = self._prepare_categorical_model_and_X(X=X, model=self.model, predict=True)
        return X_prepared

    @telemetry
    def print(self, tree_indices: List[int] = None):
        """
        Print the tree's string representation.

        Parameters:
            tree_indices: list, optional.
                Defines the indices of the trees which would be printed. By default, all trees are printed.
        """
        self._requires_tree()
        tree_indices = tree_indices or list(range(len(self.trees)))
        for tree_idx in tree_indices:
            self.trees[tree_idx].print()

    @telemetry
    def plot(
        self, dir_path: Optional[Union[str, os.PathLike]] = None, tree_indices: List[int] = None
    ) -> Dict[int, Union[str, os.PathLike]]:
        """
        Produce a tree graph plot and save figure as a local png file.

        Parameters:
            dir_path: string or PathLike, optional.
                Path to a directory to save the plot figure in.
                The directory can be local or on AWS S3, Google Cloud Platform Storage, Azure Storage.

            tree_indices: list, optional.
                Defines the indices of the trees which would be plotted. By default, all trees are plotted.

        Returns:
            Dict containing the save path for each saved tree. If dir_path is None, the dict is empty.
        """
        self._requires_tree()
        storage_manager = StorageManager()

        tree_indices = tree_indices or list(range(len(self.trees)))
        if max(tree_indices) >= len(self.trees):
            raise ValueError(f"Out of bounds index for plotting. Number of existing trees: {len(self.trees)}. Tried to plot tree at index {max(tree_indices)}")

        output = dict()
        for tree_idx in tree_indices:
            tree = self.trees[tree_idx]
            name = f"tree_{tree_idx}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            res = tree.safe_plot(dir_path, name)
            res = pathlib.Path(res) if (res and storage_manager.is_local(res)) else res
            output[tree_idx] = res
        return output

    @telemetry
    def explain(self,
                X,
                model_scoring_function: Callable[[np.ndarray, Any], float],
                selected_tree: str = None,
                ) -> Iterator[Tuple[Union[list, dict], str, str]]:
        """
        return leaf metadata and explainability path,
        using provided unlabeled examples and model scoring function.
        Parameters:
            X: array like
                unclassified samples

            model_scoring_function: callable[[array like, any], float]
                model scoring function which gets the X and the node's train model as params and returns a score in
                the range of [0,1]; this function drives the building of the explainability path.
            tree_indices: string or list.
                Which tree(s) to print. Defaults to printing all.

        Returns:
            An iterator of (metadata,explanation) tuples:
                metadata:
                    selected leaf's metadata
                explanation:
                    free text explaining the built explainability path
        """
        self._requires_tree()
        tree_indices = self.trees.values() if not selected_tree else self.trees[selected_tree]
        for t in tree_indices:
            for v in X:
                leaf_metadata, explanation, leaf_index = t.explain(np.array([v]), model_scoring_function)
                yield leaf_metadata, explanation, leaf_index

    def _set_reader_chunk_size_param(self, file_path, reader_f, reader_kwargs, reader_chunk_size_param_name,
                                     chunk_size=None):
        """Figure our the required chunk_size if not provided and set the relevant reader param when supported"""

        if chunk_size is None:
            chunk_size = self.chunk_size

        if reader_chunk_size_param_name == 'ignore':
            return
        if chunk_size == 0 or self.chunk_by is not None:
            return
        reader_chunk_size_param_name = reader_chunk_size_param_name or resolve_reader_chunk_size_param_name(reader_f)
        # TODO: when reader_f is a product of functools.partial,
        #  maybe chunk size param is already embedded inside with a value and not part of reader_kwargs.
        if not reader_chunk_size_param_name:
            return
        if not chunk_size or chunk_size <= 0:
            n_features = self.data_manager.get_file_n_columns(
                next(file_path_to_files(file_path, self.data_manager.storage_manager)),
                reader_f,
                reader_kwargs,
                reader_chunk_size_param_name
            )
            max_memory_gb = float(self.max_memory_gb) if self.max_memory_gb is not None else None

            chunk_size = tree_utils.evaluate_max_batch_size(n_features, max_memory_gb=max_memory_gb,
                                                            dtype=self._get_dtype())
        if chunk_size:
            reader_kwargs.setdefault(reader_chunk_size_param_name, chunk_size)

    def _preprocess_df(self, datasets, partial=False, chunk_by=None, **kwargs):
        if not partial:
            datasets = self.data_manager.init_and_preprocess(datasets, chunk_by=chunk_by)
        else:
            datasets = self.data_manager.preprocess(datasets, chunk_by=chunk_by)

        return datasets

    def _preprocess_datasets(self, datasets, partial=False, chunk_by=None, **kwargs):
        if not partial:
            datasets = iter(datasets)
            first = next(datasets)
            datasets = itertools.chain([first], datasets)
            self.data_manager.init_from_dataset(*first[:3], first[4])

        def _chunk_by(dataset):
            dataset = Dataset(*dataset)
            if dataset.ind is None:
                dataset = dataset._replace(ind=self.data_manager.gen_indices(dataset.X))
            df = self.data_manager.dataset_to_df(dataset.ind, dataset.X, dataset.y, dataset.props)
            for df_i in self.data_manager.split_datasets([df], chunk_by):
                yield (a[df_i.index] if a is not None else None for a in dataset)

        if chunk_by:
            datasets = itertools.chain.from_iterable(map(_chunk_by, datasets))

        datasets = map(self.data_manager.preprocess_dataset, datasets)
        return datasets

    @telemetry
    def build_from_file_insights(self,
                                 file_paths: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]],
                                 target_file_path: Union[
                                     Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]] = None,
                                 reader_f=pd.read_csv, reader_kwargs=None, reader_chunk_size_param_name=None) -> Dict:
        """
        Provide insights into the Coreset tree that would be built for the provided dataset.
        The function receives the data in the same format as its build_from_file counterpart.
        Categorical features are automatically one-hot encoded or target encoded
        and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            file_path: file, list of files, directory, list of directories.

            target_file_path: file, list of files, directory, list of directories, optional.
                Use when files are split to features and target.
                Each file should include only one column.
                The target will be ignored when the Coreset is built.

            reader_f: pandas like read method, optional, default pandas read_csv.
                For example, to read excel files use pandas read_excel.

            reader_kwargs: dict, optional.
                Keyword arguments used when calling reader_f method.

            reader_chunk_size_param_name: str, optional.
                reader_f input parameter name for reading file in chunks.
                When not provided we'll try to figure it out our self.
                Based on the data, we decide on the optimal chunk size to read
                and use this parameter as input when calling reader_f.
                Use "ignore" to skip the automatic chunk reading logic.

        Returns:
            Insights into the Coreset tree build function.
        """
        reader_kwargs = (reader_kwargs or dict()).copy()
        first_file_path, _ = iter_first(file_path_to_iterable(file_paths))
        self._set_reader_chunk_size_param(first_file_path, reader_f, reader_kwargs, reader_chunk_size_param_name, None)
        datasets = self.data_manager.read_file(first_file_path, reader_f=reader_f, reader_kwargs=reader_kwargs)
        first_df = next(datasets)
        if target_file_path is not None:
            first_target_file_path, _ = iter_first(file_path_to_iterable(target_file_path))
            target_datasets = self.data_manager.read_file(target_file_path, reader_f=reader_f,
                                                          reader_kwargs=reader_kwargs)
            first_target = next(target_datasets)
        else:
            first_target = None
        return self.build_from_df_insights(first_df, target_datasets=first_target)

    @telemetry
    def build_from_df_insights(self, datasets: Union[Iterator[pd.DataFrame], pd.DataFrame],
                               target_datasets: Union[Iterator[pd.DataFrame], pd.DataFrame] = None) -> Dict:
        """
        Provide insights into the Coreset tree that would be built for the provided dataset.
        The function receives the data in the same format as its build_from_df counterpart.
        Categorical features are automatically one-hot encoded or target encoded
        and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            datasets: pandas DataFrame or a DataFrame iterator.
                Data includes features, may include targets and may include indices.

            target_datasets: pandas DataFrame or a DataFrame iterator, optional.
                Use when data is split to features and target.
                Should include only one column.
                The target will be ignored when the Coreset is built.

        Returns:
            Insights into the Coreset tree build function.
        """
        # if the datasets is an iterator, take the first dataset to calculate the chunk size and coreset size
        first_df = list(df_to_iterable(datasets))[0]

        # if the datasets is an iterator, take the first dataset to calculate the chunk size and coreset size
        if target_datasets is not None:
            first_target = list(df_to_iterable(target_datasets))[0]
        else:
            first_target = None

        # take the 1st and only column from the target dataset
        if first_target is not None:
            y = first_target.iloc[:, 0].to_numpy()
            X = first_df.to_numpy()
        else:
            # get the y from the 1st dataset
            if self.data_manager.data_params.target is not None:
                target_field_name = self.data_manager.data_params.target if isinstance(
                    self.data_manager.data_params.target, str) else self.data_manager.data_params.target.name
                X = first_df[[c for c in first_df.columns if c != target_field_name]].to_numpy()
                y = first_df[target_field_name].to_numpy()
            else:
                X = first_df.to_numpy()
                y = None
        return self.build_insights(X, y)

    @telemetry
    def build_insights(self, X: Union[Iterable, Iterable[Iterable]],
                       y: Union[Iterable[Any], Iterable[Iterable[Any]]] = None) -> Dict:
        """
        Provide insights into the Coreset tree that would be built for the provided dataset.
        The function receives the data in the same format as its build counterpart.
        Categorical features are automatically one-hot encoded or target encoded
        and missing values are automatically handled.
        The target will be ignored when the Coreset is built.

        Parameters:
            X: array like or iterator of arrays like.
                An array or an iterator of features.
            y: array like or iterator of arrays like, optional. An array or an iterator of targets.
                The target will be ignored when the Coreset is built.

        Returns:
            Insights into the Coreset tree build function.
        """
        # check for license for build_insights
        check_feature_for_license("build_insights")

        # take the 1st dataset to calculate the chunk size and coreset size
        if isinstance(X, Iterator):
            X = next(X)

        if y is not None and isinstance(y, Iterator):
            y = next(y)

        if y is not None and self.is_classification:
            n_classes = len(pd.unique(filter_missing_and_inf(y)))
        else:
            n_classes = None

        buffer_size = X.shape[0]

        # init the data manager with the dataset to calculate the cat and array columns
        self.data_manager.init_from_dataset(None, X, y, None)
        expected_n_features, typed_feature_counts = self.data_manager._estimate_expected_n_features(
            X, return_counts=True)

        # get dtypes from coreset params dicts (training, cleaning, etc.)
        for coreset_type_params in self.coreset_params.values():
            # if one of the dtypes is float64 set the dtype to float64, if the coreset_type_params does not have
            # the dtype attribute it means that the calculation was done with the default (numpy) dtype which is float64
            if not hasattr(coreset_type_params, 'dtype') or coreset_type_params.dtype == 'float64':
                dtype = 'float64'
                break
        else:
            dtype = "float32"

        # TODO Daci: Multi tree support, we take the first coreset size for now
        coreset_size = self.data_tuning_params.coreset_size[0]
        coreset_size = {"training": coreset_size, "cleaning": coreset_size}
        # calc chunk size and coreset size based on n_instances provided to the service init or the 1st dataset size.
        chunk_size, coreset_size_tree_type, _, chunk_calc_data = utils.calc_chunks_params(
            chunk_size=self.chunk_size,
            coreset_size=coreset_size,
            n_instances=self.data_manager.n_instances,
            buffer_size=buffer_size,
            n_features=expected_n_features,
            n_classes=n_classes,
            max_memory_gb=self.max_memory_gb,
            dtype=dtype,
            return_calculated_data=True
        )

        verbose_result = {
            "Number of data instances (n_instances)": f"{f'{self.data_manager.data_params.n_instances:,}' if self.data_manager.data_params.n_instances is not None else 'Not provided'}"}

        features_message = f'{self.data_manager.n_features}.'

        if typed_feature_counts['numeric'] == self.data_manager.n_features:
            features_message += f' All features are Numeric.'
        elif typed_feature_counts['boolean'] == self.data_manager.n_features:
            features_message += f' All features are Boolean.'
        elif len(self.data_manager.data_params_internal.categorical_features_) == self.data_manager.n_features:
            features_message += f' All features are Categorical.'
        elif len(self.data_manager.data_params_internal.array_features_) == self.data_manager.n_features:
            features_message += f' All features are Array.'
        else:
            if typed_feature_counts['numeric'] > 0:
                features_message += f' Numeric: {typed_feature_counts["numeric"]}.'
            if typed_feature_counts['boolean'] > 0:
                features_message += f' Boolean: {typed_feature_counts["boolean"]}.'
            if len(self.data_manager.data_params_internal.categorical_features_) > 0:
                features_message += f' Categorical: {len(self.data_manager.data_params_internal.categorical_features_)}.'
            if len(self.data_manager.data_params_internal.array_features_) > 0:
                features_message += f' Array: {len(self.data_manager.data_params_internal.array_features_)}.'
        verbose_result['Number of features (n_features)'] = features_message

        if typed_feature_counts['TE'] + typed_feature_counts['OHE'] + typed_feature_counts['array'] > 0:
            if typed_feature_counts['TE'] + typed_feature_counts['OHE'] > 0:
                cat_message = f'{self.data_manager.data_params.cat_encoding_method}.'
                if self.data_manager.data_params.cat_encoding_method == 'MIXED':
                    ohe_cat_features = len(self.data_manager.data_params_internal.categorical_features_) - \
                                       typed_feature_counts["TE"]
                    cat_message += f' One Hot Encoded (OHE) features: {ohe_cat_features}.' \
                                   f' Target Encoded (TE) features: {typed_feature_counts["TE"]}'
                elif self.data_manager.data_params.cat_encoding_method == 'TE':
                    cat_message += f' All categorical features will be Target Encoded.'
                elif self.data_manager.data_params.cat_encoding_method == 'OHE':
                    cat_message += f' All categorical features will be One Hot Encoded.'
                verbose_result['Categorical features encoding method'] = cat_message

            estimated_n_features_message = f'{expected_n_features:,}.'
            if typed_feature_counts['numeric'] > 0:
                estimated_n_features_message += f' Numeric: {typed_feature_counts["numeric"]}.'
            if typed_feature_counts["boolean"] > 0:
                estimated_n_features_message += f' Boolean (converted to Numeric): {typed_feature_counts["boolean"]}.'
            if typed_feature_counts['TE'] > 0:
                estimated_n_features_message += f' Categorical TE: {typed_feature_counts["TE"]}.'
            if typed_feature_counts['OHE'] > 0:
                estimated_n_features_message += f' Categorical OHE: {typed_feature_counts["OHE"]}.'
            if typed_feature_counts['array'] > 0:
                estimated_n_features_message += f' Array Encoded: {typed_feature_counts["array"]}.'
            verbose_result['Estimated number of features after encoding'] = estimated_n_features_message

        if self.is_classification:
            verbose_result['Number of classes'] = f'{n_classes:,}.'

        verbose_result['Maximum available memory (max_memory_gb)'] = f'{chunk_calc_data["max_memory_gb"]:,}'

        if self.data_manager.n_instances is None:
            verbose_result['Maximum possible chunk_size'] = f'Cannot be calculated. n_instances was not provided.'
        else:
            if not chunk_calc_data['is_tree']:
                max_chunk_size_message = f"{self.data_manager.n_instances:,}. (Can't create a Coreset tree. A single Coreset will be created)."
            else:
                max_chunk_size_message = f'{min(chunk_calc_data["max_chunk_size_for_tree"], self.data_manager.n_instances):,}.'
            verbose_result[
                'Maximum possible chunk_size (based on n_instances, n_features and max_memory_gb)'] = max_chunk_size_message

        if chunk_calc_data['is_tree']:
            if self.chunk_by:
                chunk_size_message = f'Using chunk_by functionality to split the data into chunks.'
            else:
                verbose_result[
                    'Number of leaf nodes in Coreset tree'] = f'{int((self.data_manager.n_instances or buffer_size) // chunk_size):,}.'
                chunk_size_message = f'{chunk_size:,}'
                if self.chunk_size is not None:
                    chunk_size_message += ' (User defined).'
                else:
                    chunk_size_message += ' (Creating the smallest, fully balanced, Coreset tree possible).'
            verbose_result['Actual chunk_size'] = chunk_size_message

        if not self.chunk_by:
            for tree_type, csize in chunk_calc_data['coreset_size_tree_type'].items():
                tree_type_s = f' {tree_type}' if len(self.optimized_for) > 1 else ''
                if tree_type in self.optimized_for:
                    verbose_result[f'Default coreset_size{tree_type_s}'] = f'{csize:,}.'

        if coreset_size:
            for tree_type, csize in coreset_size.items():
                tree_type_s = f' {tree_type}' if len(self.optimized_for) > 1 else ''
                if tree_type in self.optimized_for:
                    if isinstance(csize, float):
                        if self.chunk_by:
                            verbose_result[f'Actual coreset_size{tree_type_s}'] = (f'{csize} of chunk_size (Using '
                                                                                   f'chunk_by functionality to split '
                                                                                   f'the data into chunks).')
                        else:
                            chunk_size = chunk_size if chunk_size else (self.data_manager.n_instances or buffer_size)
                            verbose_result[f'Actual coreset_size{tree_type_s}'] = (f'{int(chunk_size * csize):,}='
                                                                                   f'{csize} of chunk_size,'
                                                                                   f' which is {chunk_size:,} (User defined).')
                    else:
                        if csize is not None:
                            verbose_result[f'Actual coreset_size{tree_type_s}'] = f'{csize:,} (User defined).'

        for k, v in verbose_result.items():
            print(f'{k}: {v}')
        return verbose_result

    def _build_internal(self, datasets, *, partial=False, chunk_size=None, chunk_by=None, **kwargs):
        if chunk_by:
            chunk_size = 0
        else:
            chunk_size = chunk_size or self.chunk_size

        is_mutable_coreset_size = False

        # Extract first dataset for peeking into it for estimation purposes.
        first = next(datasets)
        datasets = itertools.chain([first], datasets)

        # Extract n_instances.
        if partial or self.data_manager.n_instances is None:
            # For partial build OR if n_instances is not defined, take num of samples of the first dataset.
            n_instances = first.X.shape[0]
        else:
            # For initial build, use user-defined n_instances.
            n_instances = self.data_manager.n_instances

        # Validate/reset categorical encoding method.
        self.data_manager.set_cat_encoding_method(is_supervised=self.is_supervised)

        # calculate chunk size, default training coreset size, default cleaning coreset size

        # Estimation must take place after the categorical encoding method was reset.
        n_features_expected = self.data_manager._estimate_expected_n_features(first.X)

        # get dtypes from coreset params dicts (training, cleaning, etc.)
        for coreset_type_params in self.coreset_params.values():
            # if one of the dtypes is float64 set the dtype to float64, if the coreset_type_params does not have
            # the dtype attribute it means that the calculation was done with the default (numpy) dtype which is float64
            if not hasattr(coreset_type_params, 'dtype') or coreset_type_params.dtype == 'float64':
                dtype = 'float64'
                break
        else:
            dtype = "float32"

        # calc chunk size and coreset size if chunk size is None or coreset size is not defined
        # This can happen if we have a data tuning combination that has.
        coreset_size = None
        # We need this condition for the for loop here becuase chunk_size gets overwritten
        auto_chunk_size = chunk_size is None
        for i, size in enumerate(self.data_tuning_params.coreset_size):
            if auto_chunk_size or not size:
                chunk_size, coreset_size_tree_type, is_mutable_coreset_size = utils.calc_chunks_params(
                    chunk_size=self.chunk_size,
                    coreset_size=size,
                    n_instances=self.data_manager.n_instances,
                    buffer_size=n_instances,
                    n_features=n_features_expected,
                    n_classes=self.data_manager.n_classes,
                    max_memory_gb=self.max_memory_gb,
                    dtype=dtype,
                    class_size_exists=isinstance(self.data_tuning_params, DataTuningParamsClassification)
                    and all(cs is not None for cs in self.data_tuning_params.class_size),
                )

                # update the service params with the calculated values
                # so that the values persist after saving the service and loading it again
                if size is None:
                    assert coreset_size_tree_type is not None
                    coreset_size = coreset_size_tree_type["training"] if TreeOptimizedFor.training in self.optimized_for else coreset_size_tree_type["cleaning"]
                    self.data_tuning_params.coreset_size[i] = coreset_size
        self.params['chunk_size'] = chunk_size

        # Define n_jobs.
        user_defined_n_jobs = kwargs.get("n_jobs")
        if chunk_size and (n_instances * n_features_expected) > get_min_data_cells_for_parallel_build():
            max_batch_size = evaluate_max_batch_size(n_features_expected, available=True, dtype=self._get_dtype())
            # the maximum number of chunks that can be processed in parallel
            n_chunks = max(min(max_batch_size, n_instances) // chunk_size, 1)
            n_jobs = min(n_chunks, os.cpu_count())
        else:
            n_jobs = 1

        if not can_use_threadpool_limits():
            # We can not use threadpool_limits, therefore there is NO parallel build.
            n_jobs = 1
        elif user_defined_n_jobs is not None:
            # If user has passed own value, use it - but it should not exceed the already computed n_jobs.
            n_jobs = min(user_defined_n_jobs, os.cpu_count())
        self.data_manager.n_jobs = n_jobs
        self.data_manager.verbose = kwargs.get('verbose', 1)

        # This step is necessary to populate the structures upon which the next decisions will be taken.
        self._pre_build_trees_init(
            chunk_size=self.chunk_size,
            partial=partial,
            is_mutable_coreset_size=is_mutable_coreset_size,
            coreset_size=coreset_size,
        )

        # In the following cases, do not limit parallelism & allow using the natural parallelism to its full extent:
        #
        # 1. Threadpool cannot be technically limited.
        # 2. We use a single chunk (=all-in-one tree) by providing chunk_size=-1.
        if not can_use_threadpool_limits() or (self.chunk_size is not None and self.chunk_size < 0):
            self._build_trees(datasets, partial=partial)
        else:
            limits = calc_blas_limits(n_jobs)
            if limits != os.cpu_count():
                with threadpool_limits(limits=limits, user_api="blas"):
                    self._build_trees(datasets, partial=partial)
            else:
                self._build_trees(datasets, partial=partial)

        seq_to = self._check_sequence_window()
        if seq_to:
            self.remove_by_seq(seq_from=None, seq_to=seq_to)

    def _init_tree(self, tree_data=None, which_params=None, **tree_params):

        coreset_params = (
            self.coreset_params[which_params]
            if isinstance(self.coreset_params[which_params], dict)
            else self.coreset_params[which_params].to_dict()
        )

        build_w_estimation = self.build_w_estimation if hasattr(self, "build_w_estimation") else False
        params = dict(
            data_manager=self.data_manager,
            coreset_cls=self.coreset_cls,
            chunk_size=self.chunk_size,
            coreset_params=coreset_params,
            model_train_function=self.node_train_function,
            model_train_function_params=self.node_train_function_params,
            optimized_for=which_params,
            max_memory_gb=self.max_memory_gb,
            save_all=self.save_all,
            build_w_estimation=build_w_estimation,
        )
        params.update(tree_params)

        return self._tree_cls(
            is_multitree=True,
            tree_data=tree_data,
            **params)

    def _init_tree_group_manager(self, trees: List[CoresetTree], chunk_size=None, chunk_index=None):
        # Initialize TreeGroupManager
        if not self.tree_group_manager:
            self.tree_group_manager = TreeManager(
                trees=trees,
                data_manager=self.data_manager,
                chunk_size=chunk_size,
                is_classification=self.is_classification,
                max_memory_gb=self.max_memory_gb,
                save_all=self.save_all,
                chunk_sample_ratio=self.chunk_sample_ratio,
                chunk_index=chunk_index,
            )

    def remove_trees_buffer_nodes(self):
        for tree in self.trees:
            tree.buffer_node = None

    def _pre_build_trees_init(
        self, chunk_size=None, partial: bool = False, coreset_size=None, is_mutable_coreset_size: bool = False
    ):
        """
        Necessary step before calling _build_trees() in order to initialize everything required for it.

        Parameters:
            partial: partial build (add new samples to tree).
        """

        assert not partial or self.trees, "Build must be performed before partial build"
        assert partial or not self.trees, (
            "Build on an existing tree is not supported. " "Use partial build or initialize a new tree service"
        )

        tree_params = {"is_mutable_coreset_size": is_mutable_coreset_size, "_DH_DEBUG_MODE": self._DH_DEBUG_MODE}
        if chunk_size is not None:
            tree_params["chunk_size"] = chunk_size
            if self.trees:
                for tree in self.trees:
                    # for tree in self.trees.values():
                    if tree:
                        tree.chunk_size = chunk_size

        # Initialize trees if not already initialized
        # TODO What's the relationship between training trees and data tuning?
        if not self.trees:
            # TODO Daci: better solution?
            tree_name = "cleaning" if "cleaning" in self.optimized_for else "training"
            trees = []
            for params in self.data_tuning_params.create_sample_params():
                tree_params["sample_params"] = params
                trees.append(self._init_tree(which_params=tree_name, **tree_params))
            self._init_tree_group_manager(trees=trees, chunk_size=chunk_size)

        # TODO Dacian: does this if make sense? Shouldn't we always have tree_group_manager
        if self.tree_group_manager:
            self.tree_group_manager.update_chunks_params(chunk_size, coreset_size=coreset_size)

    # TODO Daci: If this is mandatory why don't we call it? or raise something if it wasn't called.
    def _build_trees(self, datasets: Iterator = None, partial: bool = False):
        """
        Create a coreset tree from a transformed dataset iterator.
        Mandatory: _pre_build_trees_init() must be called prior to invocation.

        Parameters:
            datasets: an iterator of a tuple like (indices,X,y,*) numpy arrays.
        """

        # Build
        if partial:
            check_feature_for_license("partial build")
            # Remove buffer nodes from trees
            self.remove_trees_buffer_nodes()
        else:
            check_feature_for_license("build")
        # TODO Daci: What is the purpose of this try except here?
        try:
            self.tree_group_manager.build(datasets)
        except BaseException as e:
            if not partial:
                self.tree_group_manager = None
            raise e

    def _get_tree_coreset(
            self,
            tree_idx,
            level,
            seq_from,
            seq_to,
            with_index,
            inverse_class_weight,
            preprocessing_stage,
            sparse_threshold,
            as_df,
            return_preprocessing: bool = False,
            purpose: str = None,
    ) -> dict:
        result = self._get_coreset_internal(
            tree_idx=tree_idx,
            level=level,
            seq_from=seq_from,
            seq_to=seq_to,
            inverse_class_weight=inverse_class_weight,
            purpose=purpose,
        )
        features_out = [f.name for f in self.data_manager.data_params.features]

        if preprocessing_stage == PreprocessingStage.ORIGINAL:
            ind = result["ind"]
            result["X"] = self.data_manager.get_orig_by_index(ind, with_index)

        if preprocessing_stage == PreprocessingStage.USER:
            result["X"] = self.data_manager.convert_encoded_data_to_user(result["X"])

        if preprocessing_stage == PreprocessingStage.AUTO:
            sparse_threshold_ = sparse_threshold if not as_df else 0
            data_processed, features_out, preprocessing_params = self._apply_auto_processing(
                ind=result["ind"],
                X=result["X"],
                y=result["y"],
                w=result["w"],
                sparse_threshold=sparse_threshold_,
                preprocessing_params=PreprocessingParams(),
                calc_replacements=return_preprocessing,
            )
            X_processed = data_processed["X_processed"]
            y_processed = data_processed["y_processed"]
            ind_processed = data_processed["ind_processed"]

            if result["w"] is not None:
                mask = np.isin(result["ind"], ind_processed)
                w_processed = result["w"][mask]
            else:
                w_processed = None
            result = {
                "ind": ind_processed,
                "X": X_processed,
                "y": y_processed,
                "w": w_processed,
                "n_represents": result["n_represents"],
                "features": features_out,
                "props": result.get("props", None)}
            if return_preprocessing:
                result["preprocessing"] = preprocessing_params
        # for ORIGINAL result["data"] already contains DataFrame
        # check if X is a numpy array
        if isinstance(result["X"], pd.DataFrame) or isinstance(result["X"], np.ndarray):
            if preprocessing_stage != PreprocessingStage.ORIGINAL:

                if preprocessing_stage != PreprocessingStage.AUTO and self.data_manager.data_params_internal.categorical_features_:
                    categorical_features = [features_out[i] for i in
                                            self.data_manager.data_params_internal.categorical_features_]
                else:
                    categorical_features = None

                X_df = self._set_df_dtypes(result["X"], features_out=features_out, cat_columns=categorical_features)
                if as_df:
                    result["X"] = X_df
                else:
                    result["X"] = X_df.to_numpy()
        return result

    def _get_coreset_internal(
            self,
            level: int,
            tree_idx: int,
            inverse_class_weight: bool = True,
            preprocessing_stage: Union[str, None] = None,
            seq_from: Any = None,
            seq_to: Any = None,
            purpose: str = None,
    ):
        if self.trees:
            return self.trees[tree_idx].get_coreset(
                level,
                inverse_class_weight=inverse_class_weight,
                seq_from=seq_from,
                seq_to=seq_to,
                purpose=purpose,
            )
        else:
            raise ValueError("get_coreset is only supported when the coreset service is optimized_for 'training'")

    def _validate_and_set_default_chunk_sample_ratio(self, chunk_sample_ratio, is_training):
        """
        Validates the chunk_sample_ratio param. If the value is None, we return the default values based
        on the data size.

        Parameters:
            chunk_sample_ratio: float (it is user provided, so it can have a problematic value).
            is_training: bool
               A flag that indicates if the tree is build for training

        Returns:
            new_chunk_sample_ratio (float): chunk_sample_ratio or the default value
        """
        # chunk_sample_ratio can be 0 or 1 (int-s), valid values
        if isinstance(chunk_sample_ratio, int):
            new_chunk_sample_ratio = float(chunk_sample_ratio)
        else:
            new_chunk_sample_ratio = chunk_sample_ratio
        if not (isinstance(new_chunk_sample_ratio, float) or new_chunk_sample_ratio is None):
            raise TypeError(
                f'The parameter `chunk_sample_ratio` must have a float value from the [0, 1] range or the value None. The provided value is {chunk_sample_ratio}.')

        if new_chunk_sample_ratio is not None and (new_chunk_sample_ratio > 1.0 or new_chunk_sample_ratio < 0.0):
            raise ValueError(
                f'The parameter `chunk_sample_ratio` must have a value from the [0, 1] range or the value None. The provided value is {chunk_sample_ratio}.')
        base = 1000000
        n_instances = self.data_manager.data_params.n_instances
        # Select the default value
        if new_chunk_sample_ratio is None:
            if is_training:
                if n_instances is not None:
                    if n_instances <= base:
                        new_chunk_sample_ratio = 1.0
                    elif n_instances > base and n_instances <= 10 * base:
                        new_chunk_sample_ratio = 0.2
                    elif n_instances > 10 * base and n_instances <= 100 * base:
                        new_chunk_sample_ratio = 0.1
                    elif n_instances > 100 * base and n_instances <= 1000 * base:
                        new_chunk_sample_ratio = 0.05
                    else:
                        new_chunk_sample_ratio = 0.01
                else:
                    new_chunk_sample_ratio = 0.1
            else:
                new_chunk_sample_ratio = 0.0
        return new_chunk_sample_ratio

    def _apply_auto_processing(self, X, sparse_threshold, y=None, w=None, ind=None,
                               preprocessing_params: PreprocessingParams = None,
                               calc_replacements: bool = False,
                               allow_drop_rows: bool = True,
                               ):
        """
        if preprocessing_params are not None, that means that we should apply
        same processing as done for certain level in get_coreset.
        Only case for doing this - auto_preprocessing.
        For other cases we RETURN the preprocessing_params.

        returns tuple (processed data dict, generated feature names, preprocessing params object)
        """

        # due to performance concern we shouldn't have non-numeric data here
        if type(X) == pd.DataFrame:
            assert all([helpers.is_dtype_numeric(t) for t in X.dtypes])
        else:
            if not self.data_manager.has_array_features():
                assert helpers.is_dtype_numeric(X.dtype)
        # replacement for infrequent values - should not exist in any categories[i]
        # and should be larger than any len(categories[i]), because numeric categories[i] should be stored ordered
        # (that is sklearn OHE limitation) just take infrequent_encoded_value = max(len(categories[i])) * 2
        if self.data_manager.has_categorical_features():
            infrequent_encoded_value = max(
                [len(c) for c in self.data_manager.data_params_internal.used_categories_.values()]) * 2

        else:
            infrequent_encoded_value = None

        if preprocessing_params is None or (len(preprocessing_params.ohe_used_categories) == 0 and
                                            len(preprocessing_params.te_used_categories) == 0):
            X_prepared = X
            cat_encoding_config = self.data_manager.cat_encoding_config_clear()
        else:
            # After excluding the prediction context from this code and moving it to have a separate treatment (see
            # auto_preprocessing), this condition, while not visited in prediction, is still visited under
            # refine/resample and various folds-handling/grid-search contexts.

            # for categories that have "infrequent" column, we should do
            #   1) replace in category [1, 3, 'infrequent'] -> [1, 3, infrequent_encoded_value]
            #   2) replace all values that are not in [1, 3] with infrequent_encoded_value
            # infrequent_encoded_value = any numeric value that is does not exist in encoded data, we could use -2
            # all this done to have both in categories and X only numeric data
            X_prepared, ohe_categories_prepared, te_categories_prepared = _prepare_data_and_categories(
                X=X,
                ohe_cat_features_idxs=preprocessing_params.ohe_cat_features_idxs,
                ohe_categories=preprocessing_params.ohe_used_categories,
                te_cat_features_idxs=preprocessing_params.te_cat_features_idxs,
                te_categories=preprocessing_params.te_used_categories,
                replacement_for_infrequent=infrequent_encoded_value,
            )
            cat_encoding_config = self.data_manager.cat_encoding_config_with_categories(
                preprocessing_params=preprocessing_params,
                ohe_categories=ohe_categories_prepared,
                te_categories=te_categories_prepared,
            )

        feature_names = [f.name for f in self.data_manager.data_params.features]
        # apply both OHE and missing-values transformations, both are implemented inside Dataset.data_preprocessed
        dap = DataAutoProcessor(
            X=X_prepared,
            y=y,
            weight=w,
            ind=ind,
            categorical_features=self.data_manager.data_params_internal.categorical_features_,
            array_features=self.data_manager.data_params_internal.array_features_,
            feature_names=feature_names,
            cat_encoding_config=cat_encoding_config,
            array_encoding_config=self.data_manager.array_encoding_config(),
            missing_replacement=self.data_manager.data_params_internal.aggregated_missing_replacements,
            drop_rows_below=self.data_manager.data_params.drop_rows_below if allow_drop_rows else 0,
            drop_cols_above=self.data_manager.data_params.drop_cols_above,
            missing_values_params=preprocessing_params.missing_values_params if preprocessing_params is not None else None,
            calc_replacements=calc_replacements,
        )
        X_processed = dap.handle_missing_and_feature_encoding(sparse_threshold=sparse_threshold)
        # For OHE: features names after OHE = [country_USA, country_infrequent, gender_Female, gender_Male, Age]
        # For TE: for the time being, the only allowed learning task type is binary classification - in which case,
        #         the feature names will not change (once we support multiclass classification, they'll change as well).
        generated_feature_names = dap.get_generated_feature_names(
            non_existing_encoded_value=infrequent_encoded_value,
            used_categories_names=self.data_manager.data_params_internal.used_categories_)
        preprocessing_params = dap.get_auto_preprocessing_params_values()
        y_processed, _, ind_processed = dap.get_processed_arrays()
        data_processed = {
            "X_processed": X_processed.astype(float),
            "y_processed": y_processed,
            "ind_processed": ind_processed,
        }
        return data_processed, generated_feature_names, preprocessing_params

    @telemetry
    def grid_search(
        self,
        param_grid: Union[Dict[str, List], List[Dict[str, List]]],
        tree_indices: List[int] = None,
        level: Optional[int] = None,
        validation_method: str = "cross validation",
        model: Any = None,
        model_fit_params: Dict = None,
        scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
        refit: bool = True,
        verbose: int = 0,
        preprocessing_stage: Union[str, None] = "auto",
        sparse_threshold: float = 0.01,
        error_score: Union[str, float, int] = np.nan,
        validation_size: float = 0.2,
        seq_train_from: Any = None,
        seq_train_to: Any = None,
        seq_validate_from: Any = None,
        seq_validate_to: Any = None,
        n_jobs: int = None,
    ) -> Union[Tuple[Dict, int, pd.DataFrame, BaseEstimator], Tuple[Dict, int, pd.DataFrame]]:
        """
        A method for performing hyperparameter selection by grid search, using the coreset tree.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            param_grid: dict or list of dicts.
                Dictionary with parameters names (str) as keys and lists of parameter settings to try as values, or a list of such dictionaries, in which case the grids
                spanned by each dictionary in the list are explored. This enables searching over any sequence of parameter settings.
            tree_indices:
                Defines the indices of the trees on which the grid search will be performed. By default, grid search is run on all trees.
            level: int, optional.
                The level of the tree on which the training and validation will be performed.
                If None, the best level will be selected.
            validation_method: str, optional.
                Indicates which validation method will be used. The possible values are 'cross validation', 'hold-out validation' and 'seq-dependent validation'.
                If 'cross validation' is selected, the process involves progressing through folds. We first train and validate all hyperparameter
                combinations for each fold, before moving on to the subsequent folds.
            model: A Scikit-learn compatible model instance, optional.
                The model class needs to implement the usual scikit-learn interface.
            model_fit_params: dict, optional.
                Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            refit: bool, optional.
                If True, retrain the model on the whole coreset using the best found hyperparameters, and return the model.
                This model will be used when predict and predict_proba are called.
            verbose: int, optional
                Controls the verbosity: the higher, the more messages.
                    >=1 : The number of folds and hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                    >=2 : The score and time for each fold and hyperparameter combination.
            preprocessing_stage: string, optional, default `auto`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            error_score: "raise" or numeric, optional.
                Value to assign to the score if an error occurs in model training. If set to "raise", the error is raised. If a numeric value is given,
                FitFailedWarning is raised. This parameter does not affect the refit step, which will always raise the error.
            validation_size: float, optional, default 0.2.
                The size of the validation set, as a percentage of the training set size for hold-out validation.
            seq_train_from: Any, optional.
                The starting sequence of the training set for seq-dependent validation.
            seq_train_to: Any, optional.
                The ending sequence of the training set for seq-dependent validation.
            seq_validate_from: Any, optional.
                The starting sequence number of the validation set for seq-dependent validation.
            seq_validate_to: Any, optional.
                The ending sequence number of the validation set for seq-dependent validation.
            n_jobs: int, optional.
                Default: number of CPUs. Number of jobs to run in parallel during grid search.

        Returns:
            A dict with the best hyperparameters setting, among those provided by the user. The keys are the hyperparameters names, while the dicts' values are the hyperparameters values.
            The tree index of the Coreset tree on which the best hyperparameters where found. 
            A Pandas DataFrame holding the score for each hyperparameter combination and fold. For the 'cross validation' method the average across all folds for each hyperparameter combination is included too. 
            If refit=True, the retrained model is also returned.        
            """
        check_feature_for_license("grid_search")
        self._requires_tree()
        self._print_model_warning(model)
        if TreeOptimizedFor.training not in self.optimized_for:
            raise ValueError("`grid_search` is only supported when the coreset service is `optimized_for` 'training'")

        if all(tree.is_empty() for tree in self.trees):
            raise RuntimeError(
                "A Coreset tree is required for the `grid_search` function and any of the validation methods."
            )
        # Default to all trees
        if tree_indices is None:
            tree_indices = list(range(len(self.trees)))
        for tree_idx in tree_indices:
            if tree_idx >= len(self.trees) or tree_idx < -len(self.trees):
                raise ValueError(
                    f"Tree index {tree_idx} is out of range. There are only {len(self.trees)} trees built."
                )
            if self.trees[tree_idx].is_empty():
                raise RuntimeError(
                    f"The Coreset tree {tree_idx} is required for the `grid_search` function "
                    "and any of the validation methods."
                )

        # Check the parameters and raise exceptions if they are not correct
        self._checks_for_grid_search(param_grid, level, scoring, refit, verbose, error_score, validation_method,
                                     validation_size, seq_train_from, seq_train_to, seq_validate_from, seq_validate_to)
        if isinstance(param_grid, dict):
            param_grids = [param_grid]
        else:
            param_grids = param_grid
        if validation_method == 'cross validation':
            return self._grid_search_cross_validation(
                tree_indexes=tree_indices,
                param_grids=param_grids,
                level=level,
                model=model,
                model_fit_params=model_fit_params,
                scoring=scoring,
                refit=refit,
                verbose=verbose,
                preprocessing_stage=preprocessing_stage,
                sparse_threshold=sparse_threshold,
                error_score=error_score,
                n_jobs=n_jobs,
            )
        else:
            return self._grid_search_holdout_validation(
                tree_indexes=tree_indices,
                param_grids=param_grids,
                level=level,
                model=model,
                model_fit_params=model_fit_params,
                scoring=scoring,
                refit=refit,
                verbose=verbose,
                preprocessing_stage=preprocessing_stage,
                sparse_threshold=sparse_threshold,
                validation_size=validation_size,
                seq_train_from=seq_train_from,
                seq_train_to=seq_train_to,
                seq_validate_from=seq_validate_from,
                seq_validate_to=seq_validate_to,
                n_jobs=n_jobs,
            )

    @telemetry
    def get_hyperparameter_tuning_data(
            self,
            tree_idx: int = 0,
            level: int = None,
            validation_method: str = "cross validation",
            preprocessing_stage: Union[str, None] = "user",
            sparse_threshold: float = 0.01,
            validation_size: float = 0.2,
            seq_train_from: Any = None,
            seq_train_to: Any = None,
            seq_validate_from: Any = None,
            seq_validate_to: Any = None,
            as_df: bool = True,
    ) -> Dict[str, Union[ndarray, FoldIterator, Any]]:
        """
        A method for retrieving the data for hyperparameter tuning with cross validation, using the coreset tree.
        The returned data can be used with Scikit-learn’s GridSearchCV, with skopt’s BayesSearchCV and with any other hyperparameter tuning method that can accept a fold iterator object.
        **Note:** When using this method with Scikit-learn's `GridSearchCV` and similar methods, the `refit` parameter must be set to `False`.
        This is because the returned dataset (X, y and w) includes both training and validation data due to the use of a splitter. The returned dataset (X, y and w) is the concatenation of training data for all folds followed by validation data for all folds.
        By default, GridSearchCV refits the estimator on the entire dataset, not just the training portion, and this behavior cannot be modified and is incorrect.
        In this case, refit should be handled manually after the cross-validation process, by calling get_coreset with the same parameters that were passed to this function to retrieve the data and then fitting on the returned data using the best hyperparameters found in GridSearchCV.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional.
                The level of the tree on which the training and validation will be performed.
                If None, the best level will be selected.
            validation_method: str, optional.
                Indicates which validation method will be used. The possible values are 'cross validation', 'hold-out validation' and 'seq-dependent validation'.
            preprocessing_stage: string, optional, default `user`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **original** - Return the data as it was handed to the Coreset’s build function
                (The data_params.save_orig flag should be set for this option to be available).<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01.
                Returns the features (X) as a sparse matrix if the data density after preprocessing is below sparse_threshold,
                otherwise, will return the data as an array (Applicable only for preprocessing_stage='auto').
            validation_size: float, optional, default 0.2.
                The size of the validation set, as a percentage of the training set size for hold-out validation.
            seq_train_from: Any, optional.
                The starting sequence of the training set for seq-dependent validation.
            seq_train_to: Any, optional.
                The ending sequence of the training set for seq-dependent validation.
            seq_validate_from: Any, optional.
                The starting sequence number of the validation set for seq-dependent validation.
            seq_validate_to: Any, optional.
                The ending sequence number of the validation set for seq-dependent validation.
            as_df: boolean, optional, default False.
                When True, returns the X as a pandas DataFrame.

        Returns:
            A dictionary with the following keys:
                ind: The indices of the data.
                X: The data.
                y: The labels.
                w: The weights.
                splitter: The fold iterator.
                model_params: The model parameters.
        """

        check_feature_for_license("get_hyperparameter_tuning_data")
        self._requires_tree()
        return self._get_hyperparameter_tuning_data(
            tree_idx=tree_idx,
            level=level,
            validation_method=validation_method,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            validation_size=validation_size,
            seq_train_from=seq_train_from,
            seq_train_to=seq_train_to,
            seq_validate_from=seq_validate_from,
            seq_validate_to=seq_validate_to,
            as_df=as_df,
        )

    def _get_hyperparameter_tuning_data(
            self,
            tree_idx: int,
            level: int = None,
            validation_method: str = "cross validation",
            preprocessing_stage: Union[str, None] = None,
            sparse_threshold: float = 0.01,
            validation_size: float = 0.2,
            seq_train_from: Any = None,
            seq_train_to: Any = None,
            seq_validate_from: Any = None,
            seq_validate_to: Any = None,
            inverse_class_weight: bool = False,
            as_df: bool = True,
    ):

        sparse_threshold_ = sparse_threshold if not as_df else 0

        if validation_method == 'cross validation':
            if level is None:
                validation_level = self._find_optimal_level()
            else:
                validation_level = level
            folds = self._get_folds_structure(tree_idx=tree_idx, level=validation_level)
            coreset_validation_data = self._coreset_data_and_folds_limits(folds['nodes'])

            folds_data = self._prepare_folds(
                folds=folds,
                coreset_validation_data=coreset_validation_data
            )
            # Unpack the folds data and concatenate all X, y, w, ind, X_validate, y_validate, ind_validate
            all_data = [fold for fold in folds_data]
            if len(all_data) == 0:
                raise ValueError("Can't run get_hyperparameter_tuning_data on an empty tree.")
            ind_training = np.concatenate([fold[0] for fold in all_data])
            X = np.concatenate([fold[1] for fold in all_data])
            y = np.concatenate([fold[2] for fold in all_data])
            w = np.concatenate([fold[3] for fold in all_data])
            ind_validate = np.concatenate([fold[4] for fold in all_data])
            X_validate = np.concatenate([fold[5] for fold in all_data])
            y_validate = np.concatenate([fold[6] for fold in all_data])
            # We need to keep the fold indexes and the random sampled indexes for the fold iterator so we can
            # reproduce the same folds
            fold_indexes = [len(fold[3]) for fold in all_data]
            fold_random_sampled_indexes = [len(fold[4]) for fold in all_data]
            total_sum_orig_weights = self._compute_total_sum_orig_weights([fold[9] for fold in all_data],
                                                                          already_list=True)
            # Preprocess everything at once
            ind, X, y, w, ind_val, X_validate, y_validate, preprocessing_info = self._prepare_fold_data(
                tree_idx,
                X,
                y,
                w,
                X_validate,
                y_validate,
                None,
                preprocessing_stage,
                total_sum_orig_weights,
                dict(),
                inverse_class_weight,
                sparse_threshold_,
            )
            ind_training = ind_training[ind]
            ind_validate = ind_validate[ind_val]
            # Create the fold iterator
            fold_iterator = FoldIterator(fold_indexes, fold_random_sampled_indexes)
        else:
            datetime_format = self.data_manager.data_params_internal.seq_datetime_format
            seq_params = _compose_seq_params(seq_train_from, seq_train_to, seq_validate_from, seq_validate_to,
                                             datetime_format)
            (
                total_n_represents,
                total_sum_orig_weights,
                X_training,
                y_training,
                w_training,
                validation_nodes_levels,
                validation_nodes_indexes,
            ) = self._prepare_data_holdout_validate(
                level=level, tree_idx=tree_idx, seq_params=seq_params, validation_size=validation_size
            )
            ind_training, X, y, w, ind_validate, X_validate, y_validate, preprocessing_info = self._prepare_fold_data(
                tree_idx,
                X_training,
                y_training,
                w_training,
                validation_nodes_levels,
                validation_nodes_indexes,
                None,
                preprocessing_stage,
                total_sum_orig_weights,
                dict(),
            )
            fold_iterator = FoldIterator([X.shape[0]], [X_validate.shape[0]])

        X = vstack([X, X_validate]) if isinstance(X, csr_matrix) else np.concatenate([X, X_validate], axis=0)
        if as_df:
            if preprocessing_stage == PreprocessingStage.AUTO:
                X = self._set_df_dtypes(X, features_out=preprocessing_info['features_out'])
            else:
                cat_columns = self.data_manager.data_params_internal.categorical_features_
                cat_col_names = [preprocessing_info['features_out'][i] for i in cat_columns]
                X = self._set_df_dtypes(X, features_out=preprocessing_info['features_out'], cat_columns=cat_col_names)
        else:
            # in this case we're returning a numpy array and we need to convert the categorical features names
            # to their corresponding indices so they can actually be used
            if preprocessing_info['model_params'].get('categorical_feature') is not None:
                preprocessing_info['model_params'][
                    'categorical_feature'] = self.data_manager.data_params_internal.categorical_features_
            if preprocessing_info['model_params'].get('cat_features') is not None:
                preprocessing_info['model_params'][
                    'cat_features'] = self.data_manager.data_params_internal.categorical_features_
        return {
            'ind': np.concatenate([ind_training, ind_validate]),
            'X': X,
            'y': np.concatenate([y, y_validate]),
            'w': np.concatenate([w, np.ones(len(y_validate))]),
            'splitter': fold_iterator,
            'model_params': preprocessing_info['model_params'],
        }

    def _grid_search_cross_validation(
            self,
            tree_indexes: List[int],
            param_grids: List[Dict[str, List]],
            level: int = None,
            model: Any = None,
            model_fit_params: Dict = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            refit: bool = True,
            verbose: int = 0,
            preprocessing_stage: Union[str, None] = None,
            sparse_threshold: float = 0.01,
            error_score: Union[str, float, int] = np.nan,
            n_jobs: int = None,
    ):
        """
        Method for performing hyperparameter selection by grid search based on cross-vaidation.

        Parameters
        ----------
        param_grids: list of dicts
            A list of such dictionaries with parameters names (str) as keys and lists of parameter settings to try as
            values. This enables searching over any sequence of parameter settings.
        level: int, optional
            The level of the tree on which the training and validation will be performed.
            If None, the best level will be selected.
        model: A Scikit-learn compatible model instance, optional.
            The model class needs to implement the usual scikit-learn interface.
            Default: instantiate the service model class.
        model_fit_params: dict, optional
            Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
        scoring: callable or string, optional
            If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
            where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
            For example, it can be produced using sklearn.metrics.make_scorer
            (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
            If it is a string, it must be a valid name of a Scikit-learn scoring method
            (see https://scikit-learn.org/stable/modules/model_evaluation.html)
            If None, the default scorer of the current model is used.
        refit: bool, optional
            If True, retrain the model on the whole coreset using the best found hyperparameters, and return the model.
        verbose: int, optional
            Controls the verbosity: the higher, the more messages.
                >=1 : The number of folds and hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                >=2 : The score and time for each fold and hyperparameter combination.
            Default: 0
        preprocessing_stage: string, optional, default `user` when LightGBM or CatBoost are used, `auto` when Scikit-learn or XGBoost is used<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
        sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
            if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
            (Applicable only for preprocessing_stage='auto').
        error_score: "raise" or numeric, optional.
            Value to assign to the score if an error occurs in model training. If set to "raise", the error is raised. If a numeric value is given,
            FitFailedWarning is raised. This parameter does not affect the refit step, which will always raise the error.
        Returns
        -------
            A dict with the best hyperparameters setting, among those provided by the user. The keys are the hyperparameters names,
            while the dicts' values are the hyperparameters values.
            A Pandas DataFrame holding the score for each hyperparameter combination and fold. For the 'cross validation'
            method the average across all folds for each hyperparameter combination is included too.
            If refit=True, the retrained model is also returned.

        """
        assert tree_indexes is not None and len(tree_indexes) > 0
        assert all(not tree.is_empty() for tree in [self.trees[i] for i in tree_indexes])
        # Grid search for every tree
        best_params_per_tree = {}
        folds_scores_per_tree = {}
        async_tasks, executor = get_parallel_executor(n_jobs)
        first_log = False
        for tree_idx in tree_indexes:
            if level is None:
                validation_level = self._find_optimal_level(tree_idx=tree_idx)
            else:
                validation_level = level

            folds = self._get_folds_structure(tree_idx, validation_level)
            empty_folds = []
            for fold in folds["nodes"]:
                empty_folds.append(all([node.is_empty() for node in fold]))
            if all(empty_folds):
                raise ValueError("Can't run grid search on empty folds! Check that the coreset contains data.")

            coreset_validation_data = self._coreset_data_and_folds_limits(tree_idx, folds["nodes"])

            total_sum_orig_weights = self._compute_total_sum_orig_weights([l[0] for l in folds["nodes"]])
            model_params = {}
            (
                _,
                coreset_validation_data["X"],
                coreset_validation_data["y"],
                coreset_validation_data["w"],
                preprocessing_info,
            ) = self._prepare_training_fold_data(
                coreset_validation_data["X"],
                coreset_validation_data["y"],
                coreset_validation_data["w"],
                model,
                preprocessing_stage,
                total_sum_orig_weights,
                model_params,
            )
            n_folds = len(folds["nodes"])
            add_telemetry_attribute("No. of folds", str(n_folds))

            folds_data = self._prepare_folds(
                tree_idx=tree_idx, folds=folds, coreset_validation_data=coreset_validation_data
            )
            if verbose >= 1:
                ss = time.time()
                total_combinations = reduce(lambda x, y: x * len(list(itertools.product(*y.values()))), param_grids, 1)
                # TODO Dacian: include number of trees here.
                if first_log:
                    print(
                        f"Fitting on level {validation_level} with {n_folds} folds for {total_combinations} hyperparameter combinations "
                        f"across {len(tree_indexes)} Coreset tree, totaling {len(tree_indexes) * total_combinations * n_folds} fits"
                    )
                    first_log = False

            folds_scores = defaultdict(list)
            # if n_jobs is None or 1 or cant limit blas the executor will be None
            async_tasks = []
            cancel_event = Event()
            try:
                for validation_fold_index, (
                        _,
                        X_training_pre,
                        y_training_pre,
                        w_training_pre,
                        _,
                        X_validate,
                        y_validate,
                        fold_level,
                        total_n_represents,
                        total_sum_orig_weights,
                ) in enumerate(folds_data):

                    # stop submitting tasks if cancel event
                    if cancel_event.is_set():
                        break

                    _, X_validate_pre, y_validate_pre = self._prepare_validation_fold_data(
                        X_validate=X_validate,
                        y_validate=y_validate,
                        model=model,
                        preprocessing_stage=preprocessing_stage,
                        fold_model_params=model_params,
                        preprocessing_info=preprocessing_info,
                        sparse_threshold=sparse_threshold,
                    )

                    # generate all possible model params combinations
                    params_values_combinations = self._get_model_params_combination(param_grids)
                    for fold_model_params in params_values_combinations:
                        fold_model_params.update(model_params)
                        fold_args = dict(
                            tree_idx=tree_idx,
                            X_training_pre=X_training_pre,
                            X_validate_pre=X_validate_pre,
                            error_score=error_score,
                            folds_scores=folds_scores,
                            level=fold_level,
                            model=model,
                            model_fit_params=model_fit_params,
                            model_params=fold_model_params,
                            n_folds=n_folds,
                            preprocessing_info=preprocessing_info,
                            preprocessing_stage=preprocessing_stage,
                            scoring=scoring,
                            validation_fold_index=validation_fold_index,
                            verbose=verbose,
                            w_training_pre=w_training_pre,
                            y_training_pre=y_training_pre,
                            y_validate_pre=y_validate_pre,
                            parallel=executor is not None,
                            cancel_event=cancel_event,
                            sparse_threshold=sparse_threshold,
                        )

                        if executor is not None:
                            # executor not None meaning that we are in a parallel mode
                            # we submit (fold_index, future object) so that we can later get tasks by fold index
                            async_tasks.append(
                                (validation_fold_index, executor.submit(self._process_fold, **fold_args))
                            )
                        else:
                            self._process_fold(**fold_args)

                    # check we have enough memory for x_train_pre x_validate_pre of a new fold
                    # the _pre are after data encoding
                    # relevant only for a parallel mode since in a sequential mode we will have only one fold in memory,
                    # and it's not the last fold
                    if executor is not None and validation_fold_index + 1 < n_folds:

                        available_batch_size = tree_utils.evaluate_max_batch_size(
                            X_training_pre.shape[1], available=True
                        )
                        expected_batch_size = X_validate_pre.shape[0] + X_training_pre.shape[0]
                        if available_batch_size < expected_batch_size:
                            # get the earliest submitted fold that is still running and wait for its task to complete
                            # for example we have memory for 3 folds out of 4,
                            # so we will wait for the 1st fold to finish and submit 4th fold
                            # the async_tasks is a list of tuples [(fold index, future),...]
                            required_mb = (
                                    tree_utils.evaluate_batch_to_memory(expected_batch_size,
                                                                        X_training_pre.shape[1]) * 1024
                            )
                            available_mb = (
                                    tree_utils.evaluate_batch_to_memory(available_batch_size, X_training_pre.shape[1])
                                    * 1024
                            )
                            if verbose >= 1:
                                print(
                                    f"Available memory: {int(available_mb)}MB, Required memory: {required_mb}MB. Waiting to complete some of the tasks in order to progress with additional ones."
                                )
                            # get running folds
                            running_folds = [f[0] for f in async_tasks if f[1].running()]
                            if running_folds:
                                # get the earliest running fold and wait for it to finish
                                min_fold = min(running_folds)
                                wait(
                                    [f[1] for f in async_tasks if f[0] == min_fold], return_when=futures.FIRST_EXCEPTION
                                )

                if executor is not None:
                    # wait for the submitted tasks to complete
                    # the async_tasks is a list of tuples [(fold index, future),...]
                    self._wait_to_finish_tasks([f[1] for f in async_tasks], executor)

            except Exception:
                raise
                if executor is not None:
                    executor.shutdown(wait=False)

            # Compute average scores
            averages = {}
            for model_params_key, scores in folds_scores.items():
                average_score = sum(scores) / len(scores)
                averages[model_params_key] = average_score

            # Find the best average score and its corresponding model_params
            best_model_params_key = max(averages, key=lambda k: averages.get(k))
            best_score = averages[best_model_params_key]
            best_parameters = dict(best_model_params_key)
            best_params_per_tree[tree_idx] = {"model_params": best_parameters, "score": best_score}
            folds_scores["sample_params"] = self._data_tuning_params_cls._filter(self.trees[tree_idx].sample_params)
            folds_scores_per_tree[tree_idx] = folds_scores

        if executor is not None:
            executor.shutdown(wait=False)

        best_tree_idx = max(best_params_per_tree, key=lambda k: best_params_per_tree[k]["score"])
        best_parameters = best_params_per_tree[best_tree_idx]["model_params"]
        add_telemetry_attribute("Best score for grid search", str(best_score))

        # Prepare df of scores
        all_scores = _scores_to_df(folds_scores_per_tree, only_averages=False)

        trained_model = (
            self._fit(
                tree_idx=best_tree_idx,
                model=model,
                model_fit_params=model_fit_params,
                model_params=best_parameters,
                level=validation_level,
                coreset_params=self.coreset_params["training"],
                preprocessing_stage=preprocessing_stage,
                sparse_threshold=sparse_threshold,
            )
            if refit
            else None
        )

        if verbose >= 1:
            print(
                f"Grid_search completed in {'{0:.3f}'.format(time.time() - ss)}. The best hyperparameter "
                f"combination is {best_parameters}. The best tree is {best_tree_idx} with the following data tuning parameters: {self._data_tuning_params_cls._filter(self.trees[best_tree_idx].sample_params)} "
                f"Average score across folds is {'{0:.4f}'.format(best_score)}."
            )
        if refit:
            return best_parameters, best_tree_idx, all_scores, trained_model
        else:
            return best_parameters, best_tree_idx, all_scores

    def _process_fold(
            self,
            tree_idx: int,
            X_training_pre,
            X_validate_pre,
            error_score,
            folds_scores,
            level,
            model,
            model_fit_params,
            model_params,
            n_folds,
            preprocessing_info,
            preprocessing_stage,
            sparse_threshold,
            scoring,
            validation_fold_index,
            verbose,
            w_training_pre,
            y_training_pre,
            y_validate_pre,
            parallel=False,
            cancel_event: Event = None,
    ):

        # in case the cancel event was called we skip the task execution
        if cancel_event is not None and cancel_event.is_set():
            return

        start = time.time()
        # update the model params with cat related params
        try:
            try_validate_args = dict(X_training=X_training_pre,
                                     y_training=y_training_pre,
                                     w_training=w_training_pre,
                                     X_validate=X_validate_pre,
                                     y_validate=y_validate_pre,
                                     level=level,
                                     model=copy.deepcopy(model),
                                     model_fit_params=model_fit_params,
                                     preprocessing_stage=preprocessing_stage,
                                     sparse_threshold=sparse_threshold,
                                     preprocessing_info=preprocessing_info,
                                     scoring=scoring,
                                     **model_params)
            if parallel:
                with threadpool_limits(limits=1, user_api='blas'):
                    self._adjust_model_parallelism(model, try_validate_args)
                    fold_score, _ = self._train_and_validate_fold(**try_validate_args)
            else:
                fold_score, _ = self._train_and_validate_fold(**try_validate_args)
        except FitFailedWarning as e:
            # In principle, error_score can be numeric or 'raise'
            if isinstance(error_score, float) or isinstance(error_score, int) or error_score == np.nan:
                warnings.warn(
                    'Model fit failed. The score on this train-test partition for these parameters '
                    'will be set to np.nan.',
                    FitFailedWarning)
                fold_score = error_score
            else:
                if cancel_event is not None:
                    cancel_event.set()
                raise e
        end = time.time()
        validation_time = end - start
        if verbose >= 2:
            print(
                f"Tree {tree_idx}; Data Tuning Params: {self._data_tuning_params_cls._filter(self.trees[tree_idx].sample_params)}; "
                f"Validation Fold: {validation_fold_index + 1}/{n_folds}; Hyperparameters: {model_params}; "
                f"Score: {'{0:.4f}'.format(fold_score)}; Time: {'{0:.3f}'.format(validation_time)} (s)."
            )
        # lists in dict are not hashable
        model_params_key = frozenset([item for item in model_params.items() if not isinstance(item[1],
                                                                                              list)])
        folds_scores[model_params_key].append(fold_score)

    def _get_model_params_combination(self, param_grids: Union[List, Dict]):
        # get param combinations for either a single param grid or a list of grids
        def generate_param_combinations(param_grid):
            params_names = list(param_grid.keys())
            params_values = param_grid.values()
            return (dict(zip(params_names, params_values_combination))
                    for params_values_combination in itertools.product(*params_values))

        if isinstance(param_grids, list):
            for param_grid_i in param_grids:
                for param_combination in generate_param_combinations(param_grid_i):
                    yield param_combination
        else:
            yield generate_param_combinations(param_grids)

    def _prepare_training_fold_data(
            self,
            X_training,
            y_training,
            w_training,
            model,
            preprocessing_stage,
            total_sum_orig_weights,
            fold_model_params,
            inverse_class_weight=True,
            sparse_threshold=0
    ):
        """
        Prepare training fold data with encoding and update the fold_model_params
        with categorical params from _prepare_encoded_data
        Args:
            X_training:
            y_training:
            w_training:
            model:
            preprocessing_stage:
            total_sum_orig_weights:
            fold_model_params:
            inverse_class_weight:
            sparse_threshold:

        Returns:
            ind, X, y, w ready for training after encoding, preprocessing info
        """
        w_training = self._weights_adjustment(model, fold_model_params,
                                              total_sum_orig_weights, w_training, y_training, inverse_class_weight)

        # Check for infinity and nan values.
        if self.data_manager.data_params_internal.array_features_:
            if isinstance(X_training, pd.DataFrame):
                X_training = X_training.to_numpy()
            inf_mask = np.isinf(X_training[:,
                                [c for c in range(X_training.shape[1]) if
                                 c not in self.data_manager.data_params_internal.array_features_]].astype(float))
        else:
            inf_mask = np.isinf(X_training)

        if np.any(inf_mask):
            if self.data_manager.data_params_internal.array_features_:
                inf_mask = DataAutoProcessor.adjust_array_features_mask(inf_mask,
                                                                        self.data_manager.data_params_internal.array_features_)
            X_training[inf_mask] = np.nan

        if self.data_manager.data_params_internal.array_features_:
            missing_mask = np.isnan(X_training[:,
                                    [c for c in range(X_training.shape[1]) if
                                     c not in self.data_manager.data_params_internal.array_features_]].astype(float))
        else:
            missing_mask = np.isnan(X_training)

        calc_replacements = missing_mask.any().any()
        # prepare training x,y,w
        prepared_data = self._prepare_encoded_data(
            X=X_training,
            y=y_training,
            weights=w_training,
            params={'preprocessing_stage': preprocessing_stage},
            model=model,
            calc_replacements=calc_replacements,
            model_params=fold_model_params,
            sparse_threshold=sparse_threshold,
        )
        fold_model_params.update(prepared_data["model_params"])
        ind_training_pre, X_training_pre, y_training_pre, w_training_pre = prepared_data['data']
        return (ind_training_pre, X_training_pre, y_training_pre, w_training_pre,
                prepared_data["preprocessing_info"])

    def _prepare_validation_fold_data(self, X_validate, y_validate, model, preprocessing_stage, fold_model_params,
                                      preprocessing_info, sparse_threshold=0):
        """
        Prepare validation fold data using the provided used_categories and missing_values_params
        Args:
            X_validate:
            y_validate:
            model:
            preprocessing_stage:
            fold_model_params:
            preprocessing_info:
            sparse_threshold:

        Returns:
            ind, X, y ready for validation after encoding
        """

        # prepare validation data
        ind_validate_pre, X_validate_pre, y_validate_pre, _ = self._prepare_encoded_data(
            X=X_validate,
            y=y_validate,
            weights=None,
            params={"preprocessing_stage": preprocessing_stage},
            preprocessing_params=PreprocessingParams.from_dict(preprocessing_info),
            allow_drop_rows=False,
            model=model,
            model_params=fold_model_params,
            sparse_threshold=sparse_threshold,
        )["data"]
        return ind_validate_pre, X_validate_pre, y_validate_pre

    def _prepare_fold_data(
            self,
            tree_idx,
            X_training,
            y_training,
            w_training,
            validate_levels_or_X,
            validate_indexes_or_y,
            model,
            preprocessing_stage,
            total_sum_orig_weights,
            fold_model_params,
            inverse_class_weight=True,
            sparse_threshold=0,
    ):
        """
        Prepare fold data with encoding and update the fold_model_params
        with categorical params from _prepare_encoded_data
        Args:
            X_training:
            y_training:
            w_training:
            validate_nodes_or_X: list of nodes or X
            validate_indexes_or_y: list of indexes or y
            model:
            preprocessing_stage:
            total_sum_orig_weights:
            fold_model_params:
            inverse_class_weight:
            sparse_threshold:

        Returns:
            ind_training, X_training, y_training, w_training, ind_validate, X_validate, y_validate, preprocessing_info
        """
        ind_training_pre, X_training_pre, y_training_pre, w_training_pre, preprocessing_info = self._prepare_training_fold_data(
            X_training, y_training, w_training, model, preprocessing_stage, total_sum_orig_weights, fold_model_params,
            inverse_class_weight, sparse_threshold)

        preprocessing_info["model_params"] = fold_model_params

        if isinstance(validate_levels_or_X, list):
            validate_levels_or_X, validate_indexes_or_y = self._get_chunks_data_for_holdout_validate(
                tree_idx, validate_levels_or_X, validate_indexes_or_y, len(preprocessing_info["features_out"])
            )

        # prepare validation data
        ind_validate_pre, X_validate_pre, y_validate_pre = self._prepare_validation_fold_data(
            validate_levels_or_X, validate_indexes_or_y, model, preprocessing_stage, fold_model_params,
            preprocessing_info, sparse_threshold)

        return (ind_training_pre, X_training_pre, y_training_pre, w_training_pre, ind_validate_pre, X_validate_pre,
                y_validate_pre,
                preprocessing_info)

    def _fit_after(self, model, params: dict, preprocessing_info: dict = None):
        """
        The function should be used to save the model and everything related to the model, following
        auto_preprocessing, predict and predict_proba calls.
        The models created after every hyperparameter combination in grid_search, *should not* use this function, and
        same goes for the 3 validation methods holdout_validate, cross_validate and seq_dependent_validate.
        There are only two use cases that should trigger this function:
            (a) A call to fit (the fit function exposed to the user).
            (b) A call to grid_search where refit=True and in this case only during the refit this function is called.
        Currently, the function is called only from _fit in CoresetServiceBase, which covers both use cases mentioned
        above, and it should stay this way.
        """
        self.model = model
        self.data_manager.data_params_internal.last_fit_preprocessing_stage = (
            params.get("preprocessing_stage") if params is not None else None
        )
        self.preprocessing_info = decode_categories(
            preprocessing_info, self.data_manager.data_params_internal.used_categories_)

        # Sort decoded categories with NaN values appended at the end of the sorted lists.
        # Categories sorting is necessary because the TE encoder expects the provided categories (used_categories)
        # to be sorted and NaN to be the last element of the array. In our case, this only happens during
        # predict/predict_proba, because that's the only place where we don't actually re-encode the data.
        # The sorting obviously applies only to categorical data. Contrary to the TE, the OHE does not require sorted
        # data - but we sort the OHE data in the same go for completeness purposes.
        te_encodings = self.preprocessing_info.get("te_encodings")
        for used_cat_key in ["ohe_used_categories", "te_used_categories"]:
            used_categories = self.preprocessing_info[used_cat_key]
            for i, item in enumerate(used_categories):
                # if nan exists in the array, move it to the end and sort
                if pd.isna(item).any():
                    # Sort the non-NaN values and move NaN to the end
                    sorted_indices = np.argsort(item[~pd.isna(item)])
                    item_sorted = np.concatenate([item[~pd.isna(item)][sorted_indices], [np.nan]])
                    if used_cat_key == "te_used_categories":
                        te_encoding_sorted = te_encodings[i][~pd.isna(item)][sorted_indices]
                        te_encoding_sorted = np.concatenate([te_encoding_sorted, [np.nan]])
                else:
                    # Just sort the data
                    sorted_indices = np.argsort(item)
                    item_sorted = np.array(item)[sorted_indices]
                    if used_cat_key == "te_used_categories":
                        te_encoding_sorted = te_encodings[i][sorted_indices]

                # Update the arrays with sorted values
                self.preprocessing_info[used_cat_key][i] = item_sorted
                if used_cat_key == "te_used_categories":
                    self.preprocessing_info["te_encodings"][i] = te_encoding_sorted

    def _fit_internal(
            self,
            X,
            y,
            weights,
            model=None,
            params: Dict = None,
            preprocessing_info: Dict = None,
            sparse_threshold: float = 0.01,
            model_fit_params: Dict = None,
            **model_params,
    ):
        if X.size == 0:
            raise ValueError(
                f"Can't fit on empty data! Check that the coreset contains data. Given X: {X} with shape: {X.shape}")
        # decode y if needed

        model_params = model_params or dict()
        model_fit_params = model_fit_params or dict()

        if model is None:
            model = self.model_cls(**model_params)
        else:
            model.set_params(**model_params)
        # Not for all modeling classes' "fit" method, the sample weights are in the 3rd positional argument (Catboost,
        # for example); however, the name of the argument for all of them - as far as we know - is called
        # "sample_weight" - and that's why we specifically use the named argument for weights.
        model.fit(X, y, sample_weight=weights, **model_fit_params)

        return model

    def _prepare_encoded_data(self,
                              X, y, weights,
                              params,
                              preprocessing_params: PreprocessingParams = None,
                              allow_drop_rows=True,
                              model=None,
                              calc_replacements=False,
                              model_params=None,
                              sparse_threshold=0,
                              ):
        """
        On the base of preprocessing_stage return convert encoded data to USER or AUTO mode

        Either preprocessing_params are None and we calc and return it,
        or we use them, because we should get output data corresponding to these params.
        Due to missing values handling rows could be deleted, that is why we accept and return y and weights
        """
        if params is None:
            params = {}
        if type(X) == pd.DataFrame:
            if not self.data_manager.has_array_features():
                assert all([helpers.is_dtype_numeric(t) for t in X.dtypes])
        else:
            if not self.data_manager.has_array_features():
                assert helpers.is_dtype_numeric(X.dtype)
        preprocessing_stage = params.get("preprocessing_stage")
        preprocessing_stage = self._get_default_preprocessing_stage(preprocessing_stage, model)

        if preprocessing_stage not in (PreprocessingStage.USER, PreprocessingStage.AUTO):
            raise ValueError(f"preprocessing_stage={params.get('preprocessing_stage')} is not an allowed value")

        if preprocessing_stage == PreprocessingStage.AUTO:
            data_processed, features_out, preprocessing_params = self._apply_auto_processing(
                ind=np.arange(X.shape[0]),
                X=X,
                y=y,
                w=weights,
                sparse_threshold=sparse_threshold,
                preprocessing_params=preprocessing_params,
                allow_drop_rows=allow_drop_rows,
                calc_replacements=calc_replacements,
            )
            X_processed = data_processed["X_processed"]
            y_processed = data_processed["y_processed"]
            ind_processed = data_processed["ind_processed"]
            w_processed = weights[ind_processed] if weights is not None else None
            return {
                "data": (ind_processed,
                         X_processed.astype(float),
                         y_processed,
                         w_processed),
                "preprocessing_info": {**preprocessing_params.to_dict(), **{"features_out": features_out}},
                "model_params": model_params,
            }
        else:
            X_user = self.data_manager.convert_encoded_data_to_user(X)
            features_out = [f.name for f in self.data_manager.data_params.features]

            X_user, model_params = self._prepare_categorical_model_and_X(
                X=X_user,
                model=model,
                model_params=model_params,
            )
            return {
                "data": (np.arange(len(X_user)), X_user, y, weights),
                "preprocessing_info": {**PreprocessingParams().to_dict(), **{"features_out": features_out}},
                "model_params": model_params,
            }

    def _grid_search_holdout_validation(
            self,
            tree_indexes: List[int],
            param_grids: List[Dict[str, List]],
            level: int = None,
            model: Any = None,
            model_fit_params: Dict = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            refit: bool = True,
            verbose: int = 0,
            preprocessing_stage: Union[str, None] = None,
            sparse_threshold: float = 0.01,
            validation_size: float = 0.2,
            seq_train_from: Any = None,
            seq_train_to: Any = None,
            seq_validate_from: Any = None,
            seq_validate_to: Any = None,
            n_jobs: int = None,
    ):
        """
        Method for performing hyperparameter selection by grid search using hold-out validation.

        Parameters
        ----------
        param_grids: list of dicts
            A list of such dictionaries with parameters names (str) as keys and lists of parameter settings to try as
            values. This enables searching over any sequence of parameter settings.
        level: int, optional
            The level of the tree on which the training and validation will be performed.
            If None, the best level will be selected.
        model: A Scikit-learn compatible model instance, optional.
            The model class needs to implement the usual scikit-learn interface.
            Default: instantiate the service model class.
        model_fit_params: dict, optional
            Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
        scoring: callable or string, optional
            If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
            where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
            For example, it can be produced using sklos.cpu_count()earn.metrics.make_scorer
            (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
            If it is a string, it must be a valid name of a Scikit-learn scoring method
            (see https://scikit-learn.org/stable/modules/model_evaluation.html)
            If None, the default scorer of the current model is used.
        refit: bool, optional
            If True, retrain the model on the whole coreset using the best found hyperparameters, and return the model.
        verbose: int, optional
            Controls the verbosity: the higher, the more messages.
                >=1 : The number of hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                >=2 : The score and time for each hyperparameter combination.
        preprocessing_stage: string, optional, default `user` when LightGBM or CatBoost are used, `auto` when Scikit-learn or XGBoost is used<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
        sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
            if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
            (Applicable only for preprocessing_stage='auto').
        validation_size: float, optional, default 0.2.
            The size of the validation set, as a percentage of the training set size for hold-out validation.
        seq_train_from: Any, optional.
            The starting sequence of the training set.
        seq_train_to: Any, optional.
            The ending sequence of the training set.
        seq_validate_from: Any, optional.
            The starting sequence number of the validation set.
        seq_validate_to: Any, optional.
            The ending sequence number of the validation set.
        Returns
        -------
            A dict with the best hyperparameters setting, among those provided by the user. The keys are the hyperparameters names,
            while the dicts' values are the hyperparameters values.
            A Pandas DataFrame holding the score for each hyperparameter combination and fold. For the 'cross validation' method
            the average across all folds for each hyperparameter combination is included too.
            If refit=True, the retrained model is also returned.

        """
        assert tree_indexes is not None and len(tree_indexes) > 0
        assert all(not tree.is_empty() for tree in [self.trees[i] for i in tree_indexes])
        # Grid search for every tree
        best_params_per_tree = {}
        scores_per_tree = {}

        datetime_format = self.data_manager.data_params_internal.seq_datetime_format
        seq_params = _compose_seq_params(seq_train_from, seq_train_to, seq_validate_from, seq_validate_to,
                                         datetime_format)
        first_log = True
        for tree_idx in tree_indexes:
            scores = defaultdict()
            (
                total_n_represents,
                total_sum_orig_weights,
                X_training,
                y_training,
                w_training,
                validation_nodes_levels,
                validation_nodes_indexes,
            ) = self._prepare_data_holdout_validate(
                tree_idx=tree_idx, level=level, seq_params=seq_params, validation_size=validation_size
            )

            if verbose >= 1:
                ss = time.time()
                if first_log:
                    total_combinations = reduce(
                        lambda x, y: x * len(list(itertools.product(*y.values()))), param_grids, 1
                    )
                    print(
                        f"Fitting {total_combinations} hyperparameter combinations across {len(tree_indexes)} Coreset tree, totalling {len(tree_indexes) * total_combinations} fits."
                    )
                    first_log = False

            fold_model_params = {}
            _, X_training_pre, y_training_pre, w_training_pre, _, X_validate_pre, y_validate_pre, preprocessing_info = (
                self._prepare_fold_data(
                    tree_idx,
                    X_training,
                    y_training,
                    w_training,
                    validation_nodes_levels,
                    validation_nodes_indexes,
                    model,
                    preprocessing_stage,
                    total_sum_orig_weights,
                    fold_model_params,
                    sparse_threshold=sparse_threshold,
                )
            )

            # generate all possible model params combinations
            params_values_combinations = self._get_model_params_combination(param_grids)

            async_tasks, executor = get_parallel_executor(n_jobs)

            cancel_event = Event()
            try:
                for model_params in params_values_combinations:

                    model_params.update(fold_model_params)
                    # copy w_training
                    w_training_copy = w_training_pre.copy() if w_training_pre is not None else None
                    fold_args = dict(
                        tree_idx=tree_idx,
                        X_training_pre=X_training_pre,
                        X_validate_pre=X_validate_pre,
                        model=model,
                        model_fit_params=model_fit_params,
                        model_params=model_params,
                        preprocessing_info=preprocessing_info,
                        preprocessing_stage=preprocessing_stage,
                        scores=scores,
                        scoring=scoring,
                        verbose=verbose,
                        sparse_threshold=sparse_threshold,
                        w_training_copy=w_training_copy,
                        y_training_pre=y_training_pre,
                        y_validate_pre=y_validate_pre,
                        parallel=executor is not None,
                        cancel_event=cancel_event,
                    )

                    if executor is not None:
                        async_tasks.append(executor.submit(self._holdout_worker, **fold_args))
                    else:
                        self._holdout_worker(**fold_args)

                if executor is not None:
                    self._wait_to_finish_tasks(async_tasks, executor)

            except Exception:
                raise
            finally:
                if executor is not None:
                    executor.shutdown(wait=False)

            # Find the best average score and its corresponding model_params
            best_model_params_key = max(scores, key=lambda k: scores.get(k))
            best_score = scores[best_model_params_key]
            best_parameters = dict(best_model_params_key)
            best_params_per_tree[tree_idx] = {"model_params": best_parameters, "score": best_score}
            scores["sample_params"] = self._data_tuning_params_cls._filter(self.trees[tree_idx].sample_params)
            scores_per_tree[tree_idx] = scores

        best_tree_idx = max(best_params_per_tree, key=lambda k: best_params_per_tree[k]["score"])
        best_parameters = best_params_per_tree[best_tree_idx]["model_params"]
        add_telemetry_attribute("Best score for grid search", str(best_score))
        # Prepare df of scores
        all_scores = _scores_to_df(scores_per_tree)

        if refit:
            # NOTE: validation_level is computed also in _holdout_validate, so in principle it is possible to
            # avoid the following call, but the code may become less clear
            if level is None:
                level = (
                    self._find_optimal_level_for_holdout_validation(best_tree_idx, validation_size)
                    if seq_params is None
                    else 0
                )
            if self._DH_DEBUG_MODE:
                print('Running refit, validation level is ', level)
            trained_model = self._fit(
                tree_idx=tree_idx,
                model=model,
                model_fit_params=model_fit_params,
                model_params=best_parameters,
                level=level,
                coreset_params=self.coreset_params["training"],
                preprocessing_stage=preprocessing_stage,
                sparse_threshold=sparse_threshold,
                seq_from=seq_train_from,
                seq_to=seq_validate_to,
            )

        if verbose >= 1:
            print(
                f"grid_search completed in {'{0:.3f}'.format(time.time() - ss)}. The best hyperparameter "
                f"combination is {best_parameters}. The best tree is {tree_idx} with the following data tuning parameters: {self._data_tuning_params_cls._filter(self.trees[tree_idx].sample_params)} "
                f"Average score across folds is {'{0:.4f}'.format(best_score)}."
            )
        if refit:
            return best_parameters, best_tree_idx, all_scores, trained_model
        else:
            return best_parameters, best_tree_idx, all_scores

    def _wait_to_finish_tasks(self, async_tasks, executor):
        # wait for the submitted tasks to complete
        wait(async_tasks, return_when=futures.FIRST_EXCEPTION)

        # filter only failed tasks
        failed_executions = [f for f in async_tasks if f.exception() is not None]
        if failed_executions:
            # accessing the result of a future with exception will raise the exception
            failed_executions[0].result()

    def _holdout_worker(
            self,
            tree_idx: int,
            X_training_pre,
            X_validate_pre,
            model,
            model_fit_params,
            model_params,
            preprocessing_info,
            preprocessing_stage,
            sparse_threshold,
            scores,
            scoring,
            verbose,
            w_training_copy,
            y_training_pre,
            y_validate_pre,
            parallel=False,
            cancel_event=None,
    ):

        # in case the cancel event was called we skip the task execution
        if cancel_event is not None and cancel_event.is_set():
            return

        validation_params = dict(
            tree_idx=tree_idx,
            X_training=X_training_pre,
            y_training=y_training_pre,
            w_training=w_training_copy,
            X_validate=X_validate_pre,
            y_validate=y_validate_pre,
            model=copy.deepcopy(model),
            model_fit_params=model_fit_params,
            scoring=scoring,
            verbose=verbose,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            preprocessing_info=preprocessing_info,
            **model_params,
        )

        if parallel:
            with threadpool_limits(limits=1, user_api='blas'):
                try:
                    self._adjust_model_parallelism(model, validation_params)
                    score, _ = self._holdout_validate_fit_predict(**validation_params)
                except Exception:
                    if cancel_event is not None:
                        cancel_event.set()
                    raise
        else:
            score, _ = self._holdout_validate_fit_predict(**validation_params)
        model_params_key = frozenset([item for item in model_params.items() if not isinstance(item[1],
                                                                                              list)])
        scores[model_params_key] = score

    def _find_optimal_level(self, tree_idx: int) -> int:
        """
        Finds the optimal level for performing grid search.

        Parameters
        ----------
        -
        Returns
        -------
        Optimal level (int)

        """
        _, levels, *_ = self._get_all_nodes_at_optimal_generalised_level_internal(tree_idx)
        optimal_level = min(levels)
        return optimal_level

    @telemetry
    def holdout_validate(
            self,
            tree_idx: int = 0,
            level: int = None,
            validation_size: float = 0.2,
            model: Any = None,
            model_fit_params: Dict = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            return_model: bool = False,
            verbose: int = 0,
            preprocessing_stage: Union[str, None] = "auto",
            sparse_threshold: float = 0.01,
            **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        A method for hold-out validation on the coreset tree.
        The validation set is always the last part of the dataset.
        This function is only applicable in case the coreset tree was optimized_for `training`.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional.
                The level of the tree on which the training and validation will be performed.
                If None, the best level will be selected.
            validation_size: float, optional.
                The percentage of the dataset that will be used for validating the model.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                The model class needs to implement the usual scikit-learn interface.
                Default: instantiate the service model class using input model_params.
            model_fit_params: dict, optional.
                Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            return_model: bool, optional.
                If True, the trained model is also returned.
            verbose: int, optional.
                Controls the verbosity: the higher, the more messages.
                    >=1 : The number of hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                    >=2 : The score and time for each hyperparameter combination.
            preprocessing_stage: string, optional, default `auto`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            model_params: kwargs, optional.
                The hyper-parameters of the model. If not provided, the default values are used.

        Returns:
            The validation score. If return_model=True, the trained model is also returned.
        """
        check_feature_for_license("holdout_validate")
        self._requires_tree()
        self._print_model_warning(model)
        if self.trees[tree_idx].is_empty():
            raise RuntimeError("A Coreset tree is required for the `grid_search` function "
                               "and any of the validation methods.")

        if TreeOptimizedFor.training not in self.optimized_for:
            raise ValueError(
                "`holdout_validate` is only supported when the coreset service is `optimized_for` 'training'"
            )

        # Arguments and context checks. If not meet, raise an exception.
        self._checks_for_validation(
            level=level,
            validation_size=validation_size,
            scoring=scoring,
            return_model=return_model,
            verbose=verbose)
        return self._holdout_validate(
            tree_idx=tree_idx,
            level=level,
            validation_size=validation_size,
            model=model,
            model_fit_params=model_fit_params,
            scoring=scoring,
            verbose=verbose,
            return_model=return_model,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            **model_params,
        )

    @telemetry
    def seq_dependent_validate(
            self,
            tree_idx: int = 0,
            level: int = None,
            seq_train_from: Any = None,
            seq_train_to: Any = None,
            seq_validate_from: Any = None,
            seq_validate_to: Any = None,
            model: Any = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            return_model: bool = False,
            verbose: int = 0,
            preprocessing_stage: Union[str, None] = "auto",
            sparse_threshold: float = 0.01,
            model_fit_params: Dict = None,
            **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        The method allows to train and validate on a subset of the Coreset tree, according to the `seq_column` defined
        in the `DataParams` structure passed to the init.
        This function is only applicable in case the coreset tree was optimized_for `training`.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional.
                The level of the tree from which the search for the best matching nodes starts. Nodes closer to the
                leaf level than the specified level, may be selected to better match the provided seq parameters.If
                None, the search starts from level 0, the head of the tree.
                If None, the best level will be selected.
            seq_train_from: Any, optional.
                The starting sequence of the training set.
            seq_train_to: Any, optional.
                The ending sequence of the training set.
            seq_validate_from: Any, optional.
                The starting sequence number of the validation set.
            seq_validate_to: Any, optional.
                The ending sequence number of the validation set.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                The model class needs to implement the usual scikit-learn interface.
                Default: instantiate the service model class using input model_params.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            return_model: bool, optional.
                If True, the trained model is also returned.
            verbose: int, optional.
                Controls the verbosity: the higher, the more messages.
                    >=1 : The number of hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                    >=2 : The score and time for each hyperparameter combination.
            preprocessing_stage: string, optional, default `auto`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            model_fit_params: dict, optional.
                Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
            model_params: kwargs, optional.
                The hyper-parameters of the model. If not provided, the default values are used.

        Returns:
            The validation score. If return_model=True, the trained model is also returned.
        """
        check_feature_for_license("seq_dependent_validate")
        self._requires_tree()
        self._print_model_warning(model)

        if self.trees[tree_idx].is_empty():
            raise RuntimeError("A Coreset tree is required for the `grid_search` function "
                               "and any of the validation methods.")

        if TreeOptimizedFor.training not in self.optimized_for:
            raise ValueError(
                "`seq_dependent_validate` is only supported when the coreset service is `optimized_for` 'training'"
            )

        datetime_format = self.data_manager.data_params_internal.seq_datetime_format
        seq_params = _compose_seq_params(seq_train_from, seq_train_to, seq_validate_from, seq_validate_to,
                                         datetime_format, strict=True)

        # Arguments and context checks. If not meet, raise an exception.
        self._checks_for_validation(
            level=level,
            validation_size=0.2,
            scoring=scoring,
            return_model=return_model,
            verbose=verbose)
        return self._holdout_validate(
            tree_idx=tree_idx,
            level=level,
            seq_params=seq_params,
            model=model,
            model_fit_params=model_fit_params,
            scoring=scoring,
            verbose=verbose,
            return_model=return_model,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            **model_params,
        )

    @telemetry
    def cross_validate(
            self,
            tree_idx: int = 0,
            level: Optional[int] = None,
            model: Any = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            return_model: bool = False,
            verbose: int = 0,
            preprocessing_stage: Union[str, None] = "auto",
            sparse_threshold: float = 0.01,
            model_fit_params: Dict = None,
            **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        Method for cross-validation on the coreset tree.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional.
                The level of the tree on which the training and validation will be performed.
                If None, the best level will be selected.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                The model class needs to implement the usual scikit-learn interface.
                Default: instantiate the service model class using input model_params.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            return_model: bool, optional.
                If True, the trained model is also returned.
            verbose: int, optional.
                Controls the verbosity: the higher, the more messages.
                    >=1 : The number of folds and hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                    >=2 : the score is also displayed;
            preprocessing_stage: string, optional, default `auto`.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            model_fit_params: dict, optional.
                Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
            model_params: kwargs, optional.
                The hyper-parameters of the model. If not provided, the default values are used.

        Returns:
            A list of scores, one for each fold. If return_model=True, a list of trained models is also returned (one model for each fold).
        """
        check_feature_for_license("cross_validate")
        self._requires_tree()
        self._print_model_warning(model)

        if self.trees[tree_idx].is_empty():
            raise RuntimeError("A Coreset tree is required for the `grid_search` function "
                               "and any of the validation methods.")

        if TreeOptimizedFor.training not in self.optimized_for:
            raise ValueError(
                "`cross_validate` is only supported when the coreset service is `optimized_for` 'training'"
            )

        # Arguments and context checks. If not meet, raise an exception.
        self._checks_for_validation(level=level, scoring=scoring, return_model=return_model,
                                    verbose=verbose)
        return self._cross_validate(
            tree_idx=tree_idx,
            level=level,
            model=model,
            scoring=scoring,
            return_model=return_model,
            verbose=verbose,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            model_fit_params=model_fit_params,
            **model_params,
        )

    def _cross_validate(
            self,
            tree_idx: int,
            level: Optional[int] = None,
            model: Any = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            return_model: bool = False,
            verbose: int = 0,
            preprocessing_stage: Union[str, None] = None,
            sparse_threshold: float = 0.01,
            model_fit_params: Dict = None,
            **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        Protected (internal) method for cross-validation on the coreset tree.

        Parameters
        ----------
        level: int, optional
            The level of the tree on which the training and validation will be performed.
            If None, the best level will be selected.
        model: model: A Scikit-learn compatible model instance, optional.
            When provided, model_params are not relevant.
            Default: instantiate the service model class using input model_params.
        scoring: callable or string, optional
            If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
            where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
            For example, it can be produced using sklearn.metrics.make_scorer
            (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
            If it is a string, it must be a valid name of a Scikit-learn scoring method
            (see https://scikit-learn.org/stable/modules/model_evaluation.html)
            If None, the default scorer of the current model is used.
        return_model: bool, optional
            If True, the trained model is also returned.
        verbose: int, optional
            Controls the verbosity: the higher, the more messages.
                >=1 : The number of folds and hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                >=2 : The score and time for each fold and hyperparameter combination.
        preprocessing_stage: string, optional, default `user` when LightGBM or CatBoost are used, `auto` when Scikit-learn or XGBoost is used<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
        sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
            if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
            (Applicable only for preprocessing_stage='auto').
        model_fit_params: dict, optional
            Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
        model_params: kwargs, optional
            The hyper-parameters of the model. If not provided, the default values are used.

        Returns
        -------
            A list of scores, one for each fold.
            If return_model=True, a list of trained models is also returned (one model for each fold).
        """
        if verbose >= 1:
            if model_params:
                print(f'Start cross-validation with parameters: {model_params}.')
            else:
                print('Start cross-validation with default parameters.')
        folds = self._get_folds_structure(tree_idx=tree_idx, level=level)
        coreset_validation_data = self._coreset_data_and_folds_limits(tree_idx=tree_idx, folds_nodes=folds["nodes"])
        # Compute the metrics for each fold
        return self._train_and_validate_fold_by_fold(
            tree_idx=tree_idx,
            folds=folds,
            coreset_validation_data=coreset_validation_data,
            model=model,
            scoring=scoring,
            return_model=return_model,
            verbose=verbose,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            model_fit_params=model_fit_params,
            **model_params,
        )

    def _prepare_data_holdout_validate(
            self,
            tree_idx: int,
            level: int = None,
            seq_params: Dict[str, list] = None,
            validation_size: Union[float, None] = 0.2,
    ) -> Tuple[Union[int, Dict[Any, Any]], Any, Any, Any, Any, Any]:

        if seq_params is None:
            if level is None:
                level = self._find_optimal_level_for_holdout_validation(tree_idx, validation_size)

            nodes_data = self.trees[tree_idx].get_all_nodes_at_some_generalised_level(level)
            buffer = nodes_data[-1]
            # Order the nodes by level and index- this is important to assure the right time order for the data
            sorted_nodes, sorted_levels, sorted_indices = self._order_nodes(nodes_data)

            min_level = sorted_levels[0]
            n_regular_nodes = sorted_levels.count(min_level)
            n_validation_nodes = int(n_regular_nodes * validation_size)
            if n_validation_nodes == 0:
                n_validation_nodes = 1
            n_training_nodes = n_regular_nodes - n_validation_nodes
            if n_training_nodes < 1:
                raise ValueError('''It appears that, at the selected level, the coreset tree does not have enough nodes to 
            do the validation. Please provide a smaller value for validation_size param, or check the tree structure and select a different 
            level or construct a bigger tree (e.g., by selecting a different chunk_size value).''')
            # Get the chunks data for validation

            training_nodes_levels_indexes = list(zip(sorted_levels[:n_training_nodes],
                                                     sorted_indices[:n_training_nodes]))

            validation_nodes_levels = sorted_levels[n_training_nodes:]
            validation_nodes_indexes = sorted_indices[n_training_nodes:]

            training_nodes = sorted_nodes[:n_training_nodes]
        else:
            validation_seq_params = seq_params['params'][2:]
            validation_seq_operators = seq_params['strict_operators'][2:]
            training_seq_params = seq_params['params'][:2]
            training_seq_operators = seq_params['strict_operators'][:2]
            data_mix_threshold = float(DataHeroesConfiguration().get_param_str("data_mix_threshold") or
                                       DATA_MIX_THRESHOLD_DEFAULT)

            tree = self.trees[tree_idx]
            if level is None:
                nodes = tree._get_tree_heads(with_buffer=False)
            else:
                nodes, _, _, _ = tree.get_all_nodes_at_some_generalised_level(level)
            buffer = tree.buffer_node

            training_nodes = tree.compute_seq_nodes(
                nodes, training_seq_params, training_seq_operators, data_mix_threshold, purpose="holdout validation"
            )
            training_nodes_levels_indexes = [
                tree._where_is_node(node.node_id, root_zero=True) for node in training_nodes
            ]
            validation_nodes = tree.compute_seq_nodes(
                nodes, validation_seq_params, validation_seq_operators, data_mix_threshold, purpose="holdout validation"
            )
            validation_nodes_locations = [
                tree._where_is_node(node.node_id, root_zero=True) for node in validation_nodes
            ]
            validation_nodes_levels = [node[0] for node in validation_nodes_locations]
            validation_nodes_indexes = [node[1] for node in validation_nodes_locations]
            if len(training_nodes) == 0 or len(validation_nodes) == 0:
                raise ValueError(f'''It appears that, in the selected sequence, the coreset tree does not have enough training 
            or validation nodes. Please check the tree structure and use a different training or validation sequence.
            Number of training nodes found in given sequence: {len(training_nodes)}
            Number of validation nodes found in given sequence: {len(validation_nodes)}''')

        if buffer is not None:
            validation_nodes_levels.append(-1)
            validation_nodes_indexes.append(0)

        # Get the coreset, for training
        if not hasattr(self, "fit_params"):
            self.fit_params = {}
        self.fit_params["training_nodes_levels_indexes"] = training_nodes_levels_indexes
        X_training, y_training, w_training = self._get_training_data_for_holdout_validate(tree_idx, training_nodes)
        # Adjust weights based on class weights and n_represents
        total_n_represents = self._compute_total_n_represents(training_nodes)
        total_sum_orig_weights = self._compute_total_sum_orig_weights(training_nodes)

        return total_n_represents, total_sum_orig_weights, X_training, y_training, w_training, validation_nodes_levels, validation_nodes_indexes

    def _holdout_validate_fit_predict(
            self,
            tree_idx: int,
            w_training: np.ndarray,
            X_training: np.ndarray,
            y_training: np.ndarray,
            X_validate: np.ndarray,
            y_validate: np.ndarray,
            verbose: int = 0,
            model: Any = None,
            model_fit_params: Dict = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            preprocessing_stage: Union[str, None] = None,
            sparse_threshold: float = 0.01,
            preprocessing_info: Dict = None,
            **model_params,
    ) -> Tuple[Any, Any]:

        start = time.time()

        trained_model = self._fit_internal(
            X=X_training,
            y=y_training,
            weights=w_training,
            model=model,
            model_fit_params=model_fit_params,
            params={"preprocessing_stage": preprocessing_stage},
            preprocessing_info=preprocessing_info,
            sparse_threshold=sparse_threshold,
            **model_params,
        )

        validation_score = CoresetTreeService._compute_score(
            scoring, trained_model, X_validate, y_validate)

        end = time.time()
        validation_time = end - start
        if verbose >= 2:
            print(
                f"Tree {tree_idx}; Data Tuning Params: {self._data_tuning_params_cls._filter(self.trees[tree_idx].sample_params)}; "
                f"Hyperparameters: {model_params}; Score: {'{0:.4f}'.format(validation_score)}; "
                f"Time: {'{0:.3f}'.format(validation_time)} (s)."
            )
        add_telemetry_attribute("Training coreset sizes was", str(len(X_training)))
        add_telemetry_attribute("Validation dataset sizes was", str(len(X_validate)))

        return validation_score, trained_model

    def _holdout_validate(
            self,
            tree_idx: int,
            level: int = None,
            seq_params: Dict[str, list] = None,
            validation_size: float = 0.2,
            model: Any = None,
            model_fit_params: Dict = None,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            return_model: bool = False,
            verbose: int = 0,
            preprocessing_stage: Union[str, None] = None,
            sparse_threshold: float = 0.01,
            **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        Protected (internal) method for hold-out validation on the coreset tree.

        Parameters
        ----------
        tree_idx: int, default = 0
            Defines the index of the tree from which the coreset is extracted.
            The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
        level: int, optional
            The level of the tree on which the training and validation will be performed.
            If None, the best level will be selected.
        validation_size: float, optional
            The percentage of the dataset that will be used for validating the model.
        model: model: A Scikit-learn compatible model instance, optional.
            When provided, model_params are not relevant.
            Default: instantiate the service model class using input model_params.
        model_fit_params: dict, optional
            Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
        scoring: callable or string, optional
            If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
            where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
            For example, it can be produced using sklearn.metrics.make_scorer
            (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
            If it is a string, it must be a valid name of a Scikit-learn scoring method
            (see https://scikit-learn.org/stable/modules/model_evaluation.html)
            If None, the default scorer of the current model is used.
        return_model: bool, optional
            If True, the trained model is also returned.
        verbose: int, optional
            Controls the verbosity: the higher, the more messages.
                >=1 : The number hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                >=2 : The score and time for each hyperparameter combination.
        preprocessing_stage: string, optional, default `user` when LightGBM or CatBoost are used, `auto` when Scikit-learn or XGBoost are used<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
        sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
            if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
            (Applicable only for preprocessing_stage='auto').
        model_params: kwargs, optional
            The hyper-parameters of the model. If not provided, the default values are used.

        Returns
        -------
            The validation score.
            If return_model=True, the trained model is also returned.
        """

        (
            total_n_represents,
            total_sum_orig_weights,
            X_training,
            y_training,
            w_training,
            validation_nodes_levels,
            validation_nodes_indexes,
        ) = self._prepare_data_holdout_validate(
            level=level, tree_idx=tree_idx, seq_params=seq_params, validation_size=validation_size
        )

        fold_model_params = {}
        _, X_training_pre, y_training_pre, w_training_pre, _, X_validate_pre, y_validate_pre, preprocessing_info = (
            self._prepare_fold_data(
                tree_idx,
                X_training,
                y_training,
                w_training,
                validation_nodes_levels,
                validation_nodes_indexes,
                model,
                preprocessing_stage,
                total_sum_orig_weights,
                fold_model_params,
                sparse_threshold=sparse_threshold,
            )
        )

        model_params.update(fold_model_params)

        validation_score, trained_model = self._holdout_validate_fit_predict(
            tree_idx=tree_idx,
            X_training=X_training_pre,
            y_training=y_training_pre,
            w_training=w_training_pre,
            X_validate=X_validate_pre,
            y_validate=y_validate_pre,
            verbose=verbose,
            model=model,
            model_fit_params=model_fit_params,
            scoring=scoring,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            preprocessing_info=preprocessing_info,
            **model_params,
        )

        if return_model:
            return validation_score, trained_model
        else:
            return validation_score

    @staticmethod
    def _compute_total_n_represents(items, already_list=False, use_build_weights=False):
        """
        Computes the total number of instances represented by a list of nodes.
        If the class is available, the computation is per class.

        Parameters
        ----------
        items: list of nodes or list of n_represents

        Returns
        -------
        total_n_represents - this is a dict for classification tasks (when node.n_represents is a dict),
                             and an int otherwise
        """
        if len(items) == 0:
            return 0
        if use_build_weights:
            represents_list = [node.sum_orig_weights for node in items] if not already_list else items
        else:
            represents_list = [node.n_represents for node in items] if not already_list else items
        if isinstance(represents_list[0], dict):
            total_represents = {}
            for node_represents in represents_list:
                for key in node_represents:
                    if key in total_represents:
                        total_represents[key] += node_represents[key]
                    else:
                        total_represents[key] = node_represents[key]
        else:
            total_represents = sum(represents_list)
        return total_represents

    # TODO Daci: Unnecessary method? Same as _compute_total_n_represents
    @staticmethod
    def _compute_total_sum_orig_weights(items, already_list=False):
        return CoresetTreeService._compute_total_n_represents(items, already_list, use_build_weights=True)

    def _weights_adjustment(self, model, model_params, total_sum_orig_weights, w_training, y_training,
                            inverse_class_weight=None):
        """
        Does the weights adjustment based on the number of instances represented by the coreset and the class weight

        Parameters
        ----------
        model: the ML model
        model_params: dict
            Model parameters
        total_sum_orig_weights: dict or int
            The total sum of weights of all instances represented by the coreset (if dict, the key is the class,
            and the value the sum of weights of instances from that class)
        w_training: np.array
            The coreset weights
        y_training: np.array
            The labels
        Returns
        -------
        w_training (np.array) - the transformed weights
        """

        if inverse_class_weight is None:
            inverse_class_weight = False
            if self.is_classification:
                # If the user passed a model with pre-existing class weights, set inverse_class_weight = True.
                if model is not None and getattr(model, "class_weight", None) is not None:
                    inverse_class_weight = True
                # If the user passed in class_weight in the fit function: fit(class_weight = ...) set inverse_class_weight = True
                elif model_params is not None and model_params.get("class_weight", None) is not None:
                    inverse_class_weight = True
        w_training = weight_processing(
            w=w_training,
            sum_orig_weights=total_sum_orig_weights,
            y=y_training,
            class_weight=self.coreset_params.get("class_weight", None),
            is_classification=self.is_classification,
            inverse_class_weight=inverse_class_weight,
        )
        return w_training

    def _get_chunks_data_for_holdout_validate(
            self, tree_idx: int, validation_nodes_levels, validation_nodes_indexes, features_out=None
    ):
        """
        Method for getting the chunks data for hold-out validation.

        Parameters
        ----------
        validation_nodes_levels: list
            A list with validation nodes' levels.
        validation_nodes_indexes: list
            A list with validation nodes' indexes.
        -------
            Two np arrays: X_validate (the features), y_validate (the labels)
        """
        X_validate = np.array([])
        y_validate = np.array([])
        tree = self.trees[tree_idx]
        random_sample_percentage = tree.get_random_sample_percentage(
            features_out, validation_nodes_levels, validation_nodes_indexes
        )

        for level, index in zip(validation_nodes_levels, validation_nodes_indexes):
            chunks_dataset = tree.get_chunk_data_for_nodes(level, index, features_out, random_sample_percentage)
            X_node_chunks = chunks_dataset.X
            y_node_chunks = chunks_dataset.y
            if X_validate.size == 0:
                X_validate = X_node_chunks
            else:
                X_validate = np.concatenate((X_validate, X_node_chunks), axis=0)
            if y_validate.size == 0:
                y_validate = y_node_chunks
            else:
                y_validate = np.concatenate((y_validate, y_node_chunks), axis=0)
        return X_validate, y_validate

    def _get_training_data_for_holdout_validate(self, tree_idx: int, training_nodes: List[Node]):
        """
        Method for getting the coreset for hold-out validation.

        Parameters
        ----------
        training_nodes: list
            A list containing the nodes used for training.
        -------
            Three np arrays: X_training (the features), y_training (the labels), w_training (the weights)
        """
        X_training = np.array([])
        y_training = np.array([])
        w_training = np.array([])
        for node_i in training_nodes:
            coreset_data_node, w_coreset_data_node = self.trees[tree_idx].get_by_index(node_i.indexes, node_i.weights)
            X_node_coreset = coreset_data_node.X
            y_node_coreset = coreset_data_node.y
            if X_training.size == 0:
                X_training = X_node_coreset
            else:
                X_training = np.concatenate((X_training, X_node_coreset), axis=0)
            if y_training.size == 0:
                y_training = y_node_coreset
            else:
                y_training = np.concatenate((y_training, y_node_coreset), axis=0)
            if w_training.size == 0:
                w_training = w_coreset_data_node
            else:
                w_training = np.concatenate((w_training, w_coreset_data_node), axis=0)
        return X_training, y_training, w_training

    @staticmethod
    def _order_nodes(nodes_data):
        """
        Method for sorting nodes by level and index, in ascending order.

        Parameters
        ----------
        nodes_data: list
            A list containing tree other lists: one with node objects, one with the levels
            and the last one with indices.
        -------
            Three sorted lists: with node objects, levels and indices.
        """
        sorted_nodes = sorted(zip(nodes_data[0], nodes_data[1], nodes_data[2]), key=lambda node: (node[1], node[2]))
        nodes_values = [node[0] for node in sorted_nodes]
        nodes_levels = [node[1] for node in sorted_nodes]
        nodes_indexes = [node[2] for node in sorted_nodes]
        return nodes_values, nodes_levels, nodes_indexes

    @staticmethod
    def _compute_score(scoring, trained_model, X_validate, y_validate):
        """
        Method for computing the validation score.

        Parameters
        ----------
        scoring: str, callable or None
            The scoring method.
        trained_model: a ML model
            The trained ML model.
        X_validate: np array
            The validation data (features)
        y_validate: np array
            The validation labels
        Returns
        -------
            The score (float).
        """
        if scoring is None:
            # Use the default scorer
            validation_score = trained_model.score(X_validate, y_validate)
        elif isinstance(scoring, str):
            # Get the scoring function indicated by "scoring"
            scoring_callable = get_scorer(scoring)
            validation_score = scoring_callable(trained_model, X_validate, y_validate)
        else:
            # Use the provided callable scorer
            validation_score = scoring(trained_model, X_validate, y_validate)
        return validation_score

    def _find_optimal_level_for_holdout_validation(self, tree_idx: int, validation_size: float):
        """
        Method for finding a level on which we can have a validation
        dataset of the right size.

        Parameters
        ----------
        validation_size: float
            The relative size of the test/validation set.
        Returns
        -------
            The optimal level (int).
        """
        tree = self.trees[tree_idx]
        depth = len(tree.tree)
        best_level = 0
        best_error = float('inf')
        for level in range(depth):
            _, levels, _, _ = tree.get_all_nodes_at_some_generalised_level(level)
            min_level = min(levels)
            n_regular_nodes = levels.count(min_level)
            n_validation_nodes = int(n_regular_nodes * validation_size)
            if n_validation_nodes == 0:
                n_validation_nodes = 1
            cr_error = abs(n_validation_nodes / float(n_regular_nodes) - validation_size)
            # The current error is small enough, we can stop here
            if cr_error <= 0.01:
                return level
            elif cr_error < best_error:
                best_error = cr_error
                best_level = level
        return best_level

    def _get_folds_structure(self, tree_idx: int, level: Optional[int]) -> Dict[str, list]:
        """
        Method for splitting the nodes into folds.

        Parameters
        ----------
        tree_idx: int
            The index of the tree on which the node splitting is performed.

        level: Optional[int]
            The level of the tree on which the node splitting is performed.
            If None, the best level will be selected.

        Returns
        -------
            A dictionary containing the nodes, nodes' levels and nodes' indexes
        """
        if level is not None:
            # At the specified level, get all nodes (including the relevant orphans) + the buffer
            levels, indexes, nodes, buffer_node = self.trees[tree_idx]._get_level_nodes(
                level, include_orphans_heads=True, return_buffer=True
            )
            # Get the preliminary number of folds. Depending on the available data in the orphans,
            # the final number of folds may increase by 1
            n_folds_preliminary = self._get_preliminary_number_of_folds(levels)
        else:
            # If the level is not provided, get a good one
            nodes, levels, indexes, buffer_node, n_folds_preliminary = (
                self._get_all_nodes_at_optimal_generalised_level_internal(tree_idx)
            )
        # Split the nodes into folds
        folds_nodes, folds_levels, folds_indexes = self._split_into_folds(
            nodes,
            levels,
            indexes,
            buffer_node,
            n_folds_preliminary)
        if len(folds_nodes) < 2:
            raise ValueError('''It appears that, at the selected level, the coreset tree does not have enough nodes. 
    Please check the tree structure, and select a different level or construct a bigger tree (e.g., by selecting a 
    different chunk_size value).''')
        folds = {'nodes': folds_nodes, 'levels': folds_levels, 'indexes': folds_indexes}
        return folds

    def _prepare_folds(
            self,
            tree_idx: int,
            folds: dict,
            coreset_validation_data: dict,
    ):
        """
        Method for preparing the folds data.

        Parameters
        ----------
        folds: dict
            A dictionary containing the nodes, nodes' levels and nodes' indexes.
        coreset_validation_data: dict
            A dictionary containing the coreset data (X, y, w) and folds limits.
        Returns
        -------
            A list of scores, one for each fold.
            If return_model=True, a list of trained models is also returned (one model for each fold).
        """
        tree = self.trees[tree_idx]
        n_folds = len(folds['nodes'])
        for validation_fold_index in range(n_folds):
            # Split into training and validation nodes
            # Note that only for validation we need the levels and indexes (to get the data chunks)
            validation_folds_nodes = folds['nodes'][validation_fold_index]
            validation_folds_levels = folds['levels'][validation_fold_index]
            validation_folds_indexes = folds['indexes'][validation_fold_index]
            # Get the coreset data from all training nodes
            training_folds_lower_limit = coreset_validation_data['folds_limits'][validation_fold_index]
            training_folds_upper_limit = coreset_validation_data['folds_limits'][validation_fold_index + 1]
            X_training_1 = coreset_validation_data['X'][:training_folds_lower_limit]
            X_training_2 = coreset_validation_data['X'][training_folds_upper_limit:]
            X_training = pd.concat((X_training_1, X_training_2), axis=0) if isinstance(X_training_1, pd.DataFrame) \
                else np.concatenate((X_training_1, X_training_2), axis=0)
            y_training_1 = coreset_validation_data['y'][:training_folds_lower_limit]
            y_training_2 = coreset_validation_data['y'][training_folds_upper_limit:]
            y_training = np.concatenate((y_training_1, y_training_2), axis=0)
            w_training_1 = coreset_validation_data['w'][:training_folds_lower_limit]
            w_training_2 = coreset_validation_data['w'][training_folds_upper_limit:]
            w_training = np.concatenate((w_training_1, w_training_2), axis=0)
            ind_training_1 = coreset_validation_data['ind'][:training_folds_lower_limit]
            ind_training_2 = coreset_validation_data['ind'][training_folds_upper_limit:]
            ind_training = np.concatenate((ind_training_1, ind_training_2), axis=0)
            # Get the data from chunks for all validation nodes
            X_validate_list = []
            y_validate_list = []
            idx_validate_list = []
            random_sample_percentage = self.trees[tree_idx].get_random_sample_percentage(
                X_training.shape[1], validation_folds_levels, validation_folds_indexes
            )
            for _, level, index in zip(validation_folds_nodes, validation_folds_levels, validation_folds_indexes):
                chunks_dataset = tree.get_chunk_data_for_nodes(
                    level, index, n_features_out=X_training.shape[1], random_sample_percentage=random_sample_percentage
                )
                X_node_chunks = chunks_dataset.X
                y_node_chunks = chunks_dataset.y
                # For unsupervised methods, use dummy values for y
                if y_node_chunks is None:
                    y_node_chunks = np.zeros(len(X_node_chunks))

                X_validate_list.append(X_node_chunks)
                y_validate_list.append(y_node_chunks)
                idx_validate_list.append(chunks_dataset.ind)
            X_validate = np.concatenate(X_validate_list, axis=0)
            y_validate = np.concatenate(y_validate_list, axis=0)
            ind_validate = np.concatenate(idx_validate_list, axis=0)
            if X_validate.size == 0:
                continue
            training_folds_nodes = folds['nodes'][:validation_fold_index] + folds['nodes'][validation_fold_index + 1:]
            training_nodes = []
            for fold_nodes in training_folds_nodes:
                training_nodes.extend(fold_nodes)
            total_n_represents = self._compute_total_n_represents(training_nodes)
            total_sum_orig_weights = self._compute_total_sum_orig_weights(training_nodes)
            training_folds_levels = folds['levels'][:validation_fold_index] + folds['levels'][
                                                                              validation_fold_index + 1:]
            training_folds_levels = sum(training_folds_levels, start=[])  # list of list -> list
            training_folds_indexes = folds['indexes'][:validation_fold_index] + folds['indexes'][
                                                                                validation_fold_index + 1:]
            training_folds_indexes = sum(training_folds_indexes, start=[])  # list of list -> list
            if not hasattr(self, "fit_params"):
                self.fit_params = {}
            self.fit_params["training_nodes_levels_indexes"] = list(
                zip(training_folds_levels, training_folds_indexes)
            )
            yield ind_training, X_training, y_training, w_training, ind_validate, X_validate, y_validate, level, total_n_represents, total_sum_orig_weights

    def _train_and_validate_fold(
            self,
            X_training,
            y_training,
            w_training,
            X_validate,
            y_validate,
            level,
            model,
            model_fit_params,
            preprocessing_stage,
            preprocessing_info,
            sparse_threshold,
            scoring,
            **model_params
    ):
        trained_model = self._fit_internal(
            X=X_training,
            y=y_training, weights=w_training,
            model=model,
            params={'level': level, 'preprocessing_stage': preprocessing_stage},
            preprocessing_info=preprocessing_info,
            sparse_threshold=sparse_threshold,
            model_fit_params=model_fit_params,
            **model_params
        )
        fold_score = CoresetTreeService._compute_score(scoring, trained_model, X_validate, y_validate)
        return fold_score, trained_model

    def _train_and_validate_fold_by_fold(
            self,
            tree_idx: int,
            folds: dict,
            coreset_validation_data: dict,
            model: Any,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]],
            return_model: bool,
            verbose: int,
            preprocessing_stage: Union[str, None] = None,
            sparse_threshold: float = 0.01,
            model_fit_params: dict = None,
            **model_params,
    ):
        """
        Method for performing training and validation for each fold.

        Parameters
        ----------
        folds: dict
            A dictionary containing the nodes, nodes' levels and nodes' indexes.
        coreset_validation_data: dict
            A dictionary containing the coreset data (X, y, w) and folds limits.
        model: model: A Scikit-learn compatible model instance.
            When provided, model_params are not relevant.
            Default: instantiate the service model class using input model_params.
        scoring: callable or string
            If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
            where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
            For example, it can be produced using sklearn.metrics.make_scorer
            (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
            If it is a string, it must be a valid name of a Scikit-learn scoring method
            (see https://scikit-learn.org/stable/modules/model_evaluation.html)
            If None, the default scorer of the current model is used.
        return_model: bool
            If True, the trained model is also returned.
        verbose: int, optional
            Controls the verbosity: the higher, the more messages.
                >=1 : The number of folds and hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                >=2 : The score and time for each fold and hyperparameter combination.
        preprocessing_stage: string, optional, default `user` when LightGBM or CatBoost are used, `auto` when Scikit-learn or XGBoost are used<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
        sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
            if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
            (Applicable only for preprocessing_stage='auto').
        model_fit_params: dict, optional
            Parameters to pass to the model's fit method. The parameters should be passed as a dictionary.
        model_params: kwargs
            The hyper-parameters of the model. If not provided, the default values are used.
        Returns
        -------
            A list of scores, one for each fold.
            If return_model=True, a list of trained models is also returned (one model for each fold).
        """
        scores_for_each_fold = list()
        trained_models_for_each_fold = list()
        training_dataset_sizes = []
        validation_dataset_sizes = []
        n_folds = len(folds['nodes'])
        add_telemetry_attribute("No. of folds", str(n_folds))

        folds_data = self._prepare_folds(
            tree_idx=tree_idx, folds=folds, coreset_validation_data=coreset_validation_data
        )
        for validation_fold_index, (_, X_training, y_training, w_training, _, X_validate, y_validate, level,
                                    total_n_represents, total_sum_orig_weights) in enumerate(folds_data):
            start = time.time()
            start_time = datetime.now()

            fold_model_params = {}
            _, X_training_pre, y_training_pre, w_training_pre, _, X_validate_pre, y_validate_pre, preprocessing_info = (
                self._prepare_fold_data(
                    tree_idx,
                    X_training,
                    y_training,
                    w_training,
                    X_validate,
                    y_validate,
                    model,
                    preprocessing_stage,
                    total_sum_orig_weights,
                    fold_model_params,
                    sparse_threshold=sparse_threshold,
                )
            )

            model_params.update(fold_model_params)

            fold_score, trained_model = self._train_and_validate_fold(
                X_training=X_training_pre,
                y_training=y_training_pre,
                w_training=w_training_pre,
                X_validate=X_validate_pre,
                y_validate=y_validate_pre,
                level=level,
                model=copy.deepcopy(model),
                preprocessing_stage=preprocessing_stage,
                sparse_threshold=sparse_threshold,
                preprocessing_info=preprocessing_info,
                scoring=scoring,
                model_fit_params=model_fit_params,
                **model_params
            )
            scores_for_each_fold.append(fold_score)
            if return_model:
                trained_models_for_each_fold.append(trained_model)
            end = time.time()
            validation_time = end - start
            training_dataset_sizes.append(len(X_training))
            validation_dataset_sizes.append(len(X_validate))
            if verbose >= 1:
                print(
                    f'Training and validation time for the fold {validation_fold_index} was '
                    f'{"{0:.3f}".format(validation_time)} (s).')
            if verbose >= 2:
                print(f'The score for the fold {validation_fold_index} was {fold_score}.')
            if verbose >= 3:
                print("The computations for the current fold started at: %s:%s:%s." % (
                    start_time.hour, start_time.minute, start_time.second))
        add_telemetry_attribute("Training dataset sizes for each fold", str(training_dataset_sizes))
        add_telemetry_attribute("Validation dataset sizes for each fold", str(validation_dataset_sizes))
        if return_model:
            return scores_for_each_fold, trained_models_for_each_fold
        else:
            return scores_for_each_fold

    def _coreset_data_and_folds_limits(self, tree_idx: int, folds_nodes: List[List[Node]]) -> dict:
        """
        Method for getting the coreset data and the folds limits
        for splitting the coreset data into folds.

        Parameters
        ----------
        folds_nodes: list
            A list of lists of nodes. Each inner list corresponds to a fold.
        Returns
        -------
            A dictionary containing the coreset data (X, y, w) and folds limits.
        """
        # Get the coresets from all nodes
        coreset_validation_data = {}
        new_limit = 0
        coreset_validation_data['folds_limits'] = [new_limit]
        for fold in folds_nodes:
            for node in fold:
                # In the current implementation, passing also the weight will ensure a consistent
                # order for data and weights
                data, weights = self.trees[tree_idx].get_by_index(node.indexes, node.weights)
                y = data.y
                # For unsupervised methods, use dummy values for y
                if y is None:
                    y = np.zeros(len(data.X))
                # TODO Daci: Why don't we pass in the Dataset class if we have it
                if new_limit != 0:
                    coreset_validation_data["X"] = np.concatenate((coreset_validation_data["X"], data.X), axis=0)
                    coreset_validation_data["y"] = np.concatenate((coreset_validation_data["y"], y), axis=0)
                    coreset_validation_data["w"] = np.concatenate((coreset_validation_data["w"], weights), axis=0)
                    coreset_validation_data["ind"] = np.concatenate((coreset_validation_data["ind"], data.ind), axis=0)
                else:
                    coreset_validation_data["X"] = data.X
                    coreset_validation_data["y"] = y
                    coreset_validation_data["w"] = weights
                    coreset_validation_data["ind"] = data.ind
                new_limit = new_limit + len(data.X)
            coreset_validation_data['folds_limits'].append(new_limit)
        coreset_validation_data['X'] = pd.DataFrame(coreset_validation_data['X'])
        return coreset_validation_data

    def _checks_for_validation(
            self,
            level: Optional[int] = 0,
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
            return_model: bool = False,
            validation_size: float = 0.2,
            verbose: int = 0):
        """
        Arguments and context checks for validation. If not meet, raise an exception.
        """
        if not self.is_supervised:
            raise AttributeError(
                'The validation method can be used only with a CoresetTree for a supervised learning algorithm.')
        if self.chunk_sample_ratio <= 0.0:
            raise AttributeError(
                '''The validation method can be used only if a random sample is saved. To do validation, please set `chunk_sample_ratio` to a value greater than 0.0 when creating the CoresetTreeService object.''')
        if level is not None:
            if not isinstance(level, int):
                raise TypeError('The `level argument must be a positive integer or None.')
            elif level < 0:
                raise ValueError('The `level` argument must be a positive integer or None.')

        if scoring is not None:
            if not isinstance(scoring, Callable) and not isinstance(scoring, str):
                raise TypeError(''' The `scoring` argument must be a string, a callable or None. 
                                        If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y), 
                                        where estimator is the model to be evaluated, X is the data and y is the ground truth labeling.
                                        For example, it can be produced using sklearn.metrics.make_scorer 
                                        (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                                        If it is a string, it must be a valid name of a Scikit-learn scoring method 
                                        (see https://scikit-learn.org/stable/modules/model_evaluation.html)
                                        If None, the default scorer of the current model is used.''')
        if not isinstance(return_model, bool):
            raise TypeError('The `return_model` argument must be a Boolean value.')

        if not isinstance(validation_size, (np.floating, float)):
            raise TypeError('The `validation_size` argument must be a float value.')
        if isinstance(validation_size, (np.floating, float)) and (validation_size <= 0.0 or validation_size >= 1.0):
            raise ValueError('The argument `validation_size` must have a value from the interval (0,1).')
        if not isinstance(verbose, int):
            raise TypeError('The `verbose` argument must be a positive integer value.')

    def _checks_for_grid_search(
            self,
            param_grid: Union[Dict[str, List], List[Dict[str, List]]],
            level: Optional[int],
            scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]],
            refit: bool,
            verbose: int,
            error_score: Union[str, float, int],
            validation_method: str,
            validation_size: float,
            seq_train_from: Any,
            seq_train_to: Any,
            seq_validate_from: Any,
            seq_validate_to: Any,
    ):
        """
        Arguments and context checks for grid search. If not meet, raise an exception.
        """
        if self.chunk_sample_ratio <= 0.0:
            raise AttributeError(
                '''The grid_search(...) method can be used only if at least a random sample is saved. To do grid search, please set `chunk_sample_ratio` to a value greater than 0.0 when creating the CoresetTreeService object.''')
        self._check_param_grid(param_grid)
        if level is not None:
            if not isinstance(level, int):
                raise TypeError('The `level` argument must be a positive integer or None.')
            elif level < 0:
                raise ValueError('The `level` argument must be a positive integer or None.')
        if scoring is not None:
            if not isinstance(scoring, Callable) and not isinstance(scoring, str):
                raise TypeError(''' The `scoring` argument must be a string, a callable or None. 
                                        If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y), 
                                        where estimator is the model to be evaluated, X is the data and y is the ground truth labeling.
                                        For example, it can be produced using sklearn.metrics.make_scorer 
                                        (https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                                        If it is a string, it must be a valid name of a Scikit-learn scoring method 
                                        (see https://scikit-learn.org/stable/modules/model_evaluation.html)
                                        If None, the default scorer of the current model is used.''')
        if not isinstance(refit, bool):
            raise TypeError('The `refit` argument must be a Boolean value.')
        if not isinstance(verbose, int):
            raise TypeError('The `verbose` argument must be a positive integer value.')
        if not (
                isinstance(error_score, (np.floating, float))
                or isinstance(error_score, int)
                or isinstance(
            error_score, str
        )  # TODO Daci: here shouldn't we equal to "raise" instead of string? What if we pass smth other than "raise"
                or error_score == np.nan
        ):
            raise TypeError('The `error_score` argument must be a float value, np.nan or "raise".')
        if not isinstance(validation_method, str):
            raise TypeError(
                'The `validation_method` argument must be a string, with the value "cross validation", "hold-out validation" or "seq-dependent validation"')
        if validation_method not in ['cross validation', 'hold-out validation', 'seq-dependent validation']:
            raise ValueError(
                'The `validation_method` argument must be a string, with the value "cross validation", "hold-out validation" or "seq-dependent validation"')
        if validation_method != 'seq-dependent validation' and any(
                [seq_train_from, seq_train_to, seq_validate_from, seq_validate_to]):
            raise ValueError("The 'seq_train_from', 'seq_train_to', 'seq_validate_from' and 'seq_validate_to'"
                             " arguments can only be used with holdout validation.")
        if validation_size != 0.2 and validation_method != 'hold-out validation':
            raise ValueError("The 'validation_size' argument can only be used with holdout validation.")

    @staticmethod
    def _check_param_grid(param_grid):
        """
        Check if grid_param has proper structure. If not, raise an exception.
        """
        if param_grid is None:
            raise ValueError('`param_grid`, a mandatory argument, was not provided.')
        general_type_ex_msg = '''The `param_grid` argument must be a dictionary or a list of dictionaries. 
    The keys of the dictionary are parameter names (str) and the values are lists of parameter settings to try. 
    If a list of such dictionaries is provided, the grids spanned by each dictionary in the list are explored. '''
        if not (isinstance(param_grid, dict) or isinstance(param_grid, list)):
            raise TypeError(general_type_ex_msg)
        if isinstance(param_grid, dict):
            param_grid_list = [param_grid]
        else:
            param_grid_list = param_grid
        for param_grid_i in param_grid_list:
            if not (isinstance(param_grid_i, dict)):
                raise TypeError(f'In the `param_grid` list, dicts are expected, but {param_grid_i} was found.')
            for param_name in param_grid_i:
                if not (isinstance(param_name, str)):
                    raise TypeError(
                        f"In `param_grid`, the parameters' names must be strings, but {param_name} was found.")

    def _prepare_categorical_model_and_X(self, X, model=None, model_params=None, predict=False):

        model_params = model_params or dict()
        model_cls_name = get_model_name(model if model is not None else self.model_cls)

        if self.data_manager.has_categorical_features():
            cat_features = [f.name
                            for i, f in enumerate(self.data_manager.data_params.features)
                            if i in self.data_manager.data_params_internal.categorical_features_
                            ]
            if model_cls_name in ["XGBClassifier", "XGBRegressor"]:
                if _xgboost_user_mode():
                    if not predict:
                        model_params["categorical_feature"] = cat_features
                        model_params["enable_categorical"] = True
                    X = self._set_df_dtypes(X, cat_features)
            elif model_cls_name in ["CatBoostClassifier", "CatBoostRegressor"]:
                if _catboost_user_mode():
                    X = self._set_df_dtypes(X, cat_features)
                if not predict:
                    model_params["cat_features"] = cat_features
            elif model_cls_name in ["LGBMClassifier", "LGBMRegressor"]:
                if not predict:
                    model_params["categorical_feature"] = cat_features
                X = self._set_df_dtypes(X, cat_features)

        return X, model_params

    def _get_level_specific_n_samples_upper_bound(self, tree_idx: int, level: int) -> int:
        """
        Compute an upper bound on the number of samples matching a specifically requested level.
        For a balanced tree and a default level of 0, this number would expectedly be the coreset_size.
        But for lower levels and/or unbalanced trees (orphans/buffer), this number will be higher than just
        the coreset_size, because it depends on the amount of nodes which the data is sampled from in multiples
        of coreset_size.
        """
        # "Buffer Tree" edge case where a single coreset is created from the entire dataset.
        tree = self.trees[tree_idx]
        if tree.chunk_size < 0:
            return tree.buffer_node.coreset_size

        nodes, _, _, buffer = tree.get_all_nodes_at_some_generalised_level(level=level)
        multiplier = len(nodes)
        # chunk_size of length 0 indicates that coreset tree leaves are added in full from the batches of data as
        # they are added, in which case there will be no buffer / buffer will be empty.
        if buffer is not None and tree.chunk_size > 0:
            multiplier += buffer.n_represents_total / tree.chunk_size
        total_build_indexes = tree.get_tree_sum_build_indexes(level)
        coreset_size = tree._compose_coreset_size(tree.coreset_size, total_build_indexes)
        return round(coreset_size * multiplier)

    # def _get_all_nodes_at_some_generalised_level_internal(self, level):
    #     return self.tree.get_all_nodes_at_some_generalised_level(level)

    def _get_all_nodes_at_optimal_generalised_level_internal(self, tree_idx: int):
        """
        Find the best level to do cross-validation, and extract the relevent data
        (nodes, nodes' levels, nodes' indexes, buffer).

        Parameters
        ----------
            tree_idx: int
                Index of the desired tree
        Returns
        ----------
        nodes: list of Nodes
            A list with all nodes at the optimal generalised level.
        levels:
            list of ints A list with all nodes' levels at the optimal generalised level.
        indexes: list of ints
            A list with all nodes' indexes at the optimal generalised level.
        buffer_node: Node
            The buffer
        n_folds_preliminary: int
            Tentative number of folds.
        """
        tree = self.trees[tree_idx]
        depth = len(tree.tree)
        optimal_level_found = False
        for level in range(depth):
            levels, indexes, nodes, buffer_node = tree._get_level_nodes(
                level, include_orphans_heads=True, return_buffer=True
            )
            n_folds_preliminary = self._get_preliminary_number_of_folds(levels)
            # get real number of folds
            folds_nodes, folds_levels, folds_indexes = self._split_into_folds(
                nodes,
                levels,
                indexes,
                buffer_node,
                n_folds_preliminary)
            # If we found a level on which a 4 or 5 folds cross-validation can be done, we can stop
            # else, we continue
            if len(folds_nodes) in [4, 5]:
                add_telemetry_attribute("The optimal level computed for cross-validation:", str(level))
                return nodes, levels, indexes, buffer_node, n_folds_preliminary
            # If a 5 folds cross-validation can't be done, we will use
            # the level after which more than 10 folds are generated.
            # If this is also not available, the last level will be used
            if (not optimal_level_found) and (level == depth - 1 or tree.leaf_factor * n_folds_preliminary > 10):
                add_telemetry_attribute("The optimal level computed for cross-validation:", str(level))
                backup_output = nodes, levels, indexes, buffer_node, n_folds_preliminary
                optimal_level_found = True
        return backup_output

    @staticmethod
    def _get_preliminary_number_of_folds(levels):
        """
        Get the number of folds if only the regular nodes are considered.

        Parameters
        ----------
        levels: list of ints
            Levels at the current generalised level.
        Returns
        ----------
        n_folds_preliminary: int
            Tentative number of folds.
        """
        min_level = min(levels)
        n_regular_nodes = levels.count(min_level)
        n_folds_preliminary = 1
        if n_regular_nodes % 10 == 0:
            n_folds_preliminary = 10
        elif n_regular_nodes % 4 == 0:
            n_folds_preliminary = 4
        elif n_regular_nodes % 5 == 0:
            n_folds_preliminary = 5
        else:
            n_folds_preliminary = n_regular_nodes
        return n_folds_preliminary

    def _requires_tree(self):
        if self.trees is None or len(self.trees) == 0:
            raise RuntimeError("Invalid operation. Coreset tree must be built prior to using this operation.")

    def _check_sensi_recalc(self, sensi_recalc):
        # TODO Dacian: multiple trees?
        minus_one = len(self.trees[0].tree) - 1
        if sensi_recalc in [minus_one, -1] and self.chunk_sample_ratio != 1:
            raise ValueError("force_sensitivity_recalc = len(tree)-1 or force_sensitivity_recalc = -1 "
                             "are not supported when chunk_sample_ratio < 1")

    def _get_default_preprocessing_stage(self, preprocessing_stage=None, model=None):
        """
        Get the default preprocessing stage based on the provided model or class.

        Based on the results of October 2024 experimental runs, carried-out during the development of the TE and
        MIXED categorical encoding support, on the datasets of Criteo, Chalice, IEEE and Airline Delay (all binary
        classification problems), the results can be summarized as follows:

        * For XGBoost, preprocessing_stage AUTO is better in (almost) all cases.
        * For LightGBM, preprocessing_stage AUTO is better in most of the cases.
        * For CatBoost, preprocessing_stage USER is better in most of the cases.

        In light of these conclusions, it was decided, for DTC and DTR, to assign the default of preprocessing_stage =
        USER when CatBoost is used - and retain the other libraries on AUTO.

        Parameters:
            preprocessing_stage: PreprocessingStage, optional, default None.
                The specified preprocessing stage. If None, it will be determined based on the type of the model.

            model: A Scikit-learn compatible model instance, optional.
                The machine learning model instance. If None, the default model for the class will be considered.

        Returns:
            PreprocessingStage
        """
        if preprocessing_stage is None:
            model_cls_name = get_model_name(model if model is not None else self.model_cls)
            if model_cls_name in ["CatBoostClassifier", "CatBoostRegressor"] and _catboost_user_mode():
                return PreprocessingStage.USER
            return PreprocessingStage.AUTO
        return preprocessing_stage

    def _print_model_warning(self, model, model_type: str = "Regressor"):
        if model is None and self.user_set_model is False:
            model_name = get_model_name(model if model is not None else self.model_cls)
            message = f"Using {model_name} model."
            example_model = f"CatBoost{model_type}" if model_name == f"CatBoost{model_type}" else f"LGBM{model_type}"
            message += (
                f" To use a different model, please set the model parameter. E.g.: "
                f"service_obj.fit(model={example_model}(**params), **other_params)"
            )
            print(message)

    @staticmethod
    def _split_into_folds(nodes, levels, indexes, buffer_node, n_folds):
        """
        A method for splitting the nodes into folds (groups of nodes) for validation.

        Parameters
        ----------
        nodes: list of Nodes
            The list with the available nodes.
        levels: list of ints
            The list with the levels of the nodes.
        indexes: list of ints
            The list with the indexes of the nodes.
        buffer_node: Node
            The buffer
        n_folds: int
            The number of folds
        Returns
        ----------
        folds_nodes: list of lists of Node
            The nodes split into folds
        folds_levels: list of lists of int
            The nodes' levels split into folds
        folds_indexes: list of lists of int
            The nodes' indexes split into folds
        """
        max_level = max(levels)
        min_level = min(levels)
        folds_nodes = []
        folds_levels = []
        folds_indexes = []
        if max_level == min_level:
            # All nodes are at the same level
            fold_size = len(nodes) // n_folds
            for i in range(n_folds):
                folds_nodes.append(nodes[i * fold_size:(i + 1) * fold_size])
                folds_levels.append(levels[i * fold_size:(i + 1) * fold_size])
                folds_indexes.append(indexes[i * fold_size:(i + 1) * fold_size])
            # If there is a buffer node but no orphans, add the buffer to the last fold
            if buffer_node is not None:
                folds_nodes[-1].append(buffer_node)
                folds_levels[-1].append(-1)
                folds_indexes[-1].append(-1)
        else:
            # Orphans at higher levels exist
            regular_nodes_levels_indexes = [(node, level, index) for node, level, index in zip(nodes, levels, indexes)
                                            if level == min_level]
            fold_size = int(len(regular_nodes_levels_indexes) / n_folds)
            for i in range(n_folds):
                cr_regular_nodes_levels_indexes = regular_nodes_levels_indexes[i * fold_size:(i + 1) * fold_size]
                cr_fold_nodes = [node for node, level, index in cr_regular_nodes_levels_indexes]
                cr_fold_levels = [level for node, level, index in cr_regular_nodes_levels_indexes]
                cr_fold_indexes = [index for node, level, index in cr_regular_nodes_levels_indexes]
                folds_nodes.append(cr_fold_nodes)
                folds_levels.append(cr_fold_levels)
                folds_indexes.append(cr_fold_indexes)

            # Add the orphans to a different fold if they have enough data and the folds are made of only one node each.
            # Otherwise add them to the last fold
            orphan_nodes_levels_indexes = [(node, level, index) for node, level, index in zip(nodes, levels, indexes) if
                                           level > min_level]
            # If there is a buffer node, it is to be added to the same fold as the orphans, so add the buffer node here
            #   in order for the size_origin_data_all_orphans calculation to include the samples associated with it
            if buffer_node is not None:
                orphan_nodes_levels_indexes.append((buffer_node, -1, -1))

            size_origin_data_all_orphans = 0
            for node, level, index in orphan_nodes_levels_indexes:
                # n_represents can be a dict, a list or an int
                if isinstance(node.n_represents, dict):
                    size_origin_data_all_orphans += sum(node.n_represents.values())
                elif isinstance(node.n_represents, list):
                    size_origin_data_all_orphans += sum(node.n_represents)
                else:
                    size_origin_data_all_orphans += node.n_represents

            size_origin_data_regular_node = 0
            for node, level, index in zip(nodes, levels, indexes):
                if level == min_level:
                    if isinstance(node.n_represents, dict):
                        size_origin_data_regular_node = sum(node.n_represents.values())
                    elif isinstance(node.n_represents, list):
                        size_origin_data_regular_node = sum(node.n_represents)
                    else:
                        size_origin_data_regular_node = node.n_represents
                    break
            cr_fold_nodes = [node for node, level, index in orphan_nodes_levels_indexes]
            cr_fold_levels = [level for node, level, index in orphan_nodes_levels_indexes]
            cr_fold_indexes = [index for node, level, index in orphan_nodes_levels_indexes]
            # If each fold is composed out of just one node and the size of the original data
            # of the orphans is large enough, create a new fold for all orphans
            if fold_size == 1 and size_origin_data_all_orphans >= 0.4 * size_origin_data_regular_node:
                folds_nodes.append(cr_fold_nodes)
                folds_levels.append(cr_fold_levels)
                folds_indexes.append(cr_fold_indexes)
            else:
                # ...otherwise add orphans to the last fold
                folds_nodes[-1].extend(cr_fold_nodes)
                folds_levels[-1].extend(cr_fold_levels)
                folds_indexes[-1].extend(cr_fold_indexes)
            # Add the buffer, if it exists, to the last fold: if the last fold was just constructed for the
            #   orphans, add the buffer to this last fold; if the orphans were appended to the existing last fold
            #   add the buffer to the same existing last fold
            if buffer_node is not None:
                folds_nodes[-1].append(buffer_node)
                folds_levels[-1].append(-1)
                folds_indexes[-1].append(-1)
        return folds_nodes, folds_levels, folds_indexes

    def _adjust_model_parallelism(self, model: Any, validation_params: dict):
        """
        For a parallel grid search we need to limit the model train and predict parallelization to avoid
        competing over cpu resources.
        CatBoost, XGBoost and LGBM all have built in parallelism, GradientBoosting does not.
        Parameters
        ----------
        model - model class for grid search
        validation_params - params dict to validate
        """
        model_name = get_model_name(model if model is not None else self.model_cls)
        if model_name.startswith('CatBoost'):
            validation_params['thread_count'] = 1
        elif model_name.startswith('XGB') or model_name.startswith('LGBM'):
            validation_params['n_jobs'] = 1


def _scores_to_df(scores, only_averages=True):
    # Prepare df of scores
    all_scores = []
    for tree_idx, tree_scores in scores.items():
        for params_str, v in tree_scores.items():
            if params_str == "sample_params":
                continue
            params = dict(params_str)
            if only_averages:
                row = {"mean_folds_score": v}
            else:
                row = {"mean_folds_score": round(sum(v) / len(v), 4)}
                for i, score in enumerate(v):
                    row[f"Fold {i}"] = round(score, 4)
            row.update(params)
            row.update(tree_idx=tree_idx)
            row.update(tree_scores["sample_params"])
            all_scores.append(row)
    return pd.DataFrame(all_scores)


def _compose_seq_params(seq_train_from, seq_train_to, seq_validate_from, seq_validate_to, datetime_format,
                        strict=False):
    seq_params = [seq_train_from, seq_train_to, seq_validate_from, seq_validate_to]
    strict_operators = [False, False, False, False]
    if any([seq_train_from, seq_train_to, seq_validate_from, seq_validate_to]):
        # first check if we need to do any datetime conversion
        for i in range(4):
            if isinstance(seq_params[i], datetime):
                pass
            elif isinstance(seq_params[i], str) and datetime_format:
                try:
                    seq_params[i] = datetime.strptime(seq_params[i], datetime_format)
                except ValueError:
                    raise ValueError(
                        "`seq_column` must either be datetime "
                        "or string in the datetime format provided during build."
                    )

        params_provided = len([x for x in seq_params if x is not None])
        if params_provided in [1, 2]:
            # If the user only supplied 1 parameter we need to autofill its counterpart, so we can create the intervals.
            pairs = [[1, 2], [2, 1], [0, 3], [3, 0]]
            for pair in pairs:
                if seq_params[pair[0]] and not seq_params[pair[1]]:
                    seq_params[pair[1]] = seq_params[pair[0]]
                    strict_operators[pair[1]] = True
                    break
        if all(seq_params) and any([seq_params[0] < seq_params[2] < seq_params[1],
                                    seq_params[0] < seq_params[3] < seq_params[1]]):
            raise ValueError("The validation sequence must have no overlaps with the train sequence.")
        if seq_params[0] and seq_params[1] and seq_params[0] > seq_params[1]:
            raise ValueError("`seq_train_from` cannot be greater than `seq_train_to`")
        if seq_params[2] and seq_params[3] and seq_params[2] > seq_params[3]:
            raise ValueError("`seq_validate_from` cannot be greater than `seq_validate_to`")
        return {
            'params': seq_params,
            'strict_operators': strict_operators
        }
    else:
        if strict:
            raise ValueError("At least one of the following arguments must be provided: "
                             "`seq_train_to`, `seq_train_from`, `seq_validate_to`, `seq_validate_from`")


def decode_categories(preprocessing_info, used_categories):
    all_used_cat_keys = ["ohe_used_categories", "te_used_categories"]
    all_encoded_arrays = [preprocessing_info[all_used_cat_keys[0]], preprocessing_info[all_used_cat_keys[1]]]
    all_cat_features_idxs = [preprocessing_info["ohe_cat_features_idxs"], preprocessing_info["te_cat_features_idxs"]]

    # used_categories list still includes all the original features, including the removed ones, under their original
    # indices - so if features were removed, we need to make sure not to include them. In features removal case,
    # preprocessing_info includes updated feature indices (i.e., each current index values may now be smaller than
    # its original value, or remain the same).
    missing_values_params = preprocessing_info["missing_values_params"]
    removed_features = missing_values_params.get("removed_features", []) if missing_values_params is not None else []
    all_orig_cats_without_removed = sorted([int(k) for k in used_categories.keys() if k != 'y' and int(
        k) not in removed_features]) if used_categories is not None else []
    all_curr_cats = sorted([x for xs in all_cat_features_idxs for x in xs])  # flat list
    all_curr_to_orig_cat_idx = {curr: all_orig_cats_without_removed[i] for i, curr in enumerate(all_curr_cats)}

    # Decode the used categories
    for used_cat_key, encoded_arrays, cat_features_idxs in zip(
            all_used_cat_keys, all_encoded_arrays, all_cat_features_idxs):

        decoded_list = []
        category_dicts = [used_categories[str(all_curr_to_orig_cat_idx[idx])] for idx in cat_features_idxs]

        # Decode each array using the corresponding mapping from used_categories_
        for encoded_array, category_dict, categorical_col_idx in zip(encoded_arrays, category_dicts, cat_features_idxs):
            # Get the dictionary that corresponds to the current array
            category_dict = {v: k for k, v in category_dict.items()}
            # Appending this in the TE case is harmless (won't have any effect).
            category_dict[CATEGORICAL_INFREQUENT] = CATEGORICAL_INFREQUENT
            category_dict[0] = np.nan

            # Create a new list by replacing encoded values with their actual category names
            # use category_dict[value_as_key], all values should 100% exist in category_dict
            decoded_array = [category_dict[value_as_key] for value_as_key in encoded_array]

            # Append the decoded array to the list
            decoded_list.append(np.array(decoded_array, dtype=object))

            # Decode missing_values params as well
            if categorical_col_idx in preprocessing_info["missing_values_params"]["features"]:
                encoded_value = preprocessing_info["missing_values_params"]["features"][categorical_col_idx]
                preprocessing_info["missing_values_params"]["features"][categorical_col_idx] = category_dict[
                    encoded_value]

            preprocessing_info[used_cat_key] = decoded_list

    return preprocessing_info
