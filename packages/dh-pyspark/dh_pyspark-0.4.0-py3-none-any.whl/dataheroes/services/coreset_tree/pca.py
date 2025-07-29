import os
from typing import Union, Callable, Any, Tuple

import numpy as np

from ._base import CoresetTreeService, DataManagerT
from ._mixin import CoresetTreeServiceUnsupervisedMixin
from ..common import CoresetParams, CoresetParamsPCA, DataTuningParams
from ...core.coreset import CoresetPCA
from ...core.sklearn_extra import WPCA
from ...data import DataParams
from ...utils import telemetry


class CoresetTreeServicePCA(CoresetTreeServiceUnsupervisedMixin, CoresetTreeService):
    """
    Subclass of CoresetTreeService for PCA.
    A service class for creating a coreset tree and working with it.
    optimized_for is a required parameter defining the main usage of the service: 'training', 'cleaning' or both,
    optimized_for=['training', 'cleaning'].
    The service will decide whether to build an actual Coreset Tree or
    to build a single Coreset over the entire dataset, based on the triplet:
    n_instances, n_classes, max_memory_gb and the 'number of features' (deduced from the dataset).
    The chunk_size and coreset_size will be deduced based on the above triplet too.
    In case chunk_size and coreset_size are provided, they will override all above mentioned parameters (less recommended).

    When building the Coreset, samples are selected and weights are assigned to them, therefore it is important
    to use functions that support the receipt of sample_weight. Sklearn's PCA implementation does not support the
    receipt of sample_weight, therefore, it is highly recommended to use the built-in fit or fit_transform functions of
    the CoresetTreeServicePCA class as they were extended to receive sample_weight.

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
            The default model class is our WPCA class extending sklearn's PCA to support weights.
    """
    _coreset_cls = CoresetPCA
    _coreset_params_cls = CoresetParamsPCA
    model_cls = WPCA
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
            optimized_for: Union[list, str],
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
        super().__init__(
            data_manager=data_manager,
            data_params=data_params,
            n_instances=n_instances,
            max_memory_gb=max_memory_gb,
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
            model_cls=model_cls,
        )