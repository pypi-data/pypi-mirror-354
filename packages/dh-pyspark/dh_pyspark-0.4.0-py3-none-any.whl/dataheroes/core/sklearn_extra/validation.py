import sklearn
from sklearn.utils import check_array as check_array_sk
import inspect

if sklearn.__version__ >= "1.6":
    from sklearn.utils.validation import (
        _check_n_features as _check_n_features_sk,
        _check_feature_names as _check_feature_names_sk,
    )


def _check_n_features(estimator, X, reset):
    if sklearn.__version__ >= "1.6":
        return _check_n_features_sk(estimator=estimator, X=X, reset=reset)
    else:
        return estimator._check_n_features(X=X, reset=reset)


def _check_feature_names(estimator, X, *, reset):
    if sklearn.__version__ >= "1.6":
        return _check_feature_names_sk(estimator=estimator, X=X, reset=reset)
    else:
        return estimator._check_feature_names(X=X, reset=reset)


def check_array(
    array,
    accept_sparse=False,
    *,
    accept_large_sparse=True,
    dtype="numeric",
    order=None,
    copy=False,
    force_writeable=False,
    ensure_all_finite=None,
    ensure_non_negative=False,
    ensure_2d=True,
    allow_nd=False,
    ensure_min_samples=1,
    ensure_min_features=1,
    estimator=None,
    input_name="",
):
    params = {
        "array": array,
        "accept_sparse": accept_sparse,
        "accept_large_sparse": accept_large_sparse,
        "dtype": dtype,
        "order": order,
        "copy": copy,
        "force_writeable": force_writeable,
        "ensure_all_finite": ensure_all_finite,
        "ensure_non_negative": ensure_non_negative,
        "ensure_2d": ensure_2d,
        "allow_nd": allow_nd,
        "ensure_min_samples": ensure_min_samples,
        "ensure_min_features": ensure_min_features,
        "estimator": estimator,
        "input_name": input_name,
    }
    if sklearn.__version__ < "1.6":
        params["force_all_finite"] = ensure_all_finite if ensure_all_finite is not None  else False
    else:
        params["ensure_all_finite"] = ensure_all_finite
    s = inspect.signature(check_array_sk)
    params = {k: v for k, v in params.items() if k in s.parameters.keys()}
    return check_array_sk(**params)
