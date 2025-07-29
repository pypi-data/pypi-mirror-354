import io
import os
import joblib
import base64
import inspect
import textwrap
import numpy as np
import pandas as pd
from typing import Callable, Union

from .data_auto_processor import _find_categorical_types, _detect_types_numpy


def read_npy(
        path: Union[str, os.PathLike],
        mmap_mode=None,
        allow_pickle=True,
        fix_imports=True,
        encoding='ASCII',
        **df_kwargs
) -> pd.DataFrame:
    """
    a reader for reading a numpy file to a pandas DataFrame

    Parameters
    ----------
    path: str, PathLike
    mmap_mode: see np.load
    allow_pickle: see np.load
    fix_imports: see np.load
    encoding: see np.load
    df_kwargs: parameters for creating pandas DataFrame

    Returns
    -------
    DataFrame
    """
    data = np.load(
            path,
            mmap_mode=mmap_mode,
            allow_pickle=allow_pickle,
            fix_imports=fix_imports,
            encoding=encoding
        )
    if len(data.shape) == 1:
        # that's target, no need to detect categorical data
        return pd.DataFrame(data, **df_kwargs)
    feature_types = _find_categorical_types(
                    data,
                    feature_names=None,
                    feature_types=_detect_types_numpy(data),
                    categorical_features=None,
                    categorical_threshold=None
                )
    df = pd.DataFrame(data, **df_kwargs)
    feature_types_dict = {col_name: object if feature_types[i] == 'c' else feature_types[i]
                          for i, col_name in enumerate(df.columns.values)}
    df = df.astype(feature_types_dict)
    return df


class SerializeProtocol:
    TEXT = 'text'
    PICKLE = 'pickle'
    DEFAULT = 'text'


def serialize_function(func: Callable, protocol=None) -> dict:
    """
    serialize function to a base64 string.
    use pickling or store function body according to the input protocol

    Parameters
    ----------
    func: Callable
    protocol: str, optional
        pickle - use joblib.dump
        text - take the body
    Returns
    -------
    dict
        func_name: string
            function name
        func_body: base64 string
            serialization of the function
        protocol: string
            'text' or 'pickle'
    """
    protocol = protocol or SerializeProtocol.DEFAULT
    if protocol == SerializeProtocol.PICKLE:
        content = serialize_function_pickle(func)
    else:
        content = serialize_function_text(func)

    return dict(func_name=func.__name__, func_body=content, protocol=protocol)


def deserialize_function(func_def: dict) -> Callable:
    """
    restore a serialized function

    Parameters
    ----------
    func_def: dict
        a serialized function with information about the way it should be desirialized

    Returns
    -------
    Callable:
        the function object ready to be used

    """
    protocol = func_def.get('protocol') or SerializeProtocol.DEFAULT
    body = func_def['func_body']
    name = func_def['func_name']
    if protocol == SerializeProtocol.PICKLE:
        return deserialize_function_pickle(body)
    else:
        return deserialize_function_text(body, name)


def serialize_function_pickle(func: Callable) -> str:
    """
    pickle a function and encode it to a base64 string

    Parameters
    ----------
    func: Callable
        must be a pickle-able

    Returns
    -------
    str
        base64 serialization of the pickled object
    """
    with io.BytesIO() as tmp_bytes:
        joblib.dump(func, tmp_bytes)
        bytes_obj = tmp_bytes.getvalue()
        base64_obj = base64.b64encode(bytes_obj)
        base64_string = base64_obj.decode()
    return base64_string


def deserialize_function_pickle(func_body) -> Callable:
    """
    Restore a pickled function encoded as base64 string

    Parameters
    ----------
    func_body: str
        base64 encoded string

    Returns
    -------
    Callable
        function object
    """
    bytes_obj = base64.b64decode(func_body)
    with io.BytesIO(bytes_obj) as tmp_bytes:
        func_body = joblib.load(tmp_bytes)
    return func_body


def serialize_function_text(func: Callable) -> str:
    """
    Extract function body as text and encode it to a base64 string

    Parameters
    ----------
    func: Callable

    Returns
    -------
    base64 encode of the function body

    """
    func_text = inspect.getsource(func)
    func_text = textwrap.dedent(func_text)
    func_text = base64.b64encode(func_text.encode()).decode()

    return func_text


def deserialize_function_text(func_body: str, func_name: str) -> Callable:
    """
    Restore a pickled function encoded as base64 string
    use exec to define it as local attribute
    user func_name input to locate and return it

    Parameters
    ----------
    func_body: base64 encoded string
    func_name: string
        the name to look for in locals()

    Returns
    -------
    Callable
        function object
    """
    func_body = base64.b64decode(func_body).decode()
    exec(f'global {func_name}\n{func_body}')
    return globals()[func_name]


def _compose_missing_params(data_params, data_params_internal):
    """
    Compose missing params for each feature in the dataset.

    Parameters
    ----------
    data_params: dict
        data_params dict from the data manager

    Returns
    -------
    list
        list of missing values for each feature
    """
    to_return = []
    for idx, feature in enumerate(data_params.features):
        if feature.fill_value is None:
            if feature.categorical or data_params_internal.categorical_features_ and idx in data_params_internal.categorical_features_:
                to_return.append(data_params.fill_value_cat)
            else:
                to_return.append(data_params.fill_value_num)
        else:
            to_return.append(feature.fill_value)
    return to_return


def _update_col_indexes(column_indexes, removed_column_indexes):
    """
    Updates column_indexes list to point to the same location in the new dataset after removing columns in
    removed_column_indexes list.
    """
    if not removed_column_indexes:
        return column_indexes
    return [
        (index - sum(1 for removed in removed_column_indexes if removed < index))
        for index in column_indexes
        if index not in removed_column_indexes
    ]


