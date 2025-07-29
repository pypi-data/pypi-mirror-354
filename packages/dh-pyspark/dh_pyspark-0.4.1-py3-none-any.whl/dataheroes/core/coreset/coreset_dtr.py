import math
import traceback

import numpy as np
import pandas as pd

from typing import Union, Any, Dict, Iterable, Tuple, Optional
from numpy.random import RandomState, Generator, BitGenerator
from sklearn.base import BaseEstimator
from sklearn.tree import BaseDecisionTree, DecisionTreeRegressor
from sklearn.utils import check_random_state
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from KDEpy import FFTKDE
from scipy.signal import argrelextrema

from ._base import CoresetBase
from ..common import default_coreset_size
from ..sklearn_extra import kmeans_plusplus_w
# Import from core package (from .. import CoresetDTC, CoresetKMeans) causes circular dependency; use this instead:
from ..coreset import CoresetDTC, CoresetKMeans
from dataheroes.services import helpers


class CoresetDTR(CoresetBase):

    _coreset_type = "regression"
    # TODO "dtr_method_3" is not supported in the first release.
    _possible_sensitivities = ["dtr_method_1", "dtr_method_2", "dtr_method_4"]

    def __init__(
        self, *, algorithm: str = "dtr_method_1", random_state: Union[int, Generator] = None, **sensitivity_kwargs
    ):
        """Coreset for the Decision Trees classification task.

        Parameters
        ----------
        algorithm: str, default = "dtr_method_1"
            Sensitivity algorithm - one of:
            ["dtr_method_1", "dtr_method_2", "dtr_method_3", "dtr_method_4"]
            See mapping of generic names to actual methods in the 'sensitivity' function.

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        **sensitivity_kwargs: Key arguments
            parameters to be passed to the sensitivity function
        """
        super().__init__(random_state=random_state)
        self._algorithm = algorithm
        self.is_classification = False
        self.sensitivity_kwargs = sensitivity_kwargs
        self.y_encoded = None

        # Set sensitivity
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        else:
            self._algorithm = algorithm

    @property
    def y(self):
        if self.algorithm == "dtr_method_3":
            raise ValueError("y labels are not used with this sensitivity")
        else:
            if self.y_encoded is None:
                raise ValueError("Call `.build()` or `.sensitivity()` before")
            return self.y_encoded

    def sensitivity(self, X, y=None, w=None) -> np.ndarray:
        if self.algorithm == "dtr_method_3":
            sensitivity_f = sensitivity_partition
        elif self.algorithm == "dtr_method_4":
            sensitivity_f = sensitivity_dtc_y_clust_d_b
        elif self.algorithm == "dtr_method_2":
            sensitivity_f = sensitivity_dtc_y_clust_kde_silverman
        elif self.algorithm == "dtr_method_1":
            sensitivity_f = sensitivity_dtc_y_clust_kde_isj
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        sensitivities, self.y_encoded = sensitivity_f(X, y, w, self.random_state, **self.sensitivity_kwargs)
        return sensitivities

    def sample(
        self,
        *,
        coreset_size: Optional[Union[int, Tuple[int, int]]] = None,
        deterministic_size: Optional[float] = None,
        sample_all: Optional[Iterable[Any]] = None,
        class_size: Optional[Dict[Any, int]] = None,
        minimum_size: Optional[Union[int, str, Dict[Any, int]]] = None,
        fair: Union[str, bool] = "training",
        order: str = "sort",
        keep_duplicates: bool = False,
        sum_to_previous: bool = False,
        as_classification: bool = False,
        det_weights_behaviour: str = "keep",
        random_state: Union[int, Generator] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Ensuring sampling applied matches sensitivity computation methods:

        Important to emphasize that in the test suite, we call "build" on a CoresetDTC object which was built with
        the original X and the "converted" y.
        This "build" then computes sensitivities and samples (for classification tasks such as CoresetDTC) using
        "choice_classification".
        But, for all methods but Ernesto's here, the end product of CoresetDTR's sensitivity function is not a coreset,
        but sensitivities - which are computed as a part of the regular "build".
        So if we will be simply calling CoresetDTR.build(), what will happen is the standard execution of the "build"
        flow, like with all other coresets - the specific sensitivity calculation function will be called (that's
        our new implementation here) - and then the standard sampling, based on our coreset type - which is
        regression.
        In other words, if we do not add special treatment, "choice" will be called instead of
        "choice_classification" - and then, in our solution here, the sampling will not be matching the
        sensitivities' calculation.

        For this reason, we've implemented the following solution -

        In coreset_dtr.py:
        1. In "sensitivity" functions matching one of the DTR-to-DTC flavours, the transformed y will be saved under
           self.y_class_labels.
        2. "sample" will be overridden (similar to coreset_kmeans.py), and for the DTR-to-DTC flavours, will pass a
           "True" value to the base-class's “sample” function's new flag (see below), to use the self.y_class_labels;
           however, if it is not a DTR-to-DTC flavour (i.e. Ernesto's flavour), it'll just call the base "sample" with
           the default flag's value of "False").

        In _base.py:
        1. Add a flag to the "sample" function instructing to treat y as a regression y transformed to a
           classification y.
        2. Inside "sample", if [the new flag is "True", or if self.is_classification, or if
           self._coreset_type == "classification"), define "handle_classification = True", and use this flag as
           the sole classification indicator throughout (and not like we do with the existing disparate conditions).
        3. Additionally, if the new flag is "True", override y from the input, and define it as
           "y = self.y_class_labels".
        """
        if self.algorithm == "dtr_method_3":  # "sensitivity_partition"
            return super().sample(
                coreset_size=coreset_size,
                deterministic_size=deterministic_size,
                order=order,
                keep_duplicates=keep_duplicates,
                sum_to_previous=sum_to_previous,
                as_classification=False,
                random_state=random_state,
                det_weights_behaviour=det_weights_behaviour,
            )
        else:
            return super().sample(
                coreset_size=coreset_size,
                deterministic_size=deterministic_size,
                fair=fair,
                order=order,
                keep_duplicates=keep_duplicates,
                sum_to_previous=sum_to_previous,
                as_classification=True,
                random_state=random_state,
                det_weights_behaviour=det_weights_behaviour,
            )


def sensitivity_partition(
    X, y, weights=None, random_state: Union[int, Generator] = None, partition_tree_max_leaf_nodes: int = 64
) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    This latest Ernesto's algorithm variant is sensitivity based, and its latest version produces sensitivity values,
    which we can use – as they are – in our end-product.

    It is important to mention and keep in mind that this algorithm requires one phase of training a
    DecisionTreeRegressor (AKA "partition tree") on the full training data in its initial stage – so while being
    very useful for goals of repetitive nature, such as hyperparameter optimization via grid searches, for example –
    it is probably less appropriate for single-tree regression tasks, and we may want to default to one of the other
    3 flavours for tasks of such nature (otherwise, we're better off without coresets).

    NOTE:
        A "k" parameter is required for the algorithm today. It is eventually used as "max_leaf_nodes" when the
        DecisionTreeRegressor object is generated by the algorithm for the sake of producing an initial partition tree.
        This is the "partition_tree_max_leaf_nodes" in this method.

        We needed to define how to calculate it internally.
        In our evaluation suite, it was determined using two methods:
        1. For DecisionTreeRegressor modeling, it was found via Grid Search on the full dataset, which totally beats
           the purpose of coreset, of course, so it is not relevant as a solution.
        2. For XGBRegressor modeling, it is set as the default value which is used later by XGB models, which is 64
           (matching the default max depth of XGB trees of 6).
           We've decided here that we'll use this constant for both DTR and XGB during the building of the partition
           tree. For DTR, it doesn't matter much, because there won't be much use of it anyway, so it isn't that
           important. For XGB, that's what we've been working with thus far.

    Source:
        TODO Add reference to Ernesto's paper, once published.
    """

    legacy_random_state = rng_to_legacy_random_state(random_state)
    if weights is None:
        weights = np.ones_like(y)
    sensitivities_bicriteria = np.zeros_like(y, dtype=np.float64)
    sensitivities_dist_to_bicriteria = np.zeros_like(y, dtype=np.float64)

    # Split data into small subsets by calculating a list of [[idx1 idx2, ...], ...] data indices in each cell.
    # When splitting is based on a partition tree, after predicting leaf_id for each data point, group data into leaves.
    partition_tree = DecisionTreeRegressor(max_leaf_nodes=partition_tree_max_leaf_nodes,
                                           random_state=legacy_random_state).fit(X, y, sample_weight=weights)
    sample_idxs_by_leaves = dt_sample_idxs_by_leaves(tree_model=partition_tree, X=X)

    # Assign to every data point a sensitivity. Sensitivity of data is calculated in each cell.
    for leaf_sample_idxs in sample_idxs_by_leaves:
        X_cell = X[leaf_sample_idxs]
        y_cell = y[leaf_sample_idxs]
        ndims = X_cell.shape[-1]
        mu = np.mean(y_cell)

        for dim in range(ndims):  # TODO (Ernesto): optimize by sorting once outside

            # TODO (Igor): this section replaces "sort_on_dim" in the original code, verify correctness.
            to_sort_on_dim = np.array(leaf_sample_idxs)
            if X_cell.ndim == 2:
                Xi = X_cell[:, dim]
            else:
                Xi = X_cell
            sort_idx = np.argsort(Xi, kind="stable")
            idxs_sorted = to_sort_on_dim[sort_idx]
            # TODO (Igor): end of section.

            weights_sorted = weights[idxs_sorted]
            weights_cumsum = np.cumsum(weights_sorted)
            weights_cumsum_reverse = np.cumsum(weights_sorted[::-1])[::-1]
            for i, idx in enumerate(idxs_sorted):
                sensitivities_bicriteria[idx] = max(
                    sensitivities_bicriteria[idx],
                    1 / weights_cumsum[i],
                    1 / weights_cumsum_reverse[i])
        for _, idx in enumerate(leaf_sample_idxs):
            sensitivities_dist_to_bicriteria[idx] = (y[idx] - mu) ** 2

    # Final update of the sensitivity after processing all cells.
    dists_sum = np.sum(sensitivities_dist_to_bicriteria)
    if dists_sum > 0:
        sensitivities_dist_to_bicriteria /= dists_sum
    sensitivities = weights * np.maximum(
        np.maximum(
            4 * sensitivities_bicriteria,
            sensitivities_dist_to_bicriteria),
        weights / np.sum(weights)
    )

    # TODO (Igor) -
    #  Consult Ernesto.
    #  Our methods are based on SVD, check with him that his numbers are similar to ours.
    #  We can perhaps compare the sensitivities we get before, and after.
    #  Also, we need to consult him on the effects of sampling with replacements vs. without.
    return sensitivities, None


def sensitivity_dtc_y_clust_d_b(X,
                                y,
                                weights=None,
                                random_state: Union[int, Generator] = None,
                                scoring_type: str = "davies_bouldin",
                                preset_k=None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    This method translates the y target into classes and leverages the existing CoresetDTC for classification to
    produce a coreset.
    The goal is to divide a 1-dimensional y array into clusters based on its numeric values.
    This is achieved via work with the ClusterClassLabelingHeuristic class (see the detailed description inside).

    Now, having the original X train input and y train regression targets converted to class labels, we can generate
    a CoresetDTC object, compute its sensitivities, and return these exact sensitivities as the end-product.

    Special handling is required for ensuring that the sampling method matches the method of sensitivity calculation.
    These two algorithm options are mostly, but not all the time, the fastest between the four.
    """

    # k-Means coreset generation during the search for the optimal k requires providing coreset_size.
    # In the experimental suite, we've had the exact value, because building the coreset using this method was an
    # all-in-one process.
    # However, in this eventual implementation, the coreset_size is supplied only during the call to "build" -
    # nevertheless, we need it during the calculation of sensitivities.
    # Therefore, resembling methods elsewhere in our library, we generate a substitute value by calling the default
    # coreset size function below, which is based on the number of features and instances (whereas the number of
    # classes for a regression problem is considered to be 2).
    k_means_coreset_size = default_coreset_size(
        n_classes=2,
        n_features=X.shape[1],
        n_instances=X.shape[0]
    ).get('coreset_size')
    legacy_random_state = rng_to_legacy_random_state(random_state)
    h_input = y.reshape(-1, 1)
    h = ClusterClassLabelingHeuristic(X=h_input, w=weights, cluster_scorer=ClusterScorer(scoring_type),
                                      coreset_size=k_means_coreset_size, random_state=legacy_random_state)
    h.prepare_km_coreset()
    if preset_k is None:
        h.approximate_optimal_k()
        k = h.optimal_k
    else:
        k = preset_k
    h.produce_k_cluster_labels(k=k)
    y_class_labels = np.array(h.cluster_labels, dtype=int)

    dtc_coreset = CoresetDTC(random_state=random_state)
    sensitivities = dtc_coreset.sensitivity(X=X, y=y_class_labels, w=weights)
    return sensitivities, y_class_labels


def _sensitivity_dtc_y_clust_kde(bw: str,
                                 X,
                                 y,
                                 weights=None,
                                 random_state: Union[int, Generator] = None, dtype: str = 'float32') -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    KDE-based methods translate the y target into classes and leverage the existing CoresetDTC for classification
    to produce coresets.
    The goal is to divide a 1-dimensional y array into clusters based on its numeric values.
    This is achieved via the call to the produce_kde_based_labels function (see the detailed description inside).

    Now, having the original X train input and y train regression targets converted to class labels, we can generate
    a CoresetDTC object, compute its sensitivities, and return these exact sensitivities as the end-product.

    Special handling is required for ensuring that the sampling method matches the method of sensitivity calculation.
    These two algorithm options are mostly, but not all the time, the fastest between the four.
    """

    if bw is None or bw not in ["silverman", "ISJ"]:
        raise ValueError(f"Unexpected value {bw=}")
    y_class_labels = produce_kde_based_labels(bw=bw, y=y, w=weights)
    dtc_coreset = CoresetDTC(random_state=random_state, dtype=dtype)
    sensitivities = dtc_coreset.sensitivity(X=X, y=y_class_labels, w=weights)
    return sensitivities, y_class_labels


def sensitivity_dtc_y_clust_kde_silverman(X,
                                          y,
                                          weights=None,
                                          random_state: Union[int, Generator] = None, dtype: str = 'float32') -> Tuple[np.ndarray, Optional[np.ndarray]]:
    return _sensitivity_dtc_y_clust_kde(bw="silverman", X=X, y=y, weights=weights, random_state=random_state, dtype=dtype)


def sensitivity_dtc_y_clust_kde_isj(X,
                                    y,
                                    weights=None,
                                    random_state: Union[int, Generator] = None, dtype: str = 'float32') -> Tuple[np.ndarray, Optional[np.ndarray]]:
    return _sensitivity_dtc_y_clust_kde(bw="ISJ", X=X, y=y, weights=weights, random_state=random_state, dtype=dtype)


########################################################################################################################
#                                    Sensitivity Calculation Logic Tools and Utils                                     #
########################################################################################################################

################
#    Common    #
################


def legacy_random_state_to_rng(legacy_random_state: RandomState) -> Union[Generator, None]:
    """
    DH base coreset mechanism supports only int seed or an RNG - numpy.random.Generator (new method).
    However, many of sklearn's algorithms do not support generators yet.
    To keep working continuously with the same BitGenerator object under a (new) RNG but based on an (old)
    RandomState method, we apply a kind of dirty trick which extracts the (pretty outdated) BitGenerator straight
    from the legacy RandomState and assigned it to the RNG, which it then returns.
    If random_state is None, then None will be returned.
    """
    if legacy_random_state is not None:
        legacy_bit_generator: BitGenerator = legacy_random_state._bit_generator
        return Generator(legacy_bit_generator)
    else:
        return None


def rng_to_legacy_random_state(rng: Generator) -> Union[RandomState, None]:
    """
    DH base coreset mechanism supports only int seed or an RNG - numpy.random.Generator (new method).
    However, many of sklearn's algorithms do not support generators yet.
    To keep working continuously with the same BitGenerator object under an (old) RandomState method but based on
    a (new) RNG, we initiate a RandomState based on the RNG's existing BitGenerator.
    If rng is None, then None will be returned.
    """
    if rng is not None:
        rng_bit_generator: BitGenerator = rng.bit_generator
        return RandomState(rng_bit_generator)
    else:
        return None


def fast_1dim_unique(X):
    """
    For finding unique values only (without sorting), in a 1-dimensional array, using pd instead of np, is much
    faster (O(n) vs. O(nlogn)) - but it works only on 1D array.
    """
    return pd.unique(X)


def fast_ndim_unique(X):
    """
    For finding unique values only (without sorting), in a multidimensional array, this implementation is
    expected to be substantially faster than using np.unique().
    (pd.unique() is also much faster than np.unique (O(n) vs. O(nlogn)), but it works only on 1D array.)
    """
    return list(dict.fromkeys(map(tuple, X)))


def dt_sample_idxs_by_leaves(tree_model: BaseEstimator, X):
    """
    This function returns a list of decision tree leaves, where each leaf is a list containing indices of data
    points that belong to the leaf.

    One way to produce the leaves from model and data:
    leaves = tree_model.apply(X)

    An example for data with 18 elements returned by the call above:
    leaves = [1,1,1,1,2,2,2,2,3,3,3,3,3,3,3,1,1,1]
    The 'leaves' array represents predicted leaf indices for each data point.

    For the leaves in this example, this method will return the following result:
    result = [[0, 1, 2, 3, 15, 16, 17],
              [4, 5, 6, 7],
              [8, 9, 10, 11, 12, 13, 14]]

    This is the fastest way we know to get the task done, without relying on the decision_path which is totally
    redundant when all we want is to only get the leaves - for which it is enough to simply apply the model on X!
    """
    leaves = None
    if helpers.is_xgb_installed():
        if tree_model.__class__.__name__ == "XGBRegressor":
            leaves = tree_model.apply(X)
            # For XGBoost, see explanation in XGBModel.apply(); the last tree is SUPPOSED to be the best tree.
            if leaves.ndim == 2:
                leaves = leaves[:, -1]
    if helpers.is_lgb_installed():
        from lightgbm import Booster
        
        if tree_model.__class__.__name__ == "LGBMRegressor" or isinstance(tree_model, Booster):
            if tree_model.__class__.__name__ == "LGBMRegressor":
                num_trees = tree_model.n_estimators_
            else:
                num_trees = tree_model.num_trees()
            leaves = tree_model.predict(X, start_iteration=num_trees - 1, num_iteration=1, pred_leaf=True)
    if isinstance(tree_model, BaseDecisionTree):
        leaves = tree_model.apply(X)
    if leaves is None:
        raise ValueError(f"Model type not supported. Found {type(tree_model)}")
    # 'sort=True' will take a bit more time but will produce the same results as with alternative implementations
    # (which are run deterministically with set randoms) - however, the order of the inner lists within the outer
    # list has no meaning whatsoever. In practice, though, even with 'sort=True', the running times seem to be
    # roughly the same.
    sample_idxs_by_leaves = pd.Series(range(len(leaves))).groupby(leaves, sort=True).apply(list).tolist()
    return sample_idxs_by_leaves


#############################
#    Ernesto 2023 Method    #
#############################


# No helper methods required at the moment.


#################################################
#    Y-Clustering Reg2Class Heuristic Method    #
#################################################


class ClusterScorer:
    """
    Scorer class for the ClusterClassLabelingHeuristic method below - see a detailed description inside it.

    NOTE:
        Scoring a k candidate is applied on a sample of the full training data (which is a 1-dimensional vector
        of y values).
        1. For the (not currently used) very-long-to-compute Silhouette score, we've used to sample 1% and require
           a minimal sampling size of 10K (but not to exceed the original training size).
        2. For the other, faster-to-compute score types – including the chosen Davies-Bouldin – we currently sample
           10% and require a minimal sampling size of 100K (but not to exceed the original training size).
        3. These values were decided in the past and experimented-with throughout the whole experiment-running era,
           but they should not be considered as set in stone.
        4. In the future though, we may want to define new guidelines, maybe based on the size of input (e.g.,
           percentages will be set matching some input size thresholds, etc.).

    At the moment, however, these constants will remain as an open issue, until we will profile the performance
    once we finish implementation, and fine-tune them.
    """
    POSSIBLE_SCORERS = ["silhouette", "davies_bouldin", "calinski_harabasz"]

    def __init__(self, scorer_type: str):
        if scorer_type not in self.POSSIBLE_SCORERS:
            raise ValueError(f"Unexpected {scorer_type=}, must be in {self.POSSIBLE_SCORERS}")

        if scorer_type == "silhouette":
            self.scoring_func = silhouette_score
        elif scorer_type == "davies_bouldin":
            self.scoring_func = davies_bouldin_score
        elif scorer_type == "calinski_harabasz":
            self.scoring_func = calinski_harabasz_score
        else:
            self.scoring_func = None

    def scoring_sample_size(self, full_training_size: int) -> int:
        # TODO See remark at the class level regarding the constants below (sampling_pct, min_sample_size).
        if self.scoring_func == silhouette_score:
            # Very high cost, hard to compute - forced to use low numbers.
            sampling_pct = 0.01
            min_sample_size = 10_000
        else:
            # Low cost, easy to compute - can use high numbers.
            sampling_pct = 0.1
            min_sample_size = 100_000

        sample_size = min(full_training_size,
                          max(min_sample_size,
                              int(np.round(full_training_size * sampling_pct))))
        return sample_size

    def score(self, X_sample, cluster_labels) -> float:
        if self.scoring_func == davies_bouldin_score:
            return -self.scoring_func(X=X_sample, labels=cluster_labels)  # Lower is better.
        else:
            return self.scoring_func(X=X_sample, labels=cluster_labels)  # Higher is better.


class ClusterClassLabelingHeuristic:
    """
    This algorithm is a general heuristic able to generate class labels for any given n-dimensional input (X).
    Specifically, for n-dimensional input (X) of samples passed, it leverages clustering techniques & coresets
    in order to generate class labels at the sample level.

    While the basic use for this algorithm, at the time being, is to translate a one-dimensional y target array of
    a regression problem into class labels (in order to leverage the existing CoresetDTC for classification to
    produce a coreset) - this heuristic is able to provide class labels to any n-dimensional X input.

    The outline is as follows:

    i. Build k-Means ("lightweight") coreset using the full training data.
    ii. Approximate "optimal k":
        1. Define range between 2 and min[sqrt(len(training_data)),
                                          unique_y_values(training_data),
                                          unique_y_values(k_means_coreset)]
        2. Phase 1:
            a. Define k geometrically-spaced candidates within the above range.
            b. Iteratively score candidates using:
                i. Build k-Means model using k-Means coreset with the k candidate input.
                ii. Score k candidate by using the model to predict cluster labels on a sample from the original
                    input (more on that later) and utilizing one of the common clustering internal evaluation schemes:
                    1. Our current implementation supports Silhouette, Davies-Bouldin, and Calisnki-Harabasz scoring.
                    2. Current long-standing tool-evaluated decision is to use Davies-Bouldin (hence the “D-B” in
                       the method name).
                iii. Choose best phase 1 candidate, e,g, "k candidate at index P".
        3. Phase 2:
            a. Within the range of phase 1 candidates at indices P-1 to P+1, apply binary search using same
               scoring technique as in phase 1.
            b. The search – reasonably and based on experience – assumes that within the examined range, there is
               a monotonic increase or decrease in quality, rendering binary search as effective.
            c. Best-scoring candidate from this phase is defined as the "optimal k".
    iii. Produce new y as class labels using the "optimal k":
        1. Build k-Means model using k-Means coreset with the "optimal k" input.
        2. Use the model to predict cluster labels on the full training data set.
        3. Return predicted cluster labels as class labels.
    iv. Now, the caller of this class, having the original X train input and y train regression targets converted
        to y class labels, will be able to use a classification-based coreset generation technique (with the
        appropriate sensitivities computation and sampling).

    OPEN ITEMS:
    1. TODO Potential performance improvement:
        When we see Phase 1 passing the peak and moving to decline over progressive ks, we can add an improvement
        where we decide to cut any further exploration because the chance there will be additional peak in advanced
        ks is very slim (at least with silhouette_score case).
        UPDATE: This doesn't seem to always be the case; in general, the assumption holds - however, it is not a
                straight linear line, it has some saw teeth in it; we defer this improvement for the time-being.
    2. TODO Max value in Phase 1 is set as sqrt(n), but we may want to reconsider it.
    3. TODO "lightweight" vs. the others:
        For X_coreset, we run the CoresetKMeans lightweight here; however, we may consider running the "practical",
        with the max planned k (we know what it is), because having a bigger coreset for the max k is good enough
        for all underlying coresets
    """

    def __init__(self,
                 X,
                 w,
                 cluster_scorer: ClusterScorer,
                 coreset_size: int,
                 random_state: Union[int, RandomState] = None):
        self._X = X
        self._w = w
        self._cluster_scorer = cluster_scorer
        self._coreset_size = coreset_size
        self._X_coreset = None
        self._w_coreset = None
        self._optimal_k = None
        self._cluster_labels = None
        # sklearn is still behind DataHeroes and doesn't yet support numpy.Random.Generator; therefore, we employ
        # sklearn's check_random_state and not ours.
        # See https://github.com/scikit-learn/scikit-learn/issues/16988
        self._random_state = check_random_state(random_state)
        # DH requires RNG, so we translate the legacy random state to an RNG.
        self._rng = legacy_random_state_to_rng(self._random_state)

    @staticmethod
    def _properly_weighted_fit_kmeans(X, sample_weight, n_clusters,
                                      random_state: Union[int, RandomState] = None):
        """
        This is the proper way to produce a weighted & fit K-Means -- borrowed from:
        CoresetTreeServiceKMeans._fit_internal(...).
        """
        initial_centers, _ = kmeans_plusplus_w(X=X, n_clusters=n_clusters, w=sample_weight, random_state=random_state)
        km_model = KMeans(n_clusters=n_clusters, n_init=1, random_state=random_state)
        km_model.set_params(init=initial_centers)
        km_model.fit(X, sample_weight=sample_weight)
        return km_model

    def _score_clustering_model(self, model, verbose: bool = False):
        """
        Provided clustering model will be scored based on the cluster_scorer property on a sample from the
        full training set. The cluster_scorer provides the scoring technique and the sample size.

        While silhouette_score supports scoring on a sample of the full training set -
            `
            silhouette_avg = silhouette_score(X=X_full, labels=cluster_labels,
                                              sample_size=silhouette_sample_size, random_state=random_state)
            `
        ...the other currently supported methods do not, and require scoring on the full set.

        Moreover, silhouette_score's built-in sample scoring support has two disadvantages:
            (1) It requires predictions made on the full training set - with sampling being utilized on the sampled
                part only in the second phase.
            (2) There are some rarer cases where a sample generated via silhouette_score will consist of a single
                unique cluster label - in which case, the scoring within the silhouette_score method will fail
                because the minimum number of required labels is 2.

        In our implementation here, we solve all these issues: (a) allow sampling for non-silhouette_score, (b) require
        predictions made on sample only, and (c) if a random selection produces a single label, we will resample until
        we have at least 2 labels.
        """
        full_training_size = self._X.shape[0]
        scoring_sample_size = self._cluster_scorer.scoring_sample_size(full_training_size)

        remaining_attempts = 10_000  # Prevent possible infinite loop.
        num_labels = 0
        while num_labels < 2 and remaining_attempts > 0:
            sample_idxs = self._random_state.choice(full_training_size, scoring_sample_size, replace=False)
            X_sample = self._X[sample_idxs]
            # TODO
            #  Providing "sample_weight" to "predict" is no longer supported starting with scikit-learn 1.5, since,
            #  apparently, it never had any effect in the past during "predict" anyway, and sklearn have now cleaned-up
            #  their API. Basically, we have no way to impose prior weights at this point.
            # X_w = self._w[sample_idxs] if self._w is not None else None
            # cluster_labels = model.predict(X_sample, sample_weight=X_w)
            cluster_labels = model.predict(X_sample)
            num_labels = len(fast_1dim_unique(cluster_labels))
            if num_labels < 2:
                if verbose:
                    print(f"WARNING: {num_labels=}, retrying to find new sample")
            else:
                # TODO
                #  To the best of our knowledge, the unsupervised scoring functions of sklearn do not support
                #  prior sample weights.
                return self._cluster_scorer.score(X_sample=X_sample, cluster_labels=cluster_labels)
            remaining_attempts -= 1
        raise ValueError("Exhausted maximum number of attempts for clustering model scoring sample generation")

    def _score_k_candidate(self, k_cand, verbose: bool = False):
        km_model = self._properly_weighted_fit_kmeans(X=self._X_coreset,
                                                      sample_weight=self._w_coreset,
                                                      n_clusters=k_cand,
                                                      random_state=self._random_state)
        cluster_score = self._score_clustering_model(model=km_model, verbose=verbose)
        return cluster_score

    def _optimal_k_approximation(self, verbose: bool = False):

        full_training_size = self._X.shape[0]
        k_min = 2
        # Must make sure not to surpass the number of unique samples in the actually-selected coreset length and
        # the number of unique samples in X.
        sqrt_X = int(np.ceil(np.sqrt(full_training_size)))
        num_unique_X_coreset = len(fast_ndim_unique(self._X_coreset))
        num_unique_X = len(fast_ndim_unique(self._X))
        k_max = min(sqrt_X, num_unique_X_coreset, num_unique_X)

        # TODO Our original intent:
        #
        # k_cands = []
        # k_cand = k_min // 2
        # while k_cand < k_max:
        #     k_cand *= 2
        #     k_cands.append(int(k_cand)) if k_cand < len(self._X_coreset) else None

        # To keep the same logarithmic logic as the original intent, limit 'k_cands_num' to log2(k_max):
        k_cands_num = int(math.ceil(math.log2(k_max)))

        # TODO Alt. approach 1 - linspace is EVENLY spaced over 'k_cands_num' samples:
        # space_method = np.linspace
        # TODO Alt. approach 2 (selected) - geomspace is LOG-SCALE (GEOMETRICALLY) spaced over 'k_cands_num' samples:
        space_method = np.geomspace

        # Produce Phase 1 candidates.
        k_cands = list(dict.fromkeys([int(x) for x in space_method(k_min, k_max, k_cands_num)]))

        if verbose:
            scoring_sample_size = self._cluster_scorer.scoring_sample_size(full_training_size)
            print(f"---Phase 1 start: {full_training_size=} "
                  f"(planned){self._coreset_size=} (eventual){len(self._X_coreset)=} "
                  f"{scoring_sample_size=} {k_min=} {k_max=} "
                  f"(=min({sqrt_X=}, {num_unique_X_coreset=}, {num_unique_X=})) "
                  f"{k_cands=}")

        # Phase 1 candidate search.
        best_k_cand_idx = -1
        best_k_cand_score = float('-inf')
        for k_cand_idx, k_cand in enumerate(k_cands):
            cluster_score = self._score_k_candidate(k_cand, verbose)
            if verbose:
                print(f"{k_cand_idx=} {k_cand=} {cluster_score=}")
            if cluster_score > best_k_cand_score:
                best_k_cand_idx = k_cand_idx
                best_k_cand_score = cluster_score
        if verbose:
            print(f"---Phase 1 end: {best_k_cand_idx=} best_k={k_cands[best_k_cand_idx]} {best_k_cand_score=}")

        # Phase 2 candidate search.
        best_k_cand_zoom_idx = -1
        best_k_cand_zoom_score = float('-inf')
        k_zoom_min = k_cands[best_k_cand_idx - 1] if best_k_cand_idx > 0 else k_min
        k_zoom_max = k_cands[best_k_cand_idx + 1] if best_k_cand_idx < len(k_cands) - 1 else k_cands[-1]
        k_zoom_cands = list(np.arange(k_zoom_min, k_zoom_max, 1))
        k_zoom_cands.append(k_zoom_max)
        for k_zoom_cand_idx, k_zoom_cand in enumerate(k_zoom_cands):
            if k_zoom_cand == k_cands[best_k_cand_idx]:
                best_k_cand_zoom_idx = k_zoom_cand_idx
                best_k_cand_zoom_score = best_k_cand_score
        if best_k_cand_zoom_idx < 0:
            raise ValueError("best_k_cand_zoom_idx not found")

        if verbose:
            print(f"---Phase 2 start: {k_zoom_min=} {k_zoom_max=} {best_k_cand_zoom_idx=} "
                  f"{k_zoom_cands[best_k_cand_zoom_idx]=} {k_zoom_cands=}")

        idx_low = 0
        idx_high = len(k_zoom_cands) - 1
        idx_pivot = best_k_cand_zoom_idx

        while idx_low <= idx_high:

            idx_pivot_low = (idx_low + idx_pivot) // 2
            k_cand_low = k_zoom_cands[idx_pivot_low]
            k_cand_low_cluster_score = self._score_k_candidate(k_cand_low, verbose)

            idx_pivot_high = (idx_pivot + idx_high) // 2
            k_cand_high = k_zoom_cands[idx_pivot_high]
            k_cand_high_cluster_score = self._score_k_candidate(k_cand_high, verbose)

            if verbose:
                print(f"[{idx_low}_{idx_pivot_low}_({idx_pivot})_{idx_pivot_high}_{idx_high}] "
                      f"[{k_zoom_cands[idx_low]}_{k_zoom_cands[idx_pivot_low]}_({k_zoom_cands[idx_pivot]})_"
                      f"{k_zoom_cands[idx_pivot_high]}_{k_zoom_cands[idx_high]}] "
                      f"{idx_low=} {idx_pivot_low=} {k_cand_low=} {k_cand_low_cluster_score=}   |   "
                      f"{idx_pivot=}   |   "
                      f"{best_k_cand_zoom_score=}   |   "
                      f"{idx_high=} {idx_pivot_high=} {k_cand_high=} {k_cand_high_cluster_score=}")

            if k_cand_low_cluster_score >= k_cand_high_cluster_score:
                # Explore left (+ equality arbitrarily assigned to the left).
                if k_cand_low_cluster_score > best_k_cand_zoom_score:
                    best_k_cand_zoom_idx = idx_pivot_low
                    best_k_cand_zoom_score = k_cand_low_cluster_score
                idx_high = idx_pivot - 1
                idx_pivot = idx_pivot_low
            else:
                # Explore right.
                if k_cand_high_cluster_score > best_k_cand_zoom_score:
                    best_k_cand_zoom_idx = idx_pivot_high
                    best_k_cand_zoom_score = k_cand_high_cluster_score
                idx_low = idx_pivot + 1
                idx_pivot = idx_pivot_high

        best_k = k_zoom_cands[best_k_cand_zoom_idx]
        if verbose:
            print(f"---Phase 2 end: {best_k_cand_zoom_idx=} {best_k=} {best_k_cand_zoom_score=}")
        self._optimal_k = best_k

    def _k_cluster_labels_generation(self, n_clusters, verbose: bool = False):
        km_model = self._properly_weighted_fit_kmeans(X=self._X_coreset,
                                                      sample_weight=self._w_coreset,
                                                      n_clusters=n_clusters,
                                                      random_state=self._random_state)
        # TODO
        #  Providing "sample_weight" to "predict" is no longer supported starting with scikit-learn 1.5, since,
        #  apparently, it never had any effect in the past during "predict" anyway, and sklearn have now cleaned-up
        #  their API. Basically, we have no way to impose prior weights at this point.
        # self._cluster_labels = km_model.predict(self._X, sample_weight=self._w)
        self._cluster_labels = km_model.predict(self._X)
        if verbose:
            full_training_size = self._X.shape[0]
            clusters, cluster_counts = np.unique(self._cluster_labels, return_counts=True)
            print(f"---Cluster stats: {clusters=} {cluster_counts=} %={cluster_counts / full_training_size * 100}")

    def prepare_km_coreset(self, verbose: bool = False):
        if self._X_coreset is None and self._w_coreset is None:
            # DH Coreset classes require RNGs.
            km_coreset = CoresetKMeans(algorithm="lightweight", random_state=self._rng)
            idxs, w_coreset = km_coreset.build(X=self._X, w=self._w, coreset_size=self._coreset_size)
            self._X_coreset = self._X[idxs]
            self._w_coreset = w_coreset
        else:
            raise ValueError("k-Means coreset already prepared.")

    def approximate_optimal_k(self, verbose: bool = False):
        if self._X_coreset is None or self._w_coreset is None:
            raise ValueError("k-Means coreset not prepared.")
        elif self._optimal_k is not None:
            raise ValueError("Optimal k already approximated.")
        else:
            self._optimal_k_approximation(verbose=verbose)

    def produce_k_cluster_labels(self, k, verbose: bool = False):
        if self._X_coreset is None or self._w_coreset is None:
            raise ValueError("k-Means coreset not prepared.")
        else:
            self._k_cluster_labels_generation(n_clusters=k, verbose=verbose)

    @property
    def optimal_k(self):
        if self._optimal_k is None:
            raise ValueError("Optimal k not approximated.")
        return self._optimal_k

    @property
    def cluster_labels(self):
        if self._cluster_labels is None:
            raise ValueError("Cluster labels not predicted.")
        return self._cluster_labels


###########################
#    KDE-Based Methods    #
###########################


def produce_kde_based_labels(bw,
                             y,
                             w=None,
                             sampling_pct: Union[None, float] = None,
                             verbose: bool = False) -> np.ndarray:
    """
    This method transforms a 1-dimensional numeric array y into a clustered (class-label encoded) y, based on its
    numeric values.
    It relies on the KDEpy library which, among others, implements a fast FFTKDE algorithm for convolution (FFT)
    based computation of Kernel Density Estimation methods.
    The algorithm requires a parameter indicating the type of bandwidth to use – in our application, we support both
    "Silverman" and "ISJ", as 2 separate flavours out of the eventual 4 suggested implementation flavours for
    CoresetDTR.
    This parameter is the only difference between the 2 flavours.
    All other parameters to the FFTKDE class, such as "kernel" and "norm", remain default.
    The algorithm also requires to decide upon the number of grid points based on which local minima is first computed.
    The computed local minima are eventually deriving the clusters to which the original y regression target is
    mapped via traversal through the aforementioned minima over y values.
    """

    # Initialize labels.
    labels = np.zeros(len(y), dtype=np.int32)

    # Fit a KDE on the data y.
    if bw == "ISJ" and len(np.unique(y)) <= 2:
        bw = "silverman"
    kde = FFTKDE(kernel="gaussian", bw=bw)
    try:
        model = kde.fit(y, weights=w)
    except Exception as e:
        if verbose:
            print(f"ERROR when fitting KDE: '{e}'; returning a single label of 0.")
            print(traceback.format_exc())
        return labels

    # Evaluate random grid points.
    if sampling_pct is not None:  # In case the caller provides a specific sampling size.
        n_points = round(len(y) * sampling_pct)
    elif len(y) < 1024:  # If the number of points is less than the FFTKDE autogrid constant, use the full range.
        n_points = len(y)
    else:  # Allow FFTKDE use the autogrid default.
        n_points = None

    if verbose:
        print(f"Seeking minima using {n_points=}, {bw=}...")

    try:
        x, e = model.evaluate(n_points)
    except Exception as e:
        if verbose:
            print(f"ERROR in initial KDE model evaluation: '{e}'; returning a single label of 0.")
            print(traceback.format_exc())
        return labels

    # Get local minima.
    mi = argrelextrema(e, np.less)[0]
    # Number of clusters can be len(mi).

    # TODO
    #  Workarounds implemented below, for the case of no local minima - to be employed in the first released
    #  version, but need reviewing once we gain mileage down the road. Detailed description follows.
    #
    # i. At first, we have supplied our own sampling percentage parameter, from which the n_points (=grid points)
    #    value was derived (the model requires it as the grid points input to produce the minima, AKA "mi"”" array).
    # ii. Later, we have decided to rely on the library's default implementation (which basically comes down to some
    #     derivative of 1024 – if not this value as-is).
    # iii. With that said, there are cases where no minima are produced (the eventual list of "mi" is empty).
    # iv. The following temporary workarounds were implemented to cope with this failure during the work on the
    #     experimental runs:
    #     1. Workaround 1: if the produced "mi" is empty:
    #         a. Set n_points as the length of input (i.e., maximal value).
    #         b. Produce new "mi".
    #         c. If the new "mi" is still empty and while n_points >= 2, divide n_points by 2, and try producing
    #            a new "mi".
    #     2. Workaround 2: if the "mi" from Workaround 1 is still empty (after reaching n_points=2), apply a single
    #        cluster label of 0 to all samples, and return.
    # v. We need to decide whether these workarounds are valid in our final implementation.
    # vi. As an alternative, we may need to design our own method to decide on the proper number of grid points
    #     to supply the algorithm with.
    #     1. With that said, we may still fall under conditions for which both workarounds were added.
    #     2. Handling both cases is critical; for example, workaround #2 above, this was implemented because of
    #        cases where not only the binary, but the full range of n_points candidates starting from 2 and ending
    #        with "len(input)" has produced empty minima.

    # Handle the (maybe-not-so) edge cases.
    # Workaround #1 per the above description.
    if len(mi) == 0:
        if verbose:
            print(f"'mi' is EMPTY! Applying n_points search mechanism... "
                  f"{n_points=} {len(y)=} {len(x)=} {len(e)=} \n{y=}\n{x=}\n{e=}")
        n_points = len(y)
        while len(mi) == 0 and n_points >= 2:
            if verbose:
                print(f"Attempting {n_points=}...")
            try:
                x, e = model.evaluate(n_points)
            except Exception as e:
                if verbose:
                    print(f"ERROR in subsequent KDE model evaluation: '{e}'; returning a single label of 0.")
                    print(traceback.format_exc())
                return labels
            mi = argrelextrema(e, np.less)[0]
            n_points //= 2
    # Workaround #2 per the above description.
    if len(mi) == 0:
        if verbose:
            print("ERROR: 'mi' remained EMPTY after multiple n_points attempts; returning a single label of 0.")
        return labels

    stats = dict() if verbose else None

    # First cluster.
    c_idx = np.nonzero(y < x[mi][0])[0]
    labels[c_idx] = 0
    if verbose:
        stats['0'] = len(labels[c_idx])

    # Get middle clusters.
    for i_cluster in range(len(mi)-1):
        c_idx = np.nonzero((y >= x[mi][i_cluster]) * (y <= x[mi][i_cluster+1]))[0]
        labels[c_idx] = i_cluster + 1
        if verbose:
            stats[f'{i_cluster + 1}'] = len(labels[c_idx])

    # Get last cluster.
    c_idx = np.nonzero(y >= x[mi][-1])[0]
    labels[c_idx] = len(mi)
    if verbose:
        stats[f'{len(mi)}'] = len(labels[c_idx])
        print(f'KDE-based labels assignment stats: {stats=}')

    return labels
