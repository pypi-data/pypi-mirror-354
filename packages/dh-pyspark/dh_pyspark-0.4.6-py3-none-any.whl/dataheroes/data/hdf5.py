from importlib.util import find_spec
import pathlib
import shutil
import threading
import uuid
from typing import List, Union, Iterable, Optional

import h5py
import joblib
import numpy as np
import pandas as pd
import tables as pt
from tables.exceptions import HDF5ExtError

from dataheroes.data.storage.storage_manager import StorageManager

from .common import DMSchemaHDF5, SeqIndexField, Dataset, concat_arrays
from .manager import DataManagerBase
from . import helpers
from .utils import serialize_function


def _get_table_name_by_node_id(node_id):
    return f'table_{node_id}' if node_id else node_id


SLICE_SIZE = 150
SLICE_THRESHOLD = 0.2


class DataManagerHDF5(DataManagerBase):
    """
    Data manager using HDF5 file format for storing data.
        https://www.hdfgroup.org/solutions/hdf5/
    Manager uses three packages:
        - h5py: the basic implementation of HDF5 file structure.
        - PyTables (tables): high level wrapper for h5py (https://www.pytables.org)
        - Pandas/HDFStore: pandas DataFrame on top of PyTables.


    Parameters
    ----------
    schema: DMSchemaHDF5, optional.
        Data manager schema relevant for integrating with the database.
    connector: sql server connection handle, optional.
        True: save also original raw data.

    File structure
    ---------------
    Model X, y and indices in different tables (arrays), all under the same file.
    Indices are maintained as Pandas hdf5 table and hold reference to the data
    X, y are stored as arrays where each node is stored in a different array.
    Below is a file structure example of two nodes, each with two samples.

    - file
        - indices
            [id1, index1, table1]
            [id2, index2, table1]
            [id3, index3, table2]
            [id4, index4, table2]
        - X
            - table1
                [x1.0, x1.1, ...],
                [x2.0, x2.1, ...]
            - table2
                [x3.0, x3.1, ...]
                [x4.0, x4.1, ...]
        - y
            - table1
                y1,
                y2
            - table2
                y3,
                y4

    """
    schema_cls = DMSchemaHDF5
    default_index_column_cls = SeqIndexField
    TABLE_BUFFER = 'table_buffer'

    def __init__(self, schema: DMSchemaHDF5 = None, **kwargs):
        super(DataManagerHDF5, self).__init__(schema, **kwargs)
        self.index_cache = None
        self.mapping_cache = None
        self.removed_cache = None

    def _clear_cache(self):
        self.index_cache = None
        self.mapping_cache = None
        self.removed_cache = None

    def _clear_removed_cache(self):
        self.removed_cache = None

    # TODO: find a way to clean when object is destroy. __del__ is called after all class attributes were deleted.
    # def __del__(self):
    #     self._close()

    @property
    def table_name(self):
        return self.dataset_schema.table_name

    @property
    def db_file(self):
        return self.schema.db_file

    @db_file.setter
    def db_file(self, value):
        self.schema.db_file = str(value) if value else None

    @property
    def indices_table_path(self):
        return f'/{self.table_name}/indices'

    @property
    def table_mapping_path(self):
        return f'/{self.table_name}/table_mapping'

    @property
    def removed_path(self):
        return f'/{self.table_name}/removed'

    @property
    def indices_buffer_table_path(self):
        return f'/{self.table_name}/indices_buffer'

    @property
    def table_root_path(self):
        return f'/{self.table_name}'

    @property
    def orig_table_root_path(self):
        return f'/{self.schema.data_schema.table_name}'

    def _save_selected_samples(
            self,
            dataset: Dataset,
            indices: Optional[np.ndarray],
            async_mode=False,
            node_id=None,
            is_buffer: bool = False
    ):
        """
        An exit point for storing tree node.

        Parameters
        ----------
        dataset: tuple, required.
            instances from which tree node was constructed.
        indices: 1d ndarray, required
            tree node selected instances
        node_id: optional
            A unique identifier of the node
            A special treatment takes place when the node_id represents the buffer.

        Returns
        -------
        None

        """
        dataset = Dataset(*dataset)
        # get a subset of dataset based on selected indices.
        if indices is not None:
            idxs_ = np.isin(dataset.ind, indices)
            dataset = Dataset(*tuple(a[idxs_] if a is not None else None for a in dataset))

        # add selected samples to database

        # Because HDF5 cannot handle mixed types we need to check if y is categorical and encode it
        if self.data_params_internal.y_mixed_types:
            y_encoded = self._encode_categorical_y(dataset.y)
            dataset = dataset._replace(y=y_encoded)

        if len(dataset.ind) == 0:
            return  # Nothing to store
        table_name = self._add(dataset.ind, dataset.X, dataset.y, dataset.props, node_id=node_id, is_buffer=is_buffer)

        if self.schema.save_orig:
            self._add_orig((dataset.orig, dataset.orig_target), dataset.ind, table_name)

    def _add_orig(self, datasets, indices, table_name):
        """Store original data. Each node is stored in a different table"""
        dataset = self._np_column_stack(*datasets)  # cases where input data is separated.
        with self._get_connection_pd('a') as con:
            df = self.orig_to_df(dataset)
            df[self.schema.data_schema.index_col] = indices
            df.set_index(self.schema.data_schema.index_col)
            df.to_hdf(con, key=f'{self.orig_table_root_path}/{table_name}', append=False)

    def _add(self, indices, X, y, props=None, table_name=None, node_id=None, is_buffer: bool = False):
        """
        Store data. Each node is stored in a different table
        indices related to buffer are maintained in a different table.
        """

        # Indices are stored as table. We use pandas for this task.
        # Buffer indices are stored in a different table for easy replacement.
        table_name = _get_table_name_by_node_id(node_id) or table_name or f'table_{uuid.uuid4().hex}'
        self._update_indices_mapping(table_name, indices, is_buffer)

        if props is not None:
            with self._get_connection_pd('a') as con_pd:
                if self.schema.data_params.properties is not None:
                    columns = [c.name for c in self.schema.data_params.properties]
                else:
                    columns = None
                df = pd.DataFrame(props, columns=columns)
                df.to_hdf(con_pd, key=f'props/{table_name}', append=False)
        # X and y are stored as in different tables.
        # We use tables as in pandas appending is only supported for a table format
        #   which has limit on the number of columns.
        has_array_columns = self.data_params_internal.array_features_ is not None and len(
            self.data_params_internal.array_features_) > 0
        with self._get_connection('a') as con:
            group = con.get_node(self.table_root_path)
            group_idx = con.create_group(group, 'idx') if 'idx' not in group else group['idx']
            if table_name in group_idx:
                group_idx[table_name].remove()
            con.create_array(group_idx, table_name, indices)

            group_X = con.create_group(group, 'X') if 'X' not in group else group['X']
            if table_name in group_X:
                group_X[table_name].remove()

            try:
                x_columns = X[:, [c for c in range(X.shape[1]) if
                                  c not in self.data_params_internal.array_features_]].astype(
                    float) if has_array_columns else X
                con.create_array(group_X, table_name, x_columns)
            except HDF5ExtError:
                raise ValueError(
                    "An exception was raised during HDF5 Array's creation, indicating either a problem in the low-level HDF5 library or an error at the Input/Output level, such as running out of disk space."
                )

            if y is not None:
                y = y.astype(self.data_params.target.dtype)
                group_y = con.create_group(group, 'y') if 'y' not in group else group['y']
                if table_name in group_y:
                    group_y[table_name].remove()
                con.create_array(group_y, table_name, y)

        # for each column create group
        if has_array_columns:
            dt = h5py.vlen_dtype(np.int32)
            with self._get_connection_h5(mode='a') as f:
                base_group = f[self.table_root_path]
                group_arr = base_group.create_group('Array') if 'Array' not in base_group else base_group['Array']
                for arr_column_idx, arr_column_name in [(col_idx, col_name) for col_idx, col_name in enumerate(
                        self.features_cols) if col_idx in self.data_params_internal.array_features_]:

                    # check if group exists, create if not
                    if str(arr_column_name) not in group_arr:
                        column_group = group_arr.create_group(str(arr_column_name))
                    else:
                        column_group = group_arr[str(arr_column_name)]

                    # prepare column to insert
                    # make sure that all values are ndarrays of type int32
                    # because h5py cant save them since a list has no dtype or dtype missmatch
                    # make sure no None on nan in the arrays
                    for row_idx in range(X.shape[0]):

                        # we need to convert the list to an np.array
                        # an integer list [1,2,3] will automatically be converted to a int32 array
                        if not isinstance(X[row_idx, arr_column_idx], np.ndarray):
                            X[row_idx, arr_column_idx] = np.array(X[row_idx, arr_column_idx])

                        if X[row_idx, arr_column_idx].dtype == float:
                            # filter out nan values
                            X[row_idx, arr_column_idx] = X[row_idx, arr_column_idx][
                                ~np.isnan(X[row_idx, arr_column_idx])].astype(np.int32)
                        elif X[row_idx, arr_column_idx].dtype == object:
                            # in case the list contained None, the dtype will be: object
                            # we need to filter out the None and np.nan values
                            X[row_idx, arr_column_idx] = np.array(
                                [x for x in X[row_idx, arr_column_idx] if x is not None and not (isinstance(x, float)
                                                                                                 and np.isnan(x))],
                                dtype=np.int32)
                        else:
                            # verify that the array of the np.int32 type
                            if X[row_idx, arr_column_idx].dtype != np.int32:
                                X[row_idx, arr_column_idx] = X[row_idx, arr_column_idx].astype(np.int32)

                    column_group.create_dataset(table_name,
                                                shape=(X.shape[0],),
                                                data=X[:, arr_column_idx],
                                                dtype=dt)

        return table_name

    def add(self, table_name, data: pd.DataFrame):
        """
        Add data to database. data should be a data frame of indices, X, y.

        Parameters
        ----------
        table_name: string
        data: DataFrame

        Returns
        -------
        None

        """
        ds = self.df_to_dataset(data)
        self._add(indices=ds.ind, X = ds.X, y = ds.y, props=ds.props, table_name=table_name)

    # =============================
    # Subclass methods implementation
    # =============================

    def _get_connection(self, mode='r') -> pt.File:
        """Open a PyTable connection to the db_file"""
        pathlib.Path(self.db_file).parent.mkdir(exist_ok=True)
        return pt.File(self.db_file, mode=mode)

    def _get_connection_pd(self, mode='r') -> pd.HDFStore:
        """Open a Pandas HDFStore connection to the db_file"""
        pathlib.Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
        return pd.HDFStore(self.db_file, mode=mode)

    def _get_connection_h5(self, mode='r') -> h5py.File:
        """open h5py connection to the db_file"""
        pathlib.Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
        return h5py.File(self.db_file,  mode=mode)

    def _prepare_schema(self):
        pass

    def _replace(self, indices: np.array, X, y=None):
        """ Modify X/y data for given indices."""

        tables_groups = self._resolve_idx(indices)
        df_indices = pd.DataFrame({'ind': indices, 'idx': np.arange(len(indices))})
        with self._get_connection('a') as con:
            group = con.get_node(self.table_root_path)
            for table_name, idx, ind in tables_groups:
                df = pd.merge(df_indices, pd.DataFrame({'ind': ind, 'idx': idx}), on='ind', suffixes=("_in", "_table"))
                idx_in, idx_table = df['idx_in'], df['idx_table']
                if X is not None:
                    group.X[table_name][idx_table, :] = X[idx_in]
                if y is not None:
                    group.y[table_name][idx_table] = y[idx_in]

    def _update_indices_mapping(self, table_name, indices, is_buffer):
        with self._get_connection_pd('a') as con:
            # Resolve table index
            if self.table_mapping_path in con:
                df = con[self.table_mapping_path]
                mapping = dict(zip(df['table_name'], df['table_idx']))
            else:
                mapping = {}

            if table_name not in mapping:
                mapping[table_name] = (max(mapping.values()) + 1) if mapping else 1
                pd.DataFrame(
                    {'table_name': [table_name], 'table_idx': [mapping[table_name]]}
                ).to_hdf(con, key=self.table_mapping_path, data_columns=['table_name', 'table_idx'], append=True, min_itemsize=100)

            table_idx = mapping[table_name]

            # Store indices mapping
            df = pd.DataFrame(indices, columns=[self.index_col])
            df['table_idx'] = table_idx
            df['idx'] = np.arange(len(indices))
            if is_buffer:
                df.to_hdf(con, key=self.indices_buffer_table_path, data_columns=[self.index_col, 'table_idx', 'idx'], append=False)
            else:
                df.to_hdf(con, key=self.indices_table_path, data_columns=[self.index_col, 'table_idx', 'idx'], append=True)

            # To reduce data integrity risk, clear cache after update.
            self._clear_cache()

    def _exclude_removed(self, indices, dataset=None):
        removed = self._read_removed_cache()
        mask = None
        # indices must be a np array (not list, etc.)
        indices = np.array(indices)
        if removed is not None and len(removed) > 0:
            mask = ~np.in1d(indices, removed)
            if np.any(mask):
                indices = indices[mask]
        if dataset is not None:
            if mask is not None:
                dataset = Dataset(*[arr[mask] if arr is not None else None for arr in dataset])
            return indices, dataset

        return indices

    def _remove(self, indices):
        indices = np.array(indices)
        self._add_removed_to_cache(indices)
    

    def _remove_nodes(self, node_ids: List[str]):
        with self._get_connection('a') as con:
            fields_to_remove = [
                'idx',
                'X',
                'y',
                'props',
                'Array',
            ]
        
            for node_id in node_ids:
                table_name = _get_table_name_by_node_id(node_id)
                for field in fields_to_remove:
                    try:
                        if field == "Array":
                            for arr_column_idx, arr_column_name in [(col_idx, col_name) for col_idx, col_name in enumerate(
                                self.features_cols) if col_idx in self.data_params_internal.array_features_]:
                                con.remove_node(f'{self.table_root_path}/{field}/{arr_column_name}/{table_name}', recursive=True)

                        elif field == "props":
                            con.remove_node(f'/{field}/{table_name}', recursive=True)

                        else:
                            con.remove_node(f'{self.table_root_path}/{field}/{table_name}', recursive=True)
                    except pt.NoSuchNodeError:
                        pass # Nodes are not guaranteed to have all fields
                self._remove_index(table_name)
        return

    def _remove_index(self, table_name: str) -> None:
        with self._get_connection_pd('a') as con:
            table_mapping_df = con[self.table_mapping_path]
            # Get the DF row of the node we want to remove
            table_mapping_df_row = table_mapping_df[table_mapping_df["table_name"] == table_name]
            if len(table_mapping_df_row) == 0:
                # Node was already removed
                return

            assert len(table_mapping_df_row) == 1, f"Multiple nodes found with table name {table_name}"
            
            # Remove the node from the table_mapping DF
            table_mapping_df = table_mapping_df[table_mapping_df["table_name"] != table_name]
            table_mapping_df.to_hdf(con, key=self.table_mapping_path, data_columns=['table_name', 'table_idx'], append=False, min_itemsize=100, format='table')

            # Remove the node from the indices_table
            table_idx = table_mapping_df_row["table_idx"].item()
            indices_table_df = con[self.indices_table_path]
            indices_table_df = indices_table_df[indices_table_df["table_idx"] != table_idx]
            indices_table_df.to_hdf(con, key=self.indices_table_path, data_columns=[self.index_col, 'table_idx', 'idx'], append=False, format='table')

            self._clear_cache()


    def _read_removed_cache(self, force_reload=False):
        if force_reload or self.removed_cache is None or len(self.removed_cache) > 0:
            with self._get_connection_pd() as con:
                if self.removed_path in con:
                    self.removed_cache = con[self.removed_path].values.flatten()
                else:
                    self.removed_cache = np.array([])
        return self.removed_cache

    def _get_removed(self):
        return self._read_removed_cache()

    def _add_removed_to_cache(self, indices, flush=True):
        self._read_removed_cache()
        if self.removed_cache is None or len(self.removed_cache) == 0:
            self.removed_cache = indices
        else:
            self.removed_cache = np.concatenate([self.removed_cache, indices])
        if flush:
            self._flush_removed_cache()

    def _flush_removed_cache(self):
        with self._get_connection_pd('a') as con:
            pd.DataFrame(self.removed_cache).to_hdf(con, key=self.removed_path, append=False)

    def _read_index_cache(self):
        # fill self.index_cache if it's empty
        if self.index_cache is not None:
            return

        with self._get_connection_pd() as con:
            data = []
            if self.indices_table_path in con:
                data.append(con[self.indices_table_path])
            if self.indices_buffer_table_path in con:
                data.append(con[self.indices_buffer_table_path])
            if data:
                self.index_cache = pd.concat(data)
                self.index_cache = self.index_cache.drop_duplicates(subset=['index_column'])
            if self.table_mapping_path in con:
                df = con[self.table_mapping_path]
                self.mapping_cache = dict(zip(df['table_name'], df['table_idx']))
            else:
                self.mapping_cache = {}

    def _resolve_idx(self, indices: Iterable, use_polars: bool = True):
        """
        Use indices table to get the related table name and position of each index in the table.
        Utilize caching instead of reading mapping from file every time.
        """
        indices = np.array(indices)
        self._read_index_cache()
        assert self.index_cache is not None and self.mapping_cache is not None, "Cache is None after reading it"
        df = self.index_cache

        # Using polars if available seems to be slightly faster
        if find_spec("polars") is not None and use_polars:
            import polars as pl

            df_pl = pl.from_pandas(df)
            res = (
                df_pl.lazy()
                .filter(pl.col("index_column").is_in(indices))
                .group_by("table_idx")
                .agg([pl.col("idx"), pl.col("index_column")])
                .collect()
            )
            mapping = {v: k for k, v in self.mapping_cache.items()}
            return [
                (mapping[res["table_idx"][i]], res["idx"][i].to_numpy(), res["index_column"][i].to_numpy())
                for i in range(len(res))
            ]
        else:
            idx = np.where(df[self.index_col].isin(indices))[0]
            df = df.iloc[idx]
            df_groups = df.groupby("table_idx")
            mapping = {v: k for k, v in self.mapping_cache.items()}
            return [
                (mapping[table_idx], data["idx"].to_numpy(), data[self.index_col].to_numpy())
                for table_idx, data in df_groups
            ]

    def _gather_data(self, data, as_df):
        data = list(data)
        if len(data) == 0:
            data_shape = (0, len(self.features_cols))
            dataset = Dataset(ind=np.array([], dtype=np.int32), X=np.ones(data_shape), y=np.array([]), props=np.array([]))
        elif len(data) == 1:
            dataset = data[0]
        else:
            dataset = Dataset(*concat_arrays(data))
        if as_df:
            return self.dataset_to_df(dataset.ind, dataset.X, dataset.y, dataset.props).set_index(self.index_col)
        else:
            return dataset

    def _get_by_nodes(
        self, nodes: Iterable, as_df: bool = False, with_props: bool = False, with_removed: bool = False
    ) -> Union[pd.DataFrame, Dataset]:
        """
        Fetch dataset for given nodes.

        Parameters
        ----------
        nodes : Iterable
            nodes_ids for which data rows are fetched

        as_df : bool, default=False
            True: return rows as a pandas DataFrame
            False (default): return a tuple of indices, X, y

        with_props : bool, default=False
            if we return the props of the indexes

        with_removed : bool, default=False
            if we return the removed indexes too

        Returns
        -------
        Union[pd.DataFrame, Dataset]
            indices, X, y as a tuple or as pandas data frame
        """
        with self._get_connection() as con, self._get_connection_h5() as con_arr:
            def _get(node_id):
                table_name = _get_table_name_by_node_id(node_id)
                group = con.get_node(self.table_root_path)
                has_y = 'y' in group
                if with_props:
                    with self._get_connection_pd() as con_pd:
                        node = f'props/{table_name}'
                        props_df = con_pd[node] if node in con_pd else None

                X = group.X[table_name][:]

                if self.data_params_internal.array_features_ is not None and len(
                        self.data_params_internal.array_features_) > 0:
                    X = X.astype(object)

                    for array_index, array_name in [(col_idx, col_name) for col_idx, col_name in enumerate(
                            self.features_cols) if col_idx in self.data_params_internal.array_features_]:
                        arr_group_path = f'{self.table_root_path}/Array/{array_name}'
                        arr_group = con_arr.get(arr_group_path)
                        array_feature_dset = arr_group.get(table_name)
                        array_feature = np.array(array_feature_dset[:])
                        X = np.insert(X, array_index, array_feature, axis=1)

                dset = Dataset(
                    ind=np.array(group.idx[table_name][:]),
                    X=X,
                    y=np.array(group.y[table_name][:].astype(self.data_params.target.dtype)) if has_y else None,
                    props=np.array(props_df) if with_props and props_df is not None else None,
                )
                return dset

            data = map(_get, nodes)
            dataset = self._gather_data(data, as_df)
            if not with_removed:
                ind, dataset = self._exclude_removed(dataset.ind, dataset)
            return dataset

    def _get_by_index(self, indices: Iterable, as_df=False, with_props=False, with_removed=False) -> Union[pd.DataFrame, Dataset]:
        """
        Fetch dataset for given indices.

        Parameters
        ----------
        indices: 1d array, required
            ids for which data rows are fetched
        as_df: boolean, optional
            True: return rows as a pandas DataFrame
            False (default): return a tuple of indices, X, y

        Returns
        -------
        indices, X, y as a tuple or as pandas data frame
        """
        if not with_removed:
            indices = self._exclude_removed(indices)
        indices_groups = self._resolve_idx(indices)
        use_threading = False  # threading is currently switched off as it is not stable.

        # Internal method for slicing relevant samples data
        def gen_data(table_name, group, idx, ind, con_props, con_arr):
            has_y = 'y' in group
            node = f'props/{table_name}'
            props_df = con_props[node] if with_props and node in con_props else None

            X_table = group.X[table_name][:]

            if len(idx) > SLICE_THRESHOLD * X_table.shape[0]:
                X = np.asarray(X_table)[idx, :]
            else:
                X = np.concatenate([X_table[chunk, :] for chunk in helpers.arr_to_chunks(idx, SLICE_SIZE)])

            if self.data_params_internal.array_features_ is not None and len(self.data_params_internal.array_features_) > 0:
                X = X.astype(object)
                for array_index, array_name in [(col_idx, col_name) for col_idx, col_name in enumerate(
                            self.features_cols) if col_idx in self.data_params_internal.array_features_]:
                    arr_group_path = f'{self.table_root_path}/Array/{array_name}'
                    arr_group = con_arr.get(arr_group_path)
                    array_feature_dset = arr_group.get(table_name)
                    if len(idx) > SLICE_THRESHOLD * array_feature_dset.shape[0]:
                        array_feature = np.array(array_feature_dset)[idx]
                    else:
                        array_feature = np.concatenate([array_feature_dset[chunk] for chunk in helpers.arr_to_chunks(idx,SLICE_SIZE)])
                    X = np.insert(X, array_index, array_feature, axis=1)

            return Dataset(
                ind=ind,
                X=X,
                y=np.array(group.y[table_name][:][idx].astype(self.data_params.target.dtype)) if has_y else None,
                props=np.array(props_df.iloc[idx]) if props_df is not None else None,
            )

        if use_threading:
            # pytable is not thread safe. Use locking for opening and closing file
            # https://www.pytables.org/cookbook/threading.html
            lock = threading.Lock()

            def _get(g):
                table_name, idx, ind = g
                with lock:
                    con = self._get_connection()

                group = con.get_node(self.table_root_path)
                result = gen_data(table_name, group, idx, ind)
                with lock:
                    con.close()
                return result

            data = joblib.Parallel(n_jobs=50, backend='threading')(joblib.delayed(_get)(g) for g in indices_groups)
        else:
            with self._get_connection() as con, self._get_connection_pd() as con_pd, self._get_connection_h5() as con_h5:
                def _get(g):
                    table_name, idx, indices = g
                    group = con.get_node(self.table_root_path)
                    return gen_data(table_name, group, idx, indices, con_pd, con_h5)

                data = [_get(g) for g in indices_groups]

        result = self._gather_data(data, as_df)

        # Decode categorical y
        if self.data_params_internal.y_mixed_types:
            y_decoded = self.decode_categorical_y(result.y)
            if as_df:
                result['y'] = y_decoded
            else:
                result = result._replace(y=y_decoded)

        return result

    def _get_orig_by_index(self, indices: Iterable, with_index=False):
        """
        Fetch dataset for given indices.

        Parameters
        ----------
        indices: 1d array, required
            ids for which data rows are fetched

        Returns
        -------
        indices, X, y as a tuple or as pandas data frame
        """
        indices = self._exclude_removed(indices)
        tables_groups = self._resolve_idx(indices)
        with self._get_connection_pd() as con:
            df = None
            for table_name, idx, _ in tables_groups:
                node = f'{self.orig_table_root_path}/{table_name}'
                node_df = con[node].iloc[idx]
                df = node_df if df is None else pd.concat([df, node_df])
            if not with_index:
                df.drop(self.schema.data_schema.index_col, inplace=True, axis=1)
                df.reset_index(drop=True, inplace=True)
            return df

    def _read_data(self, chunk_size: int, condition: str = None) -> Iterable:
        """
        Read data from hdf5 file

        Parameters
        ----------
        chunk_size: hint for an optimized fetching
        condition: string, optional
            TODO: currently not supported

        Returns
        -------
        An iterator of a processed dataset (indices, X, y, props)

        """
        # Find how many rows out there
        with self._get_connection_pd() as con:
            n_samples = con[self.indices_table_path].shape[0]

        # Read in chunks
        start = 0
        while start < n_samples:
            end = start + chunk_size
            with self._get_connection_pd() as con:
                indices = con[self.indices_table_path][self.index_col][start:end].to_numpy()
            yield self._get_by_index(indices)
            start = end

    def _clear_buffer(self):

        table_name = self.TABLE_BUFFER

        with self._get_connection_pd('a') as con:
            if self.indices_buffer_table_path in con:
                con.remove(self.indices_buffer_table_path)
                self.index_cache = None

        with self._get_connection('a') as con:
            group = con.get_node(self.table_root_path)
            for t in ('X', 'y'):
                if t in group and table_name in group[t]:
                    group[t][table_name].remove()

    def _close(self):
        pass  # TODO: are there any cleanups?

    def _get_params(self, results):
        if self._db_file_bk:
            results['db_file'] = self._db_file_bk
        # check if seq_column granularity is a function
        if self.data_params.seq_column and callable(self.data_params.seq_column['granularity']):
            # if it is a function, serialise it
            granularity = self.data_params.seq_column['granularity']
            serialized_function = self.data_params_internal.seq_granularity_serialized_ or serialize_function(func=granularity)
            results['data_params']['seq_column']['granularity'] = serialized_function
            results['data_params_internal']['seq_granularity_'] = serialized_function
            results['data_params_internal']['seq_granularity_serialized_'] = serialized_function

    def _save(self, save_dir):
        """Copy database file to an input directory"""
        db_file = pathlib.Path(self.db_file)
        dest_file = self.storage_manager.joinpath(save_dir, db_file.name)
        if dest_file != str(db_file):
            self.storage_manager.local_to_storage(self.db_file, dest_file)

        self._db_file_bk = self.storage_manager.name(dest_file)

    @classmethod
    def _load(cls, schema: DMSchemaHDF5, working_directory, load_dir):
        """Copy database file from load_dir to working_directory and initialize class"""
        storage_manager = StorageManager()
        db_file = schema.db_file
        if not storage_manager.is_absolute(str(db_file)):
            db_file = storage_manager.joinpath(str(load_dir), str(db_file))
        dest_file = storage_manager.joinpath(str(working_directory), str(storage_manager.name(db_file)))
        if dest_file != db_file and storage_manager.exists(str(db_file)):
            try:
                storage_manager.storage_to_local(str(db_file), str(dest_file))
            except OSError:
                raise ValueError(
                    "Loading of a saved coreset requires existance of sufficient free disk space for copying the saved content in the `working_directory` folder."
                )

        schema.db_file = str(dest_file)

        return cls(schema, working_directory=working_directory)
