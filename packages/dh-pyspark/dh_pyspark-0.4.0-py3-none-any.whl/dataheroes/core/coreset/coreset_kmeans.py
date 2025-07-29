import numpy as np
from ._base import CoresetBase
from .common import is_int, safe_average, safe_mv, safe_norm
from ..sklearn_extra.wkmeans_plusplus import kmeans_plusplus_w

from scipy.spatial.distance import cdist
from typing import Union, List
from numpy.random import Generator
from typing import Tuple, Dict, Any, Optional
from sklearn.utils.validation import _check_sample_weight


def _lightweight_inner_sens(
    X: np.ndarray,
    w: np.ndarray,
    mu: np.ndarray,
    w_sum: Optional[Union[float, np.floating]] = None,
    di_sum: Optional[Union[float, np.ndarray]] = None,
    per_feature: bool = False,
):
    if mu.shape[0] != X.shape[1]:
        raise ValueError("mu and X must have the same number of features")
    if per_feature:
        di = safe_mv(X - mu, w) ** 2
        # di = (w.reshape(-1, 1) * (X - mu)) ** 2
        di_sum = di_sum if di_sum is not None else di.sum(axis=0)
        sp = 0.5 * (w / w_sum) + (0.5 * (di / (di_sum + 1e-20))).sum(axis=1)
    else:
        di = safe_norm(X - mu, axis=1) ** 2
        # di = np.linalg.norm(X - mu, axis=1) ** 2
        di = di * w  # weight the distance
        di_sum = di_sum if di_sum is not None else di.sum()
        sp = 0.5 * (w / w_sum) + 0.5 * (di / (di_sum + 1e-20))
    return sp, w_sum, di_sum


def sensitivity_lightweight(
    X, w=None, per_feature: bool = False, return_info: bool = False, dtype: Optional[str] = None
) -> Union[np.ndarray, Tuple[np.ndarray, dict]]:
    """
    Scalable k-Means Clustering via Lightweight Coresets
    Olivier Bachem, Mario Lucic, Andreas Krause
    https://arxiv.org/abs/1702.08248
    Algorithm 1
    Time: O(nd)
    Error: O(dklogk/eps^2)

    * if k is unbounded this is better
    """
    n_samples, _ = X.shape
    # If w is None fill with 1s
    w = _check_sample_weight(w, X, dtype=X.dtype)
    # change to float32 if needed
    # We need the dtype param because it's provided in coreset params, however this line hasn't been tested
    # yet, so we left it out for now.
    # X = X.astype(dtype, copy=X.dtype.name != dtype) if dtype is not None else X
    # For small dims just use ones
    if n_samples < 20:
        return np.ones(n_samples) / np.sum(w) * w
    mu = safe_average(X, weights=w, axis=0)  # weighted average
    sensitivities, w_sum, di_sum = _lightweight_inner_sens(X=X, w=w, mu=mu, w_sum=np.sum(w), per_feature=per_feature)
    if return_info:
        info = {"mu": mu, "w_sum": w_sum, "di_sum": di_sum}

    if return_info:
        return sensitivities, info
    else:
        return sensitivities


def estimate_lightweight(
    X: np.ndarray,
    w: np.ndarray,
    mu: np.ndarray,
    w_sum: float,
    di_sum: Union[float, np.ndarray],
    per_feature: bool = False,
) -> np.ndarray:
    X = np.atleast_2d(X)
    w = _check_sample_weight(w, X, dtype=X.dtype)
    sensitivities, _, _ = _lightweight_inner_sens(X=X, w=w, mu=mu, w_sum=w_sum, di_sum=di_sum, per_feature=per_feature)
    return sensitivities


def adjust_centers_ind(centers_ind, n_clusters_actual, n_clusters_planned):
    """
    There may be a situation in which the number of planned clusters (k) is higher than the actual number of unique
    X points. In this case, the number of actual clusters would be smaller than the planned clusters.
    Adjustment to the array is hence required in order to keep consistent data structures for subsequent usage.
    (Anything at the indices of centers_ind beyond the actual number of clusters is an initialized but not an
    assigned value - so cutting the subarray like we do here is safe.)
    """
    if n_clusters_actual < n_clusters_planned:
        import warnings
        warnings.warn(f"Number of actual distinct clusters found ({n_clusters_actual}) smaller than "
                      f"planned ({n_clusters_planned}), possibly due to duplicate points in X. "
                      f"Center indices array will be adjusted.", stacklevel=3)
        return centers_ind[:n_clusters_actual]
    return centers_ind


def sensitivity_practical(X, w=None, *, k: int = 8, dtype: Optional[str] = None):
    """
    Sensitivity function from Practical coreset paper
    Practical Coreset Constructions for Machine Learning
    Olivier Bachem, Mario Lucic, Andreas Krause
    https://arxiv.org/abs/1703.06476
    Algorithm 2
    Time: O(nkd)
    Error: Omega (dk^2log(k)/eps^2)

    Plus Supartim sample trick
    """
    n_samples, n_dim = X.shape
    # If w is None fill with 1s
    w = _check_sample_weight(w, X, dtype=X.dtype)
    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype) if dtype is not None else X
    # For small dims just use ones
    alpha = 16 * (np.log(k) + 2)
    # get cluster centers
    centers, centers_ind = kmeans_plusplus_w(X, k, w=w)
    # distances to all centers -- shape (len(X), k)
    all_dists = cdist(X, centers)
    # index of the closest center -- shape (len(X), ), index in [0 ... k]
    closest_center_idxs = np.argmin(all_dists, axis=1)

    # distances to closest centers -- shape (n_samples, )
    # center_dists = np.min(all_dists, axis=1)
    # to not run np.min() again
    center_dists = all_dists[np.arange(n_samples), closest_center_idxs]

    # Get cluster sizes. With cluster_sizes[inv] we correspond each sample to its corresponding cluster size
    # read how np.unique works
    clusters, inv, cluster_sizes = np.unique(
        closest_center_idxs, return_inverse=True, return_counts=True
    )
    # Weight cluster sizes
    cluster_sizes = np.array([np.sum(w[closest_center_idxs == c]) for c in clusters])

    # Sum of squared distances for all clusters and total
    cluster_inertia = np.array(
        [
            np.sum(
                center_dists[closest_center_idxs == c] ** 2
                * w[closest_center_idxs == c]
            )
            for c in clusters
        ]
    )
    inertia = np.sum(cluster_inertia)  # c_phi
    eps_ = np.finfo(inertia.dtype).eps  # Division to perfect clusters will produce 0 inertia - epsilon to the rescue.

    sp = alpha * w * center_dists / (inertia + eps_)
    #  cluster_inertia[closest_center_idxs] = closest center inertia for each point
    sp += (
            2
            * alpha
            * cluster_inertia[closest_center_idxs]
            / (cluster_sizes[inv] * (inertia + eps_))
    )
    sp += 4 * len(X) / cluster_sizes[inv]
    centers_ind_adj = adjust_centers_ind(centers_ind, len(clusters), k)
    return sp, centers_ind_adj, cluster_sizes, closest_center_idxs


def sensitivity_offline(X, w=None, *, k: int = 8, dtype: Optional[str] = None):
    """
    Sensitivity function from https://arxiv.org/pdf/1612.00889.pdf
    """
    n_samples, n_dim = X.shape
    # If w is None fill with 1s
    w = _check_sample_weight(w, X, dtype=X.dtype)
    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype) if dtype is not None else X

    # For small dims just use ones
    alpha = 16 * (np.log(k) + 2)
    # get cluster centers
    centers, centers_ind = kmeans_plusplus_w(X, k, w=w)
    # The below 3 lines are faster than `pairwise_distances_argmin_min`
    # distances to all centers -- shape (n_samples, k)
    all_dists = cdist(X, centers)
    # index of the closest center -- shape (n_samples, ), index in [0 ... k]
    closest_center_idxs = np.argmin(all_dists, axis=1)  # labels

    # distances to closest centers -- shape (n_samples, )
    # center_dists = np.min(all_dists, axis=1)
    # to not run np.min() again
    center_dists = all_dists[np.arange(n_samples), closest_center_idxs]

    # Get cluster sizes. With cluster_sizes[inv] we correspond each sample to its corresponding cluster size
    # read how np.unique works
    clusters, inv, cluster_sizes = np.unique(
        closest_center_idxs, return_inverse=True, return_counts=True
    )
    # Weight cluster sizes
    cluster_sizes = np.array([np.sum(w[closest_center_idxs == c]) for c in clusters])

    # Sum of squared distances for all clusters and total
    cluster_inertia = np.array(
        [
            np.sum(
                center_dists[closest_center_idxs == c] ** 2
                * w[closest_center_idxs == c]
            )
            for c in clusters
        ]
    )
    inertia = np.sum(cluster_inertia)  # weighted inertia
    eps_ = np.finfo(inertia.dtype).eps  # Division to perfect clusters will produce 0 inertia - epsilon to the rescue.

    sp = w * center_dists / (2 * inertia + eps_)
    #  cluster_inertia[closest_center_idxs] = closest center inertia for each point
    sp += w / (2 * k * cluster_sizes[inv])
    centers_ind_adj = adjust_centers_ind(centers_ind, len(clusters), k)
    return sp, centers_ind_adj, cluster_sizes, closest_center_idxs


class CoresetKMeans(CoresetBase):
    _coreset_type = "unsupervised"
    _possible_sensitivities = ["lightweight", "lightweight_per_feature", "practical", "offline"]
    _possible_estimators = ["lightweight", "lightweight_per_feature"]

    def __init__(
        self,
        *,
        algorithm: str = "lightweight",
        enable_estimation: bool = False,
        random_state: Union[int, Generator] = None,
        **sensitivity_kwargs,
    ):
        """_summary_

        Parameters
        ----------
        algorithm : str, default="lightweight"
            Sensitivity algorithm. One of ["lightweight", "lightweight_per_feature", "practical", "offline"]

        enable_estimation: bool, default = False
            True - estimation will be enabled. When the sensitivity is calculated, will compute all information necessary for estimation.
                The algorithm provided must be one of  ["lightweight", "lightweight_per_feature"]
            False - Estimation is disabled. Any attempt to estimate with this parameter false should raise an error.
            
        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        **sensitivity_kwargs: Key arguments
            Extra arguments that will be pased to the sensitivity function
        """

        super().__init__(random_state=random_state)
        self.enable_estimation = enable_estimation
        self.pred_idxs_ = None
        self.cluster_sizes_ = None
        self.center_idxs_ = None
        self.safe_mode = False
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"`Algorithm` must be one of {self._possible_sensitivities}, found {algorithm}")
        if self.enable_estimation and algorithm not in self._possible_estimators:
            raise ValueError(
                f"For estimation, `algorithm` must be one of {self._possible_estimators}, found {algorithm}"
            )
        self._algorithm = algorithm
        self.sensitivity_kwargs = sensitivity_kwargs
        if algorithm == "lightweight" and 'k' in self.sensitivity_kwargs.keys():
            self.sensitivity_kwargs.pop('k')
        self.estimation_params_ = None

    def sensitivity(self, X, y=None, w=None, estimate: bool = False) -> np.ndarray:
        # TODO: maybe a better alternative when not enough samples is to use lightweight
        #  but this later cause issues with sampling as a different coreset object is instantiate.
        # if self.safe_mode and self.algorithm != "lightweight":
        #     if len(X) < self.sensitivity_kwargs.get('k', 8):
        #         self.algorithm = "lightweight"
        #         self.sensitivity_kwargs.pop('k', None)

        if self.algorithm == "lightweight" or self.algorithm == "lightweight_per_feature":
            self.sensitivity_f = sensitivity_lightweight
        elif self.algorithm == "practical":
            self.sensitivity_f = sensitivity_practical
        elif self.algorithm == "offline":
            self.sensitivity_f = sensitivity_offline
        else:
            raise ValueError(f"`self.algorithm` must be one of {self._possible_sensitivities}, found {self.algorithm}")

        if self.algorithm in self._possible_estimators:
            self.sensitivity_kwargs["return_info"] = self.enable_estimation

        if estimate:
            # Estimation can happen only if sensitivity was computed before in the attribute estimation_params_
            self._check_estimation_requirements()
            sensitivities = estimate_lightweight(
                X=X,
                w=w,
                mu=self.estimation_params_["mu"],
                w_sum=self.estimation_params_["w_sum"],
                di_sum=self.estimation_params_["di_sum"],
                per_feature=self.algorithm == "lightweight_per_feature",
            )
        else:
            if self.algorithm == "lightweight" or self.algorithm == "lightweight_per_feature":
                if self.algorithm == "lightweight_per_feature":
                    self.sensitivity_kwargs["per_feature"] = True
                res = self.sensitivity_f(X, w, **self.sensitivity_kwargs)
                # If estimation was enabled return and save information for estimation.
                # This is used to check if estimation is possible in _check_estimation_requirements()
                if self.enable_estimation:
                    sensitivities, self.estimation_params_ = res
                    self._estimation_algorithm_used = self.algorithm
                else:
                    sensitivities = res
            else:
                if self.safe_mode and len(X) < self.sensitivity_kwargs.get("k", 8):
                    # reduce k to prevent exception be raised from kmeans_plusplus_w.
                    # TODO: see lightweight alternative above.
                    self.sensitivity_kwargs["k"] = len(X)
                sensitivities, center_idxs, cluster_sizes, pred_idxs = self.sensitivity_f(
                    X, w, **self.sensitivity_kwargs
                )
                self.center_idxs_ = center_idxs
                self.cluster_sizes_ = cluster_sizes
                self.pred_idxs_ = pred_idxs

        return sensitivities

    def compute_sensitivities(self, X, y=None, w=None, estimate: bool = False):
        self.sensitivities = self.sensitivity(X, y, w, estimate=estimate) if X.shape[0] > 0 else np.ndarray([])
        return self

    def union(self, coresets: List["CoresetKMeans"]) -> "CoresetKMeans":
        raise NotImplementedError

    def sample(
            self,
            *,
            coreset_size: Optional[Union[int, Tuple[int, int]]] = None,
            deterministic_size: Optional[Union[float, Dict[Any, float]]] = None,
            keep_duplicates: bool = False,
            sum_to_previous: bool = False,
            order: Optional[str] = "sort",
            det_weights_behaviour: str = "keep",
            **sample_kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        if coreset_size is not None and not is_int(coreset_size, positive=True):
            raise TypeError(f"`coreset_size` must be None or a positive int, found {type(coreset_size)} "
                            f"(resampling is not yet supported for k-Means)")
        if coreset_size is None:
            coreset_size = self.sample_kwargs["coreset_size"]
            assert coreset_size is not None, "sample_kwargs should contain `coreset_size` different than None"
        if self.algorithm == "lightweight" or self.algorithm == "lightweight_per_feature":
            # if no adding of centroid samples is done
            return super().sample(
                coreset_size=coreset_size,
                deterministic_size=deterministic_size,
                keep_duplicates=keep_duplicates,
                sum_to_previous=sum_to_previous,
                det_weights_behaviour=det_weights_behaviour,
                order=order,
            )
        else:
            n_samples = self.n_samples  # computed before
            # sampling "trick" adding the centroid of kmeans++
            n_clusters = len(self.center_idxs_)
            if n_clusters >= n_samples or n_clusters >= coreset_size:
                idxs = self.center_idxs_
                final_weights = self.cluster_sizes_
            else:
                idxs, final_weights = super().sample(
                    coreset_size=coreset_size - n_clusters,
                    deterministic_size=deterministic_size,
                    keep_duplicates=keep_duplicates,
                    sum_to_previous=sum_to_previous,
                    det_weights_behaviour=det_weights_behaviour,
                    order=order,
                )
                cluster_sizes = self.cluster_sizes_
                pred_idxs = self.pred_idxs_[idxs]
                center_idxs = self.center_idxs_
                for cluster in range(n_clusters):
                    t_idxs = np.where(pred_idxs == cluster)[0]
                    # if centroid is not part of the sampled index, add it.
                    if center_idxs[cluster] not in t_idxs:
                        # The final weights should be around the weighted cluster size. If they are lower
                        # add the center with a weight to adjust the difference.
                        center_weight = cluster_sizes[cluster] - np.sum(final_weights[t_idxs])
                        if center_weight > 0:
                            idxs = np.append(idxs, [center_idxs[cluster]], axis=0)
                            final_weights = np.append(final_weights, center_weight)
                    # if centroid is part of the sampled index, update it
                    else:
                        t_idxs = t_idxs[t_idxs != center_idxs[cluster]]
                        center_weight = cluster_sizes[cluster] - np.sum(final_weights[t_idxs])
                        print("exists", center_weight)
                        if center_weight > 0:
                            final_weights[idxs == center_idxs[cluster]] += center_weight

            return idxs, final_weights

    def to_dict(
        self,
        with_important: bool = True,
        to_list: bool = True,
        sensi_only: bool = False,
        use_keep_selected_only: bool = True,
    ):
        """
        Add center_idxs, cluster_sizes and pred_idxs to be saved together with the coreset object
        """

        def f_array(v):
            return v.tolist() if to_list and v is not None else v

        result = super().to_dict(
            with_important=with_important,
            to_list=to_list,
            sensi_only=sensi_only,
            use_keep_selected_only=use_keep_selected_only,
        )
        result.update(
            {
                "center_idxs_": f_array(self.center_idxs_),
                "cluster_sizes_": f_array(self.cluster_sizes_),
                "pred_idxs_": f_array(self.pred_idxs_),
            }
        )
        return result

    def set_state(self, state_dict):

        super().set_state(state_dict)
        self.center_idxs_ = np.array([] if self.center_idxs_ is None else self.center_idxs_)
        self.cluster_sizes_ = np.array([] if self.cluster_sizes_ is None else self.cluster_sizes_)
        self.pred_idxs_ = np.array([] if self.pred_idxs_ is None else self.pred_idxs_)

        return self
