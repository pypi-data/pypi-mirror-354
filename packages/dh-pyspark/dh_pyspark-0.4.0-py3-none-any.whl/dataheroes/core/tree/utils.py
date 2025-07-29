from typing import Iterable, Tuple, Optional, Union

import numpy as np
import psutil

from dataheroes.core.common import default_coreset_size

DATA_CELLS_PER_GB = 60_000_000
DATA_CELLS_PER_GB_BUILD_FLOAT64 = 30_000_000
NODES_IN_PARALLEL = 4
MAX_MEMORY_RATIO = 0.8
LEVEL_COMPENSATE_COEFFICIENT = 1.1


def evaluate_max_batch_size(
        n_features: int,
        max_memory_gb: Union[int, float] = None,
        available: bool = False,
        dtype: str = 'float32'
):
    """
    Memory consideration, compute the maximum recommended batch size to load into memory,
    considering the overall memory requires for building a tree.

    Parameters
    ----------
    n_features: int
        number of features or columns

    max_memory_gb: int, optional
        The maximum memory in GB that should be used.
        When not provided, the 80% of the total server memory is considered.

    available: bool, optional
        Flag to calculate based on the available memory, by default the total memory is taken into the calculation.

    dtype: str, optional
        float32 or float64 flag for data cells memory calculation

    Returns
    -------
    int: maximum batch size to use when loading data to memory.
    """
    cell_per_gb = DATA_CELLS_PER_GB if dtype == 'float32' else DATA_CELLS_PER_GB_BUILD_FLOAT64
    if not max_memory_gb:
        max_memory_gb = (psutil.virtual_memory().available if available else psutil.virtual_memory().total) / 2 ** 30
    max_allowed_data_cells = int(max_memory_gb * MAX_MEMORY_RATIO * cell_per_gb)
    max_batch_size = max_allowed_data_cells // n_features
    return int(max_batch_size)


def evaluate_batch_to_memory(batch_size: int, n_features: int, dtype: str = 'float32'):
    # translate batch size x features to GB required
    cell_per_gb = DATA_CELLS_PER_GB if dtype == 'float32' else DATA_CELLS_PER_GB_BUILD_FLOAT64
    return (batch_size * n_features) // cell_per_gb


def evaluate_coreset_params(
        *,
        n_instances: int,
        n_features: int,
        n_classes: Optional[int] = None,
        max_memory_gb: int = None,
        tree_allowed: bool = True,
        dtype: str = 'float32'
):
    """
    Calculate required CoresetTree parameters.
    See https://docs.google.com/document/d/1JhYXFKM12W4j_Swstc7A1FoGXtP24bN4LSt7Z4lOiss/edit
    Parameters
    ----------
    n_instances: int
        The total number of instances that are going to be processed.
    n_features: int
        Number of features
    n_classes: int
        Total number of classes (labels)
    max_memory_gb: int, optional
        The maximum memory in GB that should be used.
        When not provided, 80% of the total server memory is considered.
    tree_allowed: bool, optional, default True
        when false, the result will not consider the tree and will ignore memory limitation
    optimized_for: str or list of str
        Either 'training', 'cleaning' or or both ['training', 'cleaning'].
        The main usage of the service.
    dtype: str, optional, default float32
        dtype for sensitivity and memory calculations
    Returns
    -------
    dict
        chunk_size: int or None
        coreset_size_tree_type: dict, {'training':coreset_size_training, 'cleaning':coreset_size_cleaning}
        is_tree: indicate if a tree is required to meet the requirements
    """

    # Calculate coreset_size and chunk_size, ignoring memory restriction.
    chunk_size = None
    default_coreset_size_dict = default_coreset_size(
        n_classes,
        n_features,
        n_instances)
    coreset_size = default_coreset_size_dict.get('coreset_size')
    coreset_size_from_formula = default_coreset_size_dict.get('coreset_size_from_formula')
    coreset_size_after_min_max = coreset_size

    # When tree is not allowed, we just return the coreset_size
    if not tree_allowed:
        return dict(coreset_size_tree_type={'training': coreset_size, 'cleaning': coreset_size}, is_tree=False)

    # coreset size is calculated in default_coreset_size and maybe 0 if n_instances is 0
    k = int(np.log2(n_instances/(coreset_size if coreset_size > 0 else 1)) - 2)

    # Create a tree only when the chunk_size will be at most n_instances//4 (the tree has at least 4 chunks/leaves).
    if k <= 1:
        is_tree = False
        chunk_size_from_formula, chunk_size = int(n_instances), int(n_instances)
    else:
        is_tree = True
        # try to build tree with 4 leaf nodes only
        chunk_size_from_formula = n_instances // 4
        chunk_size = chunk_size_from_formula

    # Apply memory restriction if needed
    if max_memory_gb is None:
        max_memory_gb = int(psutil.virtual_memory().total / 2 ** 30)

    cell_per_gb = DATA_CELLS_PER_GB if dtype == 'float32' else DATA_CELLS_PER_GB_BUILD_FLOAT64

    max_allowed_data_cells = int(max_memory_gb * MAX_MEMORY_RATIO * cell_per_gb)
    max_chunk_size = max_allowed_data_cells // n_features
    max_chunk_size_for_tree = max_chunk_size // NODES_IN_PARALLEL
    if is_tree:
        if chunk_size > max_chunk_size_for_tree:
            coreset_size, chunk_size = _default_chunk_coreset_sizes_max_memory(
                n_instances, max_chunk_size_for_tree, coreset_size)
    else:
        if n_instances > max_chunk_size:
            is_tree = True
            coreset_size, chunk_size = _default_chunk_coreset_sizes_max_memory(
                n_instances, max_chunk_size_for_tree, coreset_size)

    # For cleaning, coreset_size should be at least chunk_size // 4
    coreset_size_tree_type = {}
    effective_chunk_size = chunk_size if chunk_size else n_instances
    coreset_size_tree_type['cleaning'] = max(effective_chunk_size // 4, coreset_size)
    if is_tree:
        # increase coreset_size for each additional level (besides root) of the tree
        # in order to compensate decreasing from level to level
        # but still coreset size should be <= chunk_size // 2
        n_level_add = int(np.log2(n_instances // chunk_size))
        coreset_size_tree_type['training'] = min(int(coreset_size * (LEVEL_COMPENSATE_COEFFICIENT ** n_level_add)),
                                                 chunk_size // 2)
    else:
        coreset_size_tree_type['training'] = coreset_size

    return dict(
        chunk_size=chunk_size,
        coreset_size_tree_type=coreset_size_tree_type,
        is_tree=is_tree,
        max_chunk_size=max_chunk_size,
        max_chunk_size_for_tree=max_chunk_size_for_tree,
        coreset_size_from_formula=coreset_size_from_formula,
        chunk_size_from_formula=chunk_size_from_formula,
        coreset_size_after_min_max=coreset_size_after_min_max,
        max_memory_gb=max_memory_gb
    )


def _default_chunk_coreset_sizes_max_memory(
        n_instances: int,
        max_chunk_size_for_tree: int,
        current_coreset_size: int = None) -> Tuple[int, int]:
    """
    Calculate coreset size and chunk size when the initial chunk size exceed memory limit.

    Parameters
    ----------
    n_instances: int
        The total number of instances that are going to be processed.
    max_chunk_size_for_tree: int
        The maximum chunk size

    Returns
    -------
    coreset_size: int
    chunk_size: int

    """
    # try to create balanced tree with minimal possible number of leaf nodes
    k = int(n_instances // max_chunk_size_for_tree).bit_length()
    chunk_size = n_instances // 2**k
    coreset_size = chunk_size // 2
    if current_coreset_size is not None:
        coreset_size = min(coreset_size, current_coreset_size)
    return coreset_size, chunk_size


def process_features(
        X: np.ndarray,
        data_manager,
        feature_names: Iterable
) -> np.ndarray:
    """
    Process features, replace the features in the data with the features in the data manager.

    Parameters
    ----------
    X: np.ndarray
        The data to process
    data_manager: DataManager
        The data manager to use
    feature_names: Optional[List[str]]
        The names of the features to replace

    Returns
    -------
    np.ndarray
        The processed data

    """
    if feature_names is not None:
        feature_names = list(feature_names)
        assert X.shape[1] == len(feature_names)

    X_processed = X
    if feature_names is not None:
        features_mask = np.isin(np.array([f.name for f in data_manager.data_params.features]), feature_names)
        replace_index = 0
        for i, do_replace in enumerate(features_mask):
            if do_replace:
                X_processed[::, i] = X[::, replace_index]
                replace_index += 1

    return X_processed


def is_simple_chunk_size(chunk_size):
    return chunk_size is not None and chunk_size > 0


def calc_chunks_params(
    *,
    chunk_size,
    coreset_size,
    is_mutable_coreset_size=None,
    n_instances,
    buffer_size,
    n_features,
    n_classes,
    max_memory_gb,
    dtype,
    return_calculated_data=False,
    class_size_exists: bool = False,
):

    if is_mutable_coreset_size is None:
        is_mutable_coreset_size = True

    if chunk_size is None and not n_instances:
        raise RuntimeError("Either `n_instances` or (`chunk_size` and `coreset_size`) must be provided to the service.")

    # calculate n_instances
    n_instances = n_instances or 0
    if buffer_size:
        n_instances = max(n_instances, buffer_size)

    if not n_instances:
        raise RuntimeError("Either `n_instances` or (`chunk_size` and `coreset_size`) must be provided to the service.")

    tree_allowed = chunk_size != -1

    data = evaluate_coreset_params(
        n_instances=n_instances,
        n_features=n_features,
        n_classes=n_classes,
        max_memory_gb=max_memory_gb,
        tree_allowed=tree_allowed,
        dtype=dtype
    )

    # When chunk_size is provided, coreset_size is also required and no further action are needed
    if is_simple_chunk_size(chunk_size) or chunk_size == 0:
        # check if any given coreset size is None or any tree type coreset size is None
        if not class_size_exists and (
            coreset_size is None or (isinstance(coreset_size, dict) and not all(coreset_size.values()))
        ):
            raise RuntimeError("`coreset_size` must be provided")
        if return_calculated_data:
            return chunk_size, {'training': coreset_size, 'cleaning': coreset_size}, False, data
        else:
            return chunk_size, {'training': coreset_size, 'cleaning': coreset_size}, False

    # only set coreset_size
    if is_mutable_coreset_size or is_mutable_coreset_size is None:
        coreset_size_tree_type = data['coreset_size_tree_type']
    else:
        coreset_size_tree_type = {'training': coreset_size, 'cleaning': coreset_size}
    if data['is_tree']:
        chunk_size = data['chunk_size']
        is_mutable_coreset_size = False

    if return_calculated_data:
        return chunk_size, coreset_size_tree_type, is_mutable_coreset_size, data
    else:
        return chunk_size, coreset_size_tree_type, is_mutable_coreset_size


def get_parent_nodes_for_leaf(leaf_factor, leaf_index):
    def _get_tree_by_n_leaves(n_leaves):
        result_tree = [[]]
        for i in range(n_leaves):
            result_tree[0].append(i)
            lvl = 0  # Level
            # add new root if needed
            if len(result_tree[0]) == leaf_factor ** len(result_tree):
                result_tree.append([])
            # create father for each layer if it's full
            while len(result_tree[lvl]) % leaf_factor == 0:
                father_level = lvl + 1
                result_tree[father_level].append(len(result_tree[father_level]))
                lvl += 1
        return result_tree

    # leaf_index starts with 0
    tree_old = _get_tree_by_n_leaves(leaf_index)
    tree_new = _get_tree_by_n_leaves(leaf_index + 1)
    new_nodes = []
    for level_idx, level in enumerate(tree_new):
        if level_idx > 0:
            if level_idx + 1 > len(tree_old):
                new_nodes += [(level_idx, node_idx) for node_idx in tree_new[level_idx]]
            else:
                new_nodes += [(level_idx, node_idx) for node_idx in tree_new[level_idx]
                              if node_idx not in tree_old[level_idx]]
    return new_nodes
