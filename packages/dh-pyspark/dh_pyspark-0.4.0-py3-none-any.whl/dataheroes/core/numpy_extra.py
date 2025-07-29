from typing import Any, Dict, Iterable, Literal, Union, overload, Tuple
import numpy as np
import pandas as pd
from numpy.random import Generator

def check_random_state(random_state: Union[int, Generator] = None) -> Generator:
    """Checks the random state type and returns a np.random.Generator

    Parameters
    ----------
    random_state : Union[int, Generator], default=None
        int - creates a rng using the `random_state seed


    Returns
    -------
    np.random.Generator


    Raises
    ------
    ValueError
        If the random state is not an int or a np.random.Generator
    """

    if random_state is None:
        random_state = np.random.default_rng()
    elif isinstance(random_state, Generator):
        random_state = random_state
    elif isinstance(random_state, int):
        random_state = np.random.default_rng(random_state)
    else:
        raise ValueError("Random state must be np.random.Generator or int ")

    return random_state


def pd_factorize(a):
    if pd.__version__ >= "2":
        return pd.factorize(a, True, use_na_sentinel=None)
    else:
        return pd.factorize(a, True, na_sentinel=None)


def np_hstack(tup, *, dtype=None):
    if np.__version__ < "1.24.0":
        return np.hstack(tup).astype(dtype)
    else:
        return np.hstack(tup, dtype=dtype)


def unique(X, return_counts: bool = False, return_index: bool = False, return_inverse: bool = False):
    if not return_inverse and not return_index and not return_counts:
        return pd.unique(X)

    if pd.__version__ < "1.1.2":
        return unique_1d_pd(X, return_inverse=return_inverse, return_index=return_index, return_counts=return_counts)
    inv, uniq = pd_factorize(X)

    res = (uniq,)
    if return_index:
        # This was usually the most time consuming part.
        # Other variants I've tried
        # 1. for loop and keep in dictionary the inv -> index - infinite slower in python
        # 2. Rewrite the above in lower level (Cython / Rust) -> Improvement but not enough - ~2-2.5x slower
        # 3. Instead of dict, keep what was seen in a boolean "seen" array -> 1.5x slower (in Cython / Rust)
        idx = np.zeros(len(uniq), dtype=int)
        # If you assign to an array arr[0, 1, 0] = [1, 2, 3], the last element will be in position 0.
        # Therefore we reverse the array to get the first position for each duplicate
        idx[inv[::-1]] = np.arange(len(inv))[::-1]
        res += (idx,)
    if return_inverse:
        res += (inv,)
    if return_counts:
        counts = np.bincount(inv)
        res += (counts,)
    return res


def unique_1d_pd(a, return_inverse: bool = False, return_index: bool = False, return_counts: bool = False):
    """Return unique, first found index of the unique and inverse to reconstruct the array"""
    a = np.asarray(a)
    if a.dtype == bool:
        # Backup to unique in case of np bool
        return np.unique(a, return_inverse=return_inverse, return_index=return_index, return_counts=return_counts)
    s = pd.Series(a).astype("category")
    uniq = s.cat.categories
    res = (np.asarray(uniq),)
    if return_index:
        first_appearances = s[~s.duplicated()]
        fp_rev = pd.Series(first_appearances.index, index=first_appearances.values)
        idx = fp_rev.loc[uniq].values if pd.__version__ < "2.0" else fp_rev[uniq].values
        res += (np.asarray(idx),)
    if return_inverse:
        res += (s.cat.codes.values,)
    if return_counts:
        counts = s.value_counts()
        counts = counts.loc[uniq].values if pd.__version__ < "2.0" else counts[uniq].values
        res += (np.asarray(counts),)
    return res[0] if len(res) == 1 else res


def unique_2d_hash(a, return_inverse: bool = False, return_index: bool = False, return_counts: bool = False):
    # Quickly compute 2d array unique
    # Other methods I tried but were slower (in descending order):
    # 1. Call np.unique directly on the array
    # 2. Instead of using hash(row.tobytes()) use tuple, this didn't pair well with np.array
    # 3. Instead of using hash try to concatenate the bit representation of the values in the row
    # 4. Counter(map(tuple, numpy_array)) - This didn't provide return_inverse and return_index easily.
    # 5. Use frequency hashmaps to keep all return_* flags. See https://github.com/cupy/cupy/issues/8307
    # 6. Same as above, but implemented in a lower lvl language.
    # 7. Use np.unique on the hash(row.tobytes()) - Current version.

    # More reads
    # https://github.com/numpy/numpy/issues/11136
    ah = np.asarray([hash(row.tobytes()) for row in a])
    _, idx, *rest = unique(ah, return_index=True, return_inverse=return_inverse, return_counts=return_counts)
    uniq = a[idx]
    res = (uniq,)
    if return_index:
        res += (idx,)
    res += tuple(rest)
    return res


def argisin(element, test_elements, assume_unique: bool = True, invert: bool = False) -> np.ndarray:
    """
    Similar to np.isin, but returns the indexes.
    Return an integer indices mask of test_elements contained in element.
    assume_unique : if True, both arrays are assumed positive unique ints (speeds-up calculation).
    invert: If True, the values in the returned array are inverted, as if calculating element not in test_elements.

    Example:
        element = [0, 4, 5, 8, 10, 30, 45, 46]
        test_elements = [5, 10, 46]
        return value = [2, 4, 7]

    As for the mask computation, using assume_unique=True greatly speeds up the calculation.
    If this method poses a performance problem in the future, we can try using a lookup table with bincount, e.g.:
    https://stackoverflow.com/questions/67391617/faster-membership-test-numpy-isin-too-slow
    """
    idxs = np.argwhere(np.isin(element, test_elements, assume_unique=assume_unique, invert=invert)).ravel()
    return idxs

def check_same_length(*arrays, allow_None: bool = True) -> None:
    """Checks if multiple arrays are the same length. Raises errors if not.

    Parameters
    ----------
    allow_None : bool, default=True
        True - allows None in the array list, ignoring it.

    Raises
    ------
    ValueError
    """
    n_arrays = len(arrays)
    if n_arrays == 0:
        raise ValueError("At least one array required as input")
    if n_arrays == 1:
        return None

    length = None
    for a in arrays:
        if a is None and not allow_None:
            raise ValueError("Found array that is None")
        if a is not None and length is None:
            length = len(a)
            continue
        if a is not None and len(a) != length:
            raise ValueError(f"Arrays must have the same length. {len(a)} != {length}")
    return None


def isin_select(*arrays, idxs, test_idxs, return_index: bool = True, **isin_kwargs):
    """Selects from the provided arrays, idxs from test_idxs. All *arrays  must be the same length
    test_idxs should be the same length as the arrays in *arrays as they represent the corresponding
    indexes

    Parameters
    ----------
    idxs : array-like
        idxs in test_idxs to index

    test_idxs : array-like
        corresponding idxs fore *arrays

    return_index : bool, default=True
        If True, returns the selected idxs


    Returns
    -------
    Tuple[array-like] with the selected idxs
    """
    idxs = np.asarray(idxs)
    test_idxs = np.asarray(test_idxs)
    check_same_length(*arrays, idxs, allow_None=True)
    if test_idxs.shape[0] != idxs.shape[0]:
        if test_idxs.dtype.hasobject or idxs.dtype.hasobject:
            unique_idxs = set(test_idxs)
            active_idxs = [v in unique_idxs for v in idxs]
        else:
            active_idxs = np.isin(idxs, test_idxs, **isin_kwargs)
        arrays = [np.asarray(a)[active_idxs] if a is not None else None for a in arrays]
        idxs = idxs[active_idxs]
    return (arrays, idxs) if return_index else arrays


def expand_and_select(*arrays, sel_idxs, orig_idxs=None, sel_in_orig: bool = False):
    """This method can be viewed as a "key-value" selection where the orig_idxs are keys and *arrays are values.
    We then select using `sel_idxs`.
    Instead of using dictionaries we leverage the fact that orig_idxs and sel_idxs are indexes in arrays
    and we populate an array of length max(len(orig_idxs) and we use sel_idxs to select in it.

    The `orig_idxs` are the corresponding idxs of arrays in *arrays and sel_idxs are the ones we want to select.

    Example:
    array from *arrays: [a, b, c, d, e, f]
    orig_idxs: [1, 2, 3, 7, 5]
    sel_idxs: [3, 7, 6]

    max(orig_idxs) = 7
    We create an array zeros of length 8 = 7 + 1: [0, 0, 0, 0, 0, 0, 0, 0]
    We set an array of idxs of len(orig_idxs): [1, 2, 3, 4, 5]
    We put the idxs at the 0 array at the corresponding positions: t = [0, 1, 2, 3, 0, 5, 0, 4]
    We select with k = t[sel_idxs]
    We select array[k] for array in arrays.

    Parameters
    ----------
    sel_idxs : array-like[int]
        Selected indexes

    orig_idxs : array-like[int], default=None
        Original indexes

    sel_in_orig : bool, default=False
        If True, sel_idxs are already in orig_idxs and skips this check.

    Returns
    -------
    array-like(s)
        Selected arrays from *arrays
    """
    if len(arrays) == 0:
        raise ValueError("At least one array required as input")
    sel_idxs = np.asarray(sel_idxs)
    if len(sel_idxs) == 0:
        return [np.asarray([], dtype=a.dtype) if a is not None else None for a in arrays]
    if orig_idxs is None:
        return [np.asarray(a)[sel_idxs] if a is not None else None for a in arrays]
    check_same_length(*arrays, orig_idxs, allow_None=True)
    orig_idxs = np.asarray(orig_idxs)
    if len(orig_idxs) == 0:
        return [np.asarray([]) if a is not None else None for a in arrays]

    # The user can skip this check if it's ensured beforehand
    if not sel_in_orig:
        sel_idxs = sel_idxs[np.isin(sel_idxs, orig_idxs)]

    # Shift the indexes to the min amount to create a smaller array.
    shift_amount = np.min(orig_idxs)
    if shift_amount > 0:  # if necessary because we want to copy the only if we shift.
        orig_idxs = orig_idxs - shift_amount
        sel_idxs = sel_idxs - shift_amount
    # Create array of zeros
    t = np.zeros(np.max(orig_idxs) + 1, dtype=int)
    t[orig_idxs] = np.arange(len(orig_idxs))
    # Put sorting indexes at positions in o_idxs
    # Take the selected indexes from the positions
    sorted_idxs = t[sel_idxs]
    return [np.asarray(a)[sorted_idxs] if a is not None else None for a in arrays]


def reindex_after_delete(idxs: np.ndarray, idxs_deleted: np.ndarray) -> np.ndarray:
    starting_idxs = idxs.copy()
    for idx in np.unique(idxs_deleted):
        idxs[starting_idxs >= idx] -= 1
    return idxs


def delete_and_shift(idxs, deleted) -> np.ndarray:
    idxs = np.asarray(idxs)
    deleted = np.asarray(deleted)
    deleted = np.unique(deleted)  # remove duplicates
    idxs = np.setdiff1d(idxs, deleted)
    orig = idxs.copy()
    for idx in deleted:
        idxs[orig > idx] -= 1
    return idxs


def shift_indexes(a, b, down: bool = True) -> np.ndarray:
    a = np.array(a)
    orig = a.copy()
    for idx in np.unique(b):
        if down:
            a[orig > idx] -= 1
        else:
            a[orig >= idx] += 1
    return a

def setdiff1d(a, b, assume_unique: bool = False, keep_duplicates: bool = False) -> np.ndarray:
    """Behaves the same as np.setdiff1d when keep_duplicates is false. Otherwise, keeps the duplicates 
    """
    a = np.asarray(a)
    b = np.asarray(b)
    if keep_duplicates:
        return a[~pd.Series(a).isin(pd.Series(b))]
    else:
        return np.setdiff1d(a, b, assume_unique=assume_unique)


def intersect1d(a, b, assume_unique: bool = False, keep_duplicates: bool = False):
    """Behaves the same as np.intersect1d when keep_duplicates is false. Otherwise, keeps the duplicates 
    """
    a = np.asarray(a)
    b = np.asarray(b)
    if keep_duplicates:
        return a[pd.Series(a).isin(pd.Series(b))]
    else: 
        return np.intersect1d(a, b, assume_unique=assume_unique)


@overload
def group_by_label(a: np.ndarray, labels: np.ndarray, return_idxs: Literal[False] = False) -> Dict: ...
@overload
def group_by_label(a: np.ndarray, labels: np.ndarray, return_idxs: Literal[True]) -> Tuple[Dict, Dict]: ...


def group_by_label(a: np.ndarray, labels: np.ndarray, return_idxs: bool = False) -> Union[Dict, Tuple[Dict, Dict]]:
    """Returns a dictionary where the keys are the labels and the values are the elements with the same label.

    Parameters
    ----------
    a : np.ndarray
        Values

    labels : np.ndarray
        Labels

    return_idxs : bool, default=False
        True - Return an additional dictionary with the {label: array of indexes of elements}
        

    Returns
    -------
    dict | tuple[dict]
        The dictionary with {label: array of elements of the corresponding label}

    Raises
    ------
    ValueError
        If `a` and `labels` have different lengths
    """
    if len(a) != len(labels):
        raise ValueError("`a` and `labels` must have the same length")
    d = {}
    if return_idxs:
        d_idxs = {}
    for label in unique(labels):
        idxs = np.nonzero(labels == label)
        d[label] = a[idxs]
        if return_idxs:
            d_idxs[label] = idxs
    if return_idxs:
        return d, d_idxs
    else:
        return d


def normalize_probs(p: Iterable) -> np.ndarray:
    """Normalize a vector of probabilities; treat special values inside p as follows:
        - np.inf: truncate np.inf to a value dependent on datatype's max representable number
        - np.nan: replace with datatype's epsilon value
        - 0: replace with datatype's epsilon value in order to allow a vector of all 0s to form a
             valid probability distribution (summing up to 1.0)

    Parameters
    ----------
    p : ndarray
        Array of the probabilities to be normalized

    Returns
    -------
    normalized probabilities
    """
    p = np.asarray(p)
    if len(p) == 0:
        return np.array([])
    eps_ = np.finfo(p.dtype).eps
    p[p == np.inf] = (np.finfo(p.dtype).max - 1) / (1.01 * len(p))
    p[np.isnan(p)] = eps_
    p[p == 0] = eps_

    return p / np.sum(p)


def _to_python_obj(a: Any) -> Any:
    """Helper function. Goes through collections recursively and transforms numpy types to python types if possible. Keeps everything else the same

    Parameters
    ----------
    a : Any
        Element to be transformed

    Returns
    -------
    int | float | Any
        Output python obj
    """
    if isinstance(a, np.ndarray):
        return a.tolist()
    elif isinstance(a, list):
        return [_to_python_obj(e) for e in a]
    elif isinstance(a, tuple):
        return tuple(_to_python_obj(e) for e in a)
    elif isinstance(a, dict):
        for k in list(a.keys()):
            k_ = _to_python_obj(k)
            v_ = _to_python_obj(a[k])
            a.pop(k)
            a[k_] = v_
        return a
    elif isinstance(a, np.integer):
        return int(a)
    elif isinstance(a, np.floating):
        return float(a)
    else:
        return a


def filter_missing_and_inf(a):
    """ Filter-out missing and infinite values from the provided array. """
    return a[~pd.isna(a) & (a != float('inf')) & (a != float('-inf'))]


def check_same_length(*arrays, allow_None: bool = True) -> None:
    n_arrays = len(arrays)
    if n_arrays == 0:
        raise ValueError("At least one array required as input")
    if n_arrays == 1:
        return None

    length = None
    for a in arrays:
        if a is None and not allow_None:
            raise ValueError("Found array that is None")
        if a is not None and length is None:
            length = len(a)
            continue
        if a is not None and len(a) != length:
            raise ValueError(f"Arrays must have the same length. {len(a)} != {length}")
    return None
