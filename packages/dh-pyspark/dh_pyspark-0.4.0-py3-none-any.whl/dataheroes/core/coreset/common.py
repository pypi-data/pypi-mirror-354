import traceback
import scipy
import numpy as np
import collections
from typing import Iterable, Union, Generator
from scipy.sparse.linalg import svds
import scipy.linalg as la
from scipy.sparse import issparse, isspmatrix_csr, isspmatrix_coo, isspmatrix_csc
from numpy.linalg import LinAlgError

from sklearn.utils.extmath import randomized_range_finder, randomized_svd
from sklearn.random_projection import GaussianRandomProjection, SparseRandomProjection, johnson_lindenstrauss_min_dim
import psutil

DENSE_SVD_MEM_OVERHEAD = 3
TRAINING_DIM_MAX = 780
TRAINING_DIM_THRESHOLD = 1040
CLEANING_DIM_MAX = 1500
CLEANING_DIM_THRESHOLD = 4200


def w_dot_X(X, y=None, w=None) -> np.ndarray:
    """
    Used for reweighting needs like in coreset tree or model that do not support (out-of-the-bag) weighted samples.
    Parameters
    ----------
    X: array-like of shape  (n_samples, n_features)
        features

    y: array-like of shape (n_samples, ), default = None
        labels. Optional

    w : array-like of shape(n_samples, ), default=None
        previous weights

    Returns
    -------
    array-like of shape (n_samples, )
    weighted data
    """
    if w is None:
        w = np.ones(X.shape[0], dtype="float") / X.shape[0]
    w = np.array(w)  # TODO: redundant copy. is this required? after all it is an internal method.

    # memory consideration, apply weights only when needed.
    if np.all(w == 1):
        return (X, y.flatten()) if y is not None else X
    if isinstance(X, scipy.sparse.lil_matrix):
        return scipy.sparse.lil_matrix.multiply(X, w[:, np.newaxis])
    if y is not None:
        return (
            np.multiply(X, w[:, np.newaxis]),
            y.flatten() * w,
        )  # np.multiply(y, w[:, np.newaxis])
    return np.multiply(X, w[:, np.newaxis])




def is_arraylike(array) -> bool:
    """Checks if the provided array can be indexed and it's not a string

    Parameters
    ----------
    array : Any
        The provided value to check if it's an array

    Returns
    -------
    bool
        True / False based if `array` is  array-like or not.
    """
    if isinstance(array, np.ndarray) and array.ndim != 0:
        return True
    if isinstance(array, collections.abc.Sequence) and type(array) is not str:
        return True
    return False


def is_empty(a, allow_None: bool = True) -> bool:
    if allow_None and a is None:
        return True
    return len(a) == 0


def is_int(x, positive: bool = False) -> bool:
    """Checks if the provided value is a python / np int.

    Parameters
    ----------
    x : Any
        Value to check

    positive : bool, default=False
        Checks if the int is positive too

    Returns
    -------
    bool
        True / False based on checks
    """
    if not isinstance(x, (int, np.integer)):
        return False
    else:
        if positive and x < 0:
            return False

    return True


def is_float(x, positive: bool = False) -> bool:
    """Checks if the provided value is a python / np float.

    Parameters
    ----------
    x : Any
        Value to check

    positive : bool, default=False
        Checks if the float is positive too

    Returns
    -------
    bool
        True / False based on checks
    """
    if not isinstance(x, (float, np.floating)):
        return False
    else:
        if positive and x < 0:
            return False

    return True


def is_int_or_float(x, positive: bool = False) -> bool:
    return is_int(x, positive) or is_float(x, positive)


def is_percent(x) -> bool:
    """Checks if the provided value is a float between 0 and 1

    Parameters
    ----------
    x : Any
        Value to check

    Returns
    -------
    bool
        True / False based on checks
    """
    if not isinstance(x, (np.floating, float)):
        return False
    if x < 0 or x > 1:
        return False
    return True


def sizeof_array(a) -> int:
    "Return size of a ndarray or sparse array in bytes"
    if isinstance(a, np.ndarray):
        return a.nbytes
    elif isspmatrix_csr(a) or isspmatrix_csc(a):
        return a.data.nbytes + a.indices.nbytes + a.indptr.nbytes
    elif isspmatrix_coo(a):
        return a.data.nbytes + a.row.nbytes + a.col.nbytes


def svd_random_proj(X, n_components=200):
    # X (n, d)
    # R (d, m), m << d # R <- GaussianRandom(mean = 0, std = 1 / n_components), SparseRandom, Normal (mean = 0, std = 1)
    # X' = X @ R -> (n, m)
    # U = svd(X') or qr(X')
    if issparse(X):
        X_ = SparseRandomProjection(n_components=n_components).fit_transform(X)
        u, s, vt = svds(X_, k=min(X_.shape) - 1, solver="lobpcg")
    else:
        X_ = GaussianRandomProjection(n_components=n_components).fit_transform(X)
        u, s, vt = np.linalg.svd(X_, full_matrices=False)
    return u, s, vt


def svd_xtx(X):
    if np.issubdtype(X.dtype, np.integer):
        eps = 1e-20
    else:
        eps = np.finfo(X.dtype).eps

    n, d = X.shape
    if n >= d:
        B = X.T @ X
        if scipy.sparse.issparse(X):
            # This will use a dense solver, but it will still work with sparse matrices.
            _, S_sq, Vt = scipy.sparse.linalg.svds(B, k=min(B.shape) - 1, solver="lobpcg")
        else:
            _, S_sq, Vt = np.linalg.svd(B)

        S = np.sqrt(S_sq)
        # Due to parallelism issues, U may contain NaNs. Retry 5 times.
        for _ in range(5):
            U = X.dot(Vt.T / (S + eps))
            if not np.isnan(U).any():
                break
        else: # when for is completed.
            return None, None, None
        return U, S, Vt

    else:
        B = X @ X.T
        if scipy.sparse.issparse(X):
            U, S_sq, _ = scipy.sparse.linalg.svds(B, k=min(B.shape) - 1, solver="lobpcg")
        else:
            U, S_sq, _ = np.linalg.svd(B, full_matrices=False)

        S = np.sqrt(S_sq)
        Vt = U.T @ X / (np.sqrt(S_sq) + eps).reshape(-1, 1)
        return U, S, Vt


def svd_sp(X):
    u, s, vt = la.svd(X, full_matrices=False, lapack_driver="gesdd")
    return u, s, vt


def orth(X, solver="auto", n_components=None, return_s_vt: bool = False, solver_kwargs=None, verbose: bool = False):
    """Compute an orthonormal matrix whose range approximates (up to exact) the range of X.

    Parameters
    ----------
    X : array-like of shape (n, d)
        Input matrix

    n_components: int, default = None
        number of components to compute for svd.
        Required for randomized and sparse solvers, will be ignored for full solvers.
        TODO: Ignore or raise errors?

    solver : str, default="auto"
        full solvers: ["svd_np", "svd_sp", "qr", "xtx"]
        sparse solvers: ["arpack", "propack", "lobpcg"]
        randomized solvers: ["r_orth", "r_proj"]
        randomized solvers and sparse solvers require n_components != None
        "auto" defaults to "xtx"

    return_s_vt: bool, default=False
        If True, return S and Vt matrices. Only works with svd solvers (not "qr", "r_proj").

    solver_kwargs : dict, default=None
        extra key arguments for the solver

    verbose: bool, default=False
        If True, auxiliary information may be printed out.

    """
    n, d = X.shape

    # If the matrix is fat, we will cut from the computed components
    is_fat = d > 0.75 * n

    if solver_kwargs is None:
        solver_kwargs = {}
    if n_components is None:
        n_components = min([n, d])
    else:
        # Q: Raise warning if it was given and it's > d?
        n_components = min([n_components, n, d])

    # TODO find the best way to choose a solver
    # When reducing the n_components make sure to be less than 75%
    # to avoid going into the 2nd reduction of n_components
    if issparse(X):
        sparse_solvers = ["auto", "training", "cleaning", "arpack", "propack", "lobpcg", "r_proj", "r_orth"]
        if solver not in sparse_solvers:
            raise ValueError(f"`solver` must be one of {sparse_solvers}. Found {solver}")

    # TODO: See if we scale with the matrix density somehow.
    # When dealing with sparse matrices we reduce the dimension a lot.
    # Default to r_orth, sparse random proj did not yield good results
    # on preliminary tests
    if issparse(X) and DENSE_SVD_MEM_OVERHEAD * n * d * X.dtype.itemsize < psutil.virtual_memory().total:
        X = X.todense()

    if issparse(X):
        # Deal with small n_components to avoid going into cases
        n_components = max(round(np.log(n_components) * np.sqrt(n_components)), 1)
        if solver == "auto" or solver == "training":
            n_components = min(n_components, TRAINING_DIM_MAX)
        elif solver == "cleaning":
            n_components = min(n_components, CLEANING_DIM_MAX)
        solver = "r_orth" # r_orth is faster than lobpcg when it comes sparse OHE, our usecase.
    else:
        if solver in ["auto", "training", "r_proj", "r_orth"]:
            if n_components > TRAINING_DIM_THRESHOLD:
                n_components = TRAINING_DIM_MAX
                solver = "r_orth"
            else:
                solver = "xtx"
        elif solver == "cleaning":
            if n_components > CLEANING_DIM_THRESHOLD:
                n_components = CLEANING_DIM_MAX
                solver = "r_proj" if return_s_vt else "r_orth"
            else:
                solver = "xtx"

    if return_s_vt and solver in ["r_proj", "qr"]:
        raise ValueError(f"S and Vt can't be computed with {solver} method")
    # If the provided n_components > 75% of n_samples, adjust it to avoid fat matrices
    # https://en.wikipedia.org/wiki/Johnson%E2%80%93Lindenstrauss_lemma
    # We want to calculate a dimension where we can preserve the distances of the points
    # within a multiplicative factor of (1 + eps).
    # breakpoints where JL dim < 0.75 * n for eps
    # eps = 0.1 -> 10591
    # eps = 0.2 -> 2394
    # eps = 0.3 -> 1027
    # eps = 0.5 -> 381
    # eps = 0.75 -> 201
    # if n is smaller than any of these use a hardcoded 75%.
    if n_components > n * 0.75:
        if n_components > 2394:
            n_components = johnson_lindenstrauss_min_dim(n, eps=0.2)
        else:
            n_components = round(0.75 * n)

    # Check solvers and solve
    if solver == "qr":
        u, _ = np.linalg.qr(X)
    elif solver == "svd_np":
        u, s, vt = np.linalg.svd(X, full_matrices=False)
    elif solver == "svd_sp":
        u, s, vt = svd_sp(X)
    elif solver == "xtx":
        u = None
        try:
            u, s, vt = svd_xtx(X)
        except LinAlgError as e:
            # In some datasets, Chalice.ai, for example, the call to "np.linalg.svd(B)" within svd_xtx(X) fails on
            # an "SVD did not converge" error. We don't know the real cause of this error yet, to treat it beforehand,
            # so we catch the exception and apply a backup solver.
            # For more details, see: https://github.com/Data-Heroes/dh-library/issues/1153
            if verbose:
                print(f"ERROR in orth()->svd_xtx(): '{e}'; replacing with an alternative 'svd_sp' solver.")
                print(traceback.format_exc())
        # If u is None, the process either hasn't converged (see the exception handler above), or we've encountered
        # NaN inside svd_xtx multiple times (see https://github.com/Data-Heroes/dh-library/issues/1148), and returned
        # None values. In this case, we try a backup solver, "svd_sp", which seemed to be more resilient during our
        # testing.
        if u is None:
            u, s, vt = svd_sp(X)
    # Sparse solvers
    elif solver in ["arpack", "propack", "lobpcg"]:
        # svds needs -1 components
        if n_components == min(n, d):
            n_components = n_components - 1
        u, s, vt = svds(X, k=n_components, solver=solver)
        u = u[:, ::-1]
        vt = vt[::-1, :]
        s = s[::-1]
    # Randomized solvers
    elif solver == "r_orth":
        # Here we set n_iter to 0 because of quickness. In theory n_iter = 0 should provide good results.
        if return_s_vt:
            u, s, vt = randomized_svd(X, n_components=n_components, n_iter = 0)
        else:
            u = randomized_range_finder(X, size=n_components, n_iter=0, **solver_kwargs)
    elif solver == "r_proj":
        u, s, vt = svd_random_proj(X, n_components=n_components)

    # This will only cut from the full solvers, since the random / sparse solvers already compute n_components.
    if is_fat or n_components is not None:
        u = u[:, :n_components]
        if return_s_vt:
            s = s[:n_components]
            vt = vt[:n_components, :]
    if return_s_vt:
        return u, s, vt
    return u


def safe_mv(a, x, sp_format="coo"):
    """
    Safe matrix-vector product
    a is an (n, d) matrix.
    x is an (n, ) or (d, ) dense vector.
    sp_format: the return form, for sparse x. One of ["coo, csr, csc, bsr"].
    """
    if isinstance(a, np.matrix):
        a = np.asarray(a)

    n, d = a.shape
    d_ = len(x)
    if d_ != n and d_ != d:
        raise ValueError("Dimension mismatch")
    if np.all(x == 1):
        return a
    if issparse(a):
        if n == d_:
            res = a.multiply(x[:, np.newaxis])
        else:
            res = a.multiply(x)

        # Res will be in coo format. Coo format allows for fast conversions.
        # Other formats allow for faster operations.
        if sp_format == "coo":
            return res
        elif sp_format == "csr":
            return res.tocsr()
        elif sp_format == "csc":
            return res.tocsc()
        elif sp_format == "bsr":
            return res.tobsr()
        else:
            raise ValueError("Sparse format not supported")
    else:
        if n == d_:
            return np.multiply(a, x[:, np.newaxis])
        else:
            return np.multiply(a, x)


def safe_average(a, weights=None, axis=None):
    """Safe weighted average

    Parameters
    ----------
    a : array or sparse array
        Input matrix

    weights : array, default=None
        An array of weights associated with the values in a. Each value in a contributes to the average according to its associated weight.
        The array of weights must be the same shape as a if no axis is specified, otherwise the weights must have dimensions and shape consistent
        with a along the specified axis. If weights=None, then all data in a are assumed to have a weight equal to one.

    axis : int, default=None
        Axis or axes along which to average a. The default, axis=None, will average over all of the elements of the input array. If axis is negative
        it counts from the last to the first axis

    Returns
    -------
    array or float
        Return the average along the specified axis.
    """
    if weights is None:
        return a.mean(axis=axis)
    if issparse(a):
        return np.asarray(safe_mv(a, weights).sum(axis=axis)).squeeze() / weights.sum()
    else:
        return np.average(a, weights=weights, axis=axis)


def safe_norm(a, axis=None):
    if issparse(a):
        if axis is None:
            return np.sqrt(a.multiply(a).sum())
        else:
            return np.array(np.sqrt(a.multiply(a).sum(axis))).ravel()
    else:
        return np.linalg.norm(a, axis=axis)


def fairness_policy_adaptor(
    size: Union[int, np.integer],
    class_size: Union[dict, Iterable],
    fair: bool = True,
    min_bound_0: float = 0.2,
    random_state: Union[int, Generator] = None,
) -> np.ndarray:
    """This function is responsible to distributing the sample size over different class in the training data in a fair
    manner if permitted.
    Parameters
    ----------
    size : int
         The sample size requested.
    class_sizes : array-like of shape (n_classes, )
         An array-like containing the size of each class of points (classification-tasks related)
    fair : bool, default=True
        True - use linear programming to determine the optimal amount between 3 policies
        False - Use the ratios between classes, not trying to balance any of the classes

    min_bound_0: float = 0.2
        Each of the entries of the policies that we compute has its own variable.
        The min_bound basically sets the minimal value such variables can be, where 0 basically lets
        the system of equations have much more freedom in finding a solution to the system of equations
    Returns
    -------
    np.ndarray | dict
        The size per class associated with each of the traning classes.
        A dict if class_size was of dict type, a np.array otherwise.

    """

    n_classes = len(class_size)
    if isinstance(class_size, dict):
        classes = class_size.keys()
        c_sizes = np.asarray(list(class_size.values()))
    else:
        c_sizes = np.asarray(list(class_size))

    if n_classes == 1:
        if isinstance(class_size, dict):
            k = next(iter(class_size.keys()))
            return {k: size}
        else:
            return np.array([size])

    c_sizes = np.asarray(c_sizes)
    ratios = c_sizes / np.sum(c_sizes)  # the ratio of classes

    # no fairness required; bigger classes dominate over the sample size
    if not fair:
        res = ratios * size
        res = np.round(res).astype(int)
        if isinstance(class_size, dict):
            res = {c: int(v) for c, v in zip(classes, res)}
        return res

    # A lower bound on the how much from the sample size can we take from each class
    min_bound = np.min(c_sizes / size)
    if min_bound >= 1:
        min_bound = min_bound_0  # if the ratio is larger than 1, then the lower bound is 0
    # First policy favors bigger classes over smaller ones, the second favors smaller classes over bigger ones, and the
    # third policy aims to be "almost uniform" across all classes.
    policy_1 = ratios
    policy_2 = np.abs(np.log(ratios)) / np.sum(np.abs(np.log(ratios)))
    policy_3 = np.abs(np.exp(-ratios)) / np.sum(np.abs(np.exp(-ratios)))

    # Turn the policy vector into a matrix of 'number of classes' x 3
    W = np.vstack([policy_1, policy_2, policy_3]).T
    n_policies = W.shape[1]
    # In what follows, a linear programming is invoked.
    # Recall that linear programming problem looks like:
    # min c^T x
    # s.t.
    #      A_eq * x = b_eq
    #      A_ub * x <= b_ub
    # Specifically speaking, the idea is to introduce a weighting system to policies.

    c = np.ones(n_classes * n_policies)
    A_ub = np.zeros((n_classes, n_classes * n_policies))
    A_eq = np.zeros((n_classes, n_classes * n_policies))
    for i in range(n_classes):
        A_ub[i, n_policies * i : n_policies * (1 + i)] = size * W[i]
        A_eq[i, n_policies * i : n_policies * (1 + i)] = np.ones_like(A_ub[i, n_policies * i : n_policies * (1 + i)])
    b_ub = c_sizes
    b_eq = np.ones_like(b_ub)
    for alpha in np.linspace(start=1, stop=0.1, num=10):
        bounds = [(min_bound * alpha, None) for _ in c]
        lp_res = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        if not lp_res.success:
            # warnings.warn("Linear programming problem failed")
            continue
        else:
            res = np.round(A_ub.dot(lp_res.x)).astype(int)
            break
    else:
        res = 1 / 3 * (policy_1 + policy_2 + policy_3) * size
        res = np.round(res).astype(int)

    if isinstance(class_size, dict):
        res = {c: int(v) for c, v in zip(classes, res)}
    return res


def fairness_policy_adaptor_cleaning(
    size: Union[int, np.integer],
    class_size: Union[dict, Iterable],
    fair: bool = True,
    min_bound_0: float = 0.2,
    random_state: Union[int, Generator] = None,
) -> np.ndarray:
    """This function is responsible to distributing the sample size over different class in the training data in a fair
    manner if permitted.
    Parameters
    ----------
    size : int
         The sample size requested.
    class_size : array-like of shape (n_classes, )
         An array-like containing the size of each class of points (classification-tasks related)
    fair : bool, default=True
        True - use linear programming to determine the optimal amount between 3 policies
        False - Use the ratios between classes, not trying to balance any of the classes

    min_bound_0: int = 0.2
        Each of the entries of the policies that we compute has its own variable.
        The min_bound basically sets the minimal value such variables can be, where 0 basically lets
        the system of equations have much more freedom in finding a solution to the system of equations
    Returns
    -------
    np.ndarray | dict
        The size per class associated with each of the traning classes.
        A dict if class_size was of dict type, a np.array otherwise.

    """

    n_classes = len(class_size)
    if isinstance(class_size, dict):
        classes = class_size.keys()
        c_sizes = np.asarray(list(class_size.values()))
    else:
        c_sizes = np.asarray(list(class_size))

    if n_classes == 1:
        if isinstance(class_size, dict):
            k = next(iter(class_size.keys()))
            return {k: size}
        else:
            return np.array([size])

    c_sizes = np.asarray(c_sizes)

    if c_sizes.sum() < size:
        # warnings.warn("size > sum(class_size)")
        return class_size

    if size == 0:
        if isinstance(class_size, dict):
            return {k: 0 for k in class_size.keys()}
        else:
            return np.zeros_like(class_size)
        
    ratios = c_sizes / np.sum(c_sizes)  # the ratio of classes

    # no fairness required; bigger classes dominate over the sample size
    if not fair:
        res = ratios * size
        res = np.round(res).astype(int)
        if isinstance(class_size, dict):
            res = {c: int(v) for c, v in zip(classes, res)}
        return res

    # A lower bound on the how much from the sample size can we take from each class
    min_bound = np.min(c_sizes / size)
    if min_bound >= 1:
        min_bound = min_bound_0  # if the ratio is larger than 1, then the lower bound is 0
    # First policy favors bigger classes over smaller ones, the second favors smaller classes over bigger ones, and the
    # third policy aims to be "almost uniform" across all classes.
    policy_1 = ratios
    policy_2 = np.abs(np.log(ratios)) / np.sum(np.abs(np.log(ratios)))
    policy_3 = np.abs(np.exp(-ratios)) / np.sum(np.abs(np.exp(-ratios)))

    # Turn the policy vector into a matrix of 'number of classes' x 3
    W = np.vstack([policy_1, policy_2, policy_3]).T
    n_policies = W.shape[1]
    # In what follows, a linear programming is invoked.
    # Recall that linear programming problem looks like:
    # min c^T x
    # s.t.
    #      A_eq * x = b_eq
    #      A_ub * x <= b_ub
    # Specifically speaking, the idea is to introduce a weighting system to policies.

    c = np.zeros((c_sizes.shape[0] * n_policies + 1,))
    c[0] = size

    A_ub = np.zeros((n_classes, n_classes * n_policies))
    A_eq = np.zeros((n_classes, n_classes * n_policies))
    for i in range(n_classes):
        A_ub[i, n_policies * i : n_policies * (1 + i)] = size * W[i]
        A_eq[i, n_policies * i : n_policies * (1 + i)] = np.ones(A_ub[i, n_policies * i : n_policies * (1 + i)].shape)

    c[1:] = -A_ub.flatten()[A_ub.flatten() != 0]
    A_eq = -c
    A_eq[0] = 0
    A_eq = A_eq[np.newaxis, :]
    b_ub = c_sizes
    b_eq = np.array([size])[np.newaxis, :]
    A_ub = np.hstack((np.zeros((A_ub.shape[0], 1)), A_ub))
    # A_eq = np.hstack((np.zeros((A_eq.shape[0], 1)), A_eq))
    for alpha in np.linspace(start=1, stop=0.001, num=20):
        # Unlike the above the problem formulation
        bounds = [(min_bound * alpha, None) if i > 0 else (1, 1) for i in range(c.shape[0])]
        res = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        if not res.success:
            continue
        else:
            size_per_class = np.round(A_ub.dot(res.x))
            if size_per_class.sum() != size:
                continue
                # print("HELLO")
            if np.any(np.greater(size_per_class, c_sizes)) or np.any(size_per_class == 0):
                continue
            res = size_per_class
            break

    else:
        # warnings.warn("Defaulting to ratio split")
        res = policy_1 * size

    if isinstance(class_size, dict):
        res = {c: int(v) for c, v in zip(classes, res)}

    # TODO fix to_sample containing more samples than there are in the initial pool (class_size)
    #  Same check if class_size is array.
    if sum(res.values()) < size:
        new_size = size - sum(res.values())
        to_sample = [k for k, v in res.items() if v < class_size[k]]
        operator = random_state if random_state is not None else np.random
        t = operator.choice(
            to_sample,
            size=new_size,
            replace=True,
        )
        for x in t:
            res[x] += 1

    return res


def compute_class_weight(class_weight, *, classes, y):
    """Estimate class weights for unbalanced datasets.

    Parameters
    ----------
    class_weight : dict, 'balanced' or None
        If 'balanced', class weights will be given by
        ``n_samples / (n_classes * np.bincount(y))``.
        If a dictionary is given, keys are classes and values
        are corresponding class weights.
        If None is given, the class weights will be uniform.

    classes : ndarray
        Array of the classes occurring in the data, as given by
        ``np.unique(y_org)`` with ``y_org`` the original class labels.

    y : array-like of shape (n_samples,)
        Array of original class labels per sample.

    Returns
    -------
    class_weight_vect : ndarray of shape (n_classes,)
        Array with class_weight_vect[i] the weight for i-th class.

    References
    ----------
    The "balanced" heuristic is inspired by
    Logistic Regression in Rare Events Data, King, Zen, 2001.
    """
    # Import error caused by circular imports.
    from sklearn.preprocessing import LabelEncoder

    if set(y) - set(classes):
        raise ValueError("Classes should include all valid labels that can be in y.")
    if class_weight is None or len(class_weight) == 0:
        # uniform class weights
        weight = np.ones(classes.shape[0], dtype=np.float64, order="C")
    elif class_weight == "balanced":
        # Find the weight of each class as present in y.
        le = LabelEncoder()
        y_ind = le.fit_transform(y)
        if not all(np.isin(classes, le.classes_)):
            raise ValueError("Classes should have valid labels that are in y.")

        recip_freq = len(y) / (len(le.classes_) * np.bincount(y_ind).astype(np.float64))
        weight = recip_freq[le.transform(classes)]
    else:
        # user-defined dictionary
        weight = np.ones(classes.shape[0], dtype=np.float64, order="C")
        if not isinstance(class_weight, dict):
            raise ValueError("class_weight must be dict, 'balanced', or None, got: %r" % class_weight)
        unweighted_classes = []
        for i, c in enumerate(classes):
            if c in class_weight:
                weight[i] = class_weight[c]
            else:
                unweighted_classes.append(c)

        n_weighted_classes = len(classes) - len(unweighted_classes)
        if unweighted_classes and n_weighted_classes != len(class_weight):
            raise ValueError(f"The classes, {unweighted_classes}, are not in class_weight.")

    return weight
