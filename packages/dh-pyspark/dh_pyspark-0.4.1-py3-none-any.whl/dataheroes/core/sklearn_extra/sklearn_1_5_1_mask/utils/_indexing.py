# ######################################################################################################################
# DH Specific: stripped to minimum
# ######################################################################################################################

import sys
from collections import UserList
from itertools import compress

import numpy as np
from scipy.sparse import issparse

from ._array_api import _is_numpy_namespace, get_namespace
from .validation import (
    _is_arraylike_not_scalar,
    _is_pandas_df,
    _is_polars_df_or_series,
    _use_interchange_protocol,
)


def _array_indexing(array, key, key_dtype, axis):
    """Index an array or scipy.sparse consistently across NumPy version."""
    xp, is_array_api = get_namespace(array)
    if is_array_api:
        return xp.take(array, key, axis=axis)
    if issparse(array) and key_dtype == "bool":
        key = np.asarray(key)
    if isinstance(key, tuple):
        key = list(key)
    return array[key, ...] if axis == 0 else array[:, key]


def _pandas_indexing(X, key, key_dtype, axis):
    """Index a pandas dataframe or a series."""
    if _is_arraylike_not_scalar(key):
        key = np.asarray(key)

    if key_dtype == "int" and not (isinstance(key, slice) or np.isscalar(key)):
        # using take() instead of iloc[] ensures the return value is a "proper"
        # copy that will not raise SettingWithCopyWarning
        return X.take(key, axis=axis)
    else:
        # check whether we should index with loc or iloc
        indexer = X.iloc if key_dtype == "int" else X.loc
        return indexer[:, key] if axis else indexer[key]


def _list_indexing(X, key, key_dtype):
    """Index a Python list."""
    if np.isscalar(key) or isinstance(key, slice):
        # key is a slice or a scalar
        return X[key]
    if key_dtype == "bool":
        # key is a boolean array-like
        return list(compress(X, key))
    # key is a integer array-like of key
    return [X[idx] for idx in key]


def _polars_indexing(X, key, key_dtype, axis):
    """Indexing X with polars interchange protocol."""
    # Polars behavior is more consistent with lists
    if isinstance(key, np.ndarray):
        # Convert each element of the array to a Python scalar
        key = key.tolist()
    elif not (np.isscalar(key) or isinstance(key, slice)):
        key = list(key)

    if axis == 1:
        # Here we are certain to have a polars DataFrame; which can be indexed with
        # integer and string scalar, and list of integer, string and boolean
        return X[:, key]

    if key_dtype == "bool":
        # Boolean mask can be indexed in the same way for Series and DataFrame (axis=0)
        return X.filter(key)

    # Integer scalar and list of integer can be indexed in the same way for Series and
    # DataFrame (axis=0)
    X_indexed = X[key]
    if np.isscalar(key) and len(X.shape) == 2:
        # `X_indexed` is a DataFrame with a single row; we return a Series to be
        # consistent with pandas
        pl = sys.modules["polars"]
        return pl.Series(X_indexed.row(0))
    return X_indexed


def _determine_key_type(key, accept_slice=True):
    """Determine the data type of key.

    Parameters
    ----------
    key : scalar, slice or array-like
        The key from which we want to infer the data type.

    accept_slice : bool, default=True
        Whether or not to raise an error if the key is a slice.

    Returns
    -------
    dtype : {'int', 'str', 'bool', None}
        Returns the data type of key.
    """
    err_msg = (
        "No valid specification of the columns. Only a scalar, list or "
        "slice of all integers or all strings, or boolean mask is "
        "allowed"
    )

    dtype_to_str = {int: "int", str: "str", bool: "bool", np.bool_: "bool"}
    array_dtype_to_str = {
        "i": "int",
        "u": "int",
        "b": "bool",
        "O": "str",
        "U": "str",
        "S": "str",
    }

    if key is None:
        return None
    if isinstance(key, tuple(dtype_to_str.keys())):
        try:
            return dtype_to_str[type(key)]
        except KeyError:
            raise ValueError(err_msg)
    if isinstance(key, slice):
        if not accept_slice:
            raise TypeError(
                "Only array-like or scalar are supported. A Python slice was given."
            )
        if key.start is None and key.stop is None:
            return None
        key_start_type = _determine_key_type(key.start)
        key_stop_type = _determine_key_type(key.stop)
        if key_start_type is not None and key_stop_type is not None:
            if key_start_type != key_stop_type:
                raise ValueError(err_msg)
        if key_start_type is not None:
            return key_start_type
        return key_stop_type
    # TODO(1.9) remove UserList when the force_int_remainder_cols param
    # of ColumnTransformer is removed
    if isinstance(key, (list, tuple, UserList)):
        unique_key = set(key)
        key_type = {_determine_key_type(elt) for elt in unique_key}
        if not key_type:
            return None
        if len(key_type) != 1:
            raise ValueError(err_msg)
        return key_type.pop()
    if hasattr(key, "dtype"):
        xp, is_array_api = get_namespace(key)
        # NumPy arrays are special-cased in their own branch because the Array API
        # cannot handle object/string-based dtypes that are often used to index
        # columns of dataframes by names.
        if is_array_api and not _is_numpy_namespace(xp):
            if xp.isdtype(key.dtype, "bool"):
                return "bool"
            elif xp.isdtype(key.dtype, "integral"):
                return "int"
            else:
                raise ValueError(err_msg)
        else:
            try:
                return array_dtype_to_str[key.dtype.kind]
            except KeyError:
                raise ValueError(err_msg)
    raise ValueError(err_msg)


def _safe_indexing(X, indices, *, axis=0):
    """Return rows, items or columns of X using indices.

    .. warning::

        This utility is documented, but **private**. This means that
        backward compatibility might be broken without any deprecation
        cycle.

    Parameters
    ----------
    X : array-like, sparse-matrix, list, pandas.DataFrame, pandas.Series
        Data from which to sample rows, items or columns. `list` are only
        supported when `axis=0`.
    indices : bool, int, str, slice, array-like
        - If `axis=0`, boolean and integer array-like, integer slice,
          and scalar integer are supported.
        - If `axis=1`:
            - to select a single column, `indices` can be of `int` type for
              all `X` types and `str` only for dataframe. The selected subset
              will be 1D, unless `X` is a sparse matrix in which case it will
              be 2D.
            - to select multiples columns, `indices` can be one of the
              following: `list`, `array`, `slice`. The type used in
              these containers can be one of the following: `int`, 'bool' and
              `str`. However, `str` is only supported when `X` is a dataframe.
              The selected subset will be 2D.
    axis : int, default=0
        The axis along which `X` will be subsampled. `axis=0` will select
        rows while `axis=1` will select columns.

    Returns
    -------
    subset
        Subset of X on axis 0 or 1.

    Notes
    -----
    CSR, CSC, and LIL sparse matrices are supported. COO sparse matrices are
    not supported.

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.utils import _safe_indexing
    >>> data = np.array([[1, 2], [3, 4], [5, 6]])
    >>> _safe_indexing(data, 0, axis=0)  # select the first row
    array([1, 2])
    >>> _safe_indexing(data, 0, axis=1)  # select the first column
    array([1, 3, 5])
    """
    if indices is None:
        return X

    if axis not in (0, 1):
        raise ValueError(
            "'axis' should be either 0 (to index rows) or 1 (to index "
            " column). Got {} instead.".format(axis)
        )

    indices_dtype = _determine_key_type(indices)

    if axis == 0 and indices_dtype == "str":
        raise ValueError("String indexing is not supported with 'axis=0'")

    if axis == 1 and isinstance(X, list):
        raise ValueError("axis=1 is not supported for lists")

    if axis == 1 and hasattr(X, "shape") and len(X.shape) != 2:
        raise ValueError(
            "'X' should be a 2D NumPy array, 2D sparse matrix or "
            "dataframe when indexing the columns (i.e. 'axis=1'). "
            "Got {} instead with {} dimension(s).".format(type(X), len(X.shape))
        )

    if (
        axis == 1
        and indices_dtype == "str"
        and not (_is_pandas_df(X) or _use_interchange_protocol(X))
    ):
        raise ValueError(
            "Specifying the columns using strings is only supported for dataframes."
        )

    if hasattr(X, "iloc"):
        # TODO: we should probably use _is_pandas_df_or_series(X) instead but this
        # would require updating some tests such as test_train_test_split_mock_pandas.
        return _pandas_indexing(X, indices, indices_dtype, axis=axis)
    elif _is_polars_df_or_series(X):
        return _polars_indexing(X, indices, indices_dtype, axis=axis)
    elif hasattr(X, "shape"):
        return _array_indexing(X, indices, indices_dtype, axis=axis)
    else:
        return _list_indexing(X, indices, indices_dtype)
