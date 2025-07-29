from .coreset_svd import sensitivity_svd,sensitivity_svd_super,sensitivity_svd_groups,sensitivity_woodruff
from ._base import CoresetBase
import numpy as np
from typing import Union, Optional
from numpy.random import Generator
from scipy.sparse import issparse
from scipy import sparse
# from sklearn.utils.extmath import svd_flip
from .common import safe_norm


def sensitivity_pca(X, w=None,* ,svd_function="svd", n_components: int = None, dtype: str = 'float32'):
   
    if svd_function == "svd":
        svd_function = sensitivity_svd
    elif svd_function == "super":
        svd_function = sensitivity_svd_super
    elif svd_function == "group":
        svd_function = sensitivity_svd_groups
    elif svd_function == "woodruff":
        svd_function = sensitivity_woodruff
    else:
        raise ValueError("Unknown svd_function")

    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype)

    # Add big dimension - max over the norm of each point in X
    r = 1 + np.max(safe_norm(X, axis=1))
    n_samples, n_dim = X.shape
    n_dim += 1

    # X = [X | r]
    # NOTE: 1. This copies. Can we do this better?
    if issparse(X):
        X = sparse.hstack([X, r * np.ones((n_samples, 1), dtype=dtype)], dtype=dtype)
    else:
        X = np.hstack([X, r * np.ones((n_samples, 1), dtype=dtype)])
    
    if n_components is None:
        n_components = n_dim
    else: 
        n_components +=1
    
    
    # TODO Old pca didn't had `w` when computing sensitivity. Check if this is good
    
    return svd_function(X, w=w, n_components=n_components)


class CoresetPCA(CoresetBase):

    _coreset_type = "unsupervised"
    _possible_sensitivities = ["svd","super","group","woodruff"]

    def __init__(
        self,
        n_components: int = None,
        *,
        algorithm: str = "svd",
        random_state: Union[int, Generator] = None,
        **sensitivity_kwargs,
    ):
        """Coresets for the PCA unsupervized task


        Parameters
        ----------

        algorithm : str, default="svd"
            Sensitivity algorithm. One of ["svd","super","group","woodruff"]

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        n_components: int
            Number of components for pca
        """
        super().__init__(random_state=random_state)
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        self._algorithm = algorithm
        self.sensitivity_kwargs = sensitivity_kwargs

    def sensitivity(self, X, y=None, w=None):
        return sensitivity_pca(X, w,svd_function=self.algorithm,**self.sensitivity_kwargs)
