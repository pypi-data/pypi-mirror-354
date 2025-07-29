from ast import Dict
import copy
import dataclasses
import inspect
import io
import itertools
import json
import os
import pathlib
import queue
import typing
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Callable, Union, Iterator, Optional, List, Tuple

import joblib
import numpy as np
import pandas as pd

from dataheroes.data.storage.storage_manager import StorageManager


def dicts_to_dataclasses(instance: dataclasses.dataclass) -> dataclasses.dataclass:
    """
    Helper method for converting all fields of type `dataclass` into an instance of the
    specified data class

    Parameters
    ----------
    instance: dataclass object

    Returns
    -------
    updated instance
    """

    for f in dataclasses.fields(type(instance)):
        value = getattr(instance, f.name)
        if dataclasses.is_dataclass(f.type) and isinstance(value, dict):
            setattr(instance, f.name, f.type(**value))
        elif value and len(typing.get_args(f.type)) > 0 and dataclasses.is_dataclass(typing.get_args(f.type)[0]):
            if not dataclasses.is_dataclass(value[0]):
                list_cls = typing.get_args(f.type)[0]
                setattr(instance, f.name, [dicts_to_dataclasses(list_cls(**v)) for v in value])
    return instance


def dataclass_to_dict(obj, dict_factory=dict) -> Union[dict, str]:
    """
    Our recursive implementation for dataclasses._asdict_inner for supporting a complex dataclasses.
    The method Supports class level implementation of dict_factory.
    To apply class level logic, implement  _dict_factory method that returns a dictionary.

    Parameters
    ----------
    obj:
    dict_factory: optional, factory class/method that returns a dictionary like object.

    Returns
    -------
    dict
    """
    if dataclasses.is_dataclass(obj):
        result = []
        for f in dataclasses.fields(obj):
            value = dataclass_to_dict(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return obj.dict_factory(result) if hasattr(obj, 'dict_factory') else dict_factory(result)
    elif isinstance(obj, (list, tuple)):
        return type(obj)(dataclass_to_dict(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((dataclass_to_dict(k), dataclass_to_dict(v, dict_factory)) for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


class DMThreadPoolExecutor(ThreadPoolExecutor):
    """
    Implementation of ThreadPoolExecutor with a queue
    """

    def __init__(self, *args, queue_maxsize=0, **kwargs):
        super(DMThreadPoolExecutor, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue(maxsize=queue_maxsize)


def transaction(func):
    """
    A wrapper method for functions updating the database.
    Use locking mechanism to make sure only one update is done at a time.
    When an error occurred, the whole process should stop.
    Call class method to handle errors prior starting the transaction.

    Parameters
    ----------
    func: callable
        The function to execute

    Returns
    -------
    func results

    """

    def _execute(self, *args, **kwargs):
        self._check_transaction_errors()
        with self.tran_lock:
            return func(self, *args, **kwargs)

    return _execute


def iter_first(it):
    it = iter(it)
    i = next(it)
    return i, itertools.chain([i], it)


def file_path_to_iterable(file_path):
    try:
        if isinstance(file_path, (str, os.PathLike)):
            return iter([file_path])
        else:
            iterator_to_return = iter(file_path)
    except:
        raise TypeError(f"Invalid file path type: '{file_path.__class__.__name__}'. Expected os.PathLike, str or an iterable of os.PathLike, str")

    try:
        _, iterator_to_return = iter_first(iterator_to_return)
    except StopIteration:
        raise ValueError("Empty list provided for the `file_path` argument")
    return iterator_to_return


def file_path_to_files(file_path, storage_manager: StorageManager, *, include_dirs=False, sort_by_name=True) -> Iterator:
    """
    Return an iterator of final file names based on input file_path. No recursive search.

    Parameters
    ----------
    file_path: string or path-like
        file or directory.

    storage_manager: StorageManager instance.

    include_dirs: bool, optional, default False.
        True: only files are returned, even if file_path includes subdirectories.
        False: return also subdirectories.

    sort_by_name: bool, optional, default False
        For directory -
            True: return files sorted by name ascending
            False: return files based on os fetch logic.

    Returns
    -------
    iterator:
        when input is a file - a list of 1 element
        when input is a directory - a list of files in the directory.

    """
    paths = file_path_to_iterable(file_path)

    def _to_files(path):
        files_ = []
        if storage_manager.exists(path):
            files_ = storage_manager.iterdir(path, include_dirs=include_dirs)
        for f in files_:
            yield f

    result = itertools.chain.from_iterable(map(_to_files, paths))
    if sort_by_name:
        result = iter(sorted(result))
    test_iterator, result = itertools.tee(result, 2)
    sentinel = object()
    first_element = next(test_iterator, sentinel)
    if first_element is sentinel:
        raise ValueError("A nonexistent file or an empty folder were provided for the `file_path` argument.")
    return result

def resolve_reader_chunk_size_param_name(reader_f: Callable) -> Optional[str]:
    """
    Given some reader method,
    return the name of the parameter to use for reading file in batches.

    Parameters
    ----------
    reader_f: callable

    Returns
    -------
    str: optional
        name of the reader's input parameter if resolved or None if not resolved.

    """
    if reader_f in [pd.read_csv, pd.read_hdf]:
        return 'chunksize'

    reader_args = [param.name for param in inspect.signature(reader_f).parameters.values()]
    for name in ['chunksize']:
        if name in reader_args:
            return name
    return None


def to_ranges(numbers: List[int]) -> List[Tuple[int, int]]:
    """
    Converts a list of numbers to a list of ranges.

    Parameters
    ----------
    numbers (List[int]): The list of numbers to be converted to ranges.

    Returns
    -------
    List[Tuple[int, int]]: A list of tuples, where each tuple represents a range.
    """

    ranges = []
    for k, g in itertools.groupby(enumerate(numbers), lambda i_x: i_x[0] - i_x[1]):
        group = list(map(lambda x: x[1], g))
        ranges.append((group[0], group[-1]))
    return ranges


def to_df_target(df):
    df = list(df_to_iterable(df))
    if len(df) == 1:
        return df[0], None
    return df


def df_to_iterable(df):
    return [df] if is_dataset(df) else df


def to_chunks(iterable, size):
    ''' split iteration to batches '''
    sourceiter = iter(iterable)
    while True:
        batchiter = itertools.islice(sourceiter, size)
        yield itertools.chain([batchiter.next()], batchiter)


def arr_to_chunks(arr, max_size):
    n_rows = len(arr)
    if n_rows == 0:
        return []
    n_chunks = 1 if len(arr) <= max_size else (1 + len(arr) // max_size)
    return np.array_split(arr, n_chunks)


def is_object_dtype(v: np.dtype):
    return np.issubdtype(v, np.object_)


def is_dtype_numeric(v: np.dtype):
    return np.issubdtype(v, np.number)

def is_dtype_floating(v: np.dtype):
    return np.issubdtype(v, np.floating)


def to_dtype(v) -> np.dtype:
    """convert input to a numpy dtype"""
    try:
        # normal conversion
        return np.dtype(np.dtype(v).type)
    except:
        pass

    try:
        # pandas extended types like BooleanDtype
        return np.dtype(v.numpy_dtype.type)
    except:
        pass

    try:
        # pandas extended types like StringDtype
        return np.dtype(v.type)
    except:
        pass

    # if nothing works, return object dtype
    return np.dtype(object)


def is_dataset(v) -> bool:
    """return True if input value is a dataset else false"""
    return hasattr(v, 'ndim') and hasattr(v, 'shape')


def is_pd_array(arr) -> bool:
    """return True if input value is one of pandas DataFrame or Series"""
    return issubclass(arr.__class__, (pd.DataFrame, pd.Series))


def to_df(arr) -> pd.DataFrame:
    """Convert arr to a pandas DataFrame if not already"""
    if not isinstance(arr, pd.DataFrame):
        arr = pd.DataFrame(arr)
    return arr


def is_ndarray(arr) -> bool:
    """return True if input value is not a numpy array"""
    return isinstance(arr, np.ndarray)


def to_ndarray(arr):
    """Convert arr to a numpy array if not already"""
    if not is_ndarray(arr):
        arr = np.array(arr)
    return arr


def y_to1d(y):
    """Convert y to a 1d array if not already"""
    if y.ndim == 2:
        y = y[:, 0]
    return y


def _get_inf_nan_indexes(arr):
    """
    Helper method for getting indexes of inf and nan values in an array
    """
    indexes = []

    if arr.dtype == object:  # Check if dtype is object
        for idx, value in enumerate(arr):
            if isinstance(value, float):
                if np.isnan(value) or np.isinf(value):
                    indexes.append(idx)
            elif isinstance(value, str):
                if value == 'np.nan' or value == 'np.inf' or value == '-np.inf':
                    indexes.append(idx)
            elif value is None:
                indexes.append(idx)
    elif arr.dtype in [np.float32, np.float64, np.int32, np.int64]:
        # For non-object dtype, use np.isnan and np.isinf directly
        indexes.extend(np.where(np.isnan(arr) | np.isinf(arr))[0])

    return indexes


def is_unsupported_hdf5_array(arr):
    """
    Check if a numpy array is of an unsupported type for HDF5.

    Parameters:
    arr (numpy.ndarray): The numpy array to check.

    Returns:
    bool: True if the array is of an unsupported type, False otherwise.
    """
    if arr.dtype.kind == 'O':
        try:
            # Attempt to cast the object array elements to floats
            np.array(arr, dtype=np.float64)
        except (ValueError, TypeError):
            return True
    return False


def _update_n_represents(original, new, is_classification):
    """
    Helper method for updating self.n_represents_diff
    """
    # add to self.n_represents_diff if it exists
    if original is not None:
        if is_classification:
            for k, v in new.items():
                if k in original:
                    original[k] -= v
                else:
                    original[k] = v
            original = {k: v for k, v in original.items() if v != 0}
        else:
            original -= new
    else:
        original = new
    return original


def get_feature_slice(dset, cat_feature_idx):
    if isinstance(dset, pd.DataFrame):
        return dset.iloc[:, cat_feature_idx]
    else:
        return dset[:, cat_feature_idx]
    
def joblib_dumps(py_obj: Any) -> bytes:
    data = io.BytesIO()
    joblib.dump(py_obj, data)
    data.seek(0)
    return data.getvalue()

def jsonobj_to_bytes(json_obj: Dict, cls = json.JSONEncoder) -> bytes:
    data = io.BytesIO()
    data.write(json.dumps(json_obj, cls=cls).encode())
    data.seek(0)
    return data.getvalue()

def np_to_bytes(array: Union[np.ndarray, List[np.ndarray], "Dataset"]) -> bytes:
    # This method also works for Dataset instances
    # but can't add the type hints due to circular imports
    data = io.BytesIO()
    if isinstance(array, np.ndarray):
        array = [array]
    np.savez(data, *array)
    data.seek(0)
    return data.getvalue()

def localpath_to_bytestream(path: Union[str, pathlib.Path]) -> io.BytesIO:
    result = io.BytesIO()
    with open(path, "rb") as f:
        result.write(f.read())
    result.seek(0)
    return result

def bytes_to_bytestream(data: bytes) -> io.BytesIO:
    result = io.BytesIO()
    result.write(data)
    result.seek(0)
    return result
