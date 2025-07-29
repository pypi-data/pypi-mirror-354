import os
import pathlib
import pandas as pd
import numpy as np
from typing import TypeVar, Optional, Union, Dict, Any, Iterable, Iterator, Tuple

from ...core.common import weight_processing
from ...core.coreset._base import CoresetBase, unique
from ...core.helpers import align_arrays_by_key
from ...core.coreset.common import is_percent

from ..common import CoresetParams
from .._coreset_service_base import CoresetServiceBase, DataManagerT, DataParams
from ...data import SeqIndexField
from ...utils import telemetry, check_feature_for_license


CoresetT = TypeVar('CoresetT', bound='CoresetBase')


class CoresetService(CoresetServiceBase):
    """
    Service class for creating and working with a coreset

    Parameters:
        data_manager: DataManagerBase subclass, optional

        data_params: DataParams, optional
            Preprocessing information.

        coreset_params: CoresetParams or dict, optional
            Corset algorithm specific parameters.

        working_directory: str, path, optional
            Local directory where intermediate data is stored.

        cache_dir: str, path, optional
            For internal use when loading a saved service.
    """

    coreset_cls = CoresetBase
    coreset_params_cls = CoresetParams
    model_cls = None
    create_cache_dir = False

    @telemetry
    def __init__(
            self,
            *,
            data_manager: DataManagerT = None,
            data_params: Union[DataParams, dict] = None,
            coreset_size: Union[int, dict, float] = 0.05,
            coreset_params: Union[CoresetParams, dict] = None,
            sample_all: Iterable = None,
            working_directory: Union[str, os.PathLike] = None,
            cache_dir: Union[str, os.PathLike] = None
    ):
        super().__init__(
            data_manager=data_manager,
            data_params=data_params,
            coreset_size=coreset_size,
            coreset_params=coreset_params,
            sample_all=sample_all,
            working_directory=working_directory,
            cache_dir=cache_dir
        )
        self.dataset = None
        self.coreset: Optional[CoresetT] = None
        self.data_manager.default_index_column_cls = SeqIndexField

    @telemetry
    def build_from_file(
            self,
            file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]],
            target_file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]] = None,
            *,
            reader_f=pd.read_csv,
            reader_kwargs: dict = None,
    ) -> 'CoresetService':
        """
        Create a coreset based on the data taken from a local storage.

        Parameters:
            file_path: file, list of files, directory, list of directories.
                Path(s) to the place where data is stored.
                Data includes features, may include labels and may include indices.

            target_file_path: file, list of files, directory, list of directories, optional
                Use when files are split to features and labels.
                Each file should include only one column.

            reader_f: pandas like read method, optional, default pandas read_csv
                For example, to read excel files use pandas read_excel.

            reader_kwargs: dict, optional
                Keyword arguments used when calling reader_f method.

        Returns:
            self
        """
        return self._build_from_file(
            file_path, target_file_path,
            reader_f=reader_f,
            reader_kwargs=reader_kwargs
        )

    @telemetry
    def build_from_df(
            self,
            datasets: Union[Iterator[pd.DataFrame], pd.DataFrame],
            target_datasets: Union[Iterator[pd.DataFrame], pd.DataFrame] = None,
            **params
    ) -> 'CoresetService':
        """
        Create a coreset rom pandas DataFrame(s).

        Parameters:
            datasets: pandas DataFrame or DataFrame iterator
                Data includes features, may include labels and may include indices.

            target_datasets: pandas DataFrame or DataFrame iterator, optional
                Use when data is split to features and labels.
                Should include only one column.

        Returns:
            self
        """
        return self._build_from_df(datasets, target_datasets, **params)

    @telemetry
    def build(
            self,
            X: Union[Iterable, Iterable[Iterable]],
            y: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
            indices: Union[Iterable[Any], Iterable[Iterable[Any]]] = None,
    ) -> 'CoresetService':
        """
        Create a coreset from a transformed dataset(s).

        Parameters:
            X: array like or iterator of arrays like
                an array or an iterator of features

            y: array like or iterator of arrays like, optional
                an array or an iterator of targets

            indices: array like or iterator of arrays like, optional
                an array or an iterator with indices of X

        Returns:
            self
        """
        datasets = self._convert_build_params(X, y, indices)

        return self._build(datasets)

    @telemetry
    def get_cleaning_samples(
            self,
            size: int = None,
            class_size: Dict[Any, Union[int, str]] = None,
            *,
            ignore_indices: Iterable = None,
            select_from_indices: Iterable = None
    ) -> Tuple[Iterable[int], Iterable[float]]:
        """
        Returns indices of cleaning samples order by importance. Useful for identifying miss-labeled instances.
        At least one of size, class_size must be provided. Must be called after build.

        Parameters:
            size: int, optional
                Number of samples to return.
                When class_size is provided, remaining samples are taken from classes not appearing in class_size dictionary.

            class_size: dict {class: int or "all" or "any"}, optional.
                Controls the number of samples to choose for each class.
                int: return at most size
                "all": return all samples.
                "any": limits the returned samples to the specified classes.

            ignore_indices: array-like, optional.
                An array of indices to ignore when selecting cleaning samples.

            select_from_indices: array-like, optional.
                 An array of indices to include when selecting cleaning samples.

        Returns:
            tuple:
                indices: array-like[int].
                    cleaning samples indices.
                importance: array-like[float].
                    The cleaning value. High value is more important.

        Examples
        -------
        Input:
            size=100,
            class_size={"class A": 10, "class B": 50, "class C": "all"}
        Output:
            10 of "class A",
            50 of "class B",
            12 of "class C" (all),
            28 of "class D/E"
        """

        size, class_size, classes, sample_all = self.validate_cleaning_samples_arguments(
            is_classification=self.coreset.is_classification,
            size=size,
            class_size=class_size
        )

        ind, importance = self.coreset.get_cleaning_samples(
            size=size,
            class_size=class_size,
            classes=classes,
            sample_all=sample_all,
            ignore_indices=ignore_indices,
            select_from_indices=select_from_indices
        )
        return ind, importance

    @telemetry
    def save_coreset(self, file_path):
        ind, w = self.coreset.get_index_weights()
        pd.DataFrame({'indices': ind, 'w': w}).to_csv(file_path, index=False)

    @telemetry
    def save_coreset_data(self, file_path, as_orig: bool = False, with_index: bool = False):
        """
        Save coreset data to a file along with coreset weights.

        Parameters:
            file_path: string or PathLike
                Local file path to store the coreset.

            as_orig: boolean, optional, default False
                True: save in the original format.
                False: save in a processed format (indices, X, y, weight).

            with_index: boolean, optional, default False
                Relevant only when as_orig=True. Save also index column.

        """

        data = self._get_coreset_internal()
        self.data_manager.dataset_to_df(
            data['ind'],
            data['X'],
            data['y']
        ).to_csv(file_path, index=False)

        data = self.get_coreset_data(as_orig, as_orig and with_index)
        if as_orig:
            data['X'].to_csv(file_path, index=False)
        else:
            self.data_manager.get_by_index(data['ind'], as_df=True).to_csv(file_path)

    def _get_by_index(self, ind, *arrays):
        if self.dataset:
            dataset = self.dataset[:4]
            if ind is not None:
                indices, X, y = tuple([arr[ind] if arr is not None else None for arr in dataset])
            else:
                indices, X, y = dataset
        else:
            # w is returned by get_by_index() but has value None
            indices, X, y, _, props, _, _ = self.data_manager.get_by_index(ind)

        left, (indices, X, y) = align_arrays_by_key(tuple([ind, *arrays]), (indices, X, y))
        if arrays:
            arrs, (ind, X, y) = align_arrays_by_key(tuple([ind, *arrays]), (ind, X, y))
            ind, arrays = arrs[0], arrs[1:]
            return ind, X, y, *arrays
        else:
            return ind, X, y

    def _get_orig_by_index(self, ind, with_index):
        if self.dataset:
            data = self.data_manager.orig_to_df(self.dataset[3][ind])
            if not with_index:
                del data[self.data_manager.data_schema.index_col]
        else:
            data = self.data_manager.get_orig_by_index(ind, with_index=with_index)
        return data

    def _init_coreset(self):
        self.coreset = self.coreset_cls(**self.coreset_params.to_dict())

    def _restore_coreset(self, state_dict):
        self.coreset = self.coreset_cls.from_dict(state_dict, **self.coreset_params.to_dict())

    @property
    def coreset_data(self):
        return self.coreset.get_index_weights()

    @telemetry
    def get_coreset(self) -> Tuple[Iterable, Iterable]:
        """
        Get coreset indices and weights.

        Returns:
            A tuple of indices and weights.
                indices: a numpy array of selected indices.
                weights: a numpy array of corresponding weights.
        """
        ind, w = self.coreset.get_index_weights()
        return ind, w

    @telemetry
    def get_coreset_data(self, as_orig=False, with_index=False) -> dict:
        """
        Get coreset data either in a processed format or in the original format.

        Parameters:
            as_orig: boolean, optional, default False
                Should the data be returned in it's original format or as a tuple of indices, X, and optionally y.
                True: data is returned as a pandas DataFrame.
                False: return a tuple of (indices, X, y) if target was used and (indices, X) when there is no target.

            with_index: boolean, optional, default False
                Relevant only when as_orig=True. Should the returned data include the index column.

        Returns:
            dict:
                data: numpy arrays tuple (indices,X, optional y) or a pandas DataFrame
                w: A numpy array of sample weights
                n_represents: number of instances represented by the coreset

        """
        result = self._get_coreset_internal()
        if as_orig:
            ind = result['ind']
            result['X'] = self._get_orig_by_index(ind, with_index)
        return result

    @telemetry
    def fit(self, model=None, model_fit_params=None, **model_params):
        """
        Train a model for the selected coreset.

        Parameters:
            model: object, optional.
                A model instance to train with coreset data.

            model_fit_params: keywords arguments, optional.
                Model fit parameters.

            model_params: keywords arguments, optional.
                model initialization parameters.

        Returns:
            A trained model.

        """
        return self._fit(model_params=model_params, model=model, model_fit_params=model_fit_params)

    @telemetry
    def predict(self, X):
        """
        Run prediction on the trained model.

        Parameters:
            X: array
                an array of features

        Returns:
            Model prediction results
        """
        return self._predict(X)

    @telemetry
    def predict_proba(self, X):
        return self._predict_proba(X)

    def _get_coreset_internal(self, as_orig=False, with_index=False, inverse_class_weight: bool = True, **kwargs):
        ind, w = self.coreset.get_index_weights()
        ind, X, y, w = self._get_by_index(ind, w)

        if self.is_classification:
            n_represents = dict(zip(*unique(y, return_counts=True)))
        else:
            n_represents = len(X)

        w = weight_processing(
            w=w,
            sum_orig_weights=n_represents,
            y=y,
            class_weight=self.coreset_params.to_dict().get("class_weight", None),
            is_classification=self.is_classification)

        return {
            'X': X,
            'y': y,
            'ind': ind,
            'w': w,
            'n_represents': len(X)
        }

    @telemetry
    def save(
            self,
            dir_path: Union[str, os.PathLike] = None,
            name: str = None,
            override: bool = False
    ) -> pathlib.Path:
        """
        save service configuration and relevant data to a local directory.
        Use this method when the service needs to restored.

        Parameters:
            dir_path: default self.working_directory
                A local directory for saving service's files.

            name: default service class name (lower case)
                Name of the sub-directory where the data will be stored.

            override:
                False: add a timestamp suffix so each save won’t override previous ones.
                True: existing sub-directory with that name is overridden.

        Returns:
            Save directory path.
        """

        indices, X, y = self.dataset
        if self.data_manager.support_save:
            self.data_manager.save_selected_samples((indices, X, y), None)

        # Get coreset state. Store arrays as numpy npz file.
        coreset_data = self.coreset.to_dict(with_important=True, to_list=False) if self.coreset else dict()
        d_arr = dict()
        for k in list(coreset_data):
            if isinstance(coreset_data[k], np.ndarray):
                d_arr[k] = coreset_data.pop(k)

        save_dir = self._save(dir_path, name, override, service_params=dict(coreset=coreset_data))
        save_dir = pathlib.Path(save_dir)
        if d_arr:
            np.savez(save_dir.joinpath('coreset_data.npz'), **d_arr)
        return save_dir

    def _post_load(self, load_dir: pathlib.Path):
        state_dict = self.service_params.pop('coreset', None) if self.service_params else dict()
        coreset_data_path = load_dir.joinpath('coreset_data.npz')
        if coreset_data_path.exists():
            state_dict.update(np.load(str(coreset_data_path), allow_pickle=True))

        if state_dict:
            self._restore_coreset(state_dict)

    @classmethod
    @telemetry
    def load(
            cls,
            dir_path: Union[str, os.PathLike],
            name: str = None,
            *,
            data_manager: DataManagerT = None,
            working_directory: Union[str, os.PathLike] = None
    ) -> 'CoresetService':
        """
        Restore a service object from a local directory.

        Parameters:
            dir_path:
                Local directory where service data is stored.

            name: default service class name (lower case)
                The name prefix of the sub-directory to load.
                When more than one sub-directories having the same name prefix are found, the last one, ordered by name, is selected.
                For example when saving with override=False, the chosen sub-directory is the last saved.

            data_manager:
                When specified, input data manger will be used instead of restoring it from the saved configuration.

            working_directory: default use working_directory from saved configuration
                Local directory where intermediate data is stored.

        Returns:
            CoresetService object
        """
        return cls._load(
            dir_path=dir_path,
            name=name,
            data_manager=data_manager,
            working_directory=working_directory
        )

    def _build_internal(self, datasets, **build_kwargs):
        check_feature_for_license("coreset_build")

        datasets = list(datasets)
        if len(datasets) > 1:
            dataset = tuple(np.concatenate(d, axis=0) if d[0] is not None else None for d in zip(*datasets))
        else:
            dataset = datasets[0]
        indices, X, y = dataset[:3]
        self.dataset = (indices, X, y)
        coreset_size = self.params['coreset_size']
        if is_percent(coreset_size):
            coreset_size = int(np.round(coreset_size * X.shape[0]))
            if y is not None:
                coreset_size = max(coreset_size, X.shape[1] * len(np.unique(y)))
        self._init_coreset()
        self.coreset.build(X, y, coreset_size=coreset_size)
