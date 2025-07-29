from .common import w_dot_X
from ._base import CoresetBase
import numpy as np
from sklearn.utils.extmath import svd_flip
from .coreset_svd import sensitivity_svd,sensitivity_svd_super,sensitivity_svd_groups,sensitivity_woodruff

from typing import Union, Optional
from numpy.random import Generator
from sklearn.utils.validation import _check_sample_weight


def sensitivity_dm(X, y=None, w=None, dtype: str = 'float32'):

    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype) if dtype is not None else X

    # https://www.stat.berkeley.edu/~mmahoney/pubs/l2sample.pdf
    X = np.concatenate([X, np.ones([X.shape[0], 1], dtype=dtype)], axis=1)

    if w is not None:
        w = _check_sample_weight(w, X, dtype=X.dtype)
        X, y = w_dot_X(X, y=y, w=w)

    U, _, Vt = np.linalg.svd(X, full_matrices=False)
    U, _ = svd_flip(U, Vt)
    # U_norm = np.linalg.norm(U) # = np.sum(X**2)**(1./2)
    Ui_norm = np.linalg.norm(U, axis=1)
    # y_ = U @ U.T @ y + np.mean(y)
    temp, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    y_ = X @ temp

    t1 = Ui_norm ** 2 / np.sum(Ui_norm ** 2)
    # t2 = (Ui_norm * y_) / np.sum(Ui_norm * y_)
    t3 = y_ ** 2 / np.sum(y_ ** 2)
    # print(all(t1 > 0), all(t2 > 0), all(t3> 0))
    # probs = t1 / 3 + t2 / 3 + t3 / 3
    sp = t1 / 2 + t3 / 2

    return sp


def sensitivity_lrsvd(X, y, w=None, *, svd_function="svd", n_components: int = None, dtype: str = 'float32') -> np.ndarray:

    if svd_function == "svd":
        sensitivity_f = sensitivity_svd
    elif svd_function == "super":
        sensitivity_f = sensitivity_svd_super
    elif svd_function == "group":
        sensitivity_f = sensitivity_svd_groups
    elif svd_function == "woodruff":
        sensitivity_f = sensitivity_woodruff        
    else:
        raise ValueError("Unknown sensitivity_svd")
    n_samples, n_dim = X.shape

    if n_components is None:
        n_components = min([n_samples, n_dim])

    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype)

    # Concatenate a column of ones and y to X
    # [X | 1 | y]
    X = np.concatenate([X, np.ones([n_samples, 1], dtype=dtype)], axis=1)
    if y.ndim == 1:
        X = np.concatenate([X, y[:, np.newaxis]], axis=1)
    else:
        X = np.concatenate([X, y], axis=1)

    n_components = n_components + 2  # d + 2 for bias and y columns
    if n_components > n_dim + 2:
        n_components = n_dim + 2
    return sensitivity_f(X, w=w, n_components=n_components)


class CoresetReg(CoresetBase):

    _coreset_type = "regression"
    _possible_sensitivities = ["dm", "svd"]

    def __init__(self, *, algorithm: str = "svd", random_state: Union[int, Generator] = None, **sensitivity_kwargs):
        """Coreset class for the Linear regression task

        Parameters
        ----------
        algorithm : str, default="svd"
            Sensitivity algorithm. One of ["svd", "dm"]

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator
        """
        super().__init__(random_state=random_state)
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        self._algorithm = algorithm
        self.sensitivity_kwargs = sensitivity_kwargs

    def sensitivity(self, X, y, w=None) -> np.ndarray:
        if self.algorithm == "dm":
            sensitivity_f = sensitivity_dm
        elif self.algorithm == "svd":
            sensitivity_f = sensitivity_lrsvd
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        return sensitivity_f(X, y, w, **self.sensitivity_kwargs)
