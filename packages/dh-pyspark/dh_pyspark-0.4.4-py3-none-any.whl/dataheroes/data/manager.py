import abc
import functools
import io
import itertools
import os
import re
from collections import defaultdict
# from sklearn.utils import check_array
from typing import TypeVar, Union, Iterable, List, Any, Tuple, Iterator, Callable, Optional, Dict

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from dataheroes.data.storage.storage_manager import StorageManager
import zipfile

from . import helpers
from .common import (
    DMSchema, DataParams, FeatureField, IndexField, TargetField, Column, DefaultIndexField, UUIDIndexField,
    SeqIndexField, Dataset, PropertyField
)
from .data_auto_processor import (
    CAT_T,
    _find_categorical_types,
    _detect_types_numpy,
    _categorical_features_encoding_split
)
from .helpers import _get_inf_nan_indexes, is_unsupported_hdf5_array, get_feature_slice
from .utils import _compose_missing_params, _update_col_indexes
from ..configuration import DataHeroesConfiguration
from ..core.numpy_extra import filter_missing_and_inf, unique
from ..services.common import CategoricalEncoding, PreprocessingParams, CATEGORICAL_INFREQUENT
from ..utils import user_warning, check_feature_for_license

DMSchemaT = TypeVar('DMSchemaT', bound=DMSchema)
DataManagerT = TypeVar('DataManagerT', bound='DataManagerBase')

MIN_DATA_CELLS_FOR_PARALLEL_BUILD = 10_000_000


def get_min_data_cells_for_parallel_build():
    return MIN_DATA_CELLS_FOR_PARALLEL_BUILD


def _is_datetime(data):
    if 'datetime' in str(data.dtype):
        return True
    try:
        data.astype(np.float64)
    except TypeError:  # it's datetime or timestamp
        return True
    except ValueError:  # string
        pass
    return False


class DataManagerBase:
    """
    Data manager base class

    Parameters
    ----------
    schema: DMSchemaT
        a nested dictionary like structure of manager params.

    working_directory: path like, optional
    """

    schema_cls = DMSchema
    data_params_cls = DataParams
    default_index_column_cls = DefaultIndexField
    support_save = True

    def __init__(self, schema: DMSchemaT = None, working_directory: Union[str, os.PathLike] = None):
        self.storage_manager = StorageManager()
        self.schema = schema or self.schema_cls(working_directory=working_directory)
        self.working_directory = working_directory
        self.default_index_column_cls = self.get_default_index_column()
        self.n_jobs = None
        self.verbose = 1
        # Internal attrs
        self._n_features_expected = None

    @property
    def data_params(self):
        return self.schema.data_params

    @property
    def data_params_internal(self):
        return self.schema.data_params_internal

    @data_params_internal.setter
    def data_params_internal(self, value):
        self._data_params_internal = value

    @data_params.setter
    def data_params(self, v):
        self.schema.data_params = v

    @property
    def dataset_schema(self):
        return self.schema.dataset_schema

    @dataset_schema.setter
    def dataset_schema(self, v):
        self.schema.dataset_schema = v

    @property
    def index_col(self):
        return self.dataset_schema.index_col.name

    @index_col.setter
    def index_col(self, value):
        self.dataset_schema.index_col = value

    @property
    def features_cols(self):
        return [c.name for c in self.dataset_schema.features_cols]

    @property
    def properties_cols(self):
        if self.dataset_schema.properties_cols is None:
            return None
        return [c.name for c in self.dataset_schema.properties_cols]

    @property
    def n_features(self):
        return len(self.features_cols)

    @property
    def n_features_expected(self) -> int:
        # returns the expected features from a first batch of data
        if self._n_features_expected is None:
            return self.n_features
        return self._n_features_expected

    @property
    def n_classes(self):
        return self.data_params.n_classes

    @property
    def n_instances(self):
        return self.data_params.n_instances

    @property
    def target_col(self):
        return self.dataset_schema.target_col.name if self.dataset_schema.target_col else None

    @property
    def save_orig(self):
        return self.data_params.save_orig

    @property
    def infrequent_encoding(self):
        if self.data_params_internal.used_categories_ is None or len(self.data_params_internal.used_categories_) == 0:
            return None
        return (
            max(
                [len(self.data_params_internal.used_categories_[c]) for c in self.data_params_internal.used_categories_]
            )
            * 2
        )

    def set_working_directory(self, working_directory: Union[str, os.PathLike]):
        self.working_directory = str(working_directory) if working_directory else working_directory

    def get_default_index_column(self):
        s = DataHeroesConfiguration().get_param_str('default_index_column')
        if not s:
            return self.default_index_column_cls
        elif s == 'uuid':
            return UUIDIndexField
        elif s == 'sequence':
            return SeqIndexField
        else:
            raise RuntimeError(f"Unable to resolve default_index_column: {s}")

    def read_file(
            self,
            file_path: Union[Union[str, os.PathLike], Iterable[Union[str, os.PathLike]]],
            *,
            reader_f=pd.read_csv,
            reader_kwargs: dict = None,
            sort_by_name: bool = False,
            local_copy_dir: str = None,
    ) -> Iterator[pd.DataFrame]:
        """
        create a coreset tree based on the data taken from an input file.

        Parameters
        ----------

        file_path: file/directory or an iterator of file/directory
                path to a file/directory stored locally or on the cloud (AWS S3, Google Cloud Platform Storage, Azure Storage)

        reader_f: pandas like read method or None. Default pandas read_csv
                Use this parameter for example excel files.

        reader_kwargs: dict or None
                arguments to be passed to the reader function.

        sort_by_name: bool, optional, default false
                when true, read files in a directory ordered by name

        local_copy_dir: str, optional, dafault None
                when provided, the file is copied to this directory.
                can be used if the file is stored on the cloud and a local copy is desired.
        """
        paths = helpers.file_path_to_iterable(file_path)
        reader_kwargs = reader_kwargs or dict()
        reader_f = functools.partial(reader_f, **reader_kwargs)

        def _to_files(p):
            return helpers.file_path_to_files(p, self.storage_manager, sort_by_name=sort_by_name)

        def _read_bytes(p):
            return self.storage_manager.read_bytes(p, local_copy_dir)

        def _read_file(b):
            try:
                data = reader_f(b)
                return helpers.df_to_iterable(data)
            except:
                b.seek(0)
                return _read_file_compressed(b)

        def _read_file_compressed(b):
            # read_csv can't infer the compression type from BytesIO object
            # so it needs to be specified in the method call
            compression_types = ['infer', 'zip', 'gzip', 'tar', 'bz2', 'zstd', 'xz']
            for compression in compression_types:
                try:
                    data = reader_f(b, compression=compression)
                    return helpers.df_to_iterable(data)
                except Exception:
                    b.seek(0)
                    continue
            raise UnicodeDecodeError("Unable to decode file.")


        files = itertools.chain.from_iterable(map(_to_files, paths))
        files = map(_read_bytes, files)
        datasets = itertools.chain.from_iterable(map(_read_file, files))
        return datasets

    def read_data(self, chunk_size) -> Iterable:
        return self._read_data(chunk_size)

    def get_file_n_columns(self, file_path, reader_f, reader_kwargs, reader_chunk_size_kw):
        """
        Return the number of columns in an input file.
        Read first rows to a padnas DataFrame and return the number of columns.

        Parameters
        ----------
        file_path
        reader_f
        reader_kwargs
        reader_chunk_size_kw

        Returns
        -------
        int: number of columns

        """
        reader_kwargs = reader_kwargs.copy()
        reader_chunk_size_kw = reader_chunk_size_kw or helpers.resolve_reader_chunk_size_param_name(reader_f)
        if reader_chunk_size_kw:
            reader_kwargs[reader_chunk_size_kw] = 10
        df = next(self.read_file(
            file_path,
            reader_f=reader_f,
            reader_kwargs=reader_kwargs
        ))
        return df.shape[1]

    def init_and_preprocess(
            self,
            datasets: Iterator[Union[pd.DataFrame, Tuple[pd.DataFrame, ...]]],
            chunk_by: Union[Callable, str, list] = None,
            **kwargs
    ):
        """
        Initialize preprocessing data params and database schema from a pandas DataFrame iterator.
        Preprocess datasets

        Parameters
        ----------
        datasets: pandas DataFrame iterator or an iterator of tuples
            each element can be either a single data frame or a tuple with target in a different data frame.
        chunk_by:
            key: function, column, list of columns, optional

        Returns
        -------
        processes dataset iterator

        """
        data_params = self.data_params
        self.data_params.transform_context = {}
        data_params.features = list(data_params.features) if data_params.features is not None else []

        # transform preliminary data
        datasets = map(self._run_transform_before, datasets)

        # define the schema for storing original data
        df, datasets = self._iter_first(datasets)
        df, target_df = helpers.to_df_target(df)
        columns = [Column(c, dtype=t) for c, t in zip(df.columns, df.dtypes)]
        if target_df is not None:
            columns += [Column(f'target_{c}', dtype=t) for c, t in zip(target_df.columns, target_df.dtypes)]
        self.schema.data_schema.columns = columns

        # figure out data params features, target, sample_weight, index
        index_column = data_params.index.name if data_params.index else None
        sample_w_column = data_params.sample_weight.name if data_params.sample_weight else None
        y_column = data_params.target.name if data_params.target else None

        # set target when target_datasets is provided
        if target_df is not None:
            if y_column is None:
                data_params.target = TargetField(target_df.columns.to_list()[0])
            y_column = None  # don't consider when extracting features

        # extract features
        if not data_params.features or data_params.columns_to_features:
            column_names_to_ignore = [feature.name for feature in data_params.features] + [index_column, y_column, sample_w_column]
            if data_params.properties:
                column_names_to_ignore += [prop.name for prop in data_params.properties]
            column_names_to_ignore = [c for c in column_names_to_ignore if c is not None]
            columns = df.columns.to_list()
            if isinstance(data_params.columns_to_features, dict):
                exclude = data_params.columns_to_features.get('exclude')
                include = data_params.columns_to_features.get('include')
                if exclude:
                    column_names_to_ignore += [c for c in df.columns.to_list() if
                                               any(re.fullmatch(p, c) for p in exclude)]
                if include:
                    columns = [c for c in columns if any(re.fullmatch(p, c) for p in include)]
            data_params.features += [FeatureField(name=c) for c in columns if c not in column_names_to_ignore]
        if not index_column:
            data_params.index = self.default_index_column_cls()

        data_params = self._handle_datetime_columns(data_params, df=df)

        # data transformation may change the type of a column, for example converting string to number
        # apply preprocess and set dtypes if not defined
        datasets = self.preprocess(datasets, chunk_by=chunk_by, run_before=False, init_run=True)
        dataset, datasets = self._iter_first(datasets)
        indices, X, y, sample_weight, props = dataset.ind, dataset.X, dataset.y, dataset.sample_weight, dataset.props
        ind_dtype, x_dtypes, y_dtype, sample_weight_dtype, props_dtypes, _ = self._resolve_dataset_types(indices, X, y, sample_weight, props)
        if data_params.index.dtype is None:
            data_params.index.set_dtype(ind_dtype)
        if data_params.target and data_params.target.dtype is None:
            data_params.target.set_dtype(y_dtype)
        for c, t in zip(data_params.features, x_dtypes):
            if c.dtype is None:
                c.set_dtype(t)
        if data_params.sample_weight and data_params.sample_weight.dtype is None:
            data_params.sample_weight.set_dtype(sample_weight_dtype)
        if data_params.properties:
            for c, t in zip(data_params.properties, props_dtypes):
                if c.dtype is None:
                    c.set_dtype(t)

        if data_params.n_classes is None and y is not None and data_params.is_classification:
            data_params.n_classes = len(pd.unique(filter_missing_and_inf(y)))

        self.data_params = data_params
        self._init_dataset_schema()
        self._prepare_schema()
        self.data_params_internal.aggregated_missing_replacements = _compose_missing_params(data_params,
                                                                                            self.data_params_internal)
        return datasets

    def _calc_array_features(self, data_params):
        return self.calc_features_indexes(data_params,
                                          data_params.array_features,
                                          lambda x: x.array)

    def _calc_categorical_features(self, X, data_params, init_run=False):

        categorical_features = self.calc_features_indexes(data_params,
                                                          data_params.categorical_features,
                                                          lambda x: x.categorical)

        # add auto-categories
        if data_params.detect_categorical and len(X) > 0:
            if type(X) == pd.DataFrame:
                categorical_features = sorted(set(categorical_features +
                                                  [i for i, f in enumerate(X.columns.values)
                                                   if not (is_numeric_dtype(X[f].dtype) or X[f].dtype == bool)
                                                   and i not in (
                                                       self.data_params_internal.array_features_
                                                       if self.data_params_internal.array_features_ else [])]))
            else:
                X_processed = X
                if self.data_params_internal.calculated_props_ and init_run:
                    # exclude calculated properties from categorical features
                    X_processed = np.delete(X, self.data_params_internal.calculated_props_, axis=1)
                feature_types = _find_categorical_types(
                    X_processed,
                    feature_names=None,
                    feature_types=_detect_types_numpy(X_processed),
                    categorical_features=None,
                    categorical_threshold=None
                )
                categorical_features = sorted(set(categorical_features +
                                                  [i for i, f in enumerate(feature_types) if f == CAT_T
                                                   and i not in (self.data_params_internal.array_features_
                                                   if self.data_params_internal.array_features_ else [])]))

        return categorical_features

    def calc_features_indexes(self, data_params, typed_features, feature_type_filter):
        # transform them to indexes if they're provided as strings
        if self.data_params_internal.calculated_props_ and typed_features:
            original_features = [i for i, f in enumerate(data_params.features) if f.name in
                                 typed_features or i in typed_features]

            new_features = _update_col_indexes(original_features, self.data_params_internal.calculated_props_)
        else:
            new_features = typed_features
        # fill categorical_features_ with indexes of categorical features
        typed_features_indexes = [i for i, f in enumerate(data_params.features) if feature_type_filter(f)]
        # add categories from categorical_features (indexes)
        if new_features \
                and len(new_features) > 0 \
                and type(new_features[0]) == int:
            typed_features_indexes = (sorted(set(typed_features_indexes + new_features)) or [])
        # add categories from categorical_features (feature names)
        if new_features and len(new_features) > 0:
            feature_indexes = [i for i, f in enumerate(data_params.features) if f.name in
                               new_features]
            typed_features_indexes = sorted(set(typed_features_indexes + feature_indexes))
        return typed_features_indexes

    def _calc_seq_column_index(self):
        """
        Compute index of seq column, first checking if it exists
        """

        def set_params_internal():
            self.data_params_internal.seq_granularity_ = self.data_params.seq_column.get('granularity')
            self.data_params_internal.seq_datetime_format = self.data_params.seq_column.get('datetime_format')
            self.data_params_internal.seq_chunk_by = self.data_params.seq_column.get('chunk_by')

        if self.data_params.seq_column is None:
            self.data_params_internal.seq_column_ = None
            return

        check_feature_for_license('sequence_features')

        if self.data_params.seq_column.get('chunk_by') == 'every_build':
            self.data_params_internal.seq_column_ = 'every_build'
            set_params_internal()
            return

        name = self.data_params.seq_column.get('name')
        index = None
        if name:
            for i, location in enumerate([self.data_params.features, self.data_params.properties]):
                if location is not None:
                    index = [i for i, f in enumerate(location) if f.name == name]
                    if index:
                        index = index[0]
                        break
        else:
            index = self.data_params.seq_column.get('id')
            if index is None:
                index = self.data_params.seq_column.get('prop_id')
            i = 0 if 'id' in self.data_params.seq_column else 1
            # Adjust index if seq_col is in features and we moved some features to properties:
            index = _update_col_indexes([index], self.data_params_internal.calculated_props_)[0] \
                if i == 0 else index
        if index is not None and index != []:
            self.data_params_internal.seq_column_ = index
            self.data_params_internal.seq_column_location_ = 'features' if i == 0 else 'properties'
            set_params_internal()

            return
        raise ValueError(f"`seq_column` {self.data_params.seq_column} not found in dataset")

    def init_from_dataset(self, indices: Optional[np.ndarray], X: np.ndarray, y: np.ndarray = None,
                          props: np.ndarray = None) -> DataManagerT:
        """
        Initialize preprocessing data params and database schema

        Parameters
        ----------
        indices: a numpy ndarray, required
        X: features 2d ndarray, required
        y: target, numpy ndarray. optional

        Returns
        -------
        self

        """

        ind_dtype, x_dtypes, y_dtype, _, props_dtype, x_schema_dtypes = self._resolve_dataset_types(indices, X, y, None,
                                                                                                    props)
        features = [FeatureField(f'f{i}', dtype=t) for i, t in enumerate(x_dtypes)]

        data_params = self.data_params
        data_params.features = data_params.features or features
        data_params.target = TargetField('y', dtype=y_dtype) if y is not None else None
        data_params.index = IndexField(
            'index_column',
            dtype=ind_dtype) if indices is not None else self.default_index_column_cls('index_column')

        if data_params.n_classes is None and y is not None and data_params.is_classification:
            # count unique without nan and inf
            data_params.n_classes = len(pd.unique(filter_missing_and_inf(y)))

        data_params = self._handle_datetime_columns(data_params, X=X)

        self.data_params.transform_context = {}
        self._init_dataset_schema(x_schema_dtypes)
        self._prepare_schema()
        self.data_params_internal.array_features_ = self._calc_array_features(data_params)
        self.data_params_internal.categorical_features_ = self._calc_categorical_features(X, data_params, init_run=True)
        self.data_params_internal.aggregated_missing_replacements = _compose_missing_params(data_params,
                                                                                            self.data_params_internal)
        return self

    def preprocess(
            self,
            datasets: Iterator[Union[pd.DataFrame, Tuple[pd.DataFrame]]],
            *,
            chunk_by: Union[Callable, str, list] = None,
            run_before=True,
            init_run=False,
            n_jobs: int = None,
    ):
        """
        Preprocess raw data to an indices, features, target datasets.

        Parameters
        ----------
        datasets: iterator of pandas like datasets or an iterator of a tuples

        chunk_by:
            key: function, column, list of columns, optional

        run_before: boolean, default True
            Should data_transform_before, if defined, be applied.

        n_jobs: Default: number of CPUs. Number of jobs to run in parallel during build.

        Returns
        -------
        Iterator of processed dataset

        """

        def _append_ind(df):
            df = list(helpers.df_to_iterable(df))
            indices = self._extract_indices(df, only_if_not_defined=True)
            indices = pd.DataFrame(indices) if indices is not None else indices
            return df + [indices]

        def _process(dataset):
            indices = None
            if chunk_by and chunk_by != 'every_build':
                dataset, indices = (dataset[:-1], dataset[-1])
                indices = indices.to_numpy().flatten() if indices is not None else None
            dataset, target_dataset = helpers.to_df_target(dataset)
            processed = self.preprocess_df(dataset, target_dataset, indices, run_before=False, init_run=init_run)
            orig = dataset.to_numpy() if self.save_orig else None
            orig_target = target_dataset.to_numpy() if self.save_orig and target_dataset is not None else None
            return processed._replace(orig=orig, orig_target=orig_target)

        # flow
        if run_before:
            datasets = map(self._run_transform_before, datasets)
        # chunk_by can be True, False or "every_build", we only split the data if the value is True
        if chunk_by and chunk_by != 'every_build':
            datasets = self.split_datasets(map(_append_ind, datasets), chunk_by)

        for dset in datasets:
            yield _process(dset)
            init_run = False

    @staticmethod
    def _check_columns_exists_df(*, data_params: DataParams, df, target_df, indices) -> None:
        """
        Raise an exception if any of data fields in data_params not exist in the input data frame.
        Consider only data field not having transform.
        """
        missing_columns = []

        def _check(df_to_check, columns):
            cols_to_check = df_to_check.columns.to_list()
            missing_columns.extend([col.name for col in columns if not (col.transform or col.name in cols_to_check)])

        if data_params.features:
            _check(df, data_params.features)
        if indices is None and data_params.index:
            _check(df, [data_params.index])
        if data_params.target:
            target_df = target_df if target_df is not None else df
            _check(target_df, [data_params.target])
        if data_params.properties:
            _check(df, data_params.properties)
        if data_params.sample_weight:
            _check(df, [data_params.sample_weight])

        if missing_columns:
            raise ValueError(f"Cannot find columns {missing_columns}")

    def gen_indices(self, arr, data_params=None):
        data_params = data_params or self.data_params
        transform_context = data_params.transform_context
        transform_context['feature_name'] = data_params.index.name
        indices = data_params.index.transform.run_transform(arr, transform_context)
        return indices

    def preprocess_dataset(self, dataset):
        """
        Preprocess and transform raw data if the indices are not given

        Parameters
        ----------
        dataset: iterator or iterator of iterators or iterator of pandas like dataset

        Returns
        -------
        indices, X, y, w, props

        """
        ds = Dataset(*dataset)
        # move datetime features to properties
        calculated_props = self.data_params_internal.calculated_props_
        X = np.delete(ds.X, calculated_props, axis=1) if calculated_props is not None else ds.X
        existing_props = ds.props if ds.props is not None else None
        props = np.concatenate((existing_props, X[:, calculated_props]), axis=1) if (calculated_props is not
                                                                                     None) else existing_props
        self._check_feature_types(X)
        self._calc_seq_column_index()
        # We won't encode y at this point, we will use it as is, encoding if needed is done in _save_selected_samples
        # at HDF5 level. What we need to do is to set y_mixed_types to True if y is object.
        if ds.y is not None:
            y_mixed_types = is_unsupported_hdf5_array(ds.y)
            if y_mixed_types:
                self.data_params_internal.y_mixed_types = True
        # Check for missing values in seq_column
        self._check_missing_values_seq_col(ds, target_type='ds')
        if len(self.data_params_internal.categorical_features_) > 0:
            # if there are non-numeric categorical features, convert data to df for encoding could be beneficial
            df = self._encode_categorical_data(pd.DataFrame(X))
            # check if any datetime columns exist at this point (we should have none here)
            if not self.data_params.datetime_to_properties:
                col_names = [f.name for f in self.data_params.features]
                for dtype, col_name in zip(df.dtypes, col_names):
                    if 'datetime' in str(dtype):
                        raise ValueError(f"Feature '{col_name}' is datetime and can't be processed. Please set "
                                         f"`data_params.datetime_to_properties = True` to automatically turn it into a "
                                         f"property or preprocess the feature to a String or a numeric feature.")

            df = self._preprocess_bool_df(df)
            if self.data_params_internal.array_features_ is not None and len(
                    list(self.data_params_internal.array_features_)) > 0:
                convert_dict = {c: float for c in df.columns if c not in self.data_params_internal.array_features_}
                df = df.astype(convert_dict)
            else:
                df = df.astype(float)
            X = df.to_numpy()
            ds = Dataset(ind=ds.ind, X=X, y=ds.y, sample_weight=ds.sample_weight, props=props)
        else:
            X = self._encode_categorical_data(X)
            ds = Dataset(ind=ds.ind, X=X, y=ds.y, sample_weight=ds.sample_weight, props=props)
            ds = self._preprocess_bool(ds)

        if ds.ind is None:
            ds = ds._replace(ind=self.gen_indices(X))
        y_missing = _get_inf_nan_indexes(ds.y) if ds.y is not None else False
        ds = self._check_dataset(ds, self.data_params.detect_missing, y_missing, self.has_array_features())
        return ds

    def preprocess_df(self, df, target_df=None, indices=None, *, run_before: bool = True, init_run: bool = False) -> \
            Union[Tuple, Dataset]:
        """
        Preprocess row dataset to an indices, features, target set.

        Parameters
        ----------
        df: pandas like data frame, required
        target_df: pandas like data frame, optional

        run_before: boolean, default True
            Should data_transform_before, if defined, be applied.

        Returns
        -------
        indices, X, y, sample_weight, props
        """

        data_params = self.data_params
        data_params_internal = self.data_params_internal
        self.data_params.transform_context = self.data_params.transform_context or {}
        transform_context = self.data_params.transform_context
        df = self._run_transform_before(df) if run_before else df

        # Verify all required columns exists in the relevant data frames
        self._check_columns_exists_df(data_params=data_params, df=df, target_df=target_df, indices=indices)

        def get_sub_dataset(data_frame, fields, field_transform_default, fields_transform_after, calc_typed_features,
                            cat_encoding, do_feature_check=True, do_seq_col_check=True):
            # get names of all features to be retained in X
            features_to_keep = [feature.name for feature in fields]
            # performance, when possible, avoid copy by checking if all features are in a single range.
            features_idx_to_select = [i for i, c in enumerate(data_frame.columns.to_list()) if c in features_to_keep]
            ranges = helpers.to_ranges(features_idx_to_select)
            if len(ranges) == 1:
                result_dataset = data_frame.iloc[:, ranges[0][0]:ranges[0][1] + 1]
            else:
                # determine name of all features to be dropped from data_frame (by set difference)
                # drop the features to be dropped
                features_to_drop = list(set(data_frame.columns.to_list()) - set(features_to_keep))
                result_dataset = data_frame.drop(features_to_drop, axis=1)
            # apply feature transformations
            for feature in fields:
                transform = feature.transform or field_transform_default
                if transform is not None:
                    transform_context['feature_name'] = feature.name
                    result_dataset[feature.name] = transform.run_transform(data_frame, transform_context)
            # make sure the required order of features is preserved
            if result_dataset.columns.to_list() != features_to_keep:
                result_dataset = result_dataset[features_to_keep]
            if fields_transform_after:
                result_dataset = fields_transform_after.run_transform(result_dataset, transform_context)
            if calc_typed_features:
                data_params_internal.array_features_ = self._calc_array_features(data_params)

                data_params_internal.categorical_features_ = self._calc_categorical_features(result_dataset,
                                                                                             data_params)
                self.data_params = data_params
            if do_seq_col_check:
                self._calc_seq_column_index()
                # Check for missing values in seq_column
                if not self.data_params_internal.seq_every_build:
                    self._check_missing_values_seq_col(df, target_type='df')
            if do_feature_check:
                self._check_feature_types(result_dataset.to_numpy())
            if cat_encoding:
                result_dataset = self._encode_categorical_data(result_dataset)
                result_dataset = self._preprocess_bool_df(result_dataset)
                try:
                    df_is_numeric = all([t in [float, int] for t in result_dataset.dtypes])
                    if not df_is_numeric:
                        if not self.has_array_features():
                            result_dataset = result_dataset.apply(pd.to_numeric)
                    result_dataset = result_dataset.to_numpy()
                except ValueError as e:
                    raise ValueError(f"All features must be numeric: {e}")
            else:
                # props
                result_dataset = result_dataset.to_numpy()
            return result_dataset

        X = get_sub_dataset(data_frame=df,
                            fields=data_params.features,
                            field_transform_default=data_params.feature_transform_default if data_params else None,
                            fields_transform_after=data_params.data_transform_after,
                            calc_typed_features=init_run,
                            cat_encoding=True
                            )

        props = None
        if data_params.properties:
            props = get_sub_dataset(data_frame=df,
                                    fields=data_params.properties,
                                    field_transform_default=None,
                                    fields_transform_after=None,
                                    calc_typed_features=False,
                                    cat_encoding=False,
                                    do_feature_check=False,
                                    do_seq_col_check=False,
                                    )

        target_df = df if target_df is None else target_df
        if data_params.target and data_params.target.transform:
            transform_context['feature_name'] = data_params.target.name
            y = data_params.target.transform.run_transform(target_df, transform_context).to_numpy()
        elif data_params.target:
            y = target_df[data_params.target.name].to_numpy()
        else:
            y = None

        sample_weight = None
        if data_params.sample_weight:
            sample_weight = df[data_params.sample_weight.name].to_numpy()

        # We won't encode y at this point, we will use it as is, encoding if needed is done in _save_selected_samples
        # at HDF5 level. What we need to do is to set y_mixed_types to True if y is object.
        if y is not None:
            y_mixed_types = is_unsupported_hdf5_array(y)
            if y_mixed_types:
                self.data_params_internal.y_mixed_types = True

        if indices is None:
            indices = self._extract_indices(df, data_params=data_params)

        transform_context.pop('feature_name', None)

        dataset = Dataset(ind=indices, X=X, y=y, sample_weight=sample_weight, props=props)
        y_missing = _get_inf_nan_indexes(y) if y is not None else False
        dataset = self._check_dataset(dataset, self.data_params.detect_missing, y_missing, self.has_array_features())
        return dataset

    def _preprocess_bool(self, dataset):
        if dataset.X.shape and dataset.X.shape[1] > 0 and dataset.X.shape[0] > 0:
            for col_idx in range(dataset.X.shape[1]):
                if type(dataset.X[:, col_idx][0]) == bool:
                    if self.data_params_internal.bool_features_ is None:
                        self.data_params_internal.bool_features_ = []
                    self.data_params_internal.bool_features_.append(col_idx)
                    dataset.X[:, col_idx] = dataset.X[:, col_idx].astype(float)
        return dataset

    def _preprocess_bool_df(self, df):
        if df.shape and df.shape[1] > 0 and df.shape[0] > 0:
            for col_idx, col_name in enumerate(df.columns.values):
                if helpers.to_dtype(df[col_name].dtype) == np.dtype(bool):
                    if self.data_params_internal.bool_features_ is None:
                        self.data_params_internal.bool_features_ = []
                    self.data_params_internal.bool_features_.append(col_idx)
                    df[col_name] = df[col_name].astype(float)

        return df

    def set_cat_encoding_method(self, is_supervised: bool):
        """
        Use this method to automatically set the category-encoding method in case it was undefined, or to validate a
        user-provided method before setting it.
        """

        # If there was a custom user definition which we don't support, reset the method to default configuration.
        if self.data_params.cat_encoding_method is not None and self.data_params.cat_encoding_method not in (
                CategoricalEncoding.OHE, CategoricalEncoding.TE, CategoricalEncoding.MIXED):
            if self.data_params.cat_encoding_method == CategoricalEncoding.NOTHING:
                return
            user_warning(f"Categorical encoding method '{self.data_params.cat_encoding_method}' unsupported - "
                         f"resorting to the default resolution method.")
            self.data_params.cat_encoding_method = None

        # For unsupervised learning or for regression, we use OHE regardless of the value provided in data_params.
        if not is_supervised or not self.data_params.is_classification:
            if self.data_params.cat_encoding_method is not None \
                    and self.data_params.cat_encoding_method in (CategoricalEncoding.TE, CategoricalEncoding.MIXED):
                user_warning(f"Categorical encoding method '{self.data_params.cat_encoding_method}' supported only "
                             f"for binary classification - defaulting to '{CategoricalEncoding.OHE}'")
            self.data_params.cat_encoding_method = CategoricalEncoding.OHE
            return

        if self.data_params.n_classes is None:
            user_warning(f"n_classes is None while expected to have a value, defaulting to the "
                         f"'{CategoricalEncoding.OHE}' encoding.")
            self.data_params.cat_encoding_method = CategoricalEncoding.OHE
            return

        if self.data_params.n_classes <= 0:
            user_warning(f"Unexpected value n_classes={self.data_params.n_classes}, defaulting to the "
                         f"'{CategoricalEncoding.OHE}' encoding.")
            self.data_params.cat_encoding_method = CategoricalEncoding.OHE
            return

        is_binary_classification = self.data_params.n_classes == 2

        # Default (encoding method is not provided)
        if self.data_params.cat_encoding_method is None:
            if is_binary_classification:
                self.data_params.cat_encoding_method = CategoricalEncoding.MIXED
            else:
                self.data_params.cat_encoding_method = CategoricalEncoding.OHE
            return

        # User requested own setting of TE/MIXED encoding for unsupported multiclass classification.
        if not is_binary_classification and self.data_params.cat_encoding_method in (CategoricalEncoding.TE,
                                                                                     CategoricalEncoding.MIXED):
            user_warning(f"Categorical encoding method '{self.data_params.cat_encoding_method}' supported only "
                         f"for binary classification - defaulting to '{CategoricalEncoding.OHE}'")
            self.data_params.cat_encoding_method = CategoricalEncoding.OHE

    def _encode_categorical_data(self, X):
        # Make sure to also encode missing replacement values (if any)
        missing_replacements = self.data_params_internal.aggregated_missing_replacements

        def map_to_index_func(x):
            return string_to_index.get(str(x), np.nan)

        is_df = type(X) == pd.DataFrame
        if X is None:
            return X
        if self.data_params_internal.categorical_features_:
            # loop through categorical
            for feature_index in [i for i in self.data_params_internal.categorical_features_]:
                # update lists of used values for each categorical feature
                if is_df:
                    self._update_used_categories(feature_index, X.iloc[:, feature_index], missing_replacements)
                else:
                    self._update_used_categories(feature_index, X[:, feature_index], missing_replacements)
                # used values for current feature
                string_to_index = self.data_params_internal.used_categories_[str(feature_index)]
                # replace all data values with indexes
                if is_df:
                    data_encoded = np.array(list(map(map_to_index_func, X.iloc[:, feature_index].values)))
                    # As per pandas v2.1.0 silent upcasting for setitem-like operations is deprecated (see issue #1163)
                    #   consequently, it is replaced with the isetitem(). The isetitem() operation is introduced in
                    #   pandas v1.5.0 (see https://pandas.pydata.org/docs/whatsnew/v1.5.0.html#inplace-operation-when-setting-values-with-loc-and-iloc)
                    if pd.__version__ < "1.5.0":
                        X.iloc[:, feature_index] = data_encoded
                    else:
                        X.isetitem(feature_index, data_encoded)
                else:
                    data_encoded = np.array(list(map(map_to_index_func, X[:, feature_index])))
                    X[:, feature_index] = data_encoded
        return X

    def _encode_categorical_y(self, y):
        if self.data_params_internal.y_mixed_types:
            # update lists of used values for y
            self._update_used_categories("y", y, None)
            # used values for y
            string_to_index = self.data_params_internal.used_categories_['y']
            # replace all data values with indexes
            data_encoded = np.array(list(map(lambda x: string_to_index[x], y)))
            y = data_encoded
            # update target type
            self.data_params.target.set_dtype(int)
        return y

    def _update_used_categories(self, cat_feature_idx, values, missing_replacements):
        # cat_feature_idx is index of categorical feature
        # we store them as strings
        if not self.data_params_internal.used_categories_:
            self.data_params_internal.used_categories_ = {}
        cat_feature_idx_str = str(cat_feature_idx)
        values_unique = pd.unique(filter_missing_and_inf(values))
        # if reference for index cat_feature_idx not exists - create it
        if cat_feature_idx_str not in self.data_params_internal.used_categories_:
            used_cat_values = {
                str(np.nan): np.nan,
                str(float('inf')): float('inf'),
                str(float('-inf')): float('-inf'),
            }
            # Add replacement missing value to used values (if it exists) at the beginning of the list
            if missing_replacements is not None:
                replacement = missing_replacements[cat_feature_idx]
                if replacement is not None:
                    used_cat_values[str(replacement)] = 0
                    # used_cat_values[replacement] = 0
                    values_unique = values_unique[~np.isin(values_unique, replacement)]
            used_cat_values.update({str(val): i + 1 for i, val in enumerate(values_unique)})
            self.data_params_internal.used_categories_[cat_feature_idx_str] = used_cat_values
            return

        # # if reference for index cat_feature_idx exists - add new values to its end (to preserve old value indexes)
        # have_nan_in_used_categories = np.any(np.isnan(self.data_params_internal.used_categories_[cat_feature_idx_str]))
        # if have_nan_in_used_categories and np.any(np.isnan(values_unique)):
        #     # remove nan if already have them
        #     values_unique = values_unique[~np.isnan(values_unique)]

        new_values = list(
            set([str(x) for x in values_unique]).difference(
                set(self.data_params_internal.used_categories_[cat_feature_idx_str].keys())))
        if len(new_values) > 0:
            starting_no = len(self.data_params_internal.used_categories_[cat_feature_idx_str]) + 1
            new_dict = {str(val): i + starting_no for i, val in enumerate(new_values)}
            self.data_params_internal.used_categories_[cat_feature_idx_str].update(new_dict)

    def has_categorical_features(self) -> bool:
        return self.data_params_internal.categorical_features_ is not None \
            and len(self.data_params_internal.categorical_features_) > 0

    def has_array_features(self) -> bool:
        return self.data_params_internal.array_features_ is not None \
            and len(self.data_params_internal.array_features_) > 0

    def array_encoding_config(self, preprocessing_params: PreprocessingParams = None) -> dict:
        array_encoding_conf = {'max_categories': self.data_params.array_max_categories,
                               'min_frequency': self.data_params.array_min_frequency
                               }
        if preprocessing_params is not None:
            array_encoding_conf['feature_classes'] = preprocessing_params.ae_feature_classes
        return array_encoding_conf

    def cat_encoding_config_clear(self) -> dict:
        cat_encoding_config = {
            CategoricalEncoding.ENCODING_METHOD_KEY: self.data_params.cat_encoding_method,
            CategoricalEncoding.OHE: {
                "max_categories": self.data_params.ohe_max_categories,
                "min_frequency": self.data_params.ohe_min_frequency,
            },
            CategoricalEncoding.TE: {
                "cv": self.data_params.te_cv,
                "random_state": self.data_params.te_random_state,
            },
            CategoricalEncoding.MIXED: {
                "favor_ohe_num_cats_thresh": self.data_params.favor_ohe_num_cats_thresh,
                "favor_ohe_vol_pct_thresh": self.data_params.favor_ohe_vol_pct_thresh,
            },
        }
        return cat_encoding_config

    def cat_encoding_config_with_categories(self, preprocessing_params: PreprocessingParams,
                                            ohe_categories, te_categories) -> dict:
        cat_encoding_config = {
            CategoricalEncoding.ENCODING_METHOD_KEY: self.data_params.cat_encoding_method,
            CategoricalEncoding.OHE: {
                "cat_features_idxs": preprocessing_params.ohe_cat_features_idxs,
                "categories": ohe_categories,
                "min_frequency": 0,
                "handle_unknown": "ignore",  # -> because we can have new value when we do not have "infrequent"
            },
            CategoricalEncoding.TE: {
                "cv": self.data_params.te_cv,
                "random_state": self.data_params.te_random_state,
                "cat_features_idxs": preprocessing_params.te_cat_features_idxs,
                "categories": te_categories,
                "target_type": preprocessing_params.te_target_type,
                "classes": preprocessing_params.te_classes,
                "target_mean": preprocessing_params.te_target_mean,
                "encodings": preprocessing_params.te_encodings,
            },
            CategoricalEncoding.MIXED: {
                "favor_ohe_num_cats_thresh": self.data_params.favor_ohe_num_cats_thresh,
                "favor_ohe_vol_pct_thresh": self.data_params.favor_ohe_vol_pct_thresh,
            },
        }
        return cat_encoding_config

    def _check_feature_types(self, X):
        this_categorical_features_ = self._calc_categorical_features(X, self.data_params) or []
        self.data_params_internal.categorical_features_ = [] if not self.data_params_internal.categorical_features_ \
            else self.data_params_internal.categorical_features_
        if this_categorical_features_ != self.data_params_internal.categorical_features_:
            if self.data_params.cat_encoding_method != CategoricalEncoding.NOTHING:
                raise ValueError('Categorical features are not the same in the datasets')
        if X.shape[1] != len(self.data_params.features):
            raise ValueError(f"Number of features in the dataset ({X.shape[1]}) "
                             f"is not the same as in the provided `data_params` ({len(self.data_params.features)})")

    def expand_encoded_used_categories(
            self, categories: List[np.ndarray], cat_features_idxs: List[int],
            include_mapping: bool = False, keep_encoded: bool = False
    ) -> Dict:
        """Given a list of numpy arrays from encoded categories, we return a dictionary of used categories
        that maps the category name to a dictionary that maps each category in the original form
        to the encoded category

        Parameters
        ----------
        categories : List[np.ndarray]
            Encoding categories

        cat_features_idxs : List[int]
            Indices of the features matching the encoding strategy (OHE/TE)

        Returns
        -------
        Dict

        Raises
        ------
        ValueError
        """
        cat_feats = [i for i in self.data_params_internal.categorical_features_ if i in cat_features_idxs]
        used_categories_ = self.data_params_internal.used_categories_
        real_enc_map = {k: v for k, v in used_categories_.items() if
                        k != 'y' and int(k) in cat_features_idxs} if used_categories_ is not None else {}
        if len(categories) != len(cat_feats):
            raise ValueError(
                f"Found different lengths between internal categorical features and"
                f"provided ones: internal: {len(cat_feats)}, provided: {len(categories)}"
            )

        def _inv_key(d, v):
            for k, v_ in d.items():
                if v_ == v:
                    return k
            else:
                return None

        res = {"order": {}}
        if include_mapping:
            res["mapping"] = {}
        for feat, col_cats in zip(cat_feats, categories):
            col_dict = {}
            col_list = []
            for value in col_cats:
                if value == 0:
                    real_key = _inv_key(real_enc_map[str(feat)], value)
                    if real_key is None:
                        col_dict["nan"] = 0
                        col_list.append("nan")
                    else:
                        if keep_encoded:
                            real_key = value
                        col_dict[real_key] = value
                        col_list.append(real_key)
                elif value == CATEGORICAL_INFREQUENT:
                    col_dict[CATEGORICAL_INFREQUENT] = self.infrequent_encoding
                    col_list.append(CATEGORICAL_INFREQUENT)
                else:
                    if not keep_encoded:
                        real_key = _inv_key(real_enc_map[str(feat)], value)
                    else:
                        real_key = value
                    col_dict[real_key] = value
                    col_list.append(real_key)
            if include_mapping:
                res["mapping"][feat] = col_dict
            res["order"][feat] = col_list
        return res

    @staticmethod
    def compress_encoded_used_categories(
            categories: Dict[Any, Dict], encode_infrequent: bool = False
    ) -> List[np.ndarray]:
        res = []
        for _, cat_d in categories.items():
            enc_cat = list(cat_d.values())
            if not encode_infrequent:
                if "infrequent" in cat_d:
                    infr_idx = enc_cat.index(cat_d["infrequent"])
                    enc_cat[infr_idx] = "infrequent"
            res.append(np.array(enc_cat, dtype=object))
        return res

    @staticmethod
    def _check_dataset(dset: Dataset, detect_missing: bool = False, has_missing_values: bool = False,
                       has_array_features: bool = False) -> Dataset:
        """
        Validate and fix dataset's elements.
        When X dtype is not numeric, convert it to float; raise an exception if not succeeded.
        For y, convert to simple type when dtype is object; reshape to 1d when 2d.

        Parameters
        ----------
        dset: Dataset

        Returns
        -------
        Dataset

        """
        if not helpers.is_dtype_numeric(dset.X.dtype) and not has_array_features:
            try:
                # using check_array is not used from two reasons:
                #   a. it fails to convert when dtype is string (even if all strings are numeric)
                #   b. when dtype is boolean it keeps it as boolean and we prefer numeric values.
                # dset = dset._replace(X=check_array(dset.X))
                dset = dset._replace(X=dset.X.astype(float))
            except ValueError as e:
                raise ValueError(f"All features must be numeric: {e}")
            if helpers.is_dtype_floating(dset.X.dtype) and not detect_missing:
                if np.isnan(dset.X).any():
                    raise ValueError("Feature data contains NaN or None values.")
                if np.isinf(dset.X).any():
                    raise ValueError("Feature data contains Infinity values.")
        if dset.y is not None:
            if dset.y.ndim == 2:
                # flatten y
                dset = dset._replace(y=helpers.y_to1d(dset.y))
            if helpers.is_object_dtype(dset.y.dtype) and not has_missing_values:
                # Convert y to simple dtype when possible.
                dtype = helpers.to_dtype(pd.Series(dset.y).convert_dtypes().dtype)
                if not helpers.is_object_dtype(dtype):
                    dset = dset._replace(y=dset.y.astype(dtype))
            if helpers.is_dtype_floating(dset.y.dtype) and not detect_missing:
                if np.isnan(dset.y).any():
                    raise ValueError("Target data contains NaN or None values.")
                if np.isinf(dset.y).any():
                    raise ValueError("Target data contains Infinity values.")

        return dset

    def save_selected_samples(self, dataset, indices: Optional[np.array], node_id=None):
        """
        customization point for storing new node data

        Parameters
        ----------
        dataset: a tuple of numpy ndarrays, required
        indices: 1d ndarray, required
            The Selected samples ids.
        node_id: string, optional
            the id of the node (in the tree). used to identify buffer node.

        """
        if not self.schema.save_dataset or not self.support_save:
            return
        self._save_selected_samples(dataset, indices, async_mode=False, node_id=node_id)

    def save_selected_samples_async(self, dataset, indices: Optional[np.array], node_id=None, is_buffer: bool = False):
        """
        customization point for storing new node data

        Parameters
        ----------
        dataset: a tuple of numpy ndarrays, required
        indices: 1d ndarray, required
            The Selected samples ids.
        node_id: string, optional
            A unique identifier of the node
            A special treatment takes place when the node_id represents the buffer.
        is_buffer: bool, optional, default False
            an indication if the node to be saved is the buffer node.
        """
        if not self.schema.save_dataset or not self.support_save:
            return

        self._save_selected_samples(dataset, indices, async_mode=True, node_id=node_id, is_buffer=is_buffer)

    def clear_buffer(self):
        """ clear the buffer as it is not longer needed"""

        self._clear_buffer()

    def replace(self, indices, X=None, y=None):
        """
        replace sample in database
        Input:
        indices - indices
        X - input data
        y - target (default None)
        """
        X = self._encode_categorical_data(X)
        self._replace(indices, X, y=y)

    def remove(self, indices):
        """
        Remove indices

        Parameters
        ----------
        indices: iterable
            indices to remove

        Returns
        -------

        """
        return self._remove(indices)

    def remove_nodes(self, nodes) -> None:
        self._remove_nodes(nodes)

    def get_removed(self):
        return self._get_removed()

    def get_node_metadata(self, dataset, indices: np.array, children_metadata: list = None) -> Union[list, dict, None]:
        if self.schema.node_metadata_func:
            return self.schema.node_metadata_func(dataset, indices, children_metadata)
        else:
            return None

    def _fetch_seq_column(self, X, props):
        seq_col = self.data_params_internal.seq_column_
        # get seq column values
        if self.data_params_internal.seq_column_location_ == 'features':
            seq_column = X[:, self.data_params_internal.seq_column_]
            # decode data if needed
            if seq_col in self.data_params_internal.categorical_features_:
                seq_col_dict = {v: k for k, v in self.data_params_internal.used_categories_[str(seq_col)].items()}
                seq_column = np.array(list(map(lambda x: seq_col_dict[int(x)], seq_column)))
        else:
            seq_column = props[:, self.data_params_internal.seq_column_]
        return seq_column

    def get_node_statistics(self, X, props):

        """
        Compute statistics for node
        Returns a dictionary where keys are the datapoints and values are the counts for each occurrence
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
        """

        if self.data_params_internal.seq_column_ is None:
            return

        granularity = self.data_params_internal.seq_granularity_
        fmt = self.data_params_internal.seq_datetime_format

        if self.data_params_internal.seq_column_ != 'every_build':
            seq_column = self._fetch_seq_column(X, props)

            if isinstance(granularity, str):

                if fmt:
                    seq_column = pd.to_datetime(seq_column, format=fmt)
                df = pd.DataFrame({'seq': seq_column})
                df['seq'] = pd.to_datetime(df['seq'])
                df = df.set_index('seq')
                # Create a DataFrame and perform grouping and counting
                statistics = df.groupby(pd.Grouper(freq=granularity)).size().reset_index(name='count')
                # drop rows where count is 0
                statistics = statistics[statistics['count'] != 0]
            else:
                # If the user also provided a datetime format, he probably expects us to convert the
                # column before applying the granularity function
                try:
                    statistics = np.vectorize(granularity)(seq_column)
                except ValueError as e:
                    if fmt:
                        seq_column = pd.to_datetime(seq_column, format=fmt)
                        statistics = np.vectorize(granularity)(seq_column)
                    else:
                        raise e
                unique, counts = np.unique(statistics, return_counts=True)
                # convert dictionary to DataFrame
                statistics = pd.DataFrame({'seq': unique, 'count': counts})
        else:
            seq = pd.to_datetime(self.data_params_internal.seq_every_build,
                                 format=fmt) if fmt else self.data_params_internal.seq_every_build
            statistics = pd.DataFrame({'seq': [seq], 'count': [X.shape[0]]})
        return statistics

    def decode_categorical_y(self, y):
        if self.data_params_internal.y_mixed_types:
            # used values for y
            index_to_string = {v: k for k, v in self.data_params_internal.used_categories_['y'].items()}
            # replace all data indexes with values
            data_decoded = np.array(list(map(lambda x: index_to_string[x], y)))
            y = data_decoded
        return y

    def _decode_categorical_dataset(self, dataset):
        """
        Not in use, preserved for tests
        """
        decoded_X = self._decode_categorical_df(pd.DataFrame(dataset.X))
        dataset_result = Dataset(ind=dataset.ind, X=decoded_X.to_numpy(), y=dataset.y, props=dataset.props)
        return dataset_result

    def _decode_categorical_df(self, df):
        if self.data_params_internal.used_categories_:
            for feature_index, categories in self.data_params_internal.used_categories_.items():
                if feature_index != 'y':
                    refer_dict = {v: k for k, v in categories.items()}
                    refer_dict[0] = np.nan
                    df[int(feature_index)] = df[int(feature_index)].apply(
                        lambda x: refer_dict[int(x)] if not pd.isna(x) else x)
        return df

    def convert_encoded_data_to_user(self, X):
        if (self.data_params_internal.categorical_features_ is None or len(
                self.data_params_internal.categorical_features_) == 0) \
                and (
                self.data_params_internal.bool_features_ is None or len(self.data_params_internal.bool_features_) == 0):
            return X
        X_decoded = self._decode_categorical_df(pd.DataFrame(X))
        if self.data_params_internal.bool_features_ and len(self.data_params_internal.bool_features_) > 0:
            for col_idx in self.data_params_internal.bool_features_:
                X_decoded[col_idx] = X_decoded[col_idx].astype(bool)
        return X_decoded.to_numpy()

    def get_by_index(self, indices: Iterable, as_df=False, with_props=False, with_removed=False) -> Union[
        pd.DataFrame, tuple]:
        return self._get_by_index(indices, as_df=as_df, with_props=with_props, with_removed=with_removed)

    def get_by_nodes(self, nodes: Iterable, as_df=False, with_props=False, with_removed=False) -> Union[
        pd.DataFrame, tuple]:
        return self._get_by_nodes(nodes, as_df=as_df, with_props=with_props, with_removed=with_removed)

    def get_orig_by_index(self, idxs, with_index=False):
        if not self.schema.save_orig:
            raise ValueError("self.schema.save_orig should be True to use get_orig_by_index()")
        return self._get_orig_by_index(idxs, with_index=with_index)

    def get_schema(self):
        return self.schema

    def get_params(self):
        results = self.schema.to_dict()
        self._get_params(results)
        return results

    def save(self, save_dir):
        self._save(save_dir)
        return self.get_params()

    def close(self):
        self._close()

    def commit(self):
        self._commit()

    def _commit(self):
        pass

    @classmethod
    def load(cls, schema, *, working_directory=None, load_dir=None):
        dm = cls._load(schema, working_directory, load_dir)
        return dm

    # =========================
    # Helpers
    # =========================

    @staticmethod
    def generate_data_params(*, data_params: DataParams = None, features: List = None, target=None,
                             index=None, default=None) -> DataParams:
        """
        produce a new DataParams schema or update input data_params. define features, target, index fields

        Parameters
        ----------
        data_params: DataParams, optional
        features: list of strings/dicts/FeatureField, optional
        target: dict/string/TargetField, optional
        index: dict/string/IndexField, optional

        Returns
        -------
        DataParams new or updated object

        """

        def set_type(f, d):
            r = f(d)
            if not r.dtype and default:
                r.set_dtype(default)
            return r

        data_params = data_params or DataParams()
        if features:
            data_params.features = [set_type(FeatureField.from_any, c) for c in features]
        if target:
            data_params.target = set_type(TargetField.from_any, target)
        if index:
            data_params.index = set_type(IndexField.from_any, index)
        return data_params

    def split_datasets(self,
                       datasets: Iterator[Union[pd.DataFrame, Iterator[pd.DataFrame]]],
                       key: Union[Callable, str, list]
                       ):
        """
        for each data frame in the dataset split dataset to groups based on key
        use pandas apply if key is a function before grouping.

        Parameters
        ----------
        datasets: data frame iterator or a tuple of two data frame iterators.
        key: function, column, list of columns
            the key for splitting each dataset in datasets

        Returns
        -------
        data frame iterator
        """

        def seq_to_groups(df, granularity, temp_col):
            for _, group in df.groupby(pd.Grouper(freq=granularity, key=temp_col)):
                group = group.drop(columns=[temp_col])
                if len(group) > 0:
                    yield group

        def to_groups(df: pd.DataFrame):

            dfs = list(helpers.df_to_iterable(df))
            df = dfs[0]
            df.reset_index(drop=True, inplace=True)
            if not callable(key):
                if key == 'seq_column':
                    granularity = self.data_params.seq_column.get('granularity')
                    name = self.data_params.seq_column.get('name')
                    fmt = self.data_params.seq_column.get('datetime_format')
                    temp_col = '_temp_datetime'
                    name = name if name in df.columns \
                        else next((f'f{idx}' for idx, x in enumerate(self.data_params.features) if x.name == name),
                                  None)
                    # check if it was passed as an id, and we are building from X,y
                    id = self.data_params.seq_column.get('id')
                    prop_id = self.data_params.seq_column.get('prop_id')
                    if name is not None:
                        seq_col = df[name]
                    elif id is not None:
                        name = f"f{id}"
                        seq_col = df[name] if name in df.columns else df.iloc[:, id]
                    elif prop_id is not None:
                        name = f"p{prop_id}"
                        seq_col = df[name] if name in df.columns else df.iloc[:, prop_id]
                    else:
                        raise ValueError("`seq_column` was not found in dataset")
                    # check for missing values and raise error if found
                    if _get_inf_nan_indexes(seq_col):
                        raise ValueError("seq_column contains missing values")
                    if isinstance(granularity, str):
                        df[temp_col] = pd.to_datetime(seq_col, format=fmt)
                        # Group by the temporary column
                        groups = seq_to_groups(df, granularity, temp_col)
                    else:
                        groups = (v for _, v in df.groupby(seq_col.apply(granularity)))
                else:
                    groups = (v for _, v in df.groupby(key))
            else:
                groups = (v for _, v in df.groupby(df.apply(key, axis=1)))

            other_dfs = dfs[1:]
            if not other_dfs:
                for g in groups:
                    yield g

            # Slice other based on th grouping
            df_idx = pd.DataFrame(np.arange(len(df))).set_index(df.index)
            for g_df in groups:
                idx = df_idx.loc[g_df.index].to_numpy().flatten()
                out = [g_df] + [other_df.iloc[idx] if other_df is not None else None for other_df in other_dfs]
                yield tuple(out)

        return itertools.chain.from_iterable(map(to_groups, datasets))

    def dataset_to_df(self, indices, X, y, props=None):
        return self._dataset_to_df(indices, X, y, props)

    def df_to_dataset(self, df):
        X = df[self.features_cols].to_numpy()
        y = df[self.target_col].to_numpy() if self.dataset_schema.target_col else None
        props = df[self.properties_cols].to_numpy() if self.dataset_schema.properties_cols else None
        indices = df.index.to_numpy()
        return Dataset(indices, X, y, props)

    def orig_to_df(self, data):
        return pd.DataFrame(
            data,
            columns=[c.name for c in self.schema.data_schema.columns]
        ).astype(
            {c.name: c.dtype for c in self.schema.data_schema.columns},
            copy=False
        )

    # =========================
    # Subclasses methods
    # =========================
    def _read_data(self, chunk_size) -> Iterable:
        raise NotImplementedError

    def _save_selected_samples(self, dataset, indices: np.array, async_mode=False, node_id=None, is_buffer=False):
        raise NotImplementedError

    def _replace(self, indices: np.array, X, y=None):
        raise NotImplementedError

    def _remove(self, indices):
        raise NotImplementedError

    def _remove_nodes(self, nodes):
        raise NotImplementedError

    def _get_removed(self):
        raise NotImplementedError

    def _get_by_index(self, indices: Iterable, as_df=False, with_props=False, with_removed=False) -> Union[
        pd.DataFrame, tuple]:
        raise NotImplementedError

    def _get_by_nodes(self, nodes: Iterable, as_df=False, with_props=False, with_removed=False) -> Union[
        pd.DataFrame, tuple]:
        raise NotImplementedError

    def _get_orig_by_index(self, indices, with_index=False):
        raise NotImplementedError

    def _get_params(self, results):
        pass

    def _save(self, save_dir):
        pass

    def _clear_buffer(self):
        pass

    @classmethod
    def _load(cls, schema, working_directory, load_dir):
        return cls(schema, working_directory=working_directory)

    @abc.abstractmethod
    def _prepare_schema(self):
        pass

    def _close(self):
        pass

    # TODO: find a way to clean when object is destroy. __del__ is called after all class attributes were deleted.
    def __del__(self):
        try:
            self._close()
        except BaseException:
            pass

    # =========================
    # Internal methods
    # =========================

    @staticmethod
    def _np_column_stack(*arr):
        arr = [a for a in arr if a is not None]
        if len(arr) == 1:
            return arr[0]
        arr = tuple([a.reshape(-1, 1) if len(a.shape) == 1 else a for a in arr])
        return np.hstack(arr)

    def _dataset_to_df(self, indices, X, y, props=None):
        if indices is not None:
            df = pd.concat([
                pd.DataFrame(indices, columns=[self.dataset_schema.index_col.name]),
                pd.DataFrame(X, columns=[c.name for c in self.dataset_schema.features_cols])
            ], axis=1)
        else:
            df = pd.DataFrame(X, columns=[c.name for c in self.dataset_schema.features_cols])

        if props is not None and self.dataset_schema.properties_cols is not None:
            df = pd.concat([
                df,
                pd.DataFrame(props, columns=[c.name for c in self.dataset_schema.properties_cols]),
            ], axis=1)

        if y is not None:
            df[self.dataset_schema.target_col.name] = y

        return df

    def _init_dataset_schema(self, x_schema_dtypes=None):
        data_params = self.data_params
        self.dataset_schema.index_col = Column('index_column', dtype=data_params.index.dtype)
        if x_schema_dtypes is not None:
            self.dataset_schema.features_cols = [Column(f'f{i}', dtype=f) for i, f in enumerate(x_schema_dtypes)]
        else:
            self.dataset_schema.features_cols = [Column(f'f{i}', dtype=f.dtype) for i, f in
                                                 enumerate(data_params.features)]
        self.dataset_schema.target_col = Column('y', data_params.target.dtype) if data_params.target else None
        self.dataset_schema.properties_cols = [Column(f'p{i}', dtype=p.dtype) for i, p in
                                               enumerate(data_params.properties)] if data_params.properties else None

        self.dataset_schema.columns = [self.dataset_schema.index_col] + self.dataset_schema.features_cols
        if self.dataset_schema.target_col:
            self.dataset_schema.columns.append(self.dataset_schema.target_col)

    @staticmethod
    def _resolve_dataset_types(indices: np.ndarray, X: np.ndarray, y: np.ndarray = None,
                               sample_weight: np.ndarray = None, props: np.ndarray = None):

        if indices is not None:
            ind_dtype = helpers.to_dtype(indices.dtype)
            if helpers.is_object_dtype(ind_dtype):
                ind_dtype = helpers.to_dtype(pd.Series(indices).convert_dtypes().dtype)
        else:
            ind_dtype = None

        x_schema_dtypes = []
        for i in range(X.shape[1]):
            col = X[:, i]
            if helpers.is_object_dtype(col.dtype):
                col_dtype = helpers.to_dtype(pd.Series(col).convert_dtypes().dtype)
            else:
                col_dtype = np.dtype(col.dtype)
            if 'int' in str(col_dtype):
                schema_dtype = np.dtype('int64')
            else:
                # If we're calculating these dtypes for schema purposes we will need to differentiate between
                # float and object dtypes
                schema_dtype = col_dtype if not helpers.is_object_dtype(col_dtype) else np.dtype('object')

            x_schema_dtypes.append(schema_dtype)
        x_dtypes = [np.dtype('float64') for _ in range(X.shape[1])]

        if y is not None:
            y_dtype = helpers.to_dtype(y.dtype)
            if helpers.is_object_dtype(y_dtype):
                y_dtype = helpers.to_dtype(pd.Series(y).convert_dtypes().dtype)
        else:
            y_dtype = None

        if sample_weight is not None:
            sample_weight_dtype = helpers.to_dtype(sample_weight.dtype)
        else:
            sample_weight_dtype = None

        if props is not None:
            props_dtypes = [np.dtype(props.dtype) for _ in range(props.shape[1])]
        else:
            props_dtypes = None

        return ind_dtype, x_dtypes, y_dtype, sample_weight_dtype, props_dtypes, x_schema_dtypes

        # def _conv_obj(dtype, default):
        #     dtype = helpers.to_dtype(dtype)
        #     return default if helpers.is_object_dtype(dtype) else dtype
        #
        # def _resolve_dtypes(arr, o_default=None):
        #     if arr.dtype.names:
        #         return [_conv_obj(arr.dtype.fields[f][0], o_default) for f in X.dtype.names]
        #     elif arr.ndim == 1:
        #         # use pandas convert_dtypes to guess the real dtype based on the array content
        #         dtype = pd.Series(arr).convert_dtypes().dtype if helpers.is_object_dtype(arr.dtype) else arr.dtype
        #         return [_conv_obj(dtype, o_default)]
        #     else:
        #         return [_conv_obj(arr.dtype, o_default)] * arr.shape[1]
        #
        # x_dtypes = _resolve_dtypes(X, np.dtype(float))
        # props_dtypes = _resolve_dtypes(props, np.dtype(float)) if props is not None else None
        # ind_dtype = _resolve_dtypes(indices)[0] if indices is not None else None
        # y_dtype = _resolve_dtypes(y, np.dtype(str))[0] if y is not None else None
        # return ind_dtype, x_dtypes, y_dtype, props_dtypes

    def _run_transform_before(self, data):
        data_params = self.data_params
        if data_params.data_transform_before:
            data = data_params.data_transform_before.run_transform(data)
        return data

    @staticmethod
    def _iter_first(it):
        return helpers.iter_first(it)

    def _extract_indices(self, dataset, data_params=None, only_if_not_defined=False):
        data_params = data_params or self.data_params
        df = list(helpers.df_to_iterable(dataset))[0]
        if data_params.index.transform:
            indices = self.gen_indices(df, data_params=data_params)
        elif only_if_not_defined:
            indices = None
        else:
            indices = df[data_params.index.name].to_numpy()
        return indices

    def _check_missing_values_seq_col(self, target, target_type):
        if self.data_params.seq_column is None:
            return
        # Check for missing values in seq_column
        loc = self.data_params_internal.seq_column_location_
        col_index = self.data_params_internal.seq_column_
        name = self.data_params.seq_column.get('name')
        if self.data_params.seq_column is not None:
            if target_type == 'df':
                if name is not None:
                    seq_column = target[name]
                else:
                    seq_column = target.iloc[:, col_index]
            else:
                seq_column = target.X[:, col_index] if loc == 'features' else target.props[:, col_index]
            if _get_inf_nan_indexes(seq_column):
                raise ValueError("`seq_column` contains missing values")

    def _handle_datetime_columns(self, data_params, df=None, X=None):

        # datetime fields handling (move them to properties)
        moved_feature_indexes = []
        for feature_index, feature in enumerate(data_params.features):
            # We do not handle datetime columns that appear after user-defined preprocessing
            col = df.iloc[:, feature_index] if df is not None else X[:, feature_index]
            is_in_columns = feature.name in df.columns if df is not None else feature_index < X.shape[1]
            if is_in_columns and _is_datetime(col):
                if data_params.datetime_to_properties:
                    if df is not None:  # apparently we only save properties names when building from dataframes??
                        if data_params.properties is None:
                            data_params.properties = []
                        data_params.properties += [PropertyField(
                            name=feature.name,
                            transform=feature.transform,
                            dtype=feature.dtype,
                        )]
                    moved_feature_indexes.append(feature_index)
                    user_warning(f'Feature "{feature.name}" is datetime and was automatically turned into a property. '
                                 f'Properties won’t be used to build the Coreset or train the model. If this is not '
                                 f'the desired behavior set data_params.datetime_to_properties = False and preprocess '
                                 f'the feature to a String or a numeric feature.')
                else:
                    raise ValueError(f"Feature '{feature.name}' is datetime and can't be processed. Please set "
                                     f"data_params.datetime_to_properties = True to automatically turn it into a "
                                     f"property or preprocess the feature to a String or a numeric feature.")
        if moved_feature_indexes:
            self.data_params_internal.calculated_props_ = moved_feature_indexes
            # remove properties from features
            if data_params.properties:
                data_params.features = [f for f in data_params.features
                                        if f.name not in [p.name for p in data_params.properties]]
        return data_params

    def _estimate_expected_n_features(self, dataset, return_counts=False) -> Union[int, Tuple[int, Dict]]:
        """
        Compute an estimate for the expected number of features after the categorical and array encoding takes place.
        Categorical features are check for the encoding method (TE or OHE).
        This is an estimate, because -
        (1) if some feature is OHE-encoded, we take the minimum between ohe_max_categories and the actual number
            of categories we calculated per feature, and we ignore the ohe_min_frequency, along with missing values.
        (2) if some feature is an array, we take the minimum between array_max_categories and the actual number
            of categories we calculated per feature, and we ignore the array_min_frequency.
        (3) we look only at the first dataset from a potential series of multiple datasets/cases.
        """
        if not self.has_categorical_features() and not self.has_array_features():
            self._n_features_expected = self.n_features
            if not return_counts:
                return self._n_features_expected
            else:
                n_bool_features = len(
                    [feature_idx for feature_idx in range(dataset.shape[1])
                     if (type(get_feature_slice(dataset, feature_idx)[0]) == bool or type(get_feature_slice(
                        dataset, feature_idx)[0]) == np.bool_)])
                # the default dict for the missing counts to return 0
                return self._n_features_expected, defaultdict(
                    int, {"numeric": self.n_features - n_bool_features, "boolean": n_bool_features}
                )

        cat_features = list(self.data_params_internal.categorical_features_) \
            if self.data_params_internal.categorical_features_ is not None else []
        array_features = list(self.data_params_internal.array_features_) \
            if self.data_params_internal.array_features_ is not None else []
        n_num_features = self.n_features - len(cat_features) - len(array_features)
        n_array_features = self._get_expected_num_array_features(dataset, array_features)

        if return_counts:
            # get ohe and te counts
            n_cat_features, feature_counts = self._get_expected_n_cat_features(
                dataset, cat_features, return_counts=True
            )
            # count bool features
            n_bool_features = len(
                [feature_idx for feature_idx in range(dataset.shape[1])
                 if (type(get_feature_slice(dataset, feature_idx)[0]) == bool or type(get_feature_slice(
                    dataset, feature_idx)[0]) == np.bool_)])

            feature_counts["numeric"] = n_num_features - n_bool_features
            feature_counts["array"] = n_array_features
            feature_counts["boolean"] = n_bool_features
            self._n_features_expected = n_num_features + n_cat_features + n_array_features
            return self._n_features_expected, feature_counts
        else:
            n_cat_features = self._get_expected_n_cat_features(dataset, cat_features)
            self._n_features_expected = n_num_features + n_cat_features + n_array_features
            return self._n_features_expected

    def _get_expected_num_array_features(self, dataset, array_features_idxs) -> int:
        """
        Compute the expected number of features after the array encoding takes place.
        Using the max array categories as the upper bound for the number of features.
        """
        # count the amount of unique values in each array feature
        # each array feature consists of array which need to be concatenated before passing to unique
        array_unique_counts = [len(pd.unique(
            np.concatenate([arr for arr in get_feature_slice(dataset, array_feature_idx) if arr is not None])))
            for array_feature_idx in array_features_idxs]
        arrays_total_sum = sum([min(arr_unique_count, self.data_params.array_max_categories)
                                for arr_unique_count in array_unique_counts])
        return arrays_total_sum

    def _get_expected_n_cat_features(
        self, dataset, cat_features, return_counts: bool = False
    ) -> Union[int, Tuple[int, Dict]]:
        ohe_cat_features, te_cat_features, ohe_unique_counts = _categorical_features_encoding_split(
            cat_encoding_method=self.data_params.cat_encoding_method,
            categorical_feature_idxs=cat_features,
            favor_ohe_num_cats_thresh=self.data_params.favor_ohe_num_cats_thresh,
            favor_ohe_vol_pct_thresh=self.data_params.favor_ohe_vol_pct_thresh,
            dataset=dataset,
            return_unique_ohe_counts=True
        )
        # sum ohe_unique_counts, if the unique count is bigger than max_categories, we use max_categories
        ohe_total_sum = sum([min(unique_ohe_count,
                                 self.data_params.ohe_max_categories) for unique_ohe_count in ohe_unique_counts])
        if return_counts:
            return ohe_total_sum + len(te_cat_features), {'OHE': ohe_total_sum,
                                                          'TE': len(te_cat_features)}
        else:
            return ohe_total_sum + len(te_cat_features)


class DataManagerMem(DataManagerBase):
    """Memory only without persistent"""
    support_save = False
