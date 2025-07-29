from typing import Union, Optional, List, Iterable, Dict, Any

import numpy as np
from numpy.random import Generator

from dataheroes.core.numpy_extra import unique_2d_hash

from ._base import CoresetBase
from ..helpers import aggregate_children


def sensitivity_analytics(X, w=None):
    """
    Compute the sensitivity of the data by aggregating duplicate rows and optionally
    sorting based on provided or computed weights, returning the indices of unique rows
    and their associated sensitivity values in descending order of weight.

    Parameters
    ----------
    X : np.ndarray
        A 2D numpy array where each row represents a feature vector. Duplicate rows
        are allowed and will be aggregated based on their frequency or assigned weights.
    w : np.ndarray, optional
        A 1D numpy array of weights corresponding to each row in `X`. If provided,
        it is used directly to measure sensitivity. If not provided, the function
        will count occurrences of each unique row in `X` as weights.

    Returns
    -------
    sorted_idx : np.ndarray
        Array of indices representing the first occurrence of each unique row in `X`,
        sorted by sensitivity (weight) in descending order.
    sorted_weights : np.ndarray
        Array of computed or provided weights corresponding to the unique rows in `X`,
        sorted in descending order.
    """
    if w is not None:
        # Aggregations are already computed, the presumption is that we only have unique values in each chunk
        idx = np.arange(len(X))
    else:
        # Compute aggregations with sorted order of unique rows based on their first appearance
        _, idx, w = unique_2d_hash(X, return_counts=True, return_index=True)
    mask = np.argsort(w)[::-1]
    sorted_idx = idx[mask]
    sorted_weights = w[mask]

    return sorted_idx, sorted_weights


class CoresetAnalytics(CoresetBase):

    _coreset_type = "analytics"

    def __init__(self, **sensitivity_kwargs):
        """Coreset class for the Linear regression task

        Parameters
        ----------
        algorithm : str, default="svd"
            Sensitivity algorithm. One of ["generic", "aggregated"]

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator
        """
        super().__init__(random_state=None)

        self.sensitivity_kwargs = sensitivity_kwargs

    def build(
            self,
            X,
            y=None,
            w=None,
            new_state=None,
            *,
            from_coresets: Optional[List["CoresetBase"]] = None,
            coreset_size: Optional[int],
            deterministic_size=None,
            sample_all: Iterable = None,
            class_size: Dict[Any, int] = None,
            minimum_size: Union[int, str, Dict[Any, int]] = None,
            fair: Union[str, bool] = "training",
            **sample_kwargs,
    ):

        if new_state is None:
            # father node
            sorted_idx, sorted_weights = aggregate_children(X, w)
        else:
            # leaf node
            sorted_idx = np.array(new_state["idxs"], dtype=int)
            sorted_weights = np.array(new_state["weights"], dtype=int)

        # Sample the first "coreset_size" most frequent samples
        self.idxs = sorted_idx[:coreset_size]
        self.weights = sorted_weights[:len(self.idxs)]

        return self.idxs, self.weights

    def rebuild(
        self,
        X,
        y=None,
        w=None,
        new_state=None,
        idxs_removed: Optional[Iterable[int]] = None,
        *,
        # Constraints
        coreset_size: Optional[int] = None,
        deterministic_size: Optional[float] = None,
        sample_all: Iterable[Any] = None,
        class_size: Dict[Any, int] = None,
        minimum_size: Union[int, str, Dict[Any, int]] = None,
        fair: bool = True,
        # Rebuild thresholds
        iterative_threshold: float = 0.1,
        resample_threshold: float = 0.1,
        n_iter: int = 50,
        # TODO better name for `sample_per_iter`
        sample_per_iter: Union[float, int] = 0.1,
        random_state: Union[int, Generator] = None,
    ):

        return self.build(
            X,
            y=y,
            w=w,
            new_state=new_state,
            coreset_size=coreset_size,
            deterministic_size=deterministic_size,
            sample_all=sample_all,
            class_size=class_size,
            minimum_size=minimum_size,
            fair=fair,
        )

    def sensitivity(self, X, y=None, w=None) -> np.ndarray:
        raise NotImplementedError

    def compute_sensitivities(self, X, y=None, w=None) -> None:
        selected_idxs, selected_weights = sensitivity_analytics(X, w)
        self.idxs = selected_idxs
        self.weights = selected_weights
        return

    def sample(*args, **kwargs):
        raise NotImplementedError

    def compute_sample(*args, **kwargs):
        raise NotImplementedError

    def get_cleaning_samples(*args, **kwargs):
        raise NotImplementedError
