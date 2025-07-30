import os
from typing import Union, Iterable, Callable, Any, Tuple, Dict, List

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

from ._base import CoresetTreeService, DataManagerT
from ._dt_mixin import DTMixin
from ._mixin import CoresetTreeServiceSupervisedMixin, ResampleMixin, RefinementMixin
from ..common import CoresetParams, DataTuningParams, CoresetParamsDTR
from ...core.coreset import CoresetDTR
from ...data import DataParams
from .. import helpers
from ...utils import telemetry


class CoresetTreeServiceDTR(DTMixin, CoresetTreeServiceSupervisedMixin, CoresetTreeService):
    """
    Subclass of CoresetTreeService for Decision Tree Regression-based problems.
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

        data_tuning_params: <a href="https://data-heroes.github.io/dh-library/reference/services/data_tuning_params/">DataTuningParams</a> or dict, optional. Data tuning information.

        n_instances: int.
            The total number of instances that are going to be processed (can be an estimation).
            This parameter is required and the only one from the above mentioned quadruplet,
            which isn't deduced from the data.

        max_memory_gb: int, optional.
            The maximum memory in GB that should be used.
            When not provided, the server's total memory is used.
            In any case only 80% of the provided memory or the server's total memory is considered.

        optimized_for: str or list
            Either 'training', 'cleaning' or or both ['training', 'cleaning'].
            The main usage of the service.

        chunk_size: int, optional.
            The number of instances to be used when creating a coreset node in the tree.
            When defined, it will override the parameters of optimized_for, n_instances, n_classes and max_memory_gb.
            chunk_size=0:  Nodes are created based on input chunks.
            chunk_size=-1: Force the service to create a single coreset from the entire dataset (if it fits into memory).

        chunk_by: function, label, or list of labels, optional.
            Split the data according to the provided key.
            When provided, chunk_size input is ignored.

        coreset_params: CoresetParams or dict, optional.
            Coreset algorithm specific parameters.

        node_train_function: Callable, optional.
            method for training model at tree node level.

        node_train_function_params: dict, optional.
            kwargs to be used when calling node_train_function.

        node_metadata_func: callable, optional.
            A method for storing user metadata on each node.

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
            The default model class which will be selected for this class instance will be XGBRegressor, on condition the
            xgboost library is installed. Otherwise, LGBMRegressor will be chosen if the lightgbm library is installed. Else,
            in the presence of the Catboost library, the selected class will be the CatBoostRegressor. Lastly, if none of the
            mentioned three libraries are installed, sklearn's GradientBoostingRegressor will be chosen as the final fallback.
    """

    _coreset_cls = CoresetDTR
    _coreset_params_cls = CoresetParamsDTR
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
        n_classes: int = None,
        optimized_for: Union[list, str],
        chunk_size: int = None,
        chunk_by: Union[Callable, str, list] = None,
        coreset_params: Union[CoresetParamsDTR, dict] = None,
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
        if model_cls is not None:
            self.user_set_model = True
            self.model_cls = model_cls
        elif helpers.is_xgb_installed():
            from xgboost import XGBRegressor

            self.model_cls = XGBRegressor
        elif helpers.is_lgb_installed():
            from lightgbm import LGBMRegressor

            self.model_cls = LGBMRegressor
        elif helpers.is_catboost_installed():
            from catboost import CatBoostRegressor

            self.model_cls = CatBoostRegressor
        else:
            self.model_cls = GradientBoostingRegressor
        super().__init__(
            data_manager=data_manager,
            data_params=data_params,
            n_instances=n_instances,
            max_memory_gb=max_memory_gb,
            n_classes=n_classes,
            optimized_for=optimized_for,
            chunk_size=chunk_size,
            chunk_by=chunk_by,
            data_tuning_params=data_tuning_params,
            coreset_params=coreset_params,
            working_directory=working_directory,
            cache_dir=cache_dir,
            node_train_function=node_train_function,
            node_train_function_params=node_train_function_params,
            node_metadata_func=node_metadata_func,
            chunk_sample_ratio=chunk_sample_ratio,
            model_cls=None,
        )