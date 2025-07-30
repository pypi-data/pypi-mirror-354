import math
import inspect
import os
import warnings
from typing import Any, Callable, Dict, Iterable, Iterator, Union, Tuple, Optional, List
from pathlib import Path
from time import time
import numpy as np
import pandas as pd

from dataheroes.core.coreset._base import CoresetBase
from dataheroes.core.tree.common import nodes_below
from dataheroes.utils import telemetry, localtime, colored, _is_allowed
from ..common import FoldIterator, PreprocessingParams

from ...core.coreset.coreset_dtr import fast_1dim_unique
from ...core.numpy_extra import argisin
from ...core.tree.utils import evaluate_max_batch_size
from ...utils import check_feature_for_license
from ..coreset_tree._base import CoresetTreeService
import json
from ...core.estimator import SensitivityEstimatorUnified, SensitivityEstimatorLightweight
from ...core.estimator._base import SensitivityEstimatorBase
from numpy.random import Generator
from dataheroes.data.data_auto_processor import preprocess_data_ohe
from dataheroes.services.coreset_tree._base import calc_blas_limits

# async_tasks, executor = get_parallel_executor(n_jobs)
from concurrent.futures import wait, FIRST_EXCEPTION, as_completed
from dataheroes.common import get_parallel_executor
from threadpoolctl import threadpool_limits


class CoresetTreeServiceUnsupervisedMixin:
    _is_supervised = False
    _is_classification = False


class CoresetTreeServiceSupervisedMixin:
    _is_supervised = True

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
    ) -> "CoresetTreeService":
        """
        Create a coreset tree based on data taken from local storage.
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions. Categorical features are automatically one-hot encoded and missing values are automatically handled.

        Parameters:
            file_path: file, list of files, directory, list of directories.
                Path(s) to the place where data is stored.
                Data includes features, may include targets and may include indices.
                The paths can be local or on AWS S3, Google Cloud Platform Storage, Azure Storage

            target_file_path: file, list of files, directory, list of directories, optional.
                Use when the dataset files are split to features and target.
                Each file should include only one column.
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
        return super().build_from_file(
            file_path=file_path,
            target_file_path=target_file_path,
            reader_f=reader_f,
            reader_kwargs=reader_kwargs,
            reader_chunk_size_param_name=reader_chunk_size_param_name,
            local_copy_dir=local_copy_dir,
            seq=seq,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def partial_build_from_file(
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
    ) -> "CoresetTreeService":
        """
        Add new samples to a coreset tree based on data taken from local storage.
        Categorical features are automatically one-hot encoded and missing values are automatically handled.

        Parameters:
            file_path: file, list of files, directory, list of directories.
                Path(s) to the place where data is stored.
                Data includes features, may include targets and may include indices.
                The paths can be local or on AWS S3, Google Cloud Platform Storage, Azure Storage

            target_file_path: file, list of files, directory, list of directories, optional.
                Use when files are split to features and target.
                Each file should include only one column.
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
        return super().partial_build_from_file(
            file_path=file_path,
            target_file_path=target_file_path,
            reader_f=reader_f,
            reader_kwargs=reader_kwargs,
            reader_chunk_size_param_name=reader_chunk_size_param_name,
            local_copy_dir=local_copy_dir,
            seq=seq,
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
            verbose: int = 1,
    ) -> "CoresetTreeService":
        """
        Create a coreset tree from pandas DataFrame(s).
        build functions may be called only once. To add more data to the coreset tree use one of
        the partial_build functions. Categorical features are automatically one-hot encoded and missing values are automatically handled.

        Parameters:
            datasets: pandas DataFrame or a DataFrame iterator.
                Data includes features, may include labels and may include indices.

            target_datasets: pandas DataFrame or a DataFrame iterator, optional.
                Use when data is split to features and target.
                Should include only one column.

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
        return super().build_from_df(
            datasets=datasets,
            target_datasets=target_datasets,
            seq=seq,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose,
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
            verbose: int = 1,
    ) -> "CoresetTreeService":
        """
        Add new samples to a coreset tree based on the pandas DataFrame iterator.
        Categorical features are automatically one-hot encoded and missing values are automatically handled.

        Parameters:
            datasets: pandas DataFrame or a DataFrame iterator.
                Data includes features, may include targets and may include indices.

            target_datasets: pandas DataFrame or a DataFrame iterator, optional.
                Use when data is split to features and target.
                Should include only one column.

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
        return super().partial_build_from_df(
            datasets=datasets,
            target_datasets=target_datasets,
            seq=seq,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def build(
            self,
            X: Union[Iterable, Iterable[Iterable]],
            y: Union[Iterable[Any], Iterable[Iterable[Any]]],
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
        the partial_build functions. Categorical features are automatically one-hot encoded and missing values are automatically handled.

        Parameters:
            X: array like or iterator of arrays like.
                An array or an iterator of features. Categorical features are automatically one-hot encoded
                and missing values are automatically handled.

            y: array like or iterator of arrays like.
                An array or an iterator of targets.

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
        return super().build(
            X=X,
            y=y,
            sample_weight=sample_weight,
            indices=indices,
            props=props,
            seq=seq,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def partial_build(
            self,
            X: Union[Iterable, Iterable[Iterable]],
            y: Union[Iterable[Any], Iterable[Iterable[Any]]],
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
        Categorical features are automatically one-hot encoded and missing values are automatically handled.

        Parameters:
            X: array like or iterator of arrays like.
                An array or an iterator of features. Categorical features are automatically one-hot encoded
                and missing values are automatically handled.

            y: array like or iterator of arrays like.
                An array or an iterator of targets.

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
        return super().partial_build(
            X=X,
            y=y,
            sample_weight=sample_weight,
            indices=indices,
            props=props,
            seq=seq,
            copy=copy,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def build_from_file_insights(self, file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]],
                                 target_file_path: Union[
                                     Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]] = None,
                                 reader_f=pd.read_csv, reader_kwargs=None, reader_chunk_size_param_name=None) -> Dict:
        """
        Provide insights into the Coreset tree that would be built for the provided dataset.
        The function receives the data in the same format as its build_from_file counterpart.
        Categorical features are automatically one-hot encoded or target encoded
        and missing values are automatically handled.

        Parameters:
            file_path: file, list of files, directory, list of directories.

            target_file_path: file, list of files, directory, list of directories, optional.
                Use when files are split to features and target.
                Each file should include only one column.

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
        return super().build_from_file_insights(file_paths=file_path, reader_f=reader_f,
                                                target_file_path=target_file_path,
                                                reader_kwargs=reader_kwargs,
                                                reader_chunk_size_param_name=reader_chunk_size_param_name)

    @telemetry
    def build_from_df_insights(self, datasets: Union[Iterator[pd.DataFrame], pd.DataFrame],
                               target_datasets: Union[Iterator[pd.DataFrame], pd.DataFrame] = None) -> Dict:
        """
        Provide insights into the Coreset tree that would be built for the provided dataset.
        The function receives the data in the same format as its build_from_df counterpart.
        Categorical features are automatically one-hot encoded or target encoded
        and missing values are automatically handled.

        Parameters:
            datasets: pandas DataFrame or a DataFrame iterator.
                Data includes features, may include targets and may include indices.

            target_datasets: pandas DataFrame or a DataFrame iterator, optional.
                Use when data is split to features and target.
                Should include only one column.

        Returns:
            Insights into the Coreset tree build function.
        """
        return super().build_from_df_insights(datasets=datasets, target_datasets=target_datasets)

    @telemetry
    def build_insights(self, X: Union[Iterable, Iterable[Iterable]],
                       y: Union[Iterable[Any], Iterable[Iterable[Any]]] = None) -> Dict:
        """
        Provide insights into the Coreset tree that would be built for the provided dataset.
        The function receives the data in the same format as its build counterpart.
        Categorical features are automatically one-hot encoded or target encoded
        and missing values are automatically handled.

        Parameters:
            X: array like or iterator of arrays like.
                An array or an iterator of features.
            y: array like or iterator of arrays like, optional. An array or an iterator of targets.

        Returns:
            Insights into the Coreset tree build function.
        """
        return super().build_insights(X=X, y=y)

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
        local_copy_dir: Path = None,
        n_jobs: int = None,
        verbose: int = 1,
    ) -> "CoresetTreeService":
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
        return super().build_from_databricks(
            query=query,
            target_query=target_query,
            catalog=catalog,
            schema=schema,
            http_path=http_path,
            seq=seq,
            local_copy_dir=local_copy_dir,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    @telemetry
    def partial_build_from_databricks(
        self,
        query: Union[str, List[str]],
        target_query: Union[str, List[str]] = None,
        *,
        catalog: str = None,
        schema: str = None,
        http_path: str = None,
        seq: Any = None,
        local_copy_dir: Path = None,
        n_jobs: int = None,
        verbose: int = 1,
    ) -> "CoresetTreeService":
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
        return super().partial_build_from_databricks(
            query=query,
            target_query=target_query,
            catalog=catalog,
            schema=schema,
            http_path=http_path,
            seq=seq,
            local_copy_dir=local_copy_dir,
            n_jobs=n_jobs,
            verbose=verbose,
        )


class CoresetTreeServiceClassifierMixin:
    _is_classification = True

    @telemetry
    def get_coreset(
        self,
        tree_idx: int = 0,
        level: int = 0,
        seq_from: Any = None,
        seq_to: Any = None,
        preprocessing_stage: Union[str, None] = "user",
        sparse_threshold: float = 0.01,
        as_df: bool = False,
        with_index: bool = False,
        inverse_class_weight: bool = True,
        save_path: Union[str, os.PathLike] = None
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
            seq_from: string or datetime, optional, default None.
                The start sequence to filter samples by.
            seq_to: string or datetime, optional, default None.
                The end sequence to filter samples by.
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
            as_df: boolean, optional, default False.
                When True, returns the X as a pandas DataFrame.
            with_index: boolean, optional, default False.
                Relevant only when preprocessing_stage='auto'. Should the returned data include the index column.
            inverse_class_weight: boolean, default True.
                True - return weights / class_weights.
                False - return weights as they are.
                Relevant only for classification tasks and only if class_weight was passed in
                the coreset_params when initializing the class.
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
        if _is_allowed():
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
            inverse_class_weight=inverse_class_weight,
        )

        if save_path:
            # If as_df is False, _save_coreset needs to recompute the coreset
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
    def get_cleaning_samples(
            self,
            size: int = None,
            class_size: Dict[Any, Union[int, str]] = None,
            ignore_indices: Iterable = None,
            select_from_indices: Iterable = None,
            select_from_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]
            ] = None,
            ignore_seen_samples: bool = True,
    ) -> Union[ValueError, dict]:
        """
        Returns indices of samples in descending order of importance.
        Useful for identifying mislabeled instances and other anomalies in the data.
        Either class_size (recommended) or size must be provided. Must be called after build.
        This function is only applicable in case the coreset tree was optimized_for 'cleaning'.
        This function is not for retrieving the coreset (use get_coreset in this case).

        Parameters:
            size: int, optional
                Number of samples to return.
                When class_size is provided, remaining samples are taken from classes not appearing in class_size dictionary.

            class_size: dict {class: int or "all" or "any"}, optional.
                Controls the number of samples to choose for each class.
                int: return at most size.
                "all": return all samples.
                "any": limits the returned samples to the specified classes.

            ignore_indices: array-like, optional.
                An array of indices to ignore when selecting cleaning samples.

            select_from_indices: array-like, optional.
                 An array of indices to consider when selecting cleaning samples.

            select_from_function: function, optional.
                 Pass a function in order to limit the selection of the cleaning samples accordingly.
                 The function should accept 4 parameters as input: indices, X, y, properties
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
        self._requires_tree()
        return self._get_cleaning_samples(
            size=size,
            class_size=class_size,
            ignore_indices=ignore_indices,
            select_from_indices=select_from_indices,
            select_from_function=select_from_function,
            ignore_seen_samples=ignore_seen_samples,
        )

    @telemetry
    def get_important_samples(
            self,
            size: int = None,
            class_size: Dict[Any, Union[int, str]] = None,
            ignore_indices: Iterable = None,
            select_from_indices: Iterable = None,
            select_from_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]
            ] = None,
            ignore_seen_samples: bool = True,
    ) -> Union[ValueError, dict]:
        # Raise exception saying that the functionality now is called get_cleaning_samples
        warnings.warn(
            "get_important_samples() is deprecated and will be removed in the future. "
            "Use get_cleaning_samples() instead.",
            DeprecationWarning,
        )
        return self.get_cleaning_samples(
            size=size,
            class_size=class_size,
            ignore_indices=ignore_indices,
            select_from_indices=select_from_indices,
            select_from_function=select_from_function,
            ignore_seen_samples=ignore_seen_samples,
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
            inverse_class_weight: bool = True,
            as_df: bool = True,
    ) -> Dict[str, Union[np.ndarray, FoldIterator, Any]]:
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
            inverse_class_weight: boolean, default True.
                True - return weights / class_weights.
                False - return weights as they are.
                Relevant only for classification tasks and only if class_weight was passed in
                the coreset_params when initializing the class.

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
            inverse_class_weight=inverse_class_weight,
            as_df=as_df,
        )


class ResampleMixin:

    def _get_resampling_level(self, n_rounds: int, tree_idx: int, verbose: bool = False) -> int:
        """
        Resampling level calculation will return the maximal level possible between the root and LeafLevel-1 which
        can fit into memory for the sake of pre-fetching all training data, for all sampling rounds, only once,
        ahead of time, from the DataManager (instead of fetching iteratively on every resampling round, for that
        round only, like we initially did).

        For the sake of calculation, we need to know:
        1. The maximum number of samples which can be pooled together for specific tree levels (the full training
           data of which may be required to be returned by the DataManager),
        2. The maximum number of samples which can be sampled from the pool as a direct derivative of coreset size,
           queried level and the number of rounds, and -
        3. The global limitation on the number of samples allowed to be in memory at a given time.

        To achieve #1 above, we need to utilize the sum of all nodes' build_indexes of every tree level (the size
        of the pool cannot be greater than this sum; in practice, the real pool size will be even smaller, because
        samples contain repetitions, but this is our theoretical maximum).

        To achieve #2, we need to know the number of rounds and the upper bound on the number of samples, which is
        derived directly from coreset_size and the queried level, and to calculate the following -
        (the first round is not re-sampled, hence minus 1): n_samples_upper_bound * (n_rounds - 1)
        This limit is relevant only if our coreset_size/level values are very small, because this formula's result
        for most common values will be greater than #1. Also, this bound assumes uniqueness of samples - however,
        in practice, the number will be smaller.

        To achieve #3, we can use our existing global calculation mechanism used elsewhere, specifically, call
        evaluate_max_batch_size; let's call its result "max_in_mem_samples".

        So, for the general case, it is safe to say that the max number of samples we'll require to fully pre-fetch
        from the DataManager, for a given level in the tree, for all sampling rounds, is min(#1, #2), which is:

            max_level_prefetch_samples = min(n_samples_upper_bound * (num_rounds - 1),
                                             sum(build_indexes_of_tree_level))

        We can then simply iterate the tree levels from the top, and choose the maximal level in the tree for which
        the following holds true:

            max_level_prefetch_samples <= max_in_mem_samples

        ...and use this level as the resampling level.

        NOTICE:
            1. In any case, the maximal resampling level is limited to LL-1 (we do not resample from the leaf level).
            2. Buffer is given a discount and its build indices are not taken into account when we calculate #1 above
               (Not a technical decision - this is just to allow us some more slack in choosing the level, so as not to
               back up a whole level if the only difference is the buffer; we can revert this decision at any time.)
        """

        n_features = self.data_manager.n_features
        n_features_expected = self.data_manager.n_features_expected
        max_in_mem_samples = evaluate_max_batch_size(n_features=n_features_expected)
        tree_leaf_level = self.get_max_level()
        tree = self.trees[tree_idx]

        for level in range(tree_leaf_level):
            nodes, _, _, buffer = tree.get_all_nodes_at_some_generalised_level(level=level)
            # We allow anything in the buffer for free (see above), so it's not a part of the calculation.
            sum_build_indexes = np.sum([len(node.build_indexes) for node in nodes])
            n_samples_upper_bound = self._get_level_specific_n_samples_upper_bound(tree_idx, level)
            max_sampled_idxs = n_samples_upper_bound * (n_rounds - 1)
            max_tree_level_prefetch_samples = min(max_sampled_idxs, int(sum_build_indexes))
            len_buffer_build_indexes = len(buffer.build_indexes) if buffer is not None else 0
            if verbose:
                print(
                    f"Resampling level calculation: [level {level} of {tree_leaf_level}], "
                    f"{n_rounds=}, {n_samples_upper_bound=}, {n_features=}, {n_features_expected=}, {max_in_mem_samples=}, "
                    f"{max_sampled_idxs=}, {sum_build_indexes=} [buffer EXCLUDED], "
                    f"{len_buffer_build_indexes=} [buffer EXCLUDED], "
                    f"{max_tree_level_prefetch_samples=}=min({max_sampled_idxs}, {sum_build_indexes}), "
                    f"{max_tree_level_prefetch_samples > max_in_mem_samples=}"
                )
            if max_tree_level_prefetch_samples > max_in_mem_samples:
                if level == 0:
                    raise ValueError(f"Training data for resampling cannot fit in coreset tree root {level=}")
                if verbose:
                    print(f"Resampling level calculation: returning level {level - 1} (tree traversal)")
                return level - 1

        # The maximal (deepest) level for resampling is LeafLevel-1.
        if verbose:
            print(f"Resampling level calculation: returning level {tree_leaf_level - 1} (default maximum)")
        return tree_leaf_level - 1

    @staticmethod
    def _n_resampling_rounds() -> int:
        return 10

    def _get_resample_nodes(self, n_rounds: int, tree_idx: int, level: int):
        """
        Returns node coresets to be resampled from, and the specific sample sizes to apply on each node.
        The training data of the nodes returned is guaranteed to fully fit in memory with enough room to spare.
        """
        tree = self.trees[tree_idx]
        resampling_level = self._get_resampling_level(tree_idx=tree_idx, n_rounds=n_rounds)

        # An edge case where a user-provided level is greater than the computed resampling_level.
        # In this case, we set the resampling_level as the user-provided level.
        # Even though this may fail on memory, we put it under the user's responsibility - since a too-high level
        # will probably fail even without resampling, just because the user requested to fit on too much data that
        # might not fit in memory.
        resampling_level = max(resampling_level, level)

        if "training_nodes_levels_indexes" in self.fit_params:
            nodes_lvl_idx = []
            for lvl_idx in self.fit_params["training_nodes_levels_indexes"]:
                level_below = max(resampling_level, lvl_idx[0])
                nodes_lvl_idx.extend(nodes_below(lvl_idx, level_below))
            nodes = [tree.tree[::-1][lvl][idx] for lvl, idx in nodes_lvl_idx]
        else:
            nodes, _, _, buffer = tree.get_all_nodes_at_some_generalised_level(level=resampling_level)
            if buffer is not None:
                nodes.append(buffer)
        n_samples_upper_bound = self._get_level_specific_n_samples_upper_bound(tree_idx, level)
        n_repr_sum = sum(node.n_represents_total for node in nodes)
        pcs = [node.n_represents_total / n_repr_sum for node in nodes]
        sizes = [round(n_samples_upper_bound * pc) for pc in pcs]
        return nodes, sizes

    def _get_resample_training_data(
            self,
            tree_idx: int,
            n_iter: int,
            level: int,
            model: Any = None,
            params: dict = None,
            preprocessing_info: dict = None,
            sparse_threshold: float = 0.01,
    ):
        """
        The following is handled and produced **in one go, for all resampling rounds**:
        1. Get the nodes and sizes to be used to resample from.
        2. Sample from the above nodes adhering to sizes.
        3. Fetch all training data (=coresets for all resampling rounds) from the DataManager.
        4. Encode all training data.

        'level' is the user-provided level.
        Return all training data ready to be used by 'fit' methods.
        (ind, X, y, coreset_idxs_all, weights_all, r_nums_all)
        where ind, X, y are unique samples
        and coreset_idxs_all, weights_all, r_nums_all are the coreset indices, weights and round numbers respectively.
        To get the corresponding coreset mask round_mask = r_nums_all == round and search coreset_idxs_all[round_mask] in the unique ind.
        """
        self.__resample_called = True
        nodes, sizes = self._get_resample_nodes(tree_idx=tree_idx, n_rounds=n_iter, level=level)

        non_empty_nodes_idxs = np.where([not node.is_empty() for node in nodes])[0]
        nodes = [nodes[idx] for idx in non_empty_nodes_idxs]
        sizes = [sizes[idx] for idx in non_empty_nodes_idxs]
        # Here we use just coreset_size to sample, because we are in a regression case
        # However, in classification cases we need to scale and pass .sample_params too
        # TODO Continuing comment above -
        #  The only parameter to pass to 'sample' is the coreset_size as tuple, while the rest of the original
        #  params aren't required, as long as we continue working with self.sample_kwargs in CoresetBase.
        #  However, we will need to pass all the original sampling params once we remove self.sample_kwargs.
        iw_all = [
            node.coreset.sample(coreset_size=((n_iter - 1), size), sample_all=self.sample_all)
            for node, size in zip(nodes, sizes)
        ]
        coreset_idxs_all = np.concatenate(
            [
                np.concatenate([node.preprocessed_indexes[idxs[i]] for node, (idxs, _) in zip(nodes, iw_all)])
                for i in range(n_iter - 1)
            ]
        )
        weights_all = np.concatenate([np.concatenate([w[i] for (_, w) in iw_all]) for i in range(n_iter - 1)])
        r_nums_all = np.concatenate(
            [np.concatenate([np.repeat(i, len(w[i])) for (_, w) in iw_all]) for i in range(n_iter - 1)]
        )
        coreset_idxs_all_unq = fast_1dim_unique(coreset_idxs_all)
        dset_all_unq = self.data_manager.get_by_index(coreset_idxs_all_unq)

        # While **same** coreset indices are **matched by different weights over different rounds**, weights must not
        # be passed (hence None) when pre-computed used_categories & missing_values_params are provided (a product of
        # the first iteration).
        ind_mask, X_unq, y_unq, _ = self._prepare_encoded_data(
            dset_all_unq.X,
            dset_all_unq.y,
            weights=None,
            model=model,
            params=params,
            preprocessing_params=PreprocessingParams.from_dict(preprocessing_info),
            sparse_threshold=sparse_threshold,
        )["data"]

        ind_unq = dset_all_unq.ind[ind_mask]
        # Cannot assume unique below, as coreset_idxs_all has repetitions of coreset indices between different rounds.
        a_mask = argisin(coreset_idxs_all, ind_unq, assume_unique=False)
        # return (ind_unq, X_unq, y_unq, coreset_idxs_all[a_mask], weights_all[a_mask], r_nums_all[a_mask])
        return {
            "idxs_unq": ind_unq,
            "X_unq": X_unq,
            "y_unq": y_unq,
            "idxs_all": coreset_idxs_all[a_mask],
            "weights_all": weights_all[a_mask],
            "iter_idxs": r_nums_all[a_mask],
        }

    def _get_resample_iteration_data(self, data: dict, iteration: int) -> Union[np.ndarray, np.ndarray, np.ndarray]:
        X = data["X_unq"]
        y = data["y_unq"]
        idxs = data["idxs_unq"]
        idxs_all = data["idxs_all"]
        weights_all = data["weights_all"]
        iter_idxs = data["iter_idxs"]

        iter_mask = iter_idxs == iteration
        u_mask = argisin(idxs, idxs_all[iter_mask])
        # If X_pool_unq is a DataFrame, then apply .loc, otherwise just apply the mask.
        X_fit = X.loc[u_mask] if isinstance(X, pd.DataFrame) else X[u_mask]
        y_fit, w_fit = y[u_mask], weights_all[iter_mask]

        return X_fit, y_fit, w_fit


class RefinementMixin:

    def _get_refinement_data(
            self,
            tree_idx: int,
            model=None,
            params: dict = None,
            preprocessing_info: dict = None,
            sparse_threshold: float = 0.01,
    ):
        tree = self.trees[tree_idx]
        self.__refine_called = True
        # "training_nodes_levels_indexes" contains pairs of (level, i)
        if "training_nodes_levels_indexes" in self.fit_params:
            nodes_lvl_idx = []
            for lvl_idx in self.fit_params["training_nodes_levels_indexes"]:
                nodes_lvl_idx.extend(nodes_below(lvl_idx, self.get_max_level()))
            nodes = [tree.tree[::-1][lvl][idx] for lvl, idx in nodes_lvl_idx]
        else:
            nodes, _, _, buffer = tree.get_all_nodes_at_some_generalised_level(level=self.get_max_level())
            if buffer is not None:
                nodes.append(buffer)
        ref_idxs = np.concatenate([node.random_sample_indexes for node in nodes])
        max_samples = evaluate_max_batch_size(n_features=self.data_manager.n_features_expected)
        if len(ref_idxs) > max_samples:
            n_repr_sum = sum(node.n_represents_total for node in nodes)
            pcs = [node.n_represents_total / n_repr_sum for node in nodes]
            sizes = [round(max_samples * pc) for pc in pcs]
            ref_idxs = np.concatenate(
                [np.random.choice(node.random_sample_indexes, size=s, replace=False) for node, s in zip(nodes, sizes)]
            )
        dset = self.data_manager.get_by_index(ref_idxs)
        X, y = dset.X, dset.y
        # Weights must be None when pre-computed used_categories & missing_values_params are provided.
        _, X, y, w = self._prepare_encoded_data(
            X,
            y,
            weights=None,
            params=params,
            model=model,
            preprocessing_params=PreprocessingParams.from_dict(preprocessing_info),
            sparse_threshold=sparse_threshold,
        )["data"]
        return X, y, w

    @staticmethod
    def _n_refinement_rounds(coreset_size: int, n_instances: int) -> int:
        """
        Return the number of refinement rounds according to the following requirement:
        +-----------------------------------------------------------------+
        |  min coreset_size    max coreset_size    refinement_iterations  |
        |  0%                  1%                  10                     |
        |  1%                  2%                  9                      |
        |  2%                  3%                  8                      |
        |  3%                  4%                  7                      |
        |  4%                  5%                  6                      |
        |  5%                  6%                  5                      |
        |  6%                  7%                  4                      |
        |  7%                  8%                  3                      |
        |  8%                  9%                  2                      |
        |  9%                  100%                1                      |
        +-----------------------------------------------------------------+

        IMPORTANT: Must be <= return value of _n_resampling_rounds()!
        """
        return max(1, 10 - math.floor(100 * coreset_size / n_instances))


class EstimationMixin:
    _estimator_types: List[str] = []

    def _get_estimator_cls(self, tree_idx):
        # Each Inheritor of estimator mixin must define a cls._estimator_types. Corectness is checked here.
        tree = self.trees[tree_idx]
        if tree.coreset_params["algorithm"] not in self._estimator_types:
            raise ValueError(
                f"estimator type must be one of {self._estimator_types}, found {self.tree.coreset_params['algorithm']}"
            )
        if tree.coreset_params["algorithm"] == "unified":
            est_cls = SensitivityEstimatorUnified
        elif tree.coreset_params["algorithm"] in ["lightweight", "lightweight_per_feature"]:
            est_cls = SensitivityEstimatorLightweight
        # ...list other algorithms here
        return est_cls

    def _get_coreset_for_estimation(
            self,
            tree_idx: int,
            level: int = 0,
            seq_from=None,
            seq_to=None,
    ) -> Tuple[CoresetBase, Dict, List, List]:
        # Get the data from a level.
        data = self._get_tree_coreset(
            tree_idx=tree_idx,
            level=level,
            seq_from=seq_from,
            seq_to=seq_to,
            with_index=None,
            inverse_class_weight=None,
            preprocessing_stage="auto",
            sparse_threshold=0.01,
            as_df=False,
            return_preprocessing=True,
        )
        # Keep preprocessing params. They will be used to preprocess leaf level data.
        preprocessing = data["preprocessing"]

        # This preprocessing will be exported to the frontend. For now ignore removed columns
        prep_dict = {
            "missing_values": preprocessing.missing_values_params,
            "ohe_used_categories": self.data_manager.expand_encoded_used_categories(
                preprocessing.ohe_used_categories, preprocessing.ohe_cat_features_idxs, include_mapping=False
            ),
            "te_used_categories": self.data_manager.expand_encoded_used_categories(
                preprocessing.te_used_categories, preprocessing.te_cat_features_idxs, include_mapping=False
            ),
        }
        # This is in a dictionary format that `preprocess_data` can handle
        ohe_used_cat_encoded = self.data_manager.expand_encoded_used_categories(
            preprocessing.ohe_used_categories,
            preprocessing.ohe_cat_features_idxs,
            include_mapping=False,
            keep_encoded=True,
        )["order"]
        te_used_cat_encoded = self.data_manager.expand_encoded_used_categories(
            preprocessing.te_used_categories,
            preprocessing.te_cat_features_idxs,
            include_mapping=False,
            keep_encoded=True,
        )["order"]
        tree = self.trees[tree_idx]
        if self.build_w_estimation:  # this assumes no categorical data
            if seq_from is not None or seq_to is not None:
                heads = self._get_tree_heads()
                tree.tree.tree[::-1]

                # Exclude heads which are above wanted level
                due = {key: val for key, val in heads.items() if key[0] >= level}
                # Add nodes which are on the wanted level
                due.update({(level, node_idx): node.n_represents for node_idx, node in enumerate(tree[level])})
                nodes = tree.compute_seq_nodes(due, seq_params=[seq_from, seq_to], seq_operators=[False, False])
            else:
                nodes, _, _, _ = tree.get_all_nodes_at_some_generalised_level(level)
            coresets = [node.coreset for node in nodes]
            if not all(c.enable_estimation for c in coresets):
                raise ValueError(
                    "Not all selected coresets have enable estimation on. Rebuild the tree with 'enable_estimation' set to True"
                )
            coreset = self._coreset_cls()
            coreset.union([node.coreset for node in nodes])

        else:
            X, y, w = data["X"], data["y"], data["w"]
            coreset = self._coreset_cls(**tree.coreset_params)
            coreset.compute_sensitivities(X=X, y=y, w=w)

        return coreset, prep_dict, ohe_used_cat_encoded, te_used_cat_encoded

    def _estimate_leaf_sensitivities(
            self,
            tree_idx: int,
            coreset: CoresetBase,
            preprocessing_dict: Dict,
            ohe_used_cat_encoded,
            te_used_cat_encoded,
            n_jobs: Optional[int] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        if len(te_used_cat_encoded) > 0:
            # Today, we only support OHE in "preprocess_data_ohe" (hence the name...); however, for the TE/MIXED,
            # we will need to do more effort and to actually Target-Encode the TE-group's features, which is future
            # work (and will cause "preprocess_data_ohe" name change as well).
            raise NotImplementedError("TE/MIXED encoding support not implemented for estimation")
        tree = self.trees[tree_idx]
        leaf_nodes = [node for node in tree.tree[0]]
        if tree.buffer_node is not None:
            leaf_nodes.append(tree.buffer_node)

        # Preprocessing is done preferably sequentially, estimation of sensitivities is done in parallel.
        # 4 Cases here:
        # 1. sequential execution and a node fits in memory -> execute sequentially
        # 2. sequential execution and a node doesn't fit in memory -> split in batches and execute sequentially
        # 3. parallel execution and node fits in memory -> Launch task in async then check for memory for the next node.
        # 4. parallel execution and node doesn't fit in memory -> No reason for async here. Launch a single task and wait, similar to 2.
        # Note: in #3 we might wait for all tasks to finish then find out a node doesn't fit in memory. We then backup to 4.

        # If we aren't in a parallel case, we collect in all_sens. Otherwise we collect from futures' results
        async_tasks, executor = get_parallel_executor(n_jobs=n_jobs)
        if executor is None:
            all_sens = []
        all_y = []
        dtype = tree.coreset_params["dtype"]
        # Get by index ignores props so we ignore them here too.
        n_features_ohe = (
                self.data_manager.n_features
                - len(preprocessing_dict["ohe_used_categories"]["order"])
                + sum(len(cats) for cats in preprocessing_dict["ohe_used_categories"]["order"].values())
        )

        ## Helper functions
        def _est_sens(
                X: np.ndarray, y: np.ndarray, node_idx: int, node_time: float, b_idx: int = 1, num_b: int = 1
        ) -> np.ndarray:
            limits = calc_blas_limits(n_jobs=n_jobs)
            with threadpool_limits(limits=limits if limits != os.cpu_count() else None, user_api="blas"):
                s = coreset.sensitivity(X, y, estimate=True)
            if b_idx == num_b:
                node_time = time() - node_time
                # User print
                print(
                    f"{localtime()} Completed node {node_idx + 1} / {len(leaf_nodes)} in "
                    f"{colored(f'{node_time:.3f} seconds', 'yellow')}"
                )
            return s

        def _preprocess_and_estimate(X, y, node_idx: int, node_time: float, b_idx: int = 1, num_b: int = 1):
            X = (
                preprocess_data_ohe(
                    X,
                    ohe_used_categories=ohe_used_cat_encoded,
                    te_used_categories=te_used_cat_encoded,
                    missing_values=preprocessing_dict["missing_values"]["features"],
                    removed_columns=preprocessing_dict["missing_values"].get("removed_features", []),
                    categories_as_str=False,
                    copy=False,
                )
                .astype(dtype)
                .values
            )
            assert X.shape[1] == n_features_ohe
            all_y.append(np.asarray(y))
            if executor is not None:
                async_tasks.append(
                    executor.submit(
                        _est_sens, X=X, y=y, node_time=node_time, node_idx=node_idx, b_idx=b_idx, num_b=num_b
                    )
                )
            else:
                all_sens.append(_est_sens(X=X, y=y, node_time=node_time, node_idx=node_idx, b_idx=b_idx, num_b=num_b))

        ## Start the estimation of leaf nodes
        for i, node in enumerate(leaf_nodes, start=1):
            print(f"Starting node {i} / {len(leaf_nodes)}")  # user print
            # Get indexes for current node and check for memory
            node_idxs = (
                node.build_indexes
                if tree.buffer_node is not None and i == len(leaf_nodes) - 1
                else node.random_sample_indexes
            )
            available_n_rows = evaluate_max_batch_size(n_features=n_features_ohe, available=True, dtype=dtype)
            if len(node_idxs) < available_n_rows:
                node_time = time()
                # Quick get when we save_all
                if self.save_all:
                    data = tree._get_by_nodes(nodes=[node])
                    sh_idxs = node_idxs - node.build_indexes[0]  # shifted idxs, X
                    X, y = data.X[sh_idxs], data.y[sh_idxs]
                else:
                    data = tree._get_by_index(node_idxs)
                    X, y = data.X, data.y
                _preprocess_and_estimate(X=X, y=y, node_idx=i, node_time=node_time)
            else:
                running_tasks = [f for f in async_tasks if f.running()] if async_tasks is not None else []
                # If memory check failed with no running tasks, backup to sequential execution in batches.
                # Otherwise, wait for a running task to complete.
                if len(running_tasks) == 0:
                    node_time = time()
                    idxs_split = np.array_split(node_idxs, len(node_idxs) // available_n_rows + 1)
                    for bi, idxs in enumerate(idxs_split, start=1):
                        data = tree._get_by_index(idxs)
                        _preprocess_and_estimate(data.X, data.y, i, node_time, b_idx=bi, num_b=len(idxs_split))
                        if executor is not None and async_tasks is not None:
                            as_completed(async_tasks[-1])
                else:
                    # wait(running_tasks, return_when=FIRST_COMPLETED)
                    # Check first completed task and run for
                    f = next(as_completed(running_tasks))
                    if f.exception() is not None:  # Check exception of the task.
                        f.result()
        # Wait for all tasks to complete
        if executor is not None and async_tasks is not None:
            wait(async_tasks, return_when=FIRST_EXCEPTION)
            # Check for failed tasks
            failed_tasks = [f for f in async_tasks if f.exception() is not None]
            if len(failed_tasks) > 0:
                raise failed_tasks[0].exception()
            all_sens = np.concatenate([t.result() for t in async_tasks])
        else:
            all_sens = np.concatenate(all_sens)
        all_y = np.concatenate(all_y)
        return all_sens, all_y

    def _create_estimator(
            self,
            tree_idx: int,
            estimator_params: Union[Dict, List[Dict]],
            coreset: CoresetBase,
            sensitivities: np.ndarray,
            y: np.ndarray,
    ) -> Union[SensitivityEstimatorBase, List[SensitivityEstimatorBase]]:
        # Build one or multiple estimators from a coreset and a set of sensitivities.
        one_config = isinstance(estimator_params, dict)
        config_list = [estimator_params] if one_config else estimator_params
        est_list = []
        for config in config_list:
            est = self._get_estimator_cls(tree_idx).from_coreset(
                coreset=coreset, sensitivities=sensitivities, y=y, **config
            )
            est_list.append(est)
        return est_list[0] if one_config else est_list

    @telemetry
    def get_estimator(
            self,
            tree_idx: int = 0,
            level: int = 0,
            seq_from=None,
            seq_to=None,
            percent: Union[float, dict] = 1,
            percent_step: float = 0.1,
            percent_n_steps: int = 5,
            sliding_window_size: Optional[int] = None,
            auto_adjust: bool = True,
            adjust_threshold: int = 1_000_000,
            adjustment_strength: float = 0.1,
            random_state: Optional[Union[int, Generator]] = None,
            return_preprocessing: bool = False,
            n_jobs: Optional[int] = None,
    ) -> Union[SensitivityEstimatorBase, Tuple[SensitivityEstimatorBase, Dict]]:
        check_feature_for_license("estimation")
        estimator_params = {
            "percent": percent,
            "percent_step": percent_step,
            "percent_n_steps": percent_n_steps,
            "sliding_window_size": sliding_window_size,
            "auto_adjust": auto_adjust,
            "adjust_threshold": adjust_threshold,
            "adjustment_strength": adjustment_strength,
            "random_state": random_state,
        }
        # Get a single estimator.
        ests, prep_dict = self.get_estimators(
            [estimator_params],
            tree_idx=tree_idx,
            level=level,
            seq_from=seq_from,
            seq_to=seq_to,
            n_jobs=n_jobs,
            return_preprocessing=True,
        )
        assert len(ests) == 1
        assert isinstance(prep_dict, dict)
        return (ests[0], prep_dict) if return_preprocessing else ests[0]

    @telemetry
    def get_estimators(
            self,
            estimators_params: List[Dict],
            tree_idx: int = 0,
            level: int = 0,
            seq_from=None,
            seq_to=None,
            return_preprocessing: bool = False,
            n_jobs: Optional[int] = None,
    ) -> Union[List[SensitivityEstimatorBase], Tuple[List[SensitivityEstimatorBase], Dict]]:
        check_feature_for_license("estimation")
        # User prints
        print(f"{localtime()} Estimator build started")
        print(f"{localtime()} Estimator build part 1/3 started")
        t = time()
        coreset, prep_dict, ohe_used_cat_encoded, te_used_cat_encoded = self._get_coreset_for_estimation(
            tree_idx=tree_idx, level=level, seq_from=seq_from, seq_to=seq_to
        )
        print(f"{localtime()} Estimator build part 1/3 completed in {colored(f'{time() - t:.3f} seconds', 'yellow')}")
        print(f"{localtime()} Estimator build part 2/3 started")
        t = time()
        # with threadpool_limits(limits=calc_blas_limits(n_jobs=n_jobs), user_api="blas"):
        sensitivities, y = self._estimate_leaf_sensitivities(
            tree_idx=tree_idx,
            coreset=coreset,
            preprocessing_dict=prep_dict,
            ohe_used_cat_encoded=ohe_used_cat_encoded,
            te_used_cat_encoded=te_used_cat_encoded,
            n_jobs=n_jobs,
        )
        print(f"{localtime()} Estimator build part 2/3 completed in {colored(f'{time() - t:.3f} seconds', 'yellow')}")
        print(f"{localtime()} Estimator build part 3/3 started")
        t = time()
        ests = self._create_estimator(tree_idx, estimators_params, coreset, sensitivities, y)
        print(f"{localtime()} Estimator build part 3/3 completed in {colored(f'{time() - t:.3f} seconds', 'yellow')}")
        assert isinstance(ests, list)
        return (ests, prep_dict) if return_preprocessing else ests

    @telemetry
    def save_estimator(
            self,
            file,
            as_json: bool = False,
            return_filepaths: bool = False,
            n_jobs: Optional[int] = None,
            **estimator_params,
    ):
        check_feature_for_license("estimation")
        if "return_preprocessing" in estimator_params:
            estimator_params.pop("return_preprocessing")
        estimator_params["tree_idx"] = estimator_params.get("tree_idx", 0)
        self.__last_saved_estimator_tree_idx = estimator_params["tree_idx"]
        est, preprocessing = self.get_estimator(return_preprocessing=True, n_jobs=n_jobs, **estimator_params)
        # This creates the directory if necessary
        print("Saving estimator and preprocessing parameters...")
        _, est_file = est.save(file, as_json=as_json, return_filepath=True)
        preprocessing_file = Path(f"{file}_preprocessing").with_suffix(".json")
        with open(preprocessing_file, "w") as f:
            json.dump(preprocessing, f)
        print("Saved")
        if return_filepaths:
            return est, preprocessing, est_file, preprocessing_file
        else:
            return est, preprocessing
        # return est, preprocessing, est_file, preprocessing_file if return_filepaths else est, preprocessing

    @telemetry
    def load_estimator(self, file, preprocessing_file, tree_idx: int = None) -> Tuple[SensitivityEstimatorBase, Dict]:
        check_feature_for_license("estimation")
        tree_idx = tree_idx if tree_idx is not None else self.__last_saved_estimator_tree_idx
        est = self._get_estimator_cls(tree_idx).load(file)
        with open(preprocessing_file, "r") as f:
            preprocessing = json.load(f)
        for k in list(preprocessing["missing_values"]["features"].keys()):
            preprocessing["missing_values"]["features"][int(k)] = preprocessing["missing_values"]["features"].pop(k)
        for k in list(preprocessing["ohe_used_categories"]["order"].keys()):
            preprocessing["ohe_used_categories"]["order"][int(k)] = preprocessing["ohe_used_categories"]["order"].pop(k)
        for k in list(preprocessing["te_used_categories"]["order"].keys()):
            preprocessing["te_used_categories"]["order"][int(k)] = preprocessing["te_used_categories"]["order"].pop(k)
        return est, preprocessing
