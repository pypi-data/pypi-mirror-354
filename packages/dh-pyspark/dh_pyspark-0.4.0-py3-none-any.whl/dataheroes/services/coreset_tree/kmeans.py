import os
from typing import Union, Callable, Any, Tuple, Dict

import numpy as np
from sklearn.cluster import KMeans

from ._base import CoresetTreeService, DataManagerT
from ._mixin import CoresetTreeServiceUnsupervisedMixin
from ..common import CoresetParams, CoresetParamsKMeans, DataTuningParams
from ...core.coreset import CoresetKMeans
from ...core.sklearn_extra import kmeans_plusplus_w
from ...core.tree import TreeOptimizedFor
from ...data import DataParams
from ...utils import telemetry


class CoresetTreeServiceKMeans(CoresetTreeServiceUnsupervisedMixin, CoresetTreeService):
    """
    Subclass of CoresetTreeService for KMeans.
    A service class for creating a coreset tree and working with it.
    optimized_for is a required parameter defining the main usage of the service: 'training', 'cleaning' or both,
    optimized_for=['training', 'cleaning'].
    The service will decide whether to build an actual Coreset Tree or
    to build a single Coreset over the entire dataset, based on the triplet:
    n_instances, max_memory_gb and the 'number of features' (deduced from the dataset).
    The chunk_size and coreset_size will be deduced based on the above triplet too.
    In case chunk_size and coreset_size are provided, they will override all above mentioned parameters (less recommended).

    When fitting KMeans on the Coreset, it is highly recommended to use the built-in fit function of
    the CoresetTreeServiceKMeans class. Sklearn uses by default k-means++ as its initialization method.
    While sklearn's KMeans implementation supports the receipt of sample_weight, the kmeans_plusplus
    implementation does not. When building the Coreset, samples are selected and weights are assigned to them,
    therefore, not using these weights will significantly degrade the quality of the results.
    The fit implementation of the CoresetTreeServiceKMeans solves this problem, by extending kmeans_plusplus
    to receive sample_weight.

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

        k : int, default=8.
            Only relevant when tree is optimized_for cleaning. The number of clusters to form as well
            as the number of centroids to generate.

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
            The default model class is sklearn's KMeans, with our extension to kmeans_plusplus to support sample_weight.
    """
    _coreset_cls = CoresetKMeans
    _coreset_params_cls = CoresetParamsKMeans
    model_cls = KMeans
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
            k: int = 8,
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

        if 'cleaning' in self.optimized_for:
            self.coreset_params['cleaning'].algorithm = 'practical'
            self.coreset_params['cleaning'].k = k
            self.params['k'] = k  # Don't know exactly where it's used, check tests.

    def _fit_internal(
            self, X, y, weights, model=None, params=None, preprocessing_info: Dict = None,
            sparse_threshold: float = 0.01, n_clusters=None, model_fit_params: Dict = None, **model_params
    ):
        model_fit_params = model_fit_params or dict()
        initial_centers, _ = kmeans_plusplus_w(
            X=X, n_clusters=n_clusters, w=weights, random_state=model_params.get("random_state")
        )
        model = self.model_cls(n_clusters=n_clusters, n_init=1, **model_params) if model is None else model
        model.set_params(init=initial_centers)
        # Not for all modeling classes' "fit" method, the sample weights are in the 3rd positional argument (Catboost,
        # for example); however, the name of the argument for all of them - as far as we know - is called
        # "sample_weight" - and that's why we specifically use the named argument for weights.
        model.fit(X, y, sample_weight=weights, **model_fit_params)
        self.data_manager.data_params_internal.last_fit_preprocessing_stage = (
            params.get("preprocessing_stage") if params is not None else None
        )
        return model