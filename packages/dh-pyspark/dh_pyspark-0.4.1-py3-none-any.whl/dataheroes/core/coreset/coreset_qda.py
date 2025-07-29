from ._base import CoresetBase
from .coreset_pca import sensitivity_pca
import numpy as np
from typing import Any, Dict, Union
from numpy.random import Generator
from sklearn.utils.validation import _check_sample_weight


def sensitivity_qda(
    X, y, w=None, svd_function=None, n_components: int = None, priors: np.ndarray = None, class_weight: Dict[Any, float] = None, dtype: str = 'float32'
):
    if n_components is None:
        n_components = int(np.min([X.shape[0], X.shape[1]]))

    n_samples = len(y)
    classes, counts = np.unique(y, return_counts=True)
    s_p = np.zeros(n_samples)

    # If w is None fill with 1s
    w = _check_sample_weight(w, X, dtype=X.dtype)

    if isinstance(class_weight, dict):
        cw = np.array([class_weight.get(yi, 1.0) for yi in y])
        w = w * cw

    if priors is None:
        priors = counts / n_samples

    for i, (c, prior) in enumerate(zip(classes, priors)):
        # size_c = np.max([self.coreset_size * (counts[i] / n_samples), dim])
        ind = np.where(y == c)[0]
        # TODO Old QDA didn't had `w` when computing sensitivity. Check if this is good.
        # TODO: sensitivity kmeans might make more sense. 
        s_p[ind] = sensitivity_pca(X[ind, :], w=w[ind], n_components=n_components,
                                   svd_function=svd_function, dtype=dtype) * prior

    return s_p


class CoresetQDA(CoresetBase):

    _coreset_type = "classification"
    _possible_sensitivities = ["svd","super","group","woodruff"]
    def __init__(self, algorithm: str = "svd", *, random_state: Union[int, Generator] = None, **sensitivity_kwargs):
        """Coreset for the QDA classification task

        Parameters
        ----------
        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        **sensitivity_kwargs: Key arguments
            parameters to be passed to the sensitivity function
        """

        super().__init__(random_state=random_state)
        self.is_classification = True
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        self._algorithm = algorithm
        self.sensitivity_kwargs = sensitivity_kwargs

    def sensitivity(self, X, y=None, w=None):
        if self.algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        return sensitivity_qda(X, y, w,svd_function=self.algorithm, **self.sensitivity_kwargs)
