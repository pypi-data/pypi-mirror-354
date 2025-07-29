import numpy as np
from dataheroes.core.numpy_extra import unique_2d_hash


def align_arrays_by_key(left_arrays, right_arrays, ):
    """
    Align right_arrays based on left_arrays
    First element in each arrays is the join key
    Result includes only items that exists both in left and in right
    Result is sorted according to the left arrays
    It is assumed that all keys in right_arrays exist in left_arrays (TODO: make it work for both sides)

    Parameters
    ----------
    left_arrays
    right_arrays

    Returns
    -------

    """
    left_key = left_arrays[0]
    right_key = right_arrays[0]
    if right_key.shape[0] != left_key.shape[0]:
        if right_key.dtype.hasobject or left_key.dtype.hasobject:
            indices_set = set(right_key)
            active_indices = [v in indices_set for v in left_key]
        else:
            active_indices = np.isin(left_key, right_key)
        left_arrays = [arr[active_indices] for arr in left_arrays]
        left_key = left_arrays[0]

    indices_val_to_idx = {val: idx for idx, val in enumerate(right_key)}
    indices_pos_by_ind = [indices_val_to_idx.get(val) for val in left_key]

    right_arrays = [arr[indices_pos_by_ind] if arr is not None else None for arr in right_arrays]
    return tuple(left_arrays), tuple(right_arrays)


def is_nested_params(params):
    """
    Check if params is a nested dictionary with the keys 'training' and/or 'cleaning'
    """
    if isinstance(params, dict) and set(params.keys()) <= {'training', 'cleaning'}:
        return True
    return False


def unpack_params(params, optimized_for, params_class=None, default=None):
    """
    Unpack params if it is a nested dictionary with the keys 'training' and/or 'cleaning'
    """
    def wrap(x):
        return params_class(**x) if params and params_class and isinstance(params, dict) \
            and isinstance(x, dict) else x

    final_params = dict()

    for op_for in optimized_for:
        current_default = default or params_class() if params_class else None
        if is_nested_params(params):
            final_params[op_for] = wrap(params.get(op_for, current_default))
        else:
            final_params[op_for] = wrap(params) or current_default
    return final_params


def aggregate_children(X, w):
    _, idx, inv, _ = unique_2d_hash(X, return_inverse=True, return_counts=True, return_index=True)
    w_agg = np.bincount(inv, weights=np.array(w, dtype=np.float64))
    mask = np.argsort(w_agg)[::-1]
    idx_sorted = idx[mask]
    w_sorted = w_agg[mask]
    return idx_sorted, w_sorted