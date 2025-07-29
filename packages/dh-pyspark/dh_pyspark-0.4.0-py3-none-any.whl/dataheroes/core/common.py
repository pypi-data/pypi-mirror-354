from typing import Iterable, Union, Optional
import numpy as np


def to_ndarray(arr: Iterable):
    if arr is not None and not isinstance(arr, np.ndarray):
        arr = np.array(arr)
    return arr


def get_class_represents_weighted(sum_orig_weights, class_weight):
    if class_weight:
        return sum([sum_orig_weights[class_label] * class_weight.get(class_label, 1.0) for class_label in sum_orig_weights])

    return sum(sum_orig_weights.values())


def weight_processing(
    w: Iterable,
    sum_orig_weights: Union[dict, int],
    y=None,
    class_weight=None,
    is_classification=False,
    inverse_class_weight=False,
):
    """
    Weights normalization and inversions (if necessary).
    If is_classification=True, n_represents should be dict
    """
    if is_classification:
        sum_orig_weights_total = get_class_represents_weighted(sum_orig_weights, class_weight)
    else:
        sum_orig_weights_total = sum_orig_weights

    w = w * sum_orig_weights_total / w.sum()

    if is_classification and inverse_class_weight and class_weight is not None:
        # Adjust weights with the inverse of what was provided
        cw = np.array([class_weight.get(yi, 1.0) for yi in y])
        w = w / cw

    return w


def default_coreset_size(n_classes: Optional[int], n_features: int, n_instances: int) -> dict:
    """
    Computes the default coreset size- see https://docs.google.com/document/d/1JhYXFKM12W4j_Swstc7A1FoGXtP24bN4LSt7Z4lOiss/edit.

    Parameters
    ----------
    n_classes: int (can be None)
        number of classes

    n_features: int
        number of features or columns

    n_instances: int
        number of instances

    Returns
    -------
    int: coreset size.
    """
    n_classes = n_classes or 2
    if n_classes < 2:
        n_classes = 2
    coreset_size_from_formula = int(n_classes*(19*(n_features+2)*np.log(n_classes) + np.log(n_instances)))
    # The coreset size can not be below 1% of the dataset size
    coreset_size_min = int(0.01*n_instances)
    coreset_size = max(coreset_size_from_formula, coreset_size_min)
    # The coreset size can not be bigger than 30% of the dataset size
    coreset_size_max = int(0.3 * n_instances)
    coreset_size = min(coreset_size, coreset_size_max)
    return {
        'coreset_size': coreset_size,
        'coreset_size_from_formula': coreset_size_from_formula,
        'coreset_size_min': coreset_size_min,
        'coreset_size_max': coreset_size_max,
    }
