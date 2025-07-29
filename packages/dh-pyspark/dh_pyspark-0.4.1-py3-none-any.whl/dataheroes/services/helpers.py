import inspect
import json
from typing import Any

import numpy as np
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, timedelta


def get_method_args(locals=None):
    frame = inspect.stack()[1].frame
    args, _, _, values = inspect.getargvalues(frame)
    kw = {k: values[k] for k in args if k != 'self'}
    return kw


def is_xgb_installed():
    try:
        from xgboost import XGBClassifier
        return True
    except:
        return False


def is_lgb_installed():
    try:
        from lightgbm import LGBMClassifier
        return True
    except:
        return False


def is_catboost_installed():
    try:
        from catboost import CatBoostClassifier
        return True
    except:
        return False


def get_model_name(model: Any) -> str:
    """
    The __name__ is the name of a "class or type", not an instance of a class or type.
    If the model is an instance of a model class it may not have the __name__ attribute, so we need to access
    the __class__ attribute of the model and get its name.
    Parameters
    ----------
    model

    Returns
    -------

    """
    return model.__name__ if hasattr(model, '__name__') else model.__class__.__name__


class NpEncoder(json.JSONEncoder):
    """
    Encoding of many numpy types is not supported by json library - specifically, we've had a failure on np.float32.
    We use one of the solutions suggested online to support JSON encoding.
    This solution strives to cover all types, but we may reduce it to handle only the float32 type - if we want to
    be more conservative (until we encounter a failure with a new type).
    What we use is taken from here: https://codetinkering.com/numpy-encoder-json/
    See more details here:
    https://github.com/numpy/numpy/issues/16432
    https://ellisvalentiner.com/post/serializing-numpyfloat32-json/
    https://stackoverflow.com/questions/53082708/typeerror-object-of-type-float32-is-not-json-serializable
    https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
    https://bobbyhadz.com/blog/python-typeerror-object-of-type-int64-is-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.floating, np.complexfloating)):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.string_):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return str(obj)
        return super(NpEncoder, self).default(obj)


class DataClassEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)


class JSONEncoderExtra(DataClassEncoder, NpEncoder):
    pass
