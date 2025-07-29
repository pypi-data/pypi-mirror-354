import abc
import inspect
import itertools
import json
import os
import pathlib
import re
import shutil
import uuid
from datetime import datetime
from typing import Union, Iterable, TypeVar, Iterator, Any, Dict, Callable, List

import joblib
import numpy as np
import pandas as pd

from dataheroes.data.storage.storage_manager import StorageManager

from dataheroes.data.storage.storage_manager import StorageManager

from .common import CoresetParams, PreprocessingParams, DataTuningParams
from .helpers import JSONEncoderExtra
from ..data import (
    DataManagerBase,
    DataParams,
    Dataset,
    TargetField,
    get_working_directory,
    resolve_manager_cls,
    helpers as data_helpers,
    DefaultDataManager,
    DataManagerSqlite,
    DataManagerHDF5
)
from ..configuration import DataHeroesConfiguration
from ..data.utils import deserialize_function
from ..data.databricks.connection import DatabricksConnection
from ..utils import user_warning
from ..data.databricks.manager import DatabricksQueryManager
from ..data.databricks.utils import save_databricks_chunks, PREFIX, TARGET_PREFIX

DataManagerT = TypeVar('DataManagerT', bound=DataManagerBase)
CoresetServiceBaseT = TypeVar('CoresetServiceBaseT', bound='CoresetServiceBase')

MISSING_TARGET_AND_DATAPARAM_ARGUMENT_EXCEPTION_MESSAGE = "Missing target (y). Please provide target data or use the class data_param input parameter to specify the target column."
DIFFERING_FEATURE_AND_TARGET_SAMPLES_EXCEPTION_MESSAGE = (
    "The target data has a different number of data instances compared to the feature data"
)
DIFFERING_FEATURE_AND_WEIGHT_SAMPLES_EXCEPTION_MESSAGE = (
    "The weight data has a different number of data instances compared to the feature data"
)


class CoresetServiceBase(abc.ABC):
    """
    Abstract class for coreset Services

    Parameters
    ----------
    data_manager: DataManagerBase subclass, optional

    data_params: DataParams, optional
        Preprocessing information.

    coreset_size: int, required
        Coreset size for coreset sampling.

    coreset_params: CoresetParams or dict, optional
        Corset algorithm specific parameters.

    working_directory: str, path, optional
        Local directory where intermediate data is stored.

    cache_dir: str, path, optional
        For internal use when loading a saved service.

    chunk_by: function, label, or list of labels, optional.
        Split the data according to the provided key.
        When provided, chunk_size input is ignored.   
    """
    data_manager_cls = DefaultDataManager
    _coreset_params_cls = CoresetParams
    _data_tuning_params_cls = DataTuningParams
    _coreset_cls = None
    model_cls = None
    create_cache_dir = True
    _is_classification: bool = False
    _is_supervised: bool

    @property
    def is_supervised(self):
        return self._is_supervised

    @property
    def is_classification(self):
        return self._is_classification

    @property
    def coreset_cls(self):
        return self._coreset_cls

    @property
    def coreset_params_cls(self):
        return self._coreset_params_cls

    def __init__(
        self,
        *,
        data_manager: DataManagerT = None,
        data_params: Union[DataParams, dict] = None,
        data_tuning_params: Union[DataTuningParams, dict],
        coreset_params: Union[CoresetParams, dict] = None,
        working_directory: Union[str, os.PathLike] = None,
        cache_dir: Union[str, os.PathLike] = None,
        chunk_by: Union[Callable, str, list] = None,
    ):
        working_directory = working_directory or get_working_directory()
        cache_dir_from_config = DataHeroesConfiguration().get_param_str("cache_dir")
        if cache_dir:
            self._cache_dir = pathlib.Path(cache_dir)
        elif cache_dir_from_config:
            self._cache_dir = pathlib.Path(cache_dir_from_config)
        else:
            self._cache_dir = self._make_cache_dir(working_directory, create=self.create_cache_dir)

        # set data manager
        if data_manager:
            data_manager.set_working_directory(self._cache_dir)
        else:
            data_manager = self._get_default_manager()(working_directory=self._cache_dir)
        if data_params:
            data_manager.data_params = DataParams(**data_params) if isinstance(data_params, dict) else data_params

        self.data_manager = data_manager
        self.data_manager.schema.save_orig = self.data_manager.data_params.save_orig

        if isinstance(coreset_params, dict):
            coreset_params = self.coreset_params_cls(**coreset_params)

        self.params = {
            "data_tuning_params": data_tuning_params,
            "coreset_params": coreset_params,
            "working_directory": str(working_directory),
        }
        self.coreset_params = coreset_params or self.coreset_params_cls()
        self.service_params = None
        self.model = None
        self.chunk_by = chunk_by

        self.storage_manager = StorageManager()

    @property
    def working_directory(self):
        return self.params['working_directory']

    @property
    def sample_all(self):
        return self.params.get('sample_all')

    # TODO: find a way to clean when object is destroy. __del__ is called after all class attributes were deleted.
    def __del__(self):
        try:
            self._cleanup()
        except BaseException:
            pass

    @classmethod
    def _get_default_manager(cls):
        s = DataHeroesConfiguration().get_param_str('default_data_manager')
        if s == 'sqlite':
            return DataManagerSqlite
        elif s == 'hdf5':
            return DataManagerHDF5
        else:
            return cls.data_manager_cls

    @classmethod
    def _load(
            cls,
            dir_path: Union[str, os.PathLike],
            name: str = None,
            *,
            data_manager: DataManagerT = None,
            working_directory: Union[str, os.PathLike] = None
    ) -> CoresetServiceBaseT:
        """
        Restore a service object from a local directory.
        """

        service_params, load_dir = cls._load_params(
            dir_path,
            name,
            data_manager=data_manager,
            working_directory=working_directory
        )
        load_dir = pathlib.Path(load_dir)
        service_obj = cls(**service_params.pop('class_params'))
        model_path = load_dir.joinpath('model.pickle')
        model = joblib.load(model_path) if model_path.exists() else None
        service_obj.model = model
        service_obj.service_params = service_params
        service_obj._post_load(load_dir)
        return service_obj

    def _post_load(self, load_dir: pathlib.Path):
        pass

    @abc.abstractmethod
    def _get_coreset_internal(self, **params):
        ...

    def _predict(self, X):
        return self.model.predict(X)

    def _predict_proba(self, X):
        return self.model.predict_proba(X)

    def _norm_datasets(self, datasets):

        def _to_dset(d):
            d = Dataset(*tuple(map(self._check_dataset, d)))
            if self.is_supervised and d.y is None:
                raise ValueError("Missing target (y). Please provide target data.")
            if d.y is not None and d.y.ndim == 2:
                d = d._replace(y=data_helpers.y_to1d(d.y))
            if len(d.X.shape) != 2:
                raise ValueError("Feature data must have shape of (`n_samples`,`n_features`).")
            if d.y is not None and d.X.shape[0] != d.y.shape[0]:
                raise ValueError(DIFFERING_FEATURE_AND_TARGET_SAMPLES_EXCEPTION_MESSAGE)
            if (
                d.sample_weight is not None
                and d.X.shape[0] != d.sample_weight.shape[0]
            ):
                raise ValueError(DIFFERING_FEATURE_AND_WEIGHT_SAMPLES_EXCEPTION_MESSAGE)
            return d

        datasets = [datasets] if isinstance(datasets, tuple) else datasets
        datasets = map(_to_dset, datasets)
        return datasets

    def _norm_dfs(self, datasets, target_df_must_be_valid = False):

        def _verify_df(d):
            if target_df_must_be_valid and d is None:
                raise ValueError(MISSING_TARGET_AND_DATAPARAM_ARGUMENT_EXCEPTION_MESSAGE)
            return self._check_df(d)

        # datasets = [datasets] if isinstance(datasets, (pd.DataFrame, pd.Series)) else datasets
        datasets = [datasets] if data_helpers.is_dataset(datasets) else datasets
        if datasets is not None:
            datasets = map(_verify_df, datasets)
        elif target_df_must_be_valid :
            raise ValueError(MISSING_TARGET_AND_DATAPARAM_ARGUMENT_EXCEPTION_MESSAGE)
        return datasets

    @staticmethod
    def _check_df(dataset):
        if dataset is not None and not data_helpers.is_pd_array(dataset):
            raise ValueError(f"All arrays must be pandas DataFrame or pandas Series. Found array of type {dataset.__class__.__name__}")
        elif dataset is not None:
            dataset = data_helpers.to_df(dataset)
        return dataset

    @staticmethod
    def _check_dataset(dataset):
        if dataset is not None and not data_helpers.is_ndarray(dataset):
            raise ValueError(f"All arrays must be numpy arrays. Found array of type {dataset.__class__.__name__}")
        elif dataset is not None:
            dataset = data_helpers.to_ndarray(dataset)
        return dataset

    def _build_from_tensorflow_dataset(self, dataset: (Any, Any), **params):
        """
        Process tf.data.Dataset

        Parameters
        ----------
        dataset: tuple (tf.data.Dataset, tfds.core.DatasetInfo)
        """
        import tensorflow_datasets as tfds
        df = pd.DataFrame(tfds.as_dataframe(*dataset))
        return self._build_from_df([df], partial=False, **params)

    def _partial_build_from_tensorflow_dataset(self, dataset: (Any, Any), **params):
        """
        Process new samples based on the tf.data.Dataset

        Parameters
        ----------
        dataset: tuple (tf.data.Dataset, tfds.core.DatasetInfo)
        """
        import tensorflow_datasets as tfds
        df = pd.DataFrame(tfds.as_dataframe(*dataset))
        return self._build_from_df([df], partial=True, **params)

    def _build_from_tensor(self, dataset: Any, **params):
        """
        Process torch.Tensor dataset.

        Parameters
        ----------
        dataset: torch.Tensor    
        """
        df = pd.DataFrame(dataset)
        return self._build_from_df([df], **params)

    def _partial_build_from_tensor(self, dataset: Any, **params):
        """
        Process new samples based the torch.Tensor dataset.

        Parameters
        ----------
        dataset: torch.Tensor
        """
        df = pd.DataFrame(dataset)
        return self._build_from_df([df], partial=True, **params)

    def _build_from_databricks(
        self,
        query: Union[str, List[str]],
        target_query: Union[str, List[str]] = None,
        *,
        catalog: str = None,
        schema: str = None,
        http_path: str = None,
        local_copy_dir: pathlib.Path = None,
        **params,
    ):
        """Create a coreset tree from a Databricks SQL query.


        Parameters
        ----------
        query : Union[str, List[str]]
            A SQL query or a list of SQL queries.

        target_query : Union[str, List[str]], optional
            A SQL query or a list of SQL queries for the target data.

        catalog : str, default=None
            The catalog to use for the query.

        schema : str, default=None
            The schema to use for the query.

        http_path : str, default=None
            The connector url to use for the query. Can be either an sql warehouse or a spark cluster.

        local_copy_dir : pathlib.Path, default=None
            The directory to save the local copy of the query.
        """
        if local_copy_dir is not None:
            local_copy_dir = pathlib.Path(local_copy_dir)

        if local_copy_dir is not None:
            main_files = sorted(local_copy_dir.glob(f"{PREFIX}_chunk_*.parquet"))
            target_files = sorted(local_copy_dir.glob(f"{TARGET_PREFIX}_chunk_*.parquet"))
            target_files = target_files if target_files else None
            if main_files:
                return self._build_from_file(main_files, target_files)

        # Create Databricks connection and manager
        connection = DatabricksConnection(
            catalog=catalog, schema=schema, http_path=http_path
        )

        databricks_manager = DatabricksQueryManager(connection=connection)

        # Get chunk size from params
        chunk_size = params.get("chunk_size", None)

        def concatenate_generators(queries):
            """Create a generator that concatenates all query results."""
            if isinstance(queries, str):
                # If it's a single query string, just return its generator
                yield from databricks_manager.get_data(queries, chunk_size=chunk_size)
            else:
                # If it's a list of queries, concatenate their generators
                for single_query in queries:
                    yield from databricks_manager.get_data(
                        single_query, chunk_size=chunk_size
                    )

        # Get main data iterator (handles both single query and list of queries)
        datasets = concatenate_generators(query)

        # Get target data iterator if provided (handles both single query and list of queries)
        if target_query is not None:
            target_datasets = concatenate_generators(target_query)
        else:
            target_datasets = None

        if local_copy_dir is not None:
            datasets, target_datasets = save_databricks_chunks(datasets, target_datasets, local_copy_dir)
        return self._build_from_df(datasets, target_datasets, **params)

    def _save(
        self,
        dir_path: Union[str, os.PathLike] = None,
        name: str = None,
        override: bool = False,
        service_params=None,
        is_tree=False,
    ) -> str:
        """
        Save service configuration and relevant data to a local directory.
        Use this method when the service needs to restored.

        Parameters
        ----------
        dir_path: string or PathLike, optional, default self.working_directory
            A local directory for saving service's files.

        name: string, optional, default service class name (lower case)
            Name of the sub-directory where the data will be stored.

        override: bool, optional, default false
            False: add a timestamp suffix so each save won’t override previous ones.
            True: existing sub-directory with that name is overridden.

        Returns
        -------
        Save directory path.
        """

        name = name or self._get_save_name()
        dir_path = dir_path or self.working_directory or DataHeroesConfiguration().get_param_str("dir_path")
        assert dir_path, f'Cannot resolve `dir_path`. Neither `dir_path` nor `working_directory` are defined'
        dir_path = str(dir_path)

        # create root directory if needed
        assert (not self.storage_manager.exists(dir_path) or 
                self.storage_manager.is_dir(dir_path)), \
                f"`dir_path` is not a directory ({dir_path})"
        self.storage_manager.mkdir(dir_path, parents=True, exist_ok=True)

        # create subdirectory where data will be stored
        # when override, remove existing directory
        if override:
            save_dir = self.storage_manager.joinpath(dir_path, name)
            if self.storage_manager.exists(save_dir):
                self.storage_manager.remove_dir(save_dir)
            self.storage_manager.mkdir(save_dir)
        else:
            # TODO Modify utcnow() with another method
            save_dir = self.storage_manager.joinpath(dir_path, f'{name}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}')
            assert not self.storage_manager.exists(save_dir), f'save_dir already exist ({save_dir})'
            self.storage_manager.mkdir(save_dir)

        save_dir = str(save_dir)
        model_path = self.storage_manager.joinpath(save_dir, "model.pickle")
        service_params_path = self.storage_manager.joinpath(save_dir, "service_params.json")
        class_params = dict(self.params)
        if is_tree:
            class_params['coreset_params'] = {key: val.to_json() for key, val in class_params['coreset_params'].items()} \
                if class_params['coreset_params'] else None
        else:
            class_params['coreset_params'] = class_params['coreset_params'].to_json() if class_params['coreset_params'] else None

        d = self.service_params or dict()
        d.update(
            data_manager_schema=self.data_manager.save(save_dir),
            data_manager_cls=self.data_manager.__class__.__name__,
            class_params=class_params,
            **(service_params or dict())
        )
        service_params = d

        service_params_bytes = data_helpers.jsonobj_to_bytes(service_params, JSONEncoderExtra)
        self.storage_manager.dump_bytes(service_params_bytes, service_params_path)

        if self.model:
            model_bytes = data_helpers.joblib_dumps(self.model)
            self.storage_manager.dump_bytes(model_bytes, model_path)

        return save_dir

    @classmethod
    def _load_params(
            cls,
            dir_path: Union[str, os.PathLike],
            name: str = None,
            *,
            data_manager: DataManagerT = None,
            working_directory: Union[str, os.PathLike] = None,
    ):
        """
        Restore a service object parameters from a local directory.

        Parameters
        ----------
        dir_path: str, path
            Local directory where service data is stored.

        name: string, optional, default service class name (lower case)
            The name prefix of the sub-directory to load.
            When more than one sub-directories having the same name prefix are found, the last one, ordered by name, is selected.
            For example when saving with override=False, the chosen sub-directory is the last saved.

        data_manager: DataManagerBase subclass, optional
            When specified, input data manger will be used instead of restoring it from the saved configuration.

        working_directory: str, path, optional, default use working_directory from saved configuration
            Local directory where intermediate data is stored.

        Returns
        -------
        service_params, load_dir
        """
        storage_manager = StorageManager()
        load_dir = cls._resolve_load_dir(dir_path, name, storage_manager)
        service_params_path = storage_manager.joinpath(load_dir, 'service_params.json')

        service_params = json.load(storage_manager.read_bytes(service_params_path))
        data_manager_schema = service_params['data_manager_schema']
        class_params = service_params['class_params']
        data_manager_cls = service_params['data_manager_cls']
        saved_working_directory = class_params.get('working_directory') if pathlib.Path(class_params.get('working_directory')).exists() else None
        working_directory = working_directory or saved_working_directory or get_working_directory()
        cache_dir = cls._make_cache_dir(working_directory) if working_directory else None
        if not data_manager:
            if data_manager_cls:
                data_manager_cls = resolve_manager_cls(data_manager_cls)
            data_manager_cls = data_manager_cls or cls.data_manager_cls
            # check if we need to deserialize the granularity
            if data_manager_schema['data_params']['seq_column'] is not None:
                granularity = data_manager_schema['data_params']['seq_column'].get('granularity')
                if isinstance(granularity, dict):
                    granularity = deserialize_function(granularity)
                    data_manager_schema['data_params']['seq_column']['granularity'] = granularity
                    data_manager_schema['data_params_internal']['seq_granularity_'] = granularity
            data_manager_schema = data_manager_cls.schema_cls(**data_manager_schema)
            data_manager = data_manager_cls.load(data_manager_schema, working_directory=cache_dir, load_dir=load_dir)
        class_params.update(
            data_manager=data_manager,
            cache_dir=cache_dir,
            data_tuning_params=cls._data_tuning_params_cls(**class_params["data_tuning_params"]),
        )
        service_params["tree_params"] = [
            cls._data_tuning_params_cls._sample_params_cls(**tp["sample_params"])
            for tp in service_params["tree_params"]
        ]
        return service_params, load_dir

    def _fit(
        self, tree_idx: int, model=None, model_params=None, coreset_params=None, sparse_threshold=None, model_fit_params=None, **params
    ):

        coreset_params = coreset_params or self.coreset_params

        if self.is_classification:
            if params.get('inverse_class_weight', 'empty') == 'empty':
                # If the user passed a model with pre-existing class weights, set inverse_class_weight = True.
                if model is not None and getattr(model, "class_weight", None) is not None:
                    params["inverse_class_weight"] = True
                # If the user passed in class_weight in the fit function: fit(class_weight = ...) set inverse_class_weight = True
                elif model_params is not None and model_params.get("class_weight", None) is not None:
                    params["inverse_class_weight"] = True
                # If we have a class weight passed in the build, inverse_class_weight = False
                elif coreset_params.to_dict().get("class_weight", None) is not None:
                    params["inverse_class_weight"] = False
            elif params['inverse_class_weight'] is None:
                del params['inverse_class_weight']

        result = self._get_coreset_internal(purpose="fit", tree_idx=tree_idx, **params)

        if "calc_replacements" in inspect.signature(self._prepare_encoded_data).parameters.keys():
            # Refinement or resampling require calculating replacements, since any "further" training data beyond the
            # original coreset data, such as data used for refinement or data sampled during resampling rounds, may be
            # out of date with the missing data produced for the original coreset data - which may either have
            # incomplete values or even an empty dictionary. Note that even though refinement or resampling may be
            # "turned on", they may be turned off further down the road, because of, e.g., XGB/LGB version
            # incompatibility.
            if hasattr(self, "fit_params"):
                refine = self.fit_params.get("refine", False)
                resample = self.fit_params.get("resample", False)
                calc_replacements = refine or resample
            else:
                calc_replacements = False
            encoded_res = self._prepare_encoded_data(
                X=result["X"],
                y=result.get("y"),
                weights=result["w"],
                model=model,
                params=params,
                calc_replacements=calc_replacements,
                model_params=model_params,
                sparse_threshold=sparse_threshold,
            )
            model_params = encoded_res['model_params']
        else:
            encoded_res = self._prepare_encoded_data(
                X=result["X"],
                y=result.get("y"),
                weights=result["w"],
                params=params,
            )

        _, X, y, w = encoded_res["data"]
        preprocessing_info = encoded_res["preprocessing_info"]
        model = self._fit_internal(
            X,
            y,
            w,
            model=model,
            params=params,
            preprocessing_info=preprocessing_info,
            sparse_threshold=sparse_threshold,
            model_fit_params=model_fit_params,
            **model_params,
        )
        self._fit_after(model, params, preprocessing_info=preprocessing_info)
        return self.model

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
        self.preprocessing_info = preprocessing_info

    def _prepare_encoded_data(self, X, y, weights, params, **kwargs):
        # to override in children if necessary
        return {
            "data": (np.arange(len(X)), X, y, weights),
            "preprocessing_info": {**PreprocessingParams().to_dict()},
        }

    def _fit_internal(
        self,
        X,
        y,
        weights,
        model=None,
        params=None,
        preprocessing_info: Dict = None,
        sparse_threshold: float = None,
        model_fit_params: Dict = None,
        **model_params,
    ):
        if X.size == 0:
            raise ValueError(f"Can't fit on empty data! Check that the coreset contains data. Given X: {X} with shape: {X.shape}")
        model_params = model_params or dict()
        if model is None:
            model = self.model_cls(**model_params)
        else:
            model.set_params(**model_params)

        model_fit_params = model_fit_params or dict()
        # Not for all modeling classes' "fit" method, the sample weights are in the 3rd positional argument (Catboost,
        # for example); however, the name of the argument for all of them - as far as we know - is called
        # "sample_weight" - and that's why we specifically use the named argument for weights.
        model.fit(X, y, sample_weight=weights, **model_fit_params)
        return model

    def _build_from_file(
            self,
            file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]],
            target_file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]] = None,
            *,
            reader_f=pd.read_csv,
            reader_kwargs: dict = None,
            local_copy_dir: str = None,
            **params
    ) -> CoresetServiceBaseT:

        sort_by_name = target_file_path is not None
        datasets = self.data_manager.read_file(file_path, 
                                               reader_f=reader_f, 
                                               reader_kwargs=reader_kwargs, 
                                               sort_by_name=sort_by_name, 
                                               local_copy_dir=local_copy_dir)
        if target_file_path is not None:
            target_datasets = self.data_manager.read_file(target_file_path, 
                                                          reader_f=reader_f, 
                                                          reader_kwargs=reader_kwargs, 
                                                          sort_by_name=sort_by_name, 
                                                          local_copy_dir=local_copy_dir)
        else:
            target_datasets = None

        self._build_from_df(
            datasets,
            target_datasets=target_datasets,
            **params
        )
        return self

    def _prepare_datasets_from_df(self, datasets, target_datasets=None):
        # convert to an iterator
        datasets = self._norm_dfs(datasets)
        target_datasets = self._norm_dfs(target_datasets)

        # append target_datasets to datasets
        if target_datasets:
            def _append(t):
                x_df, y_df = t
                x_df[self.data_manager.data_params.target.name] = y_df
                return x_df

            if not self.data_manager.data_params.target:
                self.data_manager.data_params.target = TargetField('y')
            datasets = map(_append, zip(datasets, target_datasets))

        return datasets

    def _preprocess_df(self, datasets, **kwargs):
        return self.data_manager.init_and_preprocess(datasets, **kwargs)

    def _preprocess_datasets(self, datasets, **kwargs):
        datasets = iter(datasets)
        dataset = next(datasets)
        datasets = itertools.chain([dataset], datasets)
        self.data_manager.init_from_dataset(*dataset[:3])
        datasets = map(self.data_manager.preprocess_dataset, datasets)
        return datasets

    def _make_chunk_by_params(self, new_sequence):
        # Raise an error if both chunk_by and seq_column.chunk_by are defined
        if self.data_manager.data_params.seq_column and self.data_manager.data_params.seq_column.get('chunk_by') and self.chunk_by:
            raise ValueError("Both `chunk_by` and `seq_column.chunk_by` are defined. Please remove one of them.")

        # Handle chunking by 'every_build'
        if (self.data_manager.data_params.seq_column and self.data_manager.data_params.seq_column.get('chunk_by') == 'every_build'
                or self.chunk_by == 'every_build'):
            format = self.data_manager.data_params.seq_column.get('datetime_format')
            current_sequence = self.data_manager.data_params_internal.seq_every_build
            # if the user passed a granularity we either need to have a sequence passed or there's an already existing sequence
            if format:
                if not new_sequence and not current_sequence:
                    raise ValueError("When using 'every_build' chunking together with a 'datetime_format', a 'seq' must be passed for every build call.")
                else:
                    # we have a sequence passed, check if it's a valid sequence
                    if pd.to_datetime(new_sequence, format=format, errors = "coerce") is pd.NaT:
                        raise ValueError(f"Invalid 'seq' passed for 'every_build' chunking with 'granularity' defined. "
                                         f"Expected format: {format}, value passed: {new_sequence}")
            else:
                # he hasn't provided a granularity, he either provides an integer sequence or we increment the sequence by 1
                if not new_sequence and not current_sequence:
                    new_sequence = 1
                    user_warning("No 'sequence' defined for 'every_build' chunking. Defaulting to 'sequence' = 1.")
                elif not new_sequence:
                    try:
                        new_sequence = current_sequence + 1
                    except TypeError:
                        raise TypeError("Invalid 'sequence' passed for 'every_build' chunking. Expected integer.")
            self.data_manager.data_params_internal.seq_every_build = new_sequence

            return 'every_build'

        # Return the chunking method if it's not 'every_build'
        return 'seq_column' if self.data_manager.data_params.seq_column and self.data_manager.data_params.seq_column.get('chunk_by') is True \
            else self.chunk_by

    def _build_from_df(
            self,
            datasets: Union[Iterator[pd.DataFrame], pd.DataFrame],
            target_datasets: Union[Iterator[Union[pd.DataFrame, pd.Series]], pd.DataFrame, pd.Series] = None,
            copy=False,
            **params

    ) -> CoresetServiceBaseT:

        params['chunk_by'] = self._make_chunk_by_params(params.get('seq'))

        def _check_processed_dataset(dataset):
            if self.is_supervised and dataset.y is None:
                raise ValueError(MISSING_TARGET_AND_DATAPARAM_ARGUMENT_EXCEPTION_MESSAGE)
            if dataset.y is not None and dataset.X.shape[0] != dataset.y.shape[0]:
                raise ValueError(DIFFERING_FEATURE_AND_TARGET_SAMPLES_EXCEPTION_MESSAGE)
            if (
                dataset.sample_weight is not None
                and dataset.X.shape[0] != dataset.sample_weight.shape[0]
            ):
                raise ValueError(DIFFERING_FEATURE_AND_WEIGHT_SAMPLES_EXCEPTION_MESSAGE)
            return dataset

        datasets = self._norm_dfs(datasets)

        target_must_be_valid = self.is_supervised and \
            self.data_manager.data_params is not None and \
            self.data_manager.data_params.target is None
        target_datasets = self._norm_dfs(target_datasets, target_must_be_valid)
        if copy:
            datasets = self._copy_datasets(datasets)
            if target_datasets is not None:
                target_datasets = self._copy_datasets(target_datasets)

        # datasets = self._prepare_datasets_from_df(datasets, target_datasets)
        datasets = zip(datasets, target_datasets) if target_datasets is not None else datasets
        datasets = self._preprocess_df(datasets, **params)
        datasets = map(_check_processed_dataset, datasets)
        self._build_internal(datasets, **params)
        return self

    def _set_df_dtypes(self, X: np.ndarray, cat_columns: List = None, features_out: List = None):
        """
        Converts numpy array into a df and sets the dtypes of the columns of the DataFrame
        Parameters:
            X: DataFrame
                The DataFrame to set dtypes for
            cat_columns: List[int]
                The indices of the categorical columns
        Returns:
            X_df: DataFrame
                The DataFrame with the dtypes set
        """
        features_out = [f.name for f in self.data_manager.data_params.features] if features_out is None \
            else features_out
        # order of columns in DataFrame - index, features, target(s)
        X_df = pd.DataFrame(X, columns=features_out)
        boolean_features_names = [f.name for i, f
                                  in enumerate(self.data_manager.data_params.features)
                                  if self.data_manager.data_params_internal.bool_features_ is not None
                                  and i in self.data_manager.data_params_internal.bool_features_]
        for column in [col for col
                       in X_df.columns
                       if X_df[col].dtype == object and col not in boolean_features_names]:
            # convert numeric columns with object type to float
            dtype = self._get_feature_type(column)
            try:
                if 'int' in dtype:
                    X_df[column] = X_df[column].astype(int)
                elif 'float' in dtype or dtype is None:
                    X_df[column] = X_df[column].astype(float)
            except (TypeError, ValueError):
                pass
        if cat_columns:
            for column in cat_columns:
                X_df[column] = X_df[column].astype('category')

        return X_df

    def _get_feature_type(self, feature_name):
        """
        Get the type of a feature.

        Parameters:
            feature_name: str
                The name of the feature.

        Returns:
            feature_type: str
                The type of the feature. Returns 'Unknown' if the feature is not found.
        """
        # Search in data_schema
        if self.data_manager.schema.data_schema.columns is not None:
            for col in self.data_manager.schema.data_schema.columns:
                if col.name == feature_name:
                    return str(col.dtype)

        if self.data_manager.schema.dataset_schema.columns is not None:
            # If not found, search in dataset_schema
            for col in self.data_manager.schema.dataset_schema.columns:
                if col.name == feature_name:
                    return str(col.dtype)

    @staticmethod
    def _copy_datasets(datasets: Iterable[Iterable]) -> Iterator:
        """create a copy of all sub-arrays (numpy or DataFrames)"""
        for dataset in datasets:
            if isinstance(dataset, (list, tuple)):
                yield tuple(d.copy() if d is not None else d for d in dataset)
            else:
                yield dataset.copy()

    @abc.abstractmethod
    def _build_internal(self, datasets, **build_params):
        """subclass hook performing the build"""
        ...

    def _build(
            self,
            datasets: Union[Iterator[tuple], tuple] = None,
            copy: bool = False,
            **params
    ):
        datasets = self._norm_datasets(datasets)
        params['chunk_by'] = self._make_chunk_by_params(params.get('sequence'))
        if copy:
            datasets = self._copy_datasets(datasets)
        datasets = self._preprocess_datasets(datasets, **params)
        self._build_internal(datasets, **params)
        return self

    @classmethod
    def _get_save_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _resolve_load_dir(cls, 
                          dir_path: Union[str, os.PathLike], 
                          name: str = None, 
                          storage_manager: StorageManager = StorageManager()):
        name = name or cls._get_save_name()
        candidates = [
            f
            for f in storage_manager.iterdir(dir_path, include_dirs=True)
            if storage_manager.is_dir(f)
            and (
                storage_manager.stem(f) == name
                or re.match(r"%s_\d{8}_\d{4}" % name, storage_manager.stem(f))
            )
        ] if storage_manager.exists(dir_path) else []
        load_dir = sorted(candidates, reverse=True)[0] if candidates else storage_manager.joinpath(dir_path, name)
        return load_dir

    @classmethod
    def _make_cache_dir(cls, root, create=True):
        root = root or get_working_directory()
        cache_dir = pathlib.Path(root, f'.dataheroes_cache', f'{cls._get_save_name()}_{str(uuid.uuid4())[:8]}')
        if create:
            cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def _cleanup(self, remove_cache=True):
        try:
            if self.data_manager:
                self.data_manager.close()
        except BaseException:
            pass

        if remove_cache and self._cache_dir and re.match('%s_.{8}$' % self._get_save_name(), self._cache_dir.name):
            try:
                if self._cache_dir.exists():
                    shutil.rmtree(self._cache_dir)
            except BaseException as err:
                user_warning(f'Failed to remove cache {self._cache_dir} ({err})')

    @staticmethod
    def _convert_build_params(X, y, indices, sample_weight=None, props=None):
        """
        Convert parameters into a tuple([indices, X, y]) or iterator of tuple([indices, X, y]).

        Parameters
        ----------
        X: array like or iterator of arrays like
            an array or an iterator of features

        y: array like or iterator of arrays like
            an array or an iterator of targets

        w: array like or iterator of arrays like
            an array or an iterator of weights

        indices: array like or iterator of arrays like
            an array or an iterator with indices of X

        Returns
        -------
        datasets
        """
        if data_helpers.is_dataset(X):
            datasets = (indices, X, y, sample_weight, props)
        else:
            indices = [] if indices is None else indices
            y = [] if y is None else y
            sample_weight = [] if sample_weight is None else sample_weight
            props = [] if props is None else props
            datasets = itertools.zip_longest(indices, X, y, sample_weight, props)

        return datasets

    def validate_cleaning_samples_arguments(
            self,
            is_classification: bool,
            size: int = None,
            class_size: Dict[Any, Union[int, str]] = None,
    ):
        """
        Argument validation method used in get_cleaning_samples in coreset_service
        and tree_service.
        -------
        Returns

        size, class_size, classes, sample_all or ValueError if arguments are not of
        expected type.
        -------
        """
        if size and size < 0:
            raise ValueError("`size` needs to be greater than 0")
        elif size is None:
            if is_classification:
                if not class_size:
                    raise ValueError("Either `class_size` or `size` must be provided.")
            else:
                raise ValueError("`size` must be provided.")

        if class_size and not isinstance(class_size, dict):
            raise TypeError("`class_size` needs to be of type dict; e.g.: class_size={\"class A\": 10, \"class B\": 50, \"class C\": \"all\"}")

        if class_size and self.data_manager.data_params.target:
            target_dtype = self.data_manager.data_params.target.dtype
            keys = np.array(list(class_size.keys()))
            if target_dtype is not None and target_dtype.kind != keys.dtype.kind and not self.data_manager.data_params_internal.y_mixed_types:
                try:
                    keys = list(keys.astype(target_dtype))
                    class_size = dict(zip(keys, class_size.values()))
                except BaseException:
                    raise ValueError(f"Cannot convert `class_size` keys. Expected {target_dtype.name} got {keys.dtype.name} instead.")

        if class_size and 'any' in class_size.values():
            classes = list(class_size.keys())
            class_size = {k: v for k, v in class_size.items() if v != 'any'}
        else:
            classes = None

        if class_size and 'all' in class_size.values():
            sample_all = [k for k, v in class_size.items() if v == 'all']
            class_size = {k: v for k, v in class_size.items() if v != 'all'}
        else:
            sample_all = None

        if not any([size, class_size]) and sample_all:
            classes = sample_all

        if (class_size or sample_all or classes) and not is_classification:
            raise ValueError("`class_size and sample_all can only be used in classification tasks")

        return size, class_size, classes, sample_all
