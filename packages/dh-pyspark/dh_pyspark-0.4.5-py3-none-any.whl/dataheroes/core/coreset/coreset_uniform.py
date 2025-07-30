import numpy as np
from ._base import CoresetBase
from typing import Union, Optional
from numpy.random import Generator
from sklearn.cluster import KMeans


def sensitivity_uniform(X, y=None, w=None, dtype: Optional[str] = None):
    return np.ones(len(X)) / len(X)


def sensitivity_kmeans(X, y=None, w=None, *, k: int = 2, dtype: Optional[str] = None):
    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype) if dtype is not None else X
    km = KMeans(k)
    y = km.fit_predict(X)
    s_p = k * np.ones(len(X))
    for i in range(k):
        ind = np.where(y == i)
        s_p[ind] *= len(ind)
    return s_p


class CoresetUniform(CoresetBase):
    _possible_sensitivities = ["uniform", "kmeans"]
    _coreset_type = "unsupervised"

    def __init__(
        self,
        *,
        algorithm: str = "uniform",
        random_state: Union[int, Generator] = None,
        det_weights_behaviour: str = "auto",  # TODO Temporary bad solution, remove this in the future.
        deterministic_size: Optional[float] = None,  # TODO Temporary bad solution, remove this in the future.
        is_classification: bool = False,
        **sensitivity_kwargs,
    ):
        """Coresets for unifrom sampling.

        Parameters
        ----------

        algorithm : str, default="uniform"
            Sensitivity algorithm. One of ["uniform", "kmeans"]

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        is_classification: bool
            If we should uniform sample with a minimum from each class
            like in a classification scenario
        """

        super().__init__(random_state=random_state)
        if self._coreset_type == "classification":
            self.is_classification = True
        else:
            self.is_classification = is_classification

        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        self._algorithm = algorithm
        self.sensitivity_kwargs = sensitivity_kwargs

    def sensitivity(self, X, y=None, w=None) -> np.ndarray:
        if self.algorithm == "uniform":
            sensitivity_f = sensitivity_uniform
        elif self.algorithm == "kmeans":
            sensitivity_f = sensitivity_kmeans
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        return sensitivity_f(X, w, **self.sensitivity_kwargs)


class CoresetUniformClassification(CoresetUniform):
    _coreset_type = "classification"

class CoresetUniformRegression(CoresetUniform):
    _coreset_type = "regression"