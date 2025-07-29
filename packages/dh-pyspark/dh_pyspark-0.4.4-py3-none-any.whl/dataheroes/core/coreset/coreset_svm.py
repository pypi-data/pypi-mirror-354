"""
TODO
 This experimental CoresetSVM implementation is a non-finalized snapshot of an in-development code from 2024-01-29,
 and should under no circumstances be used as an official library code until further notice.
"""
from ._base import CoresetBase
from .coreset_dtr import rng_to_legacy_random_state
from .coreset_lg import sensitivity_unified
import math
import numpy as np

from typing import Union, Dict, Any
from numpy.random import Generator, RandomState
from scipy.linalg import norm
from scipy.optimize import minimize
from sklearn.cluster._kmeans import _labels_inertia
from sklearn.preprocessing import StandardScaler

from ..sklearn_extra import kmeans_plusplus_w


class CoresetSVM(CoresetBase):

    _coreset_type = "classification"
    _possible_sensitivities = ["unified", "kmeans"]

    def __init__(
            self,
            *,
            algorithm: str = "unified",
            random_state: Union[int, Generator] = None,
            fair: bool = None,
            **sensitivity_kwargs,
    ):
        """Coreset for the SVM classification task.

        Parameters
        ----------
        algorithm: str, default = "unified"
            sensitivity algorithm. One of ["unified", "kmeans"]

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        **sensitivity_kwargs: Key arguments
            parameters to be passed to the sensitivity function
        """
        super().__init__(
            random_state=random_state,
        )
        self._algorithm = algorithm
        self.is_classification = True
        self.sensitivity_kwargs = sensitivity_kwargs

        # Set sensitivity
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        self._algorithm = algorithm

    def sensitivity(self, X, y=None, w=None) -> np.ndarray:
        algorithm_kwargs = dict()
        if self.algorithm == "unified":
            sensitivity_f = sensitivity_svm_unified
        elif self.algorithm == "kmeans":
            sensitivity_f = sensitivity_svm_kmeans
            algorithm_kwargs["random_state"] = self.random_state
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        return sensitivity_f(X, y, w, **{**algorithm_kwargs, **self.sensitivity_kwargs})


def sensitivity_svm_unified(X,
                            y,
                            weights=None,
                            C: float = 1.0,
                            **sensitivity_kwargs) -> np.ndarray:
    """
    IMPORTANT note on 'C':
     The value of 'C' must be in full sync with the SVM model built later, outside of coreset building mechanism,
     using the coreset produced via this method.
    TODO
     If the SVM coreset is applied on DTC models, as opposed to the SVM models - the default C value of 1.0 is
     probably good enough for DTs to begin with - but we can experiment with larger values, e.g. 10, 100, etc.
    """
    return sensitivity_unified(X, y, weights, reg_lambda=1/C, use_for_svm_unified=True, **sensitivity_kwargs)


def sensitivity_svm_kmeans(X,
                           y,
                           weights=None,
                           random_state: Generator = None,
                           class_weight: Dict[Any, float] = None,
                           C: float = 1.0,
                           fit_intercept: bool = True,
                           use_k_median: bool = False,
                           normalize_data: bool = True,
                           scale_data: bool = True,
                           ) -> np.ndarray:
    """
    Returns bounded sensitivity vector of n_samples entries.

    This method works only in a one-vs-all manner; one-vs-one will require |class_labels|^2 run time, or even more,
    hence non-feasible.

    IMPORTANT note on 'C':
     The value of 'C' must be in full sync with the SVM model built later, outside of coreset building mechanism,
     using the coreset produced via this method.

    TODO Current open items:
     0. This implementation is SUPER SLOW, with main offenders being the (1) 'minimize' call (2) kmeans_plusplus_w.
     1. If the SVM coreset is applied on DTC models, as opposed to the SVM models - the default C value of 1.0 is
        probably good enough for DTs to begin with - but we can experiment with larger values, e.g. 10, 100, etc.
     2. We can try both True and False for 'use_k_median' - might as well be two different techniques with
        different resulting performance.
     3. Although we call compute_optimal_solver_using_scipy below, for faster computation and approximated solution,
        it may be better to use the PEGASOS solver instead of scipy.
     4. About "class_weight": its presence here, allows defining _coreset_params_cls (used by the service class),
        as an extension of "CoresetParamsClassification", rather than as an extension of just the "CoresetParams".
        However, if we won't actually need it, then we can revert to defining the coreset params class as simply
        the "CoresetParams" extension.
    """

    # kmeans_plusplus_w down the road works with legacy RandomState and not with Generators.
    legacy_random_state = rng_to_legacy_random_state(random_state)

    # While normalization and scaling is not mandatory, in general - it can basically improve results.
    if normalize_data:
        norms = np.sqrt(np.sum(X ** 2, axis=1))
        max_norm = np.max(norms)
        if max_norm > 1:
            X = np.divide(X, max_norm)
    if scale_data:
        X = StandardScaler().fit_transform(X, y)

    # Prepare for computation.
    n_samples = X.shape[0]
    class_labels = np.unique(y)
    if weights is None:
        weights = np.ones(X.shape[0])
    w_sum_all = np.sum(weights)
    sensitivities = np.zeros(n_samples)

    # Loop over class_labels.
    for class_label in class_labels:

        # Build a class-specific y, where all indices of current class get 1, and the rest - get -1 (IMPORTANT: not 0).
        idx_class = np.where(y == class_label)[0]
        y_class = np.full_like(y, -1)
        y_class[idx_class] = 1

        # Compute class-specific SVM suboptimal solution w_opt_class with b_opt_class as bias.
        w_opt_class, b_opt_class = compute_optimal_solver_using_scipy(X=X,
                                                                      y=y_class,
                                                                      weights=weights,
                                                                      w_sum=w_sum_all,
                                                                      C=C,
                                                                      fit_intercept=fit_intercept,
                                                                      random_state=random_state)
        # Compute the class optimal value.
        opt_class = evaluate_svms_per_s(X=X,
                                        y=y_class,
                                        weights=weights,
                                        w_sum=w_sum_all,
                                        w_opt=w_opt_class,
                                        b_opt=b_opt_class,
                                        C=C)

        # Extract the class-specific X, weights and number of samples.
        X_class = X[idx_class, :]
        w_class = weights[idx_class]
        n_samples_class = np.size(idx_class)

        # Bound the sensitivity of the points with current class labels.
        if n_samples_class > 0:
            sensitivities[idx_class] = get_analytical_bound(
                X=X_class,
                opt=opt_class,
                weights=w_class,
                w_sum_all=w_sum_all,
                use_k_median=use_k_median,
                legacy_random_state=legacy_random_state,
            )

    # Bound the sensitivity by 1 after element-wise multiplication with the weights.
    sensitivities = np.multiply(sensitivities, weights.flatten())
    return sensitivities


def compute_optimal_solver_using_scipy(X, y, weights, w_sum, C: float, fit_intercept: bool, random_state: Generator):
    """
    :param X: A numpy array of nxd excluding the labels.
    :param y: A numpy array containing the labels.
    :param weights: A weight vector with respect to X.
    :param w_sum: Sum of weights.
    :param C: A regularization parameter.
    :param fit_intercept: Whether to fit an intercept.
    :param random_state: pass same random_state for reproducible results.
    :return: The optimal solution of the SVMs problem with respect to X, y and weights using SciPy solver.
    """
    # Define the cost function.
    f = (lambda x, X_train=X, y_train=y: evaluate_svms_per_s(X=X_train,
                                                             y=y_train,
                                                             weights=weights,
                                                             w_sum=w_sum,
                                                             w_opt=x[:-1],
                                                             b_opt=x[-1],
                                                             C=C))

    # Define the gradient of the cost function.
    g = (lambda x, X_train=X, y_train=y: gradient(X=X_train,
                                                  y=y_train,
                                                  weights=weights,
                                                  w_sum=w_sum,
                                                  w_opt=x[:-1],
                                                  b_opt=x[-1],
                                                  C=C))

    # Sample random starting point of size = number of features + 1 (for bias).
    x0 = random_state.random(X.shape[1] + 1)

    # Solve the problem.
    # TODO: The run-time performance of call below is VERY, VERY BAD!
    res = minimize(f, x0, jac=g, tol=10.0, options={'disp': False, 'maxiter': 30})

    # Attain the optimal variables (w,b).
    if fit_intercept:
        weights = res.x[:-1]
        b = res.x[-1]
    else:
        weights = res.x
        b = 0.0
    return weights, b


def evaluate_svms_per_s(X, y, weights, w_sum, w_opt, b_opt, C: float):
    """
    IMPORTANT:
     y **must** contain only values of 1 and -1; if it contains a label with a value of 0 - the hinge will simply be 1.
    """
    reg = 0.5 * norm(w_opt) ** 2
    hinge = np.maximum(0, 1 - np.multiply(y, X.dot(w_opt.T).flatten() + b_opt))
    return np.sum(weights) / w_sum * reg + C * np.sum(np.multiply(weights[:, np.newaxis].T, hinge))


def gradient(X, y, weights, w_sum, w_opt, b_opt, C: float):
    """
    IMPORTANT:
     y **must** contain only values of 1 and -1; if it contains a label with a value of 0 - the hinge will simply be 1.
    """
    indicator = np.multiply(y, X.dot(w_opt.T).flatten() + b_opt) < 1
    sub_grad = np.multiply(indicator.astype(float)[:, np.newaxis], (-np.multiply(y[:, np.newaxis], X)))
    sub_grad = np.sum(weights) / w_sum * w_opt + C * np.sum(np.multiply(weights[:, np.newaxis], sub_grad), axis=0)
    sub_grad = np.append(sub_grad, np.sum(np.multiply(weights, np.multiply(y, -C * indicator.astype(float)))))
    return sub_grad


def get_analytical_bound(X, opt, weights, w_sum_all, use_k_median: bool, legacy_random_state: RandomState):
    n = X.shape[0]
    if n <= 1:
        return np.ones(n)

    start_k = int(2 * np.ceil(np.log(2 * n)))
    start_k = min(int(math.ceil(n / 10.0)), start_k)
    end_k = int(np.ceil(n ** (1.0 / 2)))
    end_k = max(start_k + 1, end_k)
    num_k = int(2 * np.ceil(np.log(n))) if n > 1 else 1
    MIN_K = 3
    if num_k > MIN_K:
        num_k = MIN_K if n > 1 else 1
    k_list = np.geomspace(start_k, end_k, num=num_k, dtype=int)
    k_list = np.unique(k_list)

    best_sens = None
    best_sum_sens = np.Inf
    strike = 0
    for k in k_list:
        sens = get_analytical_bound_core(
            X=X,
            opt=opt,
            k=k,
            weights=weights,
            w_sum_all=w_sum_all,
            use_k_median=use_k_median,
            legacy_random_state=legacy_random_state,
        )
        sum_sens = np.sum(sens)
        if sum_sens < best_sum_sens:
            best_sum_sens = sum_sens
            best_sens = sens
            strike = 0
        else:
            strike += 1

        if strike >= 2:
            break

    return best_sens


def get_analytical_bound_core(X, opt, k, weights, w_sum_all, use_k_median: bool, legacy_random_state: RandomState):
    """
    Return a bound for the sensitivities of P.
    """
    n = X.shape[0]
    k = int(min(k, n ** (3.0 / 5.0)))

    # Produce centers using our standard library approach (centers_ind_ is ignored).
    # TODO: VERY SLOW!
    centers, centers_ind_ = kmeans_plusplus_w(
        X=X,
        n_clusters=k,
        x_squared_norms=None,
        random_state=legacy_random_state,
        n_local_trials=None,
        w=weights,
        squared=not use_k_median,
    )
    # Produce labels using k-means private method (no need to compute inertia).
    # TODO There may be a more elegant approach + may need performance improvement in the future.
    labels = _labels_inertia(X=X,
                             sample_weight=weights,
                             centers=centers,
                             return_inertia=False)
    # TODO
    #  If producing this matrix will prove to have negative running-time performance, we can apply some of
    #  Murad's alternatives from 2024-01-22 email exchange.
    indicator_matrix = adv_indexing_roll(np.repeat(np.eye(1, k, 0), np.ma.size(X, 0), axis=0), labels)

    # Computing a matrix of centers
    c_X = np.array([centers[x] for x in labels])
    weight_per_cluster = np.dot(indicator_matrix, np.sum(np.multiply(indicator_matrix,
                                                                     np.expand_dims(weights, 1)), axis=0).T)
    p_delta = c_X - X

    # alpha value
    a = (w_sum_all - weight_per_cluster) / (2.0 * w_sum_all * weight_per_cluster)

    # compute the norms
    p_delta_norms = np.linalg.norm(p_delta, axis=1)
    p = p_delta_norms

    # Proper one
    expr = 9 / 2 * (np.sqrt(4 * a ** 2 + (2 * p**2) / (9 * opt)) - 2 * a)
    expr = np.maximum(3 * a, expr)

    term = 1.0 / weight_per_cluster + expr
    term = np.minimum(term, 1)

    return np.maximum(term, 0.0)


def adv_indexing_roll(A, r):
    rows, col_indices = np.ogrid[:A.shape[0], :A.shape[1]]
    r[r < 0] += A.shape[1]
    col_indices = (col_indices if col_indices.ndim > 1 else col_indices[:, np.newaxis].T) - r[:, np.newaxis]
    return A[rows, col_indices]

