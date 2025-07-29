import numpy as np
from ._base import CoresetBase
from ..sklearn_extra.wkmeans_plusplus import kmeans_plusplus_w
from scipy.spatial.distance import cdist
from typing import Union
from numpy.random import Generator


def sensitivity_gmm(X,w=None, *, k: int = 2):
    """
    http://people.csail.mit.edu/dannyf/nips11.pdf
    """
    n_samples, n_dim = X.shape
    if w is None:
        w = np.ones(n_samples)
    # get cluster centers
    centers, centers_ind = kmeans_plusplus_w(X, k,w=w)

    all_dists = cdist(X, centers)

    # index of the closest center -- shape (n_samples, ), index in [0 ... k]
    closest_center_idxs = np.argmin(all_dists, axis=1)  # labels
    center_dists = all_dists[np.arange(n_samples), closest_center_idxs]

    clusters, inv, cluster_sizes = np.unique(
        closest_center_idxs, return_inverse=True, return_counts=True
    )
    # Weight cluster sizes
    cluster_sizes = np.array([np.sum(w[closest_center_idxs == c]) for c in clusters])

    sp = center_dists/np.sum(center_dists)
    sp += 5 / (cluster_sizes[inv])

    return sp


class CoresetGMM(CoresetBase):
    _coreset_type = "unsupervised"
    _possible_sensitivities = ["kmeans"]

    def __init__(
        self,
        *,
        algorithm: str = "kmeans",
        random_state: Union[int, Generator] = None,
        **sensitivity_kwargs,
    ):
        """_summary_

        Parameters
        ----------
        algorithm : str, default="kmeans"
            Sensitivity algorithm. One of ["kmeans"]

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        **sensitivity_kwargs: Key arguments
            Extra arguments that will be pased to the sensitivity function


        """

        super().__init__(
            random_state=random_state,
        )

        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        else:
            self._algorithm = algorithm

        self.sensitivity_kwargs = sensitivity_kwargs

    def sensitivity(self, X, y=None, w=None) -> np.ndarray:
        if self.algorithm == "kmeans":
            self.sensitivity_f = sensitivity_gmm
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        res = self.sensitivity_f(X, w, **self.sensitivity_kwargs)
        return res
