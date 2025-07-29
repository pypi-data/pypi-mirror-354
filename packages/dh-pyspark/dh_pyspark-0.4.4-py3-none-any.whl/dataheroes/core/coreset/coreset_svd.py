import numpy as np

from .common import orth
from ._base import CoresetBase
from typing import Union, Optional
from numpy.random import Generator
from sklearn.utils.validation import _check_sample_weight
from .common import safe_mv
from scipy.sparse import issparse, isspmatrix_csr

def sensitivity_woodruff(X, w=None, *, n_components: int = None,gamma = 0.5, dtype: str = 'float32'):
    """
    https://arxiv.org/pdf/1207.6365.pdf
    O(nd)
    n_components - is not used and only API compatibility 
    """
    
    n,d = X.shape
    #First we build a sketch of the data.
    S1_row = round(np.log(n) / gamma**2)  # Number of rows in the sketch
    Sketch1 = np.zeros((S1_row, d))  # Initialize sketch to all zeros
    X = X.astype(dtype, copy=X.dtype.name != dtype)
    # For every input point a(i), randomly sample an integer j from (1,S_row) and add
    # the point a(i) to Sketch(j) with weight with either +1 or -1 with equal
    # probability.
    js = np.random.choice(S1_row,n)
    signs = np.sign(np.random.randn(n))
    # Y = np.multiply(signs[:, np.newaxis], X)
    Y = safe_mv(X, signs, sp_format="csr")
    js = np.hstack((js[:, np.newaxis], np.arange(n)[:, np.newaxis]))
    js = js[js[:, 0].argsort()]
    indices = np.split(js[:, 1], np.unique(js[:, 0], return_index=True)[1][1:])
    for i, j in enumerate(np.unique(js[:, 0])):
        Sketch1[j, :] = np.sum(Y[indices[i], :], axis=0)

    Q, R = np.linalg.qr(Sketch1, "complete")  # Copmute QR decomposition of Sketch
    iR = np.linalg.pinv(R)

    # Create second sketch to improve the running time.
    Temp2 = np.random.randn(d, S1_row) / np.sqrt(S1_row)  # Create Sketch2 matrix.
    Sketch2 = iR * Temp2  # Create Sketch of inverse of R
    tU = X.dot(Sketch2)  # Approximate orthonormal space.
    sp = np.sum(tU.T**2,axis = 0)                    # Approximate leverage scores.
    return sp


def sensitivity_svd_groups(X, w=None, *, n_components=None, dtype: str = 'float32'):
    """
    n_components - is not used and only API compatibility 
    """
    n_samples, n_dim = X.shape
    # X = np.atleast_2d(X)
    if w is not None:
        w = _check_sample_weight(w, X, dtype=X.dtype)
        # Even though csc is for col slicing, csr seems faster to cast to. Needs more investigation.
        X = safe_mv(X, np.sqrt(w), sp_format="csr")
        # X = w_dot_X(X=X, w=np.sqrt(w))

    if issparse(X) and not isspmatrix_csr(X):
        X = X.tocsr(copy=False)
    jumps = np.sqrt(n_dim)
    inx = np.arange(0,n_dim,int(jumps),dtype=np.uint32)
    sp = np.zeros(n_samples)
    for i in range(len(inx)-1):
        sp += sensitivity_svd(X[:,inx[i]:inx[i+1]], w=w, n_components = None)
    sp += sensitivity_svd(X[:,inx[i]:inx[i+1]], n_components = None, dtype=dtype)

    return sp


def sensitivity_svd_super(X, w=None, *, n_components=None, dtype: str = 'float32'):
    """
    n_components - is not used and only API compatibility 
    """
    n_samples, n_dim = X.shape
    X = X.astype(dtype, copy=X.dtype.name != dtype)
    # X = np.atleast_2d(X)
    if w is not None:
        X = safe_mv(X, np.sqrt(w))
        # X = w_dot_X(X=X, w=np.sqrt(w))
    
    # NOTE: This copies
    if issparse(X):
        X = X.power(2)
        U = np.array(X.sum(0)).squeeze() + np.finfo(X.dtype).eps
        # Casting to another format may be slower than just computing on COO
        U = safe_mv(X, 1 / U)
        sp = np.array(U.sum(1)).squeeze()

    else:
        X = X**2
        U = np.sum(X, axis=0) + np.finfo(type(X[0, 0])).eps
        U = X / U
        sp = np.sum(U, axis=1)

    return sp


def sensitivity_svd(X, w=None, *, n_components: int = None, solver: str = "auto", solver_kwargs=None, dtype: str = 'float32'):

    n_samples, n_dim = X.shape
    if n_components is None:
        n_components = int(np.min([n_samples, n_dim]))

    X = X.astype(dtype, copy=X.dtype.name != dtype)

    if w is not None:
        w = _check_sample_weight(w, X, dtype=X.dtype)
        X = safe_mv(X, np.sqrt(w))
        # X = w_dot_X(X=X, w=np.sqrt(w))

    try:
        u = orth(X, n_components=n_components, solver=solver, solver_kwargs=solver_kwargs)
    except Exception as e:
        if str(e) == "array must not contain infs or NaNs" and dtype != np.float64:
            X = X.astype(np.float64)
            u = orth(X, n_components=n_components, solver=solver, solver_kwargs=solver_kwargs)
        else:
            raise e

    # TODO: This is not theory backed, needs testing.
    # if k < X.shape[1]:
    #     s_p = np.linalg.norm(u[:, :k], axis=1) ** 2
    # else:
    s_p = np.linalg.norm(u, axis=1) ** 2
    return s_p


class CoresetSVD(CoresetBase):

    _coreset_type = "unsupervised"
    _possible_sensitivities = ["svd", "super", "group", "woodruff"]

    def __init__(self, *, random_state: Union[int, Generator] = None, algorithm: str = "svd", **sensitivity_kwargs):
        """Coresets for the SVD unsupervized task.

        Parameters
        ----------
        n_components: int, default = 2
            Number of svd dimensions

        algorithm : str, default="svd"
            Sensitivity algorithm. One of ["svd", "super", "group", "woodruff"]


        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator
        """

        super().__init__(random_state=random_state)
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        self._algorithm = algorithm
        self.sensitivity_kwargs = sensitivity_kwargs

    def sensitivity(self, X, y=None, w=None):
        if self.algorithm == "svd":
            sensitivity_f = sensitivity_svd
        elif self.algorithm == "super":
            sensitivity_f = sensitivity_svd_super
        elif self.algorithm == "group":
            sensitivity_f = sensitivity_svd_groups
        elif self.algorithm == "woodruff":
            sensitivity_f = sensitivity_woodruff
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        return sensitivity_f(X, w, **self.sensitivity_kwargs)
