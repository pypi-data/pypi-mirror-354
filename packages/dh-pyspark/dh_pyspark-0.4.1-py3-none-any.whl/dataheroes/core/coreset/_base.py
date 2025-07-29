import inspect
import math
from abc import ABC
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
import numpy as np
from numpy.random import Generator
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_consistent_length

from ..sklearn_extra.validation import check_array

from ...utils import user_warning
from .common import (
    fairness_policy_adaptor,
    fairness_policy_adaptor_cleaning,
    is_arraylike,
    is_int,
    is_percent,
    is_int_or_float,
)
from ..numpy_extra import (
    delete_and_shift,
    unique,
    setdiff1d,
    intersect1d,
    check_random_state,
    normalize_probs,
)


def _adjust_sample_params(sample_params: dict, pc: float) -> dict:
    """
    Adjust sample_kwargs numeric values, by multiplying them with (percent)
    """
    res = sample_params.copy()
    for key in ["minimum_size", "class_size"]:
        if key in sample_params:
            if isinstance(sample_params[key], dict):
                res[key] = {k: math.ceil(v * pc) for k, v in sample_params[key].items()}
            elif isinstance(sample_params[key], int):
                res[key] = math.ceil(sample_params[key] * pc)
            elif isinstance(sample_params[key], float):
                res[key] = sample_params[key] * pc

    return res


def take_important(
    importance,
    y=None,
    size: int = None,
    class_size: Dict[Any, int] = None,
    sample_all: list = None,
    ignore_idxs: Iterable = None,
    classes: list = None,
    include_idxs: Iterable = None,
):
    """Return samples with the highest importance value"""

    if y is not None:
        y = check_array(y, ensure_2d=False, dtype=None)
        check_consistent_length(y, importance)

    if size is not None and not is_int(size, positive=True):
        raise TypeError(f"`size` must be None or a positive int, found {size}")

    if class_size is not None and any(not is_int(v, positive=True) for v in class_size.values()):
        raise TypeError("All values in `class_size` must be positive int")

    # sample_all takes precedence over class size
    if class_size is not None and sample_all is not None:
        class_size = {k: v for k, v in class_size.items() if k not in sample_all}

    avail_idxs = np.arange(len(importance))
    # consider only specific classes
    if classes:
        avail_idxs = avail_idxs[np.isin(y, classes)]

    if include_idxs is not None:
        avail_idxs = np.intersect1d(avail_idxs, include_idxs)

    if ignore_idxs is not None:
        ignore_idxs = check_array(ignore_idxs, ensure_2d=False, dtype=int, ensure_min_samples=0)
        if np.any(ignore_idxs < 0):
            raise ValueError("Ignore indices cannot include negative numbers.")

        if ignore_idxs.size > 0:
            avail_idxs = np.setdiff1d(avail_idxs, ignore_idxs)

    # start computing
    final_idxs = np.array([]).astype(int)

    def _take(idxs, max_size):
        idxs = np.intersect1d(idxs, avail_idxs) if idxs is not None else avail_idxs
        if max_size is not None:
            idxs = idxs[np.argsort(importance[idxs])[::-1]]
            idxs = idxs[:max_size]
        return idxs

    if class_size is not None:
        for c, c_size in class_size.items():
            c_idxs = np.where(y == c)[0]
            final_idxs = np.concatenate([final_idxs, _take(c_idxs, c_size)])
            avail_idxs = np.setdiff1d(avail_idxs, c_idxs)

    if sample_all is not None:
        for c in sample_all:
            c_idxs = np.where(y == c)[0]
            final_idxs = np.concatenate([final_idxs, _take(c_idxs, None)])
            avail_idxs = np.setdiff1d(avail_idxs, c_idxs)

    if size:
        r_size = size - final_idxs.size
        if r_size > 0 and avail_idxs.size > 0:
            final_idxs = np.concatenate([final_idxs, _take(None, r_size)])

    # Return final indexes sorted bt importance
    return final_idxs[np.argsort(importance[final_idxs])[::-1]]


def _n_samples_from_input(a: Union[int, Tuple[int, int], Iterable]) -> int:
    if is_int(a, positive=True):
        n_samples = a
    elif isinstance(a, tuple):
        if len(a) != 2:
            raise ValueError("When `a` is a tuple, it must have 2 elements, (min, max)")
        if a[0] < a[1]:
            a = (a[1], a[0])
        n_samples = a[1] - a[0]
    elif is_arraylike(a):
        n_samples = len(a)
    else:
        raise ValueError("`a` must be a positive int, a tuple or an array-like")

    return n_samples

# MARK: Choice function
def choice(
    a: Union[int, Tuple[int, int], Iterable],
    size: Union[int, Tuple[int, int]] = 1,
    *,
    p: Optional[Iterable] = None,
    deterministic_size: Optional[float] = None,
    return_info: bool = False,
    order: str = "sort",
    random_state: Optional[Union[int, Generator]] = None,
):
    # Check size.
    n_sampling_rounds, sample_size = validate_coreset_size(size, allow_none=False)

    # Set rng
    random_state = check_random_state(random_state)
    n_samples = _n_samples_from_input(a)

    # Check probability parameter
    if p is None:
        p = np.ones(n_samples) / n_samples  # uniform
    else:
        p = check_array(p, ensure_2d=False, dtype=float, ensure_all_finite=True, copy=True)
        if p.ndim != 1:
            raise ValueError("The probability distribution must be 1-dimensional")
        p = normalize_probs(p)

    if n_samples is None:
        n_samples = len(p)
    else:
        if n_samples != len(p):
            raise ValueError("The probability array must have the same length as the sample pool")

    # Check deterministic size.
    if deterministic_size is not None:
        if is_percent(deterministic_size):
            size_det = math.floor(sample_size * deterministic_size)
            size_prb = sample_size - size_det
        else:
            raise TypeError(f"`deterministic_size` must be a percent.  Found {type(deterministic_size)}")
    else:
        size_det = 0
        size_prb = sample_size

    # Start sampling.
    pool = np.arange(n_samples, dtype=int)  # pool of indexes
    # selected = np.empty((n_sampling_rounds, sample_size), dtype=int)
    selected = np.empty((n_sampling_rounds, 0), dtype=int)
    selected_det = np.empty(0, dtype=int)
    if deterministic_size is not None:
        if size_det > 0:
            idxs = take_important(importance=p[pool], size=size_det)  # (size_det, )
            pool_idxs = pool[idxs]
            idxs = np.repeat(pool_idxs[None, :], n_sampling_rounds, axis=0)
            selected = np.concatenate([selected, idxs], axis=-1)
            selected_det = np.concatenate([selected_det, pool_idxs])
            pool = np.setdiff1d(pool, pool_idxs)  # remove important samples from pool
        if size_prb > 0:
            p_ = normalize_probs(p[pool])
            idxs = random_state.choice(pool, size=(n_sampling_rounds, size_prb), p=p_, replace=True)
            selected = np.concatenate([selected, idxs], axis=-1)

    else:
        p_ = normalize_probs(p[pool])
        idxs = random_state.choice(pool, size=(n_sampling_rounds, sample_size), p=p_, replace=True)
        selected = np.concatenate([selected, idxs], axis=-1)

    # Decide order of samples here.
    if order == "sort":
        selected = np.sort(selected, axis=-1)
    elif order == "shuffle":
        selected = random_state.permutation(selected, axis=-1)
    elif order is None:
        pass
    else:
        t = ["sort", "shuffle", None]
        raise ValueError(f"Order must be one of {t}, found {order}")
    info = {
        "size": size,
        "n_sampling_rounds": n_sampling_rounds,
        "sample_size": sample_size,
        "deterministic_size": deterministic_size,
        "size_det": size_det,
        "size_prb": size_prb,
        "selected_det": selected_det,
    }

    if n_sampling_rounds == 1:
        selected = selected.ravel()
    if return_info:
        return selected, info
    else:
        return selected


def complete_choice(
    a: Union[int, Tuple[int, int], Iterable],
    size: Optional[int] = None,
    selected: Iterable[int] = None,
    *,
    p: Optional[Iterable] = None,
    deterministic_size: Optional[float] = None,
    return_info: bool = False,
    order: str = "sort",
    random_state: Optional[Union[int, Generator]] = None,
):
    if size is not None and not is_int(size, positive=True):
        raise TypeError(f"`size` must be None or a positive int, found {size}")

    if selected is None or len(selected) == 0:
        return choice(
            a,
            size=size,
            p=p,
            deterministic_size=deterministic_size,
            return_info=return_info,
            order=order,
            random_state=random_state,
        )

    selected = np.asarray(selected)
    n_samples = _n_samples_from_input(a)
    if np.max(selected) > n_samples:
        raise ValueError(f"Index {np.max(selected)} found in `selected`, for an array with length {n_samples}")

    if size:
        size = max(0, size - len(selected))
    idxs, info = choice(
        a,
        size=size,
        p=p,
        deterministic_size=deterministic_size,
        return_info=True,
        order=order,
        random_state=random_state,
    )
    # TODO: If idxs or selected is 1d, and the other 2d, repeat and concateante.
    # if idxs.ndim == 2 and selected.dim == 2:
    #     if selected.shape[0] != info.shape[0]:
    #         raise ValueError(f"`selected` must have the same number of rows as `idxs`. Found {selected.shape[0]} "
    #                             f"and {idxs.shape[0]}")
    # if selected.ndim == 1 and idxs.ndim == 2:
    #     selected = np.repeat(selected[None, :], idxs.shape[0], axis=0)
    # elif idxs.ndim == 2 and idxs.ndim == 1:
    #     idxs = np.repeat(idxs[None, :], selected.shape[0], axis=0)
    # selected = np.concatenate([selected, idxs], axis = -1)

    selected = np.concatenate([selected, idxs], axis=-1)
    info["selected_size"] = selected.shape

    if return_info:
        return selected, info
    else:
        return selected


# MARK: Choice Classification
def choice_classification(
    y: Iterable,
    *,
    p: Optional[Iterable] = None,
    # Constraints
    size: Optional[Union[Union[int, np.integer], Tuple[int, Union[int, np.integer]]]] = None,
    sample_all: Optional[Iterable] = None,
    class_size: Dict[Any, Union[int, np.integer, float]] = None,
    minimum_size: Union[int, str, Dict[Any, int]] = None,
    deterministic_size: Optional[float] = None,
    # Flags and indicators.
    fair: Union[str, bool] = "training",
    return_info: bool = False,
    order: Optional[str] = "sort",
    classes: Optional[Iterable] = None,
    counts: Optional[Iterable] = None,
    n_features: Optional[int] = None,
    random_state: Optional[Union[int, Generator]] = None,
):
    # Check input arrays
    y = check_array(y, ensure_2d=False, dtype=None)

    # Check size.
    n_sampling_rounds, sample_size = validate_coreset_size(size, allow_none=True)
    initial_sample_size = sample_size

    # Set rng
    random_state = check_random_state(random_state)

    # Check given classes and counts
    if classes is None or counts is None:
        classes, counts = unique(y, return_counts=True)  # get classes
        classes_counts = dict(zip(classes, counts))
        classes = set(classes)
    else:
        classes = set(classes)
        classes_counts = dict(zip(classes, counts))
    n_samples = len(y)

    # Check probability parameter
    if p is None:
        p = np.ones(n_samples) / n_samples  # uniform
    else:
        p = check_array(p, ensure_2d=False, dtype=float, ensure_all_finite=True, copy=True)
        if p.ndim != 1:
            raise ValueError("The probability distribution must be 1-dimensional")
        p = normalize_probs(p)

    if n_samples is None:
        n_samples = len(p)
    else:
        if n_samples != len(p):
            raise ValueError("The probability array must have the same length as the sample pool")

    # Flags for steps. If the pool is empty after some step, we'll stop sampling and return
    # Priority: sample_all > class_size > fair > min_size > size
    min_flag = True  # Apply minimum size
    complete_flag = True  # Complete up to size at the end
    class_flag = True  # Apply class size (given or fairness)
    removed_classes = set()
    remaining_classes = set(classes)

    if size is None:
        complete_flag = False
    # Check sample_all
    if sample_all is not None:
        sample_all = list(set(sample_all).intersection(classes))  # Make sure sample all classes exist
        if size is not None:
            t = sum(classes_counts[c] for c in sample_all)
            if t > sample_size:
                raise ValueError(
                    f"The number of samples taken from the classes in {sample_all=}, {t}, "
                    f"will be greater than the coreset_size requested"
                )
        removed_classes = set(sample_all.copy())
        remaining_classes.difference_update(removed_classes)
        if size is not None:
            for c in removed_classes:
                sample_size -= classes_counts.get(c, 0)

    # Edge case where sample_all has all classes. Here, return
    if len(remaining_classes) == 0:
        min_flag, complete_flag, class_flag = False, False, False

    # Check class_size
    if class_flag:
        # Check if we need to apply fairness policy.
        # TODO: This will overwrite the given class_size. Check if this is the best approach.
        if fair and size is not None and sample_size < len(classes) * 2:  # TODO do this with remaining classes?
            fair = False
            minimum_size = "auto" if minimum_size is None else minimum_size
        if fair and size is not None:
            if class_size is not None:
                user_warning(
                    "`class_size` and `fair` are both passed in. In this case the fairness mechanism will be used."
                )
            min_flag = False
            complete_flag = False  # Fairness will compute an exact split.
            cc_rem = {c: v for c, v in classes_counts.items() if c not in removed_classes}
            if fair is True or fair == "training":
                fairness_f = fairness_policy_adaptor
            elif fair == "cleaning":
                fairness_f = fairness_policy_adaptor_cleaning
            else:
                t = ["training", "cleaning", True, False]
                raise ValueError(f"`fair` must be one of {t}, found {fair}")

            class_size = fairness_f(size=sample_size, class_size=cc_rem, random_state=random_state)
            # Edge case. Add up to size.
            if sum(class_size.values()) < sample_size:
                diff = sample_size - sum(class_size.values())
                t = random_state.choice(list(class_size.keys()), size=diff)
                for e in t:
                    class_size[e] += 1
            removed_classes.update(class_size.keys())  # This should include all classes now
            remaining_classes.difference_update(removed_classes)
            assert (
                removed_classes == set(classes) and len(remaining_classes) == 0
            ), "When fairness is applied `removed_classes` should include all classes"
        elif not fair and class_size is not None:
            # Remove classes from sample_all and make sure class_size is a subset of classes_counts.
            # Also transform from floats to int
            class_size = {
                c: v if isinstance(v, int) else int(v * size) for c, v in class_size.items() if c in remaining_classes
            }
            if size is not None:
                t = sum(class_size.values())
                if t > initial_sample_size:
                    raise ValueError(
                        f"The number of samples taken from the classes in {class_size=}, {t}, "
                        f"will be greater than the {sample_size=} requested"
                    )
            removed_classes.update(class_size.keys())
            remaining_classes.difference_update(removed_classes)

        # Subtract from sample_size, if class_size is given OR computed by fairness.
        if class_size is not None and size is not None:
            for c, v in class_size.items():
                sample_size -= v

    if len(remaining_classes) == 0:
        complete_flag = False
        min_flag = False

    # Check deterministic_size
    # TODO: support deterministic size as a Dict[Any, float | int]
    if deterministic_size is not None:
        min_flag = False  # Ignore min_size when deterministic size is used.
        if class_size is None:
            if is_percent(deterministic_size):
                size_det = math.floor(sample_size * deterministic_size)
                size_prb = sample_size - size_det
            else:
                raise TypeError(
                    f"`deterministic_size` must be percent when `class_size` is None, found {type(deterministic_size)}"
                )
        elif is_percent(deterministic_size):
            class_size_det = {c: math.floor(v * deterministic_size) for c, v in class_size.items()}
            class_size_prb = {c: math.ceil(v * (1 - deterministic_size)) for c, v in class_size.items()}
            if complete_flag:
                size_det = math.floor(sample_size * deterministic_size)
                size_prb = sample_size - size_det
        else:
            raise TypeError(f"`deterministic_size` must be a percent. Found {type(deterministic_size)}")
    else:
        if class_size is not None:
            class_size_det = {}
            class_size_prb = class_size.copy()
        if complete_flag:
            size_det = 0
            size_prb = sample_size

    # Check minimum_size
    if min_flag and minimum_size is not None:
        if minimum_size == "auto":
            # Try to take n_features per class. If you can't, take size // len(rem_classes).
            if n_features is None:
                n_features = min(math.ceil(0.01 * n_samples // len(classes)), len(classes))
            if n_features * len(remaining_classes) > sample_size:
                ms = sample_size // len(remaining_classes)
            else:
                ms = n_features

            minimum_size = {c: ms for c in remaining_classes}
        if isinstance(minimum_size, dict):
            # Take only the remaining classes
            minimum_size = {c: v for c, v in minimum_size.items() if c in remaining_classes}
        if is_int(minimum_size, positive=True):
            minimum_size = {c: minimum_size for c in remaining_classes}

        # Always upper bound minimum size by the max number of samples per class.
        minimum_size = {c: min(v, classes_counts[c]) for c, v in minimum_size.items()}
        for c, v in minimum_size.items():
            sample_size -= v

    # Start sampling
    pool = np.arange(n_samples, dtype=int)  # pool of indexes
    # selected = list([np.array([], dtype=int) for i in range(n_sampling_rounds)])  # selected samples
    selected = np.empty((n_sampling_rounds, 0), dtype=int)
    selected_det = np.empty(0, dtype=int)
    selected_sample_all = np.empty(0, dtype=int)

    def _normalize_sample_add(
        selected: np.ndarray, p: np.ndarray, c_idxs: np.ndarray, size: Union[int, np.integer], scale: int = 1
    ) -> np.ndarray:
        size = max(int(size), 0)
        p_c = normalize_probs(p[c_idxs])
        idxs = random_state.choice(c_idxs, size=(n_sampling_rounds, size), p=p_c, replace=True)
        return np.concatenate([selected, idxs], axis=-1)

    # Take all indexes from a class, add them to `selected` and remove them from `pool`
    if sample_all is not None:
        for c in sample_all:
            c_idxs = pool[np.where(y[pool] == c)[0]]  # (sample_size,)
            selected_sample_all = np.concatenate([selected_sample_all, c_idxs])
            idxs = np.repeat(c_idxs[None, :], n_sampling_rounds, axis=0)
            selected = np.concatenate([selected, idxs], axis=-1)
            pool = np.setdiff1d(pool, c_idxs)  # remove class from pool

    if class_size is not None:
        if deterministic_size is not None:
            for c, v in class_size_det.items():
                c_idxs = pool[np.where(y[pool] == c)[0]]
                if c_idxs.size > 0:
                    p_c = p[c_idxs]
                    idxs = take_important(importance=p_c, size=v)
                    pool_idxs = c_idxs[idxs]
                    idxs = np.repeat(c_idxs[idxs][None, :], n_sampling_rounds, axis=0)
                    selected = np.concatenate([selected, idxs], axis=-1)
                    selected_det = np.concatenate([selected_det, pool_idxs])
                    pool = np.setdiff1d(pool, pool_idxs)  # remove selected idxs from pool
            for c, v in class_size_prb.items():
                c_idxs = pool[np.where(y[pool] == c)[0]]
                pool = np.setdiff1d(pool, c_idxs)  # remove whole class from pool
                if c_idxs.size > 0:
                    selected = _normalize_sample_add(selected, p, c_idxs, v)
        else:
            c_idxs_all = np.array([])
            for c, v in class_size.items():
                c_idxs = pool[np.where(y[pool] == c)[0]]
                c_idxs_all = np.concatenate([c_idxs_all, c_idxs])
                if c_idxs.size > 0:
                    selected = _normalize_sample_add(selected, p, c_idxs, v)
            pool = np.setdiff1d(pool, c_idxs_all)  # remove whole class from pool
    if min_flag and minimum_size is not None:
        for c, v in minimum_size.items():
            c_idxs = pool[np.where(y[pool] == c)[0]]
            if c_idxs.size > 0:
                selected = _normalize_sample_add(selected, p, c_idxs, v)

    if complete_flag and sample_size > 0 and len(pool) > 0:
        p_ = normalize_probs(p[pool])
        if deterministic_size is not None:
            if size_det > 0:
                idxs = take_important(importance=p[pool], size=size_det)
                pool_idxs = pool[idxs]
                idxs = np.repeat(pool_idxs[None, :], n_sampling_rounds, axis=0)
                selected = np.concatenate([selected, idxs], axis=-1)
                selected_det = np.concatenate([selected_det, pool_idxs])
                pool = np.setdiff1d(pool, pool_idxs)  # remove important samples from pool
            if size_prb > 0:
                p_ = normalize_probs(p[pool])
                idxs = random_state.choice(pool, size=(n_sampling_rounds, size_prb), p=p_, replace=True)
                selected = np.concatenate([selected, idxs], axis=-1)
        else:
            idxs = random_state.choice(pool, size=(n_sampling_rounds, sample_size), p=p_, replace=True)
            selected = np.concatenate([selected, idxs], axis=-1)

    # Decide order of samples here.
    if order == "sort":
        selected = np.sort(selected, axis=-1)
        # selected = [np.sort(selected[i]) for i in range(n_sampling_rounds)]
    elif order == "shuffle":
        selected = random_state.permutation(selected, axis=-1)
        # [random_state.shuffle(selected[i]) for i in range(n_sampling_rounds)]  # inplace shuffle
    elif order is None:
        pass
    else:
        t = ["sort", "shuffle", None]
        raise ValueError(f"order must be one of {t}. Received {order}")

    info = {
        "size": size,
        "n_sampling_rounds": n_sampling_rounds,
        "sample_size": sample_size,
        "class_size": class_size,
        "deterministic_size": deterministic_size,
        "fair": fair,
        "class_size_prb": class_size_prb if class_size is not None else None,
        "class_size_det": class_size_det if class_size is not None else None,
        "size_det": size_det if complete_flag else None,
        "size_prb": size_prb if complete_flag else None,
        "minimum_size": minimum_size,
        "class_flag": class_flag,
        "min_flag": min_flag,
        "complete_flag": complete_flag,
        "removed_classes": removed_classes,
        "remaining_classes": remaining_classes,
        "selected_det": selected_det,
        "selected_sample_all": selected_sample_all,
    }
    if n_sampling_rounds == 1:
        selected = selected.ravel()
    if return_info:
        return selected, info
    else:
        return selected


def complete_choice_classification(
    y,
    selected: Optional[Iterable[int]] = None,
    *,
    p: Optional[Iterable] = None,
    # Constraints
    size: Optional[int] = None,
    sample_all: Optional[List[Any]] = None,
    class_size: Optional[Dict[Any, int]] = None,
    minimum_size: Optional[Union[int, str, Dict[Any, int]]] = None,
    deterministic_size: Optional[float] = None,
    # Flags and indicators.
    fair: Union[str, bool] = "training",
    return_info: bool = False,
    order: Optional[str] = "sort",
    classes: Optional[Iterable] = None,
    counts: Optional[Iterable] = None,
    n_features: Optional[int] = None,
    random_state: Optional[Union[int, Generator]] = None,
):
    if size is not None and not is_int(size, positive=True):
        raise TypeError(f"`size` must be None or a positive int, found {size}")

    if selected is None or len(selected) == 0:
        return choice_classification(
            y=y,
            size=size,
            p=p,
            sample_all=sample_all,
            deterministic_size=deterministic_size,
            class_size=class_size,
            minimum_size=minimum_size,
            fair=fair,
            return_info=return_info,
            order=order,
            classes=classes,
            counts=counts,
            n_features=n_features,
            random_state=random_state,
        )

    selected = np.asarray(selected)
    n_samples = len(y)
    if np.max(selected) > n_samples:
        raise ValueError(
            f"Indices in selected are out of bounds: index {np.max(selected)} found, for an array with length {n_samples}"
        )
    s_classes, s_counts = unique(y[selected], return_counts=True)
    s_classes_counts = dict(zip(s_classes, s_counts))
    # Subtract selected samples from the constraints.
    if size:
        size = max(0, size - len(selected))
    if class_size:
        class_size = {c: max(0, v - s_classes_counts[c]) if c in s_classes_counts else v for c, v in class_size.items()}
    if minimum_size:
        minimum_size = {
            c: max(0, v - s_classes_counts[c]) if c in s_classes_counts else v for c, v in minimum_size.items()
        }

    idxs, info = choice_classification(
        y=y,
        size=size,
        p=p,
        sample_all=sample_all,
        deterministic_size=deterministic_size,
        class_size=class_size,
        minimum_size=minimum_size,
        fair=fair,
        return_info=True,
        order=order,
        classes=classes,
        counts=counts,
        n_features=n_features,
        random_state=random_state,
    )
    # if len(idxs) > 1:
    #     raise ValueError(f"Choice method expected to return a single array for number of sampling rounds of "
    #                      f"1, not {len(idxs)}")
    info["selected_counts"] = s_classes_counts
    selected = np.concatenate([selected, idxs], axis=-1)
    if return_info:
        return selected, info
    else:
        return selected


def aggregate_and_reweight(idxs, sample_weight):
    """Removes duplicate indexes and sums up the weights of the array
    Ex: for idxs = [1, 1, 0, 0] and sample_weight = [10, 10, 20, 20]
    we get idxs [1, 0] with weights [20, 40]

    Parameters
    ----------
    idxs : array-like
        Indexes array

    sample_weight : array-like
        weight for each index

    Returns
    -------
    (array-like, array-like)
        new aggregated indexes and weights
    """
    new_idxs, counts = unique(idxs, return_counts=True)
    new_weights = sample_weight[new_idxs] * counts

    return new_idxs, new_weights


def compute_weights(probs, n_requested: int, previous_weights=None):
    if previous_weights is None:
        previous_weights = np.ones(len(probs))
    return previous_weights / (n_requested * probs)


def validate_coreset_size(coreset_size: Union[int, Tuple[int, int]], allow_none: bool) -> Tuple[int, Union[None, int]]:
    if coreset_size is None:
        if allow_none:
            return 1, None
        else:
            ValueError("Coreset size cannot be None")

    if type(coreset_size) is tuple:
        if len(coreset_size) != 2:
            raise ValueError(f"`coreset_size` as a tuple must be of length 2, not {len(coreset_size)}")
        if not is_int(coreset_size[0], positive=True) or not is_int(coreset_size[1], positive=True):
            raise TypeError(
                f"`coreset_size` as a tuple must contain two positive integers, not "
                f"({coreset_size[0]},{coreset_size[1]}) of types ({type(coreset_size[0])},{type(coreset_size[1])})"
            )
        return coreset_size[0], coreset_size[1]
    else:
        if not is_int_or_float(coreset_size, positive=True):
            raise TypeError(
                f"`coreset_size` must either be a positive integer, a float or a tuple of positive "
                f"integers of size 2, not {coreset_size} of type {type(coreset_size)})"
            )
        return 1, coreset_size


class CoresetBase(ABC):
    _coreset_type: str = "base"
    _possible_sensitivities = []
    _possible_estimators = []
    _possible_unions = []

    def __init__(self, *, random_state: Union[int, Generator] = None):
        """Sampler class. This class handles the coreset sampling
        Parameters
        ----------
        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        """

        # Keeps the weights and indexes of the last iteration of `self.build()`.
        # TODO: Should this be None and raise error in
        # self.get_index_weights() if the user attempts to get them before build?

        # Internal state
        self.weights = np.array([])
        self.idxs = np.array([], dtype=int)
        self.sensitivities = np.array([])
        self.keep_selected_only = False
        self.is_classification = self._coreset_type == "classification"
        self.sample_kwargs = None
        # Counts and classes for the data we sampled for in classification task.
        self.classes = None
        self.counts = None
        self.y_encoded = None
        self.random_state = check_random_state(random_state=random_state)
        # Unchangable state
        self._algorithm = None

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def y(self):
        # May be overwritten in subclasses. Might not coincide with the given y.
        # This may be the encoded y, usually used for sampling in "classification" mode.
        if self._coreset_type in ["classification", "regression"]:
            return self.y_encoded
        else:
            raise ValueError("required `y` is None. Call `.build()` before.")

    def to_dict(self, with_important: bool = True, to_list=True, sensi_only=False, use_keep_selected_only=True):
        def f_array(v):
            return v.tolist() if to_list else v

        result = {"sensitivities": f_array(self.sensitivities)}
        if sensi_only:
            return result

        result.update(
            {
                "weights": f_array(self.weights),
                "idxs": f_array(self.idxs),
            }
        )
        if hasattr(self, "estimation_params_") and self.estimation_params_ is not None:
            result.update(
                {
                    "estimation_params_": self.estimation_params_,
                    "_estimation_algorithm_used": self._estimation_algorithm_used,
                }
            )
        if use_keep_selected_only:
            result["keep_selected_only"] = self.keep_selected_only

        if with_important:
            if self.y_encoded is not None:
                result["y_encoded"] = f_array(self.y_encoded)
            if self.classes is not None:
                result["classes"] = f_array(self.classes)
        return result

    @classmethod
    def from_dict(cls, state_dict: dict, **kwargs):
        coreset = cls(**kwargs)
        coreset.set_state(state_dict)
        return coreset

    def set_state(self, state_dict):
        for k, v in state_dict.items():
            setattr(self, k, v)
        self.weights = np.array([] if self.weights is None else self.weights)
        self.idxs = np.array([] if self.idxs is None else self.idxs, dtype=int)
        self.sensitivities = np.array([] if self.sensitivities is None else self.sensitivities)
        self.y_encoded = np.array(self.y_encoded, dtype=int) if self.y_encoded is not None else None
        self.classes = np.array(self.classes) if self.classes is not None else None
        return self

    def union(self, coresets: List["CoresetBase"]) -> "CoresetBase":
        raise NotImplementedError(f"Union is not implemented for {self.__class__.__name__}.")


    def clear(self):
        # empty the coreset
        self.idxs = np.array([], dtype=np.int64)
        self.n_samples = 0
        self.sensitivities = np.array([]) # TODO Check if this zero is needed
        self.weights = np.array([])
        if hasattr(self, "w_build"):
            self.w_build = np.array([]) if self.w_build is not None else None
        self.y_encoded = np.array([]) if self.y_encoded is not None else None
        self.classes = np.array([]) if self.classes is not None else None


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
        """Builds the coreset. Computes sensitivities and calls `.sample()`
        on the given X, y, w with the constraints and parameters
        given in the **sample_kwargs(). Saves the indexes and weights
        Some parameters are for classification only. They will be ignored if the _coreset_type != "classification"

        Parameters
        ----------
        X: array-like of shape  (n_samples, n_features)
            features

        y: array-like of shape (n_samples, ), default = None
            labels. Optional

        w : array-like of shape(n_samples, ), default=None
            previous weights

        coreset_size: int
            int - number of samples to sample.

        deterministic_size: float, default = None
            The percent of samples to be taken deterministically.

        sample_all: List, default = None,
            Classification only
            Classes in this list will have all samples returned.

        class_size: Dict[Any, int], default = None
            Classification only.
            Number of data instances to sample per class. Classes already in `sample_all` are ignored.

        minimum_size: int | dict, default = None
            Classification only.
            Minimum size per class. Classes common with `class_size` and `sample_all` are ignored

        fair: str, default = 'training'
            Classification only.
            If fairness is to be applied. It will compute the appropiate amount per class.
            It will override the `class_size`.
            It will apply the appropriate fairness_policy_adapter depending on the value (training or cleaning)

        **sample_kwargs: Key arguments
            Extra key arguments pased to `.sample()`
            Check `.sample()` docs


        Returns
        -------
        idxs: array-like of shape (coreset_size, ) or (sum(coreset_size), ) if coreset_size is a list.
            Indexes of the selected samples
        weights: array-like of shape (coreset_size, ) or (sum(coreset_size), ) if coreset_size is a list.
            Weights of the selected samples
        """

        # Check constraints.
        deterministic_size, sample_all, class_size, minimum_size = self._check_constraints(
            deterministic_size=deterministic_size,
            sample_all=sample_all,
            class_size=class_size,
            minimum_size=minimum_size,
        )

        # Check coreset_size.
        if coreset_size is not None and not is_int_or_float(coreset_size, positive=True):
            raise TypeError(f"`coreset_size` must be None or a positive int or float, found {coreset_size}")

        if new_state is None:
            if from_coresets is not None:

                self.union(coresets=from_coresets)
                # Only functions with union can estimate
                self.compute_sensitivities(X=X, y=y, w=w, estimate=True)
            else:
                self.compute_sensitivities(X=X, y=y, w=w)
        else:
            self.set_state(new_state)
        if y is not None and self.is_classification:
            # Needed for the important calculation, and classification sampling
            self.classes, self.y_encoded, self.counts = unique(y, return_counts=True, return_inverse=True)
            self.classes_encoded = np.arange(len(self.classes))
        self.n_samples, self.n_features = X.shape
        self.w_build = w  # needed for sampling and computing weights
        self.sample_kwargs = {
            "coreset_size": coreset_size,
            "deterministic_size": deterministic_size,
            "sample_all": sample_all,
            "class_size": class_size,
            "minimum_size": minimum_size,
            "det_weights_behaviour": sample_kwargs.get("det_weights_behaviour", "auto"),
            "fair": fair,
            **sample_kwargs,
        }
        self.compute_sample(**self.sample_kwargs)
        if self.keep_selected_only:
            self.sensitivities = self.sensitivities[self.idxs]
            if self.y_encoded is not None:
                self.y_encoded = self.y_encoded[self.idxs]

        return self.idxs, self.weights

    # MARK: Sample function
    def sample(
        self,
        *,
        coreset_size: Optional[Union[int, Tuple[int, int]]] = None,
        deterministic_size: Optional[float] = None,
        sample_all: Optional[Iterable[Any]] = None,
        class_size: Optional[Dict[Any, int]] = None,
        minimum_size: Optional[Union[int, str, Dict[Any, int]]] = None,
        fair: Union[str, bool] = "training",
        order: Optional[str] = "sort",
        keep_duplicates: bool = False,
        sum_to_previous: bool = False,
        det_weights_behaviour: str = "keep",  # prop, inv
        as_classification: bool = False,
        random_state: Union[int, Generator] = None,  # TODO This input argument is ignored and reset from self!
    ) -> Union[Tuple[List, List], Tuple[np.ndarray, np.ndarray]]:
        """Given some dataset (X, y) sample using the given sensitivity or the precomputed one.

        Parameters
        ----------
        coreset_size : int | Tuple[int, int]
            int - number of samples to sample.
            Tuple[int, int] - number of (re)sampling iterations, number of samples to sample.

        minimum_size: int | Dict[label, int], default = None
            Minimum size per class.
            If `size` is array-like then this parameter is ignored.
            This parameter is ignored if the task is not classification.

        sample_all: Iterable[label], default = None
            Only for classification tasks. List of classes from where to take every sample.
            For an array of [1, 2] we will sample everything for class 1 and 2.
            Raises an error if the number of taken samples is > coreset_size.

        sensitivities: array-like of shape (n_samples, ), default = None
            Custom sensitivities. Optional.
            If set to None will use the sensitivities computed with compute_sensitivities()
            If no sensitivities were computed will raise an error.

        order: Optional[str], default = "sort"
            The order in which the indexes are returned.
            "sort" = the order they appear in the dataset.
                This is the only option that works for nonclassification tasks
            "shuffle" = shuffle on them using the seed.
                None = No action taken. Sometimes they may be grouped by class
                in the order they were selected by np.random.choice

        random_state: int or np.random.Generator, default = None
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        keep_duplicates: bool, default = False
            Duplicates may appear when sampling with replace = True.
            True - Aggregate and reweight the selected samples to remove duplicates

        as_classification: bool, default = False
            Some regression-oriented coresets utilize classification coreset methods in order to solve a regression
            problem. This is achieved by transforming the y regression target values to class label targets.
            True - Use y stored as class labels (originally transformed from regression target values during the
                   calculation of sensitivities phase) instead of the original y as target regression values.

        det_weights_behaviour: str, default = "keep"
            "inv" - The deterministic weights will be inversely proportional to the probabilities
            "keep" - The deterministic sample weights are kept as given, and the probabilistic sample weights are summing up to (prev_W - sum(det))
            "prop" - The deterministic sample weights are summing up proportionally to the deterministic size (prev_W * det_size) and the 
                prob sample weights are summing up to (1 - det_size) * prev_W
                
        sum_to_previous: bool, default = False
            If True, the weights will be summed to the previous weights.

        Returns
        -------
        idxs: array-like of shape (coreset_size, ) or a list of array-likes of shape (coreset_size, )
              if the provided coreset_size is a tuple.
            Indexes of the selected samples, or a list of indexes of the selected samples when multiple rounds of
            sampling was requested.
        weights: array-like of shape (coreset_size, ) or a list of array-likes of shape (coreset_size, )
                 if the provided coreset_size is a tuple.
            Weights of the selected samples, or a list of weights of the selected sample when multiple rounds of
            sampling was requested.
        """

        # Overwrite existing sample params, if others non-default were provided as input.
        # sample_kwargs may include parameters that were not passed in build and are defaulted here.
        # TODO Dacian to review/remove self.sample_kwargs (requires adapting dtr.py).
        sample_kwargs = self.sample_kwargs.copy()
        for name, param in inspect.signature(self.sample).parameters.items():
            new_val = locals()[name]
            if param.default is not new_val or name not in self.sample_kwargs:
                sample_kwargs[name] = new_val
                # Don't update self.sample_kwargs with the values from sample_kwargs, in the common keys.
                # if name in self.sample_kwargs:
                # self.sample_kwargs[name] = new_val

        if det_weights_behaviour == "auto":
            det_weights_behaviour = "keep"

        # Handle a case with no samples.
        n_samples, n_features = self.n_samples, self.n_features
        if n_samples == 0:
            return np.array([], dtype=int), np.array([])

        # Check random & coreset size.
        random_state = check_random_state(self.random_state)
        multi_rounds = isinstance(coreset_size, tuple)
        n_sampling_rounds, sample_size = validate_coreset_size(coreset_size, allow_none=True)

        # Retrieve sensitivities & convert to probabilities.
        if self.sensitivities is None:
            raise ValueError("Sensitivities must be computed first.")
        sensitivities = self.sensitivities
        probs = normalize_probs(sensitivities)

        handle_classification = self.is_classification or self._coreset_type == "classification" or as_classification

        # Sample
        if handle_classification:
            y = self.y
            if not hasattr(self, "counts_") or self.counts is None or self.classes_encoded is None:
                classes, counts = unique(y, return_counts=True)  # Get the classes
            else:
                classes = self.classes_encoded
                counts = self.counts
            # If constraints are given in og classes, translate them to encoded classes
            for name, constraint in sample_kwargs.items():
                if isinstance(constraint, dict):
                    sample_kwargs[name] = {
                        self.classes_encoded[list(self.classes).index(k)]: v
                        for k, v in constraint.items()
                        if k in self.classes
                    }
                if isinstance(constraint, list):
                    sample_kwargs[name] = [
                        self.classes_encoded[list(self.classes).index(k)] for k in constraint if k in self.classes
                    ]
                if isinstance(constraint, np.ndarray):
                    sample_kwargs[name] = np.array(
                        [self.classes_encoded[list(self.classes).index(k)] for k in constraint if k in self.classes]
                    )

            # Meta stuff, keep for idea.
            # choice_kwargs = {k: v for k, v in sample_kwargs.items() if k in inspect.signature(choice_classification).parameters.keys()}
            # idxs, self.sample_info_ = choice_classification(
            #     y=y,
            #     p=probs,
            #     size=sample_kwargs["coreset_size"]
            #     classes=classes,
            #     counts=counts,
            #     n_features=n_features,
            #     return_info=True,
            #     random_state=random_state
            #     **choice_kwargs,
            # )
            idxs, self.sample_info_ = choice_classification(
                y,
                p=probs,
                size=sample_kwargs["coreset_size"],
                sample_all=sample_kwargs["sample_all"],
                class_size=sample_kwargs["class_size"],
                minimum_size=sample_kwargs["minimum_size"],
                deterministic_size=sample_kwargs["deterministic_size"],
                fair=sample_kwargs["fair"],
                order=sample_kwargs["order"],
                classes=classes,
                counts=counts,
                n_features=n_features,
                return_info=True,
                random_state=random_state,
            )
        else:
            idxs, self.sample_info_ = choice(
                len(probs),
                p=probs,
                size=sample_kwargs["coreset_size"],
                deterministic_size=sample_kwargs["deterministic_size"],
                order=sample_kwargs["order"],
                return_info=True,
                random_state=random_state,
            )

        # Compute weights.
        prev_weights = self.w_build if self.w_build is not None else np.ones(n_samples)
        selected_det = self.sample_info_["selected_det"]
        all_idxs = []
        all_weights = []

        # Modifies the `weights` array inplace
        def _adjust_weights(all_idxs, coreset_idxs, deterministic_size):
            if deterministic_size is None:
                deterministic_size = 0
            if det_weights_behaviour == "inv":
                weights[all_idxs] = prev_weights[all_idxs] / (len(coreset_idxs) * probs[all_idxs] + 1e-20)
            else:
                det_idxs = intersect1d(selected_det, all_idxs, selected_det, keep_duplicates=True)
                prb_idxs = setdiff1d(
                    intersect1d(coreset_idxs, all_idxs, keep_duplicates=True), selected_det, keep_duplicates=True
                )
                to_fill = setdiff1d(all_idxs, selected_det, keep_duplicates=True)
                scale_det = (
                    prev_weights[all_idxs].sum() * deterministic_size / prev_weights[det_idxs].sum()
                    if det_weights_behaviour == "prop"
                    else 1
                )
                weights[det_idxs] = prev_weights[det_idxs] * scale_det
                scale_prb = (
                    (1 - deterministic_size) * prev_weights[all_idxs].sum() / prev_weights[to_fill].sum()
                    if det_weights_behaviour == "prop"
                    else 1
                )
                probs_c = normalize_probs(p=sensitivities[to_fill])
                weights[to_fill] = prev_weights[to_fill] * scale_prb / (len(prb_idxs) * probs_c + 1e-20)

        for i in range(n_sampling_rounds):
            weights = np.ones(n_samples, dtype=float)
            idxs_i = idxs[i] if idxs.ndim > 1 else idxs
            if handle_classification:
                for c in classes:
                    c_idxs = np.where(y == c)[0]
                    _adjust_weights(c_idxs, idxs_i, deterministic_size)
                if sample_all is not None and det_weights_behaviour in ["keep", "prop"]:
                    weights[self.sample_info_["selected_sample_all"]] = prev_weights[
                        self.sample_info_["selected_sample_all"]
                    ]
            else:
                _adjust_weights(np.arange(n_samples), idxs_i, deterministic_size)

            if not sample_kwargs["keep_duplicates"]:
                idxs_i, weights_i = aggregate_and_reweight(idxs=idxs_i, sample_weight=weights)
            else:
                weights_i = weights[idxs_i]
            if sample_kwargs["sum_to_previous"]:
                weights_i = (
                    weights_i * (np.sum(self.w_build) if self.w_build is not None else n_samples) / np.sum(weights_i)
                )
            all_idxs.append(idxs_i)
            all_weights.append(weights_i)

        if not multi_rounds:
            return all_idxs[0], all_weights[0]
        else:
            return all_idxs, all_weights

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
        det_weights_behaviour: str = "keep",  # prop, inv
        order: Optional[str] = "sort",
        # Rebuild thresholds
        iterative_threshold: float = 0.1,
        resample_threshold: float = 0.1,
        n_iter: int = 50,
        # TODO better name for `sample_per_iter`
        sample_per_iter: Union[float, int] = 0.1,
        random_state: Union[int, Generator] = None,
    ):
        # Check input
        n_samples, n_dim = X.shape
        force_build = self.keep_selected_only
        if n_samples != 0:
            # Check input
            X = check_array(
                X,
                ensure_2d=True,
                dtype="numeric",
                ensure_all_finite=True,
                accept_sparse=True,
                accept_large_sparse=True,
            )
        if w is None:
            w = np.ones(n_samples)
        else:
            if len(w) != 0:
                w = check_array(w, ensure_2d=False)
            check_consistent_length(X, w)

        if y is not None:
            check_consistent_length(X, y)
            if self._coreset_type == "classification":
                classes, counts = unique(y, return_counts=True)
                classes_counts = dict(zip(classes, counts))
                n_classes = len(classes)

            else:
                # TODO: This can be better.
                n_classes = None
                classes_counts = None
        else:
            y = None
            classes_counts = None

        # Check constraints.
        deterministic_size, sample_all, class_size, minimum_size = self._check_constraints(
            deterministic_size=deterministic_size,
            sample_all=sample_all,
            class_size=class_size,
            minimum_size=minimum_size,
        )
        # sample_all = self.check_sample_all(sample_all, coreset_size, classes_counts)

        # Check coreset_size.
        if coreset_size is not None and not is_int(coreset_size, positive=True):
            raise TypeError(f"`coreset_size` must be None or a positive int, found {coreset_size}")

        if idxs_removed is None:
            idxs_removed = np.array([])

        # Adapt the old coreset to the new X and y dimensions
        # For this we delete the removed indexes and reindex
        # So for an old coreset [0, 5, 9] with removed indexes [5, 8] we would get a new coreset [0, 7]
        idxs_coreset = delete_and_shift(self.idxs, idxs_removed)  # These are now idxs in the new data
        assert len(idxs_coreset) <= len(self.idxs)
        # If fewer than `resample_threshold` samples are common then rebuild the coreset.
        if force_build or len(self.idxs) == 0 or len(idxs_coreset) / len(self.idxs) < resample_threshold:
            self.resampling_iter = None
            self.build(
                X,
                y,
                w,
                new_state=new_state,
                coreset_size=coreset_size,
                deterministic_size=deterministic_size,
                sample_all=sample_all,
                class_size=class_size,
                minimum_size=minimum_size,
                fair=fair,
                random_state=random_state,
                det_weights_behaviour=det_weights_behaviour,
                order=order,
            )
            return self

        # idxs common between the old X and the new X.
        idxs_common = np.arange(len(self.sensitivities))
        idxs_common = np.setdiff1d(idxs_common, idxs_removed)
        # old sensitivity values that are common with the new ones
        old_sensitivities = self.sensitivities[idxs_common]
        # Compute new sensitivity. Expensive function
        if not new_state:
            new_sensitivities = self.sensitivity(X, y, w=w) if X.shape[0] > 0 else np.array([])
        else:
            # self.set_state(new_state)
            new_sensitivities = np.array(new_state["sensitivities"])
        new_classes = new_counts = None
        new_y_encoded = y
        if y is not None and self.is_classification:
            new_classes, new_counts = unique(y, return_counts=True)
            new_y_encoded = self._encode_classes(y, classes=new_classes)  # Needed for the important calculation

        # Compute ratio
        # old_ratio = self.sensitivities[self.idxs] / np.sum(self.sensitivities)
        # KL idea:
        # s_new[idxs] vs s_old[idxs]
        # s_new[idxs] vs s_new
        def ratio_diff(s_new, s_old, idxs_new, idxs_old) -> float:
            """Compute difference between the ratios of the sensitivities of the
            newly selected indexes and the old ones.
            """
            new_ratio = np.sum(s_new[idxs_new]) / np.sum(s_new)
            old_ratio = np.sum(s_old[idxs_old]) / np.sum(s_old)
            return np.abs(old_ratio - new_ratio)

        def complete_coreset(y, probs, selected):
            """Complete the coreset, given the selected samples"""
            probs = normalize_probs(probs)
            if self._coreset_type == "classification":
                idxs, info = complete_choice_classification(
                    y=y,
                    p=probs,
                    selected=selected,
                    size=coreset_size,
                    sample_all=sample_all,
                    class_size=class_size,
                    minimum_size=minimum_size,
                    # deterministic_size=deterministic_size,
                    # order=order,
                    fair=fair,
                    return_info=True,
                    random_state=random_state,
                )
            else:
                idxs, info = complete_choice(
                    len(probs),
                    selected=selected,
                    p=probs,
                    size=coreset_size,
                    # deterministic_size=deterministic_size,
                    # order=order,
                    return_info=True,
                    random_state=random_state,
                )
            return idxs

        # If the condition is not satisfied start iterative resampling
        # until we meet the condition.
        # else just sample the missing samples and roll with it (because we trust the old coreset)
        # check if any of idxs coreset is greater than lenght of old_sensitivities
        if np.any(idxs_coreset >= len(old_sensitivities)):
            print("stop")
        if np.any(idxs_coreset >= len(new_sensitivities)):
            print("stop")
        _starting_ratio_diff = ratio_diff(new_sensitivities, old_sensitivities, idxs_coreset, idxs_coreset)
        if _starting_ratio_diff > iterative_threshold:
            # Iterative resampling
            # 1. Recomplete the coreset.
            # 2. Check threshold. If the condition passes end here.
            # 3. Remove a percent of samples uniformly
            # 4. GOTO 1.
            final_idxs = complete_coreset(y, probs=new_sensitivities, selected=idxs_coreset)
            self.resampling_iter = 0

            # 2. If the condition is not met start iterative resampling
            curr_ratio_diff = ratio_diff(new_sensitivities, old_sensitivities, unique(final_idxs), idxs_coreset)
            if curr_ratio_diff > iterative_threshold:
                for i in range(n_iter):
                    # Remove a percent from the coreset and resample.
                    # final_idxs should be the completed coreset here.

                    # Check given sample_per_iter
                    # if isinstance(coreset_size, dict):
                    #     if is_percent(sample_per_iter):
                    #         rest_coreset_size = {c: round(v * sample_per_iter) for c, v in coreset_size.items()}

                    #     elif isinstance(sample_per_iter, dict):
                    #         if all([is_int(s) for s in sample_per_iter.values()]):
                    #             rest_coreset_size = sample_per_iter
                    #         elif all(is_percent(s) for s in sample_per_iter.values()):
                    #             rest_coreset_size = {c: round(v * sample_per_iter) for c, v in coreset_size.items()}
                    #         else:
                    #             raise ValueError(
                    #                 "When `coreset_size` is an dict and `sample_per_iter` is given as a dict it must either contain positive ints or percents"
                    #             )
                    #     else:
                    #         raise ValueError(
                    #             "When coreset_size is a dict, sample_per iter must be either a percent or a dict of ints / percents for each class"
                    #         )
                    # else:
                    #     if is_percent(sample_per_iter):
                    #         rest_coreset_size = round(coreset_size * sample_per_iter)
                    #     elif is_int(sample_per_iter, positive=True):
                    #         rest_coreset_size = sample_per_iter
                    #     else:
                    #         raise ValueError(
                    #             "When `coreset_size` is an int and `sample_per_iter`  must either a percent or int"
                    #         )

                    # rest_min_size = remaining_size(minimum_size, y[final_idxs])

                    # idxs, _ = self.sample(
                    #     X,
                    #     y,
                    #     w=w,
                    #     coreset_size=rest_coreset_size,
                    #     minimum_size=rest_min_size,
                    #     sensitivities=new_sensitivities,
                    # )

                    # Check sample per iter
                    if is_int(sample_per_iter, positive=True):
                        n_replaced = min(coreset_size, sample_per_iter)
                    elif is_percent(sample_per_iter):
                        n_replaced = round(coreset_size * sample_per_iter)
                    # Uniformly replace indexes only if they are better
                    to_replace = np.random.choice(len(final_idxs), n_replaced)
                    remaining_idxs = np.setdiff1d(final_idxs, to_replace)

                    idxs_temp = complete_coreset(y=y, probs=new_sensitivities, selected=remaining_idxs)
                    new_ratio_diff = ratio_diff(
                        new_sensitivities,
                        old_sensitivities,
                        unique(idxs_temp),
                        idxs_coreset,
                    )
                    if new_ratio_diff < curr_ratio_diff:
                        curr_ratio_diff = new_ratio_diff
                        final_idxs = idxs_temp
                    if new_ratio_diff < iterative_threshold:
                        final_idxs = idxs_temp
                        break
                self.resampling_iter = i
        else:
            final_idxs = complete_coreset(y=y, probs=new_sensitivities, selected=idxs_coreset)
            self.resampling_iter = None

        handle_classification = self.is_classification or self._coreset_type == "classification"
        probs = normalize_probs(new_sensitivities)
        idxs_len = final_idxs.shape[0] if final_idxs.ndim == 1 else final_idxs.shape[1]
        weights = np.ones(n_samples, dtype=float)
        prev_weights = w if w is not None else np.ones(n_samples)
        if handle_classification:
            for c in np.unique(y):
                c_idxs = np.where(y == c)[0]
                c_len = len(np.where(y[final_idxs] == c)[0])
                probs_c = normalize_probs(new_sensitivities[c_idxs])
                weights[c_idxs] = prev_weights[c_idxs] / (c_len * probs_c + 1e-20)
        else:
            weights = prev_weights / (idxs_len * probs)

        # Reweight samples sampled more than once and eliminate duplicates
        final_idxs, final_weights = aggregate_and_reweight(idxs=final_idxs, sample_weight=weights)
        _final_ratio_diff = ratio_diff(new_sensitivities, old_sensitivities, final_idxs, idxs_coreset)
        # Change attributes
        self.idxs = final_idxs
        self.weights = final_weights
        self.sensitivities = new_sensitivities
        self.classes = new_classes
        self.counts = new_counts
        self.y_encoded = new_y_encoded
        self._starting_ratio_diff = _starting_ratio_diff
        self._final_ratio_diff = _final_ratio_diff

        return final_idxs, final_weights

    def _encode_classes(self, arr, classes=None):
        """Encode classes array to an integer array using self.classes"""
        if classes is None:
            classes = self.classes
        return LabelEncoder().fit(classes).transform(arr)

    def _decode_classes(self, arr):
        """Decode encoded classes array back to class value"""
        return LabelEncoder().fit(self.classes).inverse_transform(arr)

    def _to_internal_idxs(self, idxs: Optional[np.ndarray], check_missing=False) -> Optional[np.ndarray]:
        """
        Translates input idxs to indices representing the position in self.idxs array.
        When keep_selected_only is True arrays like sensitivities don't include all the data.
        In this case look for idxs in self.idxs and return the corresponding indices.
        """
        if idxs is not None:
            if check_missing and len(np.intersect1d(self.idxs, idxs)) < len(idxs):
                raise RuntimeError("Some of input idxs were not found in self.idxs")
            if self.keep_selected_only:
                idxs = np.where(np.isin(self.idxs, idxs))[0]
        return idxs

    def get_cleaning_samples(
        self,
        size: int = None,
        class_size: Dict[Any, int] = None,
        classes: list = None,
        sample_all: list = None,
        ignore_indices: Iterable = None,
        select_from_indices: Iterable = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return samples with highest sensitivity value.
        For classification coreset it is possible to control how many to return per class.
        sample_all takes higher priority over class_size.
        When size and class_size/sample_all are provided, remaining samples are taken from the rest of the classes.

        Parameters
        ----------
        size: int, optional
            Number of samples to return.

        class_size: dict, optional
            Classification only, Number of samples to return per class.

        sample_all: list optional
            Classification only, classes to return all samples.

        ignore_indices: array-like, optional.
            An array of indices to ignore when selecting cleaning samples.

        classes: array-like, optional.
            classes to consider.

        select_from_indices: array-like, optional.
             An array of indices to include when selecting cleaning samples.

        Returns
        -------
        selected indices and sensitivities

        """
        if (class_size or sample_all or classes) and not self.is_classification:
            raise ValueError("`class_size and sample_all can only be used in classification tasks")

        if class_size:
            class_size = dict(zip(self._encode_classes(list(class_size.keys())), class_size.values()))
        if sample_all:
            sample_all = list(self._encode_classes(sample_all))
        if classes:
            classes = list(self._encode_classes(classes))
        if ignore_indices is not None:
            ignore_indices = np.array(ignore_indices)
        if select_from_indices is not None:
            select_from_indices = np.array(select_from_indices)

        # When only sensitivities of the selected are kept,
        # align ignore_indices/select_from_indices to match the sensitivities array.
        if self.keep_selected_only:
            if select_from_indices is not None:
                select_from_indices = self._to_internal_idxs(select_from_indices)
            if ignore_indices is not None:
                ignore_indices = self._to_internal_idxs(ignore_indices)

        ind = take_important(
            self.sensitivities,
            self.y_encoded,
            size,
            class_size,
            sample_all,
            ignore_indices,
            classes,
            select_from_indices,
        )
        # We want to return the "original indices" and not the relative indices.
        if self.keep_selected_only:
            return self.idxs[ind], self.sensitivities[ind]
        else:
            return ind, self.sensitivities[ind]

    def get_index_weights(self):
        """Returns the indexes and weights

        Returns
        -------
        idxs: array-like of  shape (n_samples, ) of ints
            indexes of the selected samples
        weights: array-like of  shape (n_samples, ) of ints
            weights of the selected samples


        """
        # TODO Should we raise error if the coreset was not built?
        #     raise NotBuiltError(f"This {self.__class__.__name__} is not built yet. Please call `.build` before trying to get the indexes and weights")
        return self.idxs, self.weights

    # def get_y_decoded(self):
    #     """
    #     Get y decoded
    #
    #     Decode the self.y_encoded
    #     -------
    #     """
    #     return self._decode_classes(self.y_encoded)

    def get_y_decoded_selected(self):
        """
        Get y decoded for the selected indices.
        Note that when keep_selected_only os True,
        there is no correlation between the values in self.idx and y_encoded indices.

        Decode the self.y_encoded
        -------
        """
        if self.keep_selected_only:
            return self._decode_classes(self.y_encoded)
        else:
            return self._decode_classes(self.y_encoded)[self.idxs]

    def get_sensitivities_selected(self):
        """
        Get sensitivities for the selected indices.
        -------
        """
        if self.keep_selected_only:
            return self.sensitivities
        else:
            return self.sensitivities[self.idxs]

    def compute_sensitivities(self, X, y=None, w=None):
        """Computes the sensitivities by calling `.sensitivity() and saves them.
        This function must be called before sampling if no sensitivities are provided

        Parameters
        ----------
        X: array-like of shape  (n_samples, n_features)
            features

        y: array-like of shape (n_samples, ), default = None
            labels. Optional

        Returns
        -------
        array-like of shape (n_samples, )
            sensitivities
        """
        self.sensitivities = self.sensitivity(X, y, w) if X.shape[0] > 0 else np.ndarray([])
        return self

    def compute_sample(
        self,
        *,
        coreset_size: Optional[int] = None,
        deterministic_size: Optional[float] = None,
        **sample_kwargs,
    ):
        """Builds the coreset. Calls `.sample()` on the given X, y, w with the parameters
        given in the **sample_kwargs(). Saves the indexes and weights

        Parameters
        ----------
        X: array-like of shape  (n_samples, n_features)
            features

        y: array-like of shape (n_samples, ), default = None
            labels. Optional

        w : array-like of shape(n_samples, ), default=None
            previous weights

        coreset_size: int
            int - number of samples to sample.

        deterministic_size: float, default = None
            The percent of samples to be taken deterministically.

        sample_all: List, default = None,
            Classification only
            Classes in this list will have all samples returned.

        class_size: Dict[Any, int], default = None
            Classification only.
            Number of data instances to sample per class. Classes already in `sample_all` are ignored.

        minimum_size: int | dict, default = None
            Classification only.
            Minimum size per class. Classes common with `class_size` and `sample_all` are ignored

        fair: str, default = 'training'
            Classification only.
            If fairness is to be applied. It will compute the appropiate amount per class.
            It will override the `class_size`.
            It will apply the appropriate fairness_policy_adapter depending on the value (training or cleaning)



        Returns
        -------
        idxs: array-like of shape (coreset_size, ) or (sum(coreset_size), ) if coreset_size is a list.
            Indexes of the selected samples
        weights: array-like of shape (coreset_size, ) or (sum(coreset_size), ) if coreset_size is a list.
            Weights of the selected samples
        """

        # Check coreset_size.
        if coreset_size is not None and not is_int_or_float(coreset_size, positive=True):
            raise TypeError(f"`coreset_size` must be None or a positive int or float, found {coreset_size}")

        self.idxs, self.weights = self.sample(
            coreset_size=coreset_size,
            deterministic_size=deterministic_size,
            **sample_kwargs,
        )
        return self.idxs, self.weights

    def sensitivity(self, X, y=None, w=None) -> np.ndarray:
        raise NotImplementedError

    def set_sensitivities(self, sensitivities):
        self.sensitivities = sensitivities

    @classmethod
    def _check_constraints(
        cls,
        deterministic_size: Optional[float] = None,
        sample_all: Optional[Iterable] = None,
        class_size: Dict[Any, int] = None,
        minimum_size: Union[int, str, Dict[Any, int]] = None,
    ):
        """Checks parameters and returns them.
        Raises Errors on types.
        Warns and sets to None if a parameter is given for a wrong coreset task.

        Returns
            deterministic_size, sample_all, class_size, minimum_size
        """
        # Check constraints against the class type.
        # Warn the user and set them accordingly if some are given badly.
        if cls._coreset_type != "classification":

            def warn_ctype(name, value):
                user_warning(
                    f"`{name}` is not None in coreset with type {cls._coreset_type}. `{name}` has value {value}. It will be set to None"
                )

            if sample_all is not None:
                warn_ctype("sample_all", sample_all)
            checked_sample_all = None
            if class_size is not None:
                warn_ctype("class_size", class_size)
            checked_class_size = None
            if minimum_size is not None:
                warn_ctype("minimum_size", minimum_size)
            checked_minimum_size = None

        else:
            if sample_all is not None and not is_arraylike(sample_all):
                raise TypeError(f"`sample_all` must be an array with class labels. Found {sample_all}")
            checked_sample_all = sample_all

            if class_size is not None and not isinstance(class_size, dict):
                raise TypeError(f"`class_size` must be a dict containing ints. Found {class_size}")
            checked_class_size = class_size

            if minimum_size is not None and not (
                minimum_size == "auto" or is_int(minimum_size, positive=True) or isinstance(minimum_size, dict)
            ):
                raise TypeError(
                    f"`minimum_size` must be 'auto' or a positive int or a dict containing ints. Found {minimum_size}"
                )
            checked_minimum_size = minimum_size

        if deterministic_size is not None and not is_percent(deterministic_size):
            raise TypeError("`deterministic_size` must be a percent")
        checked_deterministic_size = deterministic_size

        return checked_deterministic_size, checked_sample_all, checked_class_size, checked_minimum_size

    def _check_estimation_requirements(self):
        """Checks if it's possible to estimate with the current algorithm, and if the coreset was built with estimation in mind"""
        if self.algorithm not in self._possible_estimators:
            raise ValueError(
                f"For estimation, `algorithm` must be one of {self._possible_estimators}, found {self.algorithm}"
            )
        if self.estimation_params_ is None:
            raise ValueError(
                "No sensitivity information is available for estimation. Compute sensitivities once before."
            )
        if self._estimation_algorithm_used != self.algorithm:
            raise ValueError(
                f"Algorithm mismatch: sensitivity information was computed with `{self._estimation_algorithm_used}', estimation is requested with `{self.algorithm}`."
            )
