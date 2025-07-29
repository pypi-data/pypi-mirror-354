import abc
import functools
import pathlib
import shutil
import sqlite3
import uuid
import threading

import numpy as np
import pandas as pd
from pandas.io.sql import SQLiteTable, pandasSQL_builder
from typing import Iterable, Union, Optional

from .common import DMSchemaSql, DMSchemaSqlite, Dataset
from .manager import DataManagerBase
from .helpers import transaction, DMThreadPoolExecutor
from ..utils import user_warning
from ..core.helpers import align_arrays_by_key


class DataManagerSql(DataManagerBase):
    """
    Parameters
    ----------
    schema: DMSchemaSql, optional
        Data manager schema relevant for integrating with an sql database
    connector: sql server connection handle, optional
        True: save also original raw data

    """
    schema_cls = DMSchemaSql
    MAX_QUERY_VARIABLES_NUMBER = None

    def __init__(self, schema: DMSchemaSql = None, connector=None, **kwargs):
        super(DataManagerSql, self).__init__(schema, **kwargs)
        self._connector = connector

    # TODO: find a way to clean when object is destroy. __del__ is called after all class attributes were deleted.
    # def __del__(self):
    #     self._close()

    @property
    def connector(self):
        return self._connector

    @property
    def table_name(self):
        return self.dataset_schema.table_name

    @abc.abstractmethod
    def create_table_from_df(self, table_name, df: pd.DataFrame, keys: Union[list, str] = None):
        pass

    def add(self, table_name, data: pd.DataFrame, index=True, async_mode=False):
        """
        Add new rows to database. Method is expected to handle duplicate keys.
        Parameters
        ----------
        table_name: string
        data: DataFrame
        index: should index be stored
        async_mode: should save by done synchronously or in the background

        Returns
        -------
        None

        """
        raise NotImplementedError

    def update_data(self, table_name, data: pd.DataFrame):
        raise NotImplementedError

    # =============================
    # Subclass methods implementation
    # =============================

    def _get_connection(self):
        return self.connector

    def _prepare_schema(self):
        """
        Creates database tables for storing processed dataset and optionally original data.
        """
        columns = self.dataset_schema.columns
        df = pd.DataFrame(columns=[c.name for c in columns]).astype(dtype={c.name: c.dtype for c in columns})
        self.create_table_from_df(self.table_name, df, keys=self.index_col)

    def _read_data(self, chunk_size: int, condition: str = None) -> Iterable:
        """
        perform an sql query to fetch working data into a pandas DataFrame
        apply preprocessing on fetched rows.

        Parameters
        ----------
        chunk_size: hint for an optimized fetching
        condition: string, optional
            an sql condition for filtering rows

        Returns
        -------
        An iterator of a processed dataset (indices, X, y)

        """

        sql = f'SELECT * FROM {self.table_name}'
        if condition:
            sql += f' WHERE {condition}'
        datasets = pd.read_sql(sql, self._get_connection(), chunksize=chunk_size)
        datasets = self.preprocess(datasets)
        return datasets

    def _replace(self, indices: np.array, X=None, y=None):
        db_indices, db_X, db_y, db_props = self._get_by_index(indices)[:4]
        _, (indices, X, y, props) = align_arrays_by_key((db_indices,), (indices, X, y, db_props))
        if X is not None:
            db_X = X
        if y is not None:
            db_y = y
        if props is not None:
            db_props = props

        df = self.dataset_to_df(db_indices, db_X, db_y, db_props)

        self.update_data(self.table_name, df)

    def _remove(self, s):
        return
    
    def _remove_nodes(self, node_ids):
        raise NotImplementedError()

    def _get_removed(self):
        return np.array([])

    def _save_selected_samples(
            self,
            dataset: Dataset,
            indices: Optional[np.ndarray],
            async_mode=False, node_id=None,
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

        Returns
        -------
        None

        """
        dataset = Dataset(*dataset)
        # get a subset of dataset based on selected indices.
        if indices is not None:
            idxs_ = np.isin(dataset.ind, indices)
            dataset = tuple(a[idxs_] if a is not None else None for a in dataset)

        # add selected samples to database
        dataset = Dataset(*dataset)
        df = self._dataset_to_df(dataset.ind, dataset.X, dataset.y, dataset.props).set_index(self.index_col)
        self.add(self.table_name, df, async_mode=async_mode)
        if self.schema.save_orig:
            df_original = pd.DataFrame(self._np_column_stack(dataset.orig, dataset.orig_target))  # cases where input data is separated.
            if self.schema.data_schema.columns is not None:
                df_original.columns = [column.name for column in self.schema.data_schema.columns]
            df_original[self.schema.data_schema.index_col] = dataset.ind
            df_original.set_index(self.schema.data_schema.index_col)
            self.add(self.schema.data_schema.table_name, df_original, index=False)

    def _query_params_to_chunks(self, indices):
        indices = np.array(indices)
        if self.MAX_QUERY_VARIABLES_NUMBER and len(indices) > self.MAX_QUERY_VARIABLES_NUMBER:
            chunks = np.array_split(indices, (len(indices) // self.MAX_QUERY_VARIABLES_NUMBER) + 1)
        else:
            chunks = [indices]
        return chunks

    def _get_by_index(self, indices: Iterable, as_df=False, with_props=False, with_removed=False) -> Union[pd.DataFrame, tuple]:
        """
        Tree exit point for fetching dataset based on ids.

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

        sql = f'SELECT * FROM {self.schema.dataset_schema.table_name}'

        def _fetch(ind):
            ind = ind.tolist()
            cond = f' WHERE "{self.index_col}" IN ({",".join("?" * len(ind))})'
            return pd.read_sql(sql + cond, self._get_connection(), index_col=self.index_col, params=ind)

        if indices is not None:
            # Split to chunks when number of indices exceeds the maximum variables limitation.
            chunks = self._query_params_to_chunks(indices)
            df = pd.concat(map(_fetch, chunks))
        else:
            df = pd.read_sql(sql, self._get_connection(), index_col=self.index_col)

        if as_df:
            return df
        else:
            return self.df_to_dataset(df)

    def _get_orig_by_index(self, indices: Iterable, with_index=False):

        sql = f"SELECT * FROM {self.schema.data_schema.table_name}"

        def _fetch(ind):
            ind = ind.tolist()
            cond = f' WHERE "{self.index_col}" IN ({",".join("?" * len(ind))})'
            return pd.read_sql(sql + cond, self._get_connection(), params=ind)

        if indices is not None:
            # Split to chunks when number of indices exceeds the maximum variables limitation.
            chunks = self._query_params_to_chunks(indices)
            df = pd.concat(map(_fetch, chunks))
        else:
            df = pd.read_sql(sql, self._get_connection())

        if not with_index:
            del df[self.schema.data_schema.index_col]
        return df

    def _close(self):
        if self._connector:
            try:
                self._connector.close()
            except BaseException as e:
                user_warning(f"Error closing sql connection: {e}")


def sqlite_version():
    return sqlite3.connect(':memory:').execute("select sqlite_version();").fetchone()[0]


class DataManagerSqlite(DataManagerSql):
    """
    manager using sqlite3 builtin python library
    """
    schema_cls = DMSchemaSqlite
    MAX_COLUMNS = 1000
    MAX_QUERY_VARIABLES_NUMBER = 999 if sqlite_version() < '3.32.0' else 100_000
    copy_using_sqlite_backup = True
    async_save = True
    async_save_queue_maxsize = 10
    connection_timeout = 60*30  # wait fo any transaction to be completed

    def __init__(self, schema: DMSchemaSqlite = None, **kwargs):
        super(DataManagerSqlite, self).__init__(schema, **kwargs)
        self._db_file_bk = None
        self._async_executor: Optional[DMThreadPoolExecutor] = None
        self._init_async_executor()
        if self.in_memory:
            self._connector = self._connect()
        self.tran_lock = threading.RLock()
        self._async_error = None

    @staticmethod
    def sql_version():
        return sqlite3.connect(':memory:').execute("select sqlite_version();").fetchone()[0]

    @property
    def connector(self):
        return self._connector or self._connect()

    @connector.setter
    def connector(self, v):
        self._connector = v

    @property
    def db_file(self):
        return self.schema.db_file

    @db_file.setter
    def db_file(self, value):
        self.schema.db_file = str(value) if value else None

    @property
    def in_memory(self):
        return self.schema.in_memory

    @transaction
    def create_table_from_df(self, table_name, df: pd.DataFrame, keys=None):
        """
        Use pandas library classes to create an sqlite table based on the input data frame structure

        Parameters
        ----------
        table_name: string, required
        df: DataFrame, required.
        keys: list or string, optional
            primary key columns of the table

        Returns
        -------
        None

        """
        con = self._get_connection()
        pandas_sql = pandasSQL_builder(con, schema=None)
        table = SQLiteTable(name=table_name, frame=df, pandas_sql_engine=pandas_sql, index=False, keys=keys)
        if table.exists():
            pandas_sql.drop_table(table_name)
        table.create()

    def exists(self, table_name) -> bool:
        """
        check if table exists in database

        Parameters
        ----------
        table_name

        Returns
        -------
        boolean

        """
        con = self._get_connection()
        return bool(con.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';").fetchone())

    @transaction
    def add(self, table_name, data: pd.DataFrame, index=True, *, async_mode=False):
        """
        SqlLite implementation for inserting new instances to the database asynchronously

        Parameters
        ----------
        table_name: string
        data: DataFrame
        index: should index be stored
        async_mode: should save by done synchronously or in the background

        Returns
        -------
        None

        """

        _add = functools.partial(self._add, table_name, data, index)

        if self.async_save:
            result = self._async_executor.submit(_add)
            result.add_done_callback(self._handle_async_error)
            if not async_mode:
                self.commit()
        else:
            _add()

    def _add(self, table_name, data: pd.DataFrame, index=True):
        """
        SqlLite implementation for inserting new instances to the database.
        Use INSERT OR IGNORE to skip existing instances
        Parameters
        ----------
        table_name: string
        data: DataFrame
        index: should index be stored
        async_mode: should save by done synchronously or in the background

        Returns
        -------
        None

        """

        def insert_method(table_obj, conn, keys, data_iter):
            data_list = list(data_iter)
            if pd.__version__ < '1.1':  # In old pandas version there is no num_rows parameter
                stmt = table_obj.insert_statement()
            else:
                stmt = table_obj.insert_statement(num_rows=1)
            stmt = 'INSERT OR IGNORE' + stmt[6:]  # Do not insert rows if their key already exists in the table.
            conn.executemany(stmt, data_list)
            return conn.rowcount

        con = self._get_connection()
        data.to_sql(table_name, con, if_exists='append', index=index, method=insert_method)

    def _commit(self):
        self._init_async_executor()

    @transaction
    def update_data(self, table_name, data: pd.DataFrame):
        """
        SqlLite  implementation for updating instances in the database.
        Parameters
        ----------
        table_name: string
        data: DataFrame

        Returns
        -------
        None

        """
        tmp_table_name = 'table_' + uuid.uuid4().hex
        # create tmp table with data
        self._add(tmp_table_name, data, False)
        # delete from destination table
        sql_text = f'DELETE FROM {table_name} ' \
                   f'WHERE "{self.data_params.index.name}" IN ' \
                   f'(SELECT "{self.data_params.index.name}" FROM {tmp_table_name});'
        con = self._get_connection()
        con.execute(sql_text)
        # insert into destination table
        con.execute(f'INSERT INTO  {table_name} SELECT * FROM {tmp_table_name};')
        # drop tmp table
        con.execute(f'DROP TABLE  {tmp_table_name};')

    def _save(self, save_dir):
        """
        copy database to an input directory using sqlite3 backup utility or os file copy.
        """
        db_file = pathlib.Path(self.db_file)
        dest_file = pathlib.Path(save_dir, db_file.name)
        if self.in_memory:
            with sqlite3.connect(dest_file) as bk:
                with self._get_connection() as conn:
                    conn.backup(bk)
        elif dest_file != db_file:
            with self._get_connection() as conn:
                if self.copy_using_sqlite_backup:
                    with sqlite3.connect(dest_file) as bk:
                        conn.backup(bk)
                else:
                    conn.close()
                    shutil.copy(db_file, dest_file)
                    self._connect()

        self._db_file_bk = str(dest_file.name)

    @classmethod
    def _load(cls, schema: DMSchemaSqlite, working_directory, load_dir):
        db_file = pathlib.Path(schema.db_file)
        if not db_file.is_absolute():
            db_file = pathlib.Path(load_dir, db_file)
        dest_file = pathlib.Path(working_directory, db_file.name)
        if dest_file != db_file:
            if cls.copy_using_sqlite_backup:
                with sqlite3.connect(db_file) as con, sqlite3.connect(dest_file) as bk:
                    con.backup(bk)
            else:
                shutil.copy(db_file, dest_file)

        schema.db_file = str(dest_file)

        return cls(schema, working_directory=working_directory)

    def _init_async_executor(self):
        if self.async_save:
            if self._async_executor:
                self._async_executor.shutdown()
                self._check_transaction_errors()
            self._async_executor = DMThreadPoolExecutor(max_workers=1, queue_maxsize=self.async_save_queue_maxsize)

    def _handle_async_error(self, r):
        if r and r.exception():
            self._async_error = r.exception()

    def _check_transaction_errors(self):
        if self._async_error:
            error = self._async_error
            self._async_error = None
            raise error

    def _get_params(self, results):
        if self._db_file_bk:
            results['db_file'] = self._db_file_bk
            results['in_memory'] = False

    def _connect(self):
        schema = self.schema
        if schema.in_memory:
            con = sqlite3.connect(':memory:', check_same_thread=False, timeout=self.connection_timeout, isolation_level=None)
        elif schema.db_file:
            pathlib.Path(schema.db_file).parent.mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(schema.db_file, check_same_thread=False, timeout=self.connection_timeout, isolation_level=None)
        else:
            raise RuntimeError("Cannot connect to database. Either in_memory or db_file are required")

        con.execute('PRAGMA journal_mode=WAL;')  # better concurrency https://www.sqlite.org/wal.html
        return con

    def _get_connection(self):
        return self._connect() if not self.in_memory else self._connector

    def _close(self):
        self._commit()
