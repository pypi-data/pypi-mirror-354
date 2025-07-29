from dataheroes.core.coreset.coreset_kmeans import sensitivity_lightweight, estimate_lightweight
from dataheroes.core.numpy_extra import _to_python_obj, np_hstack
from .coreset_qda import sensitivity_qda
from ._base import CoresetBase
import numpy as np
from ...utils import user_warning

from .coreset_reg import sensitivity_dm, sensitivity_lrsvd

from .common import w_dot_X, orth
from typing import Any, Optional, Union, Dict, List, Tuple
from numpy.random import Generator
from sklearn.preprocessing import LabelBinarizer
from .common import safe_mv
from sklearn.utils.validation import _check_sample_weight
from scipy.sparse import issparse
from scipy import sparse
from sklearn.utils.extmath import svd_flip


def sensitivity_logit(
    X, y, w=None, *, sketch_size=None, use_y=True, class_weight: Dict[Any, float] = None, dtype: str = "float32"
):
    """
    Logit sampling from 2018 Paper On Coresets for Logistic Regression.
    """
    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype)

    X = np.concatenate([X, np.ones([X.shape[0], 1], dtype=dtype)], axis=1)

    if w is not None:
        w = _check_sample_weight(w, X, dtype=X.dtype)
        X, y = w_dot_X(X, y=y, w=w)
    else:
        w = _check_sample_weight(w, X, dtype=X.dtype)

    # 1. Obtain fast QR approximation
    n, d = X.shape

    if sketch_size is None:
        sketch_size = d**2
    elif sketch_size < d**2:
        user_warning(f"Sketch size ({sketch_size}) is smaller than d**2 ({d**2})")

    f = np.random.randint(sketch_size, size=n)
    if use_y:
        g = LabelBinarizer(neg_label=-1, pos_label=1).fit_transform(y).flatten()
    else:
        g = np.random.randint(2, size=n) * 2 - 1

    X_sketch = np.zeros((sketch_size, d))
    for i in range(n):
        X_sketch[f[i]] += g[i] * X[i]

    R = np.linalg.qr(X_sketch, mode="r")
    # R_inv = np.linalg.inv(R) # This leads to "singular matrix" error
    R_inv = np.linalg.pinv(R)

    k = 20
    g = np.random.normal(loc=0, scale=1 / np.sqrt(k), size=(R_inv.shape[1], k))
    r = np.dot(R_inv, g)
    Q = np.dot(X, r)

    # 2. Obtain square roots of leverage scores and add 1/n term
    scores = np.linalg.norm(Q, axis=1) + 1 / np.sum(w)

    return scores


def sensitivity_lgqda(
    X,
    y,
    w=None,
    n_components: int = None,
    priors: np.ndarray = None,
    svd_function: str = "svd",
    class_weight: Dict[Any, float] = None,
    dtype: str = "float32",
):
    return sensitivity_qda(
        X,
        y,
        w,
        n_components=n_components,
        priors=priors,
        svd_function=svd_function,
        class_weight=class_weight,
        dtype=dtype,
    )


def sensitivity_lg_lightweight(
    X, y=None, w=None, per_feature: bool = False, return_info: bool = False, dtype: Optional[str] = None
) -> Union[np.ndarray, Tuple[np.ndarray, dict]]:
    """Wrapper over sensitivity_lighweight, ignores y. See that function for details"""
    return sensitivity_lightweight(X=X, w=w, per_feature=per_feature, return_info=return_info, dtype=dtype)


def _unified_norm_lg(U, w, w_sum, reg_lambda: float = 1.0) -> Union[np.ndarray, float]:
    return 32 / reg_lambda * (2 * w / w_sum + np.linalg.norm(U, ord=2, axis=-1) ** 2) * w_sum


def sensitivity_unified(
    X,
    y,
    w=None,
    n_components=None,
    class_weight: Dict[Any, float] = None,
    reg_lambda: float = 1,
    solver: str = "auto",
    solver_kwargs=None,
    use_for_svm_unified: bool = False,
    return_info: bool = False,
    dtype: str = None,
):
    """The gist of this function is to split X into classes based on y, and compute svd per class.
    Sensitivities are based on the norms of the U matrices.
    """
    # reg_lambda = regularization param
    n_samples, n_dim = X.shape
    classes = _to_python_obj(np.unique(y))

    # change to float32 if needed
    X = X.astype(dtype, copy=X.dtype.name != dtype) if dtype is not None else X

    # If w is None fill with 1s
    if w is None or w.size > 0:
        w = _check_sample_weight(w, X, dtype=X.dtype)

    if isinstance(class_weight, dict):
        cw = np.array([class_weight.get(yi, 1.0) for yi in y], dtype=dtype)
        w = w * cw

    # X = [X | 1]
    # NOTE: 1. This copies. 2. In the sparse case this may be inefficient.
    # How necessary is concatenating 1?
    if issparse(X):
        X = sparse.hstack([X, np.ones((n_samples, 1), dtype=dtype)], dtype=dtype, format="csr")
    else:
        X = np_hstack([X, np.ones((n_samples, 1), dtype=dtype)], dtype=dtype)

    def comp_s_svm(U, w, w_sum, w_sum_complement):
        """
        NOTE:
            Assumes one-vs-all (because of using the complement), and will work for one-vs-one as an upper boundary.
            (For a more tight/precise one-vs-one, probably need to do a nested loop and max between them.)
        """
        return (
            np.maximum(9 * w / w_sum, 2 * w / w_sum_complement)
            + 13 * w / (4 * w_sum)
            + 125
            * (w_sum + w_sum_complement)
            / (4 * reg_lambda)
            * (np.linalg.norm(U, ord=2, axis=1) ** 2 + w / (w_sum + w_sum_complement))
        )

    if return_info:
        info = {}
    sensitivities = np.zeros(n_samples)
    w_sum_all = np.sum(w)
    # split per classes
    for c in classes:
        idxs = np.where(y == c)[0]
        w_class = w[idxs]
        w_sum_class = np.sum(w_class)
        w_sum_complement = w_sum_all - w_sum_class
        incorporate_w = np.any(w_class != 1)  # memory consideration, apply weights only when needed.
        # TODO: Dacian notes: I don't approve of try except.
        try:
            res = orth(
                safe_mv(X[idxs], np.sqrt(w_class)) if incorporate_w else X[idxs],
                n_components=n_components,
                solver=solver,
                solver_kwargs=solver_kwargs,
                return_s_vt=return_info,
            )
        except Exception as e:
            if str(e) == "array must not contain infs or NaNs" and dtype != np.float64:
                X = X.astype(np.float64)
                res = orth(
                    safe_mv(X[idxs], np.sqrt(w_class)) if incorporate_w else X[idxs],
                    n_components=n_components,
                    solver=solver,
                    solver_kwargs=solver_kwargs,
                    return_s_vt=return_info,
                )
            else:
                raise e
        if return_info:
            u, s, vt = res  # type: ignore
            u, vt = svd_flip(u, vt, u_based_decision=False)
            n_components_ = len(s)
            # When automatically computed, n_components might be different per class.
            info[c] = {
                "D": s[:, None] * vt,
                "D_inv": vt.T / s,
                "n_components": n_components_,
                "w_sum": w_sum_class,
            }
        else:
            u = res
        if use_for_svm_unified:
            sensitivities[idxs] = comp_s_svm(u, w_class, w_sum_class, w_sum_complement)
        else:
            sensitivities[idxs] = _unified_norm_lg(u, w_class, w_sum_class, reg_lambda=reg_lambda)

    if return_info:
        return sensitivities, info
    else:
        return sensitivities


def union_unified(c_dicts: List[dict]) -> dict:
    """Union the estimation information into one..
    Given a list of dictionaries representing information for estimation computed during the
    sensitivitiy calculation, we combine it into one that is ready to be used for estimation.

    Parameters
    ----------
    c_dicts : List[dict]
        A list of dictionaries containing information for estimation.

    Returns
    -------
    dict
        A dictionary containing information for estimation.

    Raises
    ------
    ValueError
        If the list is empty.
    """
    if len(c_dicts) == 0:
        raise ValueError("No coresets available for union.")
    info = {}
    classes = set.union(*[set(c_dict.keys()) for c_dict in c_dicts])

    # For each class, we get the corresponding D matrix (s * vt) and concatenate them row-wise
    # Then we compute the SVD of that. We compute thew new d, d_inv matrices and return them.
    for c in classes:
        ds = [c_dict[c]["D"] for c_dict in c_dicts if c in c_dict]
        w_sum = sum([c_dict[c]["w_sum"] for c_dict in c_dicts if c in c_dict])
        ds = np.concatenate(ds, axis=0)
        u, s, vt = np.linalg.svd(ds, full_matrices=False)
        u, vt = svd_flip(u, vt, u_based_decision=False)
        ns = min(c_dict[c]["n_components"] for c_dict in c_dicts if c in c_dict)
        s = s[:ns]
        vt = vt[:ns]
        d = s[:, None] * vt
        d_inv = vt.T / s
        info[c] = {"D": d, "D_inv": d_inv, "n_components": len(s), "w_sum": w_sum}
    return info


def estimate_unified(X, y, d_dict: dict, w=None, reg_lambda: float = 1) -> np.ndarray:
    """Given information about estimation in d_dict, estimate sensitivities of some new X, y
    X_build = U * S @ Vt => U = X_build @ V / S
    D_inv = V / S
    U_new = (X_new * sqrt(w)) @ D_inv
    sens = unified_norm(U_new, w)

    Parameters
    ----------
    X : 2D np.ndarray
        The features.

    y : 1D np.ndarray
        The labels.

    d_dict : dict
        A dictionary containing information for estimation.

    w : 1D np.ndarray, default = None
        The sample weights, by default None

    Returns
    -------
    np.ndarray
        The estimated sensitivities.
    """
    n_samples = len(y)
    dtype = X.dtype
    sensitivities = np.zeros(n_samples, dtype=dtype)
    w = _check_sample_weight(w, X, dtype=dtype)

    classes = np.unique(y)
    for c in classes:
        d_inv = d_dict[c]["D_inv"].astype(dtype)
        w_sum = d_dict[c]["w_sum"]
        idxs = np.where(y == c)[0]
        X_c = X[idxs]
        X_c = np_hstack([X_c, np.ones((len(X_c), 1))], dtype=dtype)
        X_c = safe_mv(X_c, np.sqrt(w[idxs])) if w is not None else X_c
        u_temp = np.dot(X_c, d_inv)
        sensitivities[idxs] = _unified_norm_lg(u_temp, w[idxs], w_sum=w_sum, reg_lambda=reg_lambda)
    return sensitivities


def estimate_unified_one(X, y, d_dict, w=None, reg_lambda: float = 1) -> float:
    """Given information about estimation in d_dict, estimate sensitivities of some new X, y

    Parameters
    ----------
    X : 1D np.ndarray

    y : Any
        The label.

    d_dict : dict
        A dictionary containing information for estimation.

    w : numeric, default = None
        The sample weight

    Returns
    -------
    float
        The estimated sensitivities.
    """
    d_inv = d_dict[y]["D_inv"]
    w_sum = d_dict[y]["w_sum"]
    X = np.hstack([X, 1])
    X = X * np.sqrt(w) if w is not None else X
    u_temp = np.dot(X, d_inv)
    return float(_unified_norm_lg(u_temp, w, w_sum=w_sum, reg_lambda=reg_lambda))  # type: ignore


class CoresetLG(CoresetBase):
    _coreset_type = "classification"
    _possible_sensitivities = ["unified", "qda", "lightweight", "lightweight_per_feature"]
    _possible_estimators = ["unified", "lightweight", "lightweight_per_feature"]
    _possible_unions = ["unified"]

    def __init__(
        self,
        *,
        algorithm: str = "unified",
        enable_estimation: bool = False,
        random_state: Union[int, Generator] = None,
        **sensitivity_kwargs,
    ):
        """Coreset for the Logistic Regression classification task.

        Parameters
        ----------
        algorithm: str, default = "unified"
            sensitivity algorithm. One of ["unified", "qda", "lightweight", "lightweight_per_feature"]

        enable_estimation: bool, default = False
            True - estimation will be enabled. When the sensitivity is calculated, will compute all information necessary for estimation.
                The algorithm provided must be one of  ["unified", "lightweight", "lightweight_per_feature"]
            False - Estimation is disabled. Any attempt to estimate with this parameter false should raise an error.

        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        **sensitivity_kwargs: Key arguments
            parameters to be passed to the sensitivity function
        """
        super().__init__(random_state=random_state)
        self._algorithm = algorithm
        self.sensitivity_kwargs = sensitivity_kwargs
        self.enable_estimation = enable_estimation
        self.estimation_params_ = None

        # Set sensitivity
        # TODO Daci: Move this to CoresetBase level.
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        if self.enable_estimation and algorithm not in self._possible_estimators:
            raise ValueError(
                f"For estimation, `algorithm` must be one of {self._possible_estimators}, found {algorithm}"
            )
        self._algorithm = algorithm

    def sensitivity(self, X, y=None, w=None, estimate: bool = False) -> np.ndarray:
        if self.algorithm == "unified":
            sensitivity_f = sensitivity_unified
        elif self.algorithm == "qda":
            sensitivity_f = sensitivity_lgqda
        elif self.algorithm == "lightweight" or self.algorithm == "lightweight_per_feature":
            sensitivity_f = sensitivity_lg_lightweight
            if self.algorithm == "lightweight_per_feature":
                self.sensitivity_kwargs["per_feature"] = True
            if "class_weight" in self.sensitivity_kwargs:
                self.sensitivity_kwargs.pop("class_weight")
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        if self.algorithm in self._possible_estimators:
            self.sensitivity_kwargs["return_info"] = self.enable_estimation

        if estimate:
            # Estimation can happen only if sensitivity was computed before in the attribute estimation_params_
            self._check_estimation_requirements()
            if self.algorithm == "unified":
                sensitivities = estimate_unified(X, y, d_dict=self.estimation_params_, w=w)
            elif self.algorithm == "lightweight" or self.algorithm == "lightweight_per_feature":
                sensitivities = estimate_lightweight(
                    X=X,
                    w=w,
                    mu=self.estimation_params_["mu"],
                    w_sum=self.estimation_params_["w_sum"],
                    di_sum=self.estimation_params_["di_sum"],
                    per_feature=self.algorithm == "lightweight_per_feature",
                )
        else:
            res = sensitivity_f(X=X, y=y, w=w, **self.sensitivity_kwargs)
            # If estimation was enabled return and save information for estimation.
            # This is used to check if estimation is possible in _check_estimation_requirements()
            if self.enable_estimation:
                sensitivities, self.estimation_params_ = res
                self._estimation_algorithm_used = self.algorithm
            else:
                sensitivities = res
        return sensitivities

    def compute_sensitivities(self, X, y=None, w=None, estimate: bool = False):
        self.sensitivities = self.sensitivity(X, y, w, estimate=estimate) if X.shape[0] > 0 else np.ndarray([])
        return self

    def union(self, coresets: List["CoresetLG"]) -> "CoresetLG":
        """Updates Self estimation capabilities by combining a list of coresets.
        This method does not need the coresets to be fully built. It just needs `sens_info` to be available and their algorithm to match.
        This method will enable the newly built CoresetDTC to estimate sensitivities.

        Parameters
        ----------
        coresets : List[CoresetDTC]

        Returns
        -------
        CoresetLG
            Self

        Raises
        ------
        NotImplementedError
            If the union is not implemented for the algorithms provided
        ValueError
            If the algorithm of the provided coresets do not match
        """
        if self.algorithm not in self._possible_unions:
            raise NotImplementedError(f"union for {self.algorithm} does not exist yet")
        else:
            if any(c.algorithm != coresets[0].algorithm for c in coresets) or any(
                c._estimation_algorithm_used != coresets[0]._estimation_algorithm_used for c in coresets
            ):
                raise ValueError("All provided coresets must have been prepared with the same sensitivity algorithm")
            if self.algorithm == "unified":
                self.estimation_params_ = union_unified([c.estimation_params_ for c in coresets])
            self.enable_estimation = True
            self._estimation_algorithm_used = self.algorithm
        return self


class CoresetLGBinary(CoresetBase):
    _coreset_type = "classification"
    _possible_sensitivities = ["svd", "dm", "logit"]

    def __init__(
        self,
        algorithm: str = "svd",
        random_state: Union[int, Generator] = None,
        **sensitivity_kwargs,
    ):
        """Coreset class for the Linear regression task

        Parameters
        ----------
        algorithm : str, default="lp"
            Sensitivity algorithm. One of ["dm", "logit", "svd"]
            "lp" works best

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
        else:
            self._algorithm = algorithm

        self.sensitivity_kwargs = sensitivity_kwargs

    def sensitivity(self, X, y=None, w=None) -> np.ndarray:
        if self.algorithm == "svd":
            sensitivity_f = sensitivity_lrsvd
        elif self.algorithm == "dm":
            sensitivity_f = sensitivity_dm
        elif self.algorithm == "logit":
            sensitivity_f = sensitivity_logit
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        if "class_weight" in self.sensitivity_kwargs:
            class_weight = self.sensitivity_kwargs.pop("class_weight")
            # If w is None fill with 1s
            w = _check_sample_weight(w, X, dtype=X.dtype)
            if isinstance(class_weight, dict):
                cw = np.array([class_weight.get(yi, 1.0) for yi in y])
                w = w * cw

        # Transform into -1, 1
        y = LabelBinarizer(neg_label=-1, pos_label=1).fit_transform(y).flatten()
        return sensitivity_f(X, y, w, **self.sensitivity_kwargs)
