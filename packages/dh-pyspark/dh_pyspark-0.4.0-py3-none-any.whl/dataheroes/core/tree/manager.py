import datetime
import gc
import time
from itertools import groupby
from typing import Iterable, Iterator, Callable, Union, Any, List, Tuple, Optional
from uuid import uuid4

import numpy as np
from dataheroes.data.manager import DataManagerBase

from .chunk_layer import ChunkSensitivitiesParams, ChunkLayer
from . import utils
from .tree import CoresetTree, Node
from ...common import ThreadPoolManager


class TreeGroup:
    """
    A collection of trees.

    Attributes:
        coreset_params (Iterable[coresets.base.CoresetParams]): The coreset parameters to use for each tree.
        coreset_cls (Type[coresets.base.Coreset]): The coreset class to use for each tree.
        trees (List[CoresetTree]): The list trees to group.
        group_id (str): The unique identifier for the group.
    """

    def __init__(self, coreset_params, coreset_cls, trees):
        self.coreset_params = coreset_params
        self.coreset_cls = coreset_cls
        self.trees = list(trees)
        self.group_id = uuid4().hex


class TreeManager:
    """
    Manages a group of trees and the chunk layer.

    Attributes:
    -----------
    trees : list of Tree
        A list of trees.
    data_manager : DataManager
        The data manager object used to manage the training data.
    tree_groups : list of TreeGroup
        A list of tree groups that have the same coreset parameters and chunk sizes.
    chunk_size : int
        The chunk size to use for processing data.
    chunk_layer : ChunkLayer
        The chunk layer used to manage the chunks of data.
    """

    def __init__(
            self,
            trees: Iterable[CoresetTree],
            data_manager: DataManagerBase,
            chunk_size=None,
            is_classification=False,
            max_memory_gb: int = None,
            save_all: bool = False,
            chunk_sample_ratio: float = 0,
            chunk_index=None,
    ):

        self.data_manager = data_manager
        self.is_classification = is_classification
        self.trees = list(trees)
        self.max_memory_gb = max_memory_gb
        self.save_all = save_all
        self.chunk_sample_ratio = chunk_sample_ratio
        # Group trees
        self.tree_groups: List[TreeGroup] = self._group_trees(self.trees)
        self.chunk_size = self.tree_groups[0].trees[0].chunk_size if chunk_size is None else chunk_size
        self.chunk_index = chunk_index
        self._init_chunk_layer()

    def set_buffer(self, buffer: Union[List[np.ndarray], Tuple[np.ndarray]] = None):
        """
        set tree's internal buffer of unhandled instances

        Parameters
        ----------
        buffer: list of numpy ndarrays

        Returns
        -------

        """
        self.chunk_layer.set_buffer(buffer)

    def _init_chunk_layer(self):
        """
        Initializes the chunk layer object.
        """

        chunk_params = [ChunkSensitivitiesParams(
            coreset_params=g.coreset_params,
            coreset_cls=g.coreset_cls,
            chunk_id=g.group_id
        ) for g in self.tree_groups]
        self.chunk_layer = ChunkLayer(
            chunk_size=self.chunk_size,
            parent=self,
            data_manager=self.data_manager,
            chunk_coreset_params=chunk_params,
            chunk_index=self.chunk_index,
        )

        for tree in self.trees:
            tree.chunk_layer = self.chunk_layer

    def update_chunks_params(self, chunk_size, coreset_size=None):
        self.chunk_size = chunk_size
        if self.chunk_layer:
            self.chunk_layer.chunk_size = chunk_size
        if self.trees:
            for tree in self.trees:
                tree._update_chunks_params(chunk_size=chunk_size, coreset_size=coreset_size)

    def _group_trees(self, trees) -> List[TreeGroup]:
        """
        Groups trees by the same parameters and chunk sizes.

        Parameters:
        -----------
        trees : list of Tree
            A list of trees.

        Returns:
        --------
        tree_groups : list of TreeGroup
            A list of tree groups that have the same coreset parameters and chunk sizes.
        """
        chunk_sizes = [tree.chunk_size for tree in trees]
        if not all(x == chunk_sizes[0] for x in chunk_sizes):
            raise TypeError("All trees must have the same `chunk_size`")

        tree_groups = []

        def key_f(x):
            return tuple(sorted([z for z in x.coreset_params.items() if z[1]])), x.coreset_cls

        groups = groupby(sorted(trees, key=key_f), key=key_f)
        for (coreset_params, coreset_cls), group in groups:
            coreset_params = dict(coreset_params)
            tree_groups.append(TreeGroup(coreset_params, coreset_cls, group))
        return tree_groups

    def _group_add_leaf(self, chunk_node, group, coreset, random_chunk_data_indices, leaf_index=None):
        """
           Adds a new leaf node to each tree in the given group, using the provided chunk_node and coreset.

           Parameters:
               chunk_node (ChunkNode): The chunk node to be added to each tree.
               group (TreeGroup): The group of trees that the chunk_node should be added to.
               coreset (coresets.Coreset): The coreset to be used when adding the chunk_node.
                partial (bool): Partial build or full build.

           Returns:
               None
        """
        # MARK: Build Trees over leaf
        for tree in group.trees:
            if chunk_node.is_buffer():
                tree.add_buffer_node(chunk_node, coreset, random_chunk_data_indices)
            else:
                tree.add_leaf(chunk_node, coreset, random_chunk_data_indices, leaf_index)

    def _group_rebuild_leaf(self, chunk_node, group, coreset, force_resample_all, force_sensitivity_recalc):
        """
       Rebuild leaf node to each tree in the given group, using the provided chunk_node and coreset.
       """
        for tree in group.trees:
            min_level, min_level_full = tree._get_actual_levels_for_update(force_sensitivity_recalc, force_resample_all)
            tree.rebuild_leaf(chunk_node, coreset, min_level, min_level_full)

    def _take_random_sample(self, chunk_indices, chunk_sample_ratio=0.0):
        """
        Generates a random subsample from a chunk, based on the indices.

        Parameters
        ----------
        chunk_indices: np.array
            An array of indices representing data instances from the chunk.
        chunk_sample_ratio: float
            The relative size of the random sample (0- 0%, ..., 1- 100%)

        Returns
        -------
        The indices of the random sample (as np.array)

        """
        if chunk_sample_ratio > 0.0 and chunk_sample_ratio < 1.0:
            rng = np.random.default_rng()
            chunk_data_size = len(chunk_indices)
            random_sample_size = int(chunk_sample_ratio * chunk_data_size)
            if random_sample_size < 1:
                random_sample_size = 1
            random_chunk_data_indices = rng.choice(
                chunk_indices,
                size=random_sample_size,
                replace=False,
                shuffle=False)
            return random_chunk_data_indices
        elif chunk_sample_ratio == 1.0:
            return chunk_indices
        else:
            return np.array([])

    def _print_missing_stats(self, removed_rows_stats):
        for group in self.tree_groups:
            n_instances = group.trees[0].get_tree_sum_build_indexes()
            if len(removed_rows_stats[group.group_id]) > 0:
                print(f"Total number of rows with missing values: "
                      f"{len(removed_rows_stats[group.group_id]) / n_instances:.2%}")
            break

    def build(self, datasets: Iterator = None):
        """
        Builds the trees in this TreeGroupManager using the provided datasets.

        Parameters:
            datasets (list): A list of datasets to be used when building the trees.
            partial (bool): Partial build or full build.
        Returns:
            None
        """
        build_start_time = time.time()
        if self.data_manager.n_jobs is not None and self.data_manager.n_jobs > 1:
            ThreadPoolManager().restart_executor(max_workers=self.data_manager.n_jobs)
        removed_rows_stats = {tree_group.group_id: np.array([], dtype=int) for tree_group in self.tree_groups}
        removed_cols_stats = {tree_group.group_id: [] for tree_group in self.tree_groups}

        def after_create_leaf_node(added_chunk_node, leaf_node_index):
            # This function gets called after the chunk layer finishes processing.
            # In this function we build the rest of the trees from each group over the leaf layer.
            random_sample_indices = self._take_random_sample(added_chunk_node.dset.ind, self.chunk_sample_ratio)
            for coreset in added_chunk_node.coresets:
                for group in self.tree_groups:
                    if coreset.params.chunk_id == group.group_id:
                        self._group_add_leaf(
                            added_chunk_node,
                            group,
                            coreset,
                            random_sample_indices,
                            leaf_node_index,
                        )
                        # append the indices of the removed rows to the stats but keep only unique indices
                        removed_rows_stats[group.group_id] = np.concatenate([removed_rows_stats[group.group_id], coreset.removed_rows])
                        removed_cols_stats[group.group_id].append(coreset.n_features)
            if len(random_sample_indices) > 0:
                added_chunk_node.add_indices(random_sample_indices)
            if self.data_manager.n_jobs is not None and self.data_manager.n_jobs > 1:
                with ThreadPoolManager().dm_lock:
                    added_chunk_node.save(self.data_manager, save_all=self.save_all)
                    # call to gc collect to remove the (other) added_chunk_node objects from memory
                    gc.collect()
            else:
                added_chunk_node.save(self.data_manager, save_all=self.save_all)

        chunk_nodes = self.chunk_layer.process(dsets=datasets,
                                               create_buffer=True,
                                               is_classification=self.is_classification,
                                               after_create_leaf_node=after_create_leaf_node
                                               )
        if self.data_manager.verbose > 0:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Build Started.")
        # MARK: Build Leaf layer.
        # we should iterate through chunk_nodes to run build
        for _ in chunk_nodes:
            pass

        if self.data_manager.n_jobs is not None and self.data_manager.n_jobs > 1:
            ThreadPoolManager().wait_until_empty()
        # Trigger telemetry and licence check
        for tree in self.trees:
            current_group = [x for x in self.tree_groups if tree in x.trees][0]
            stats = removed_rows_stats[current_group.group_id]
            stats = f"{len(stats) / tree.get_tree_sum_build_indexes():.2%}" if len(stats) > 0 else "0%"
            col_stats = removed_cols_stats[current_group.group_id]
            col_stats_str = f"Min cols: {min(col_stats)}, Max cols: {max(col_stats)}, " \
                            f"Avg: {sum(col_stats) / len(col_stats)}" if col_stats else ""

            tree.finish_build(self.chunk_layer.build_params, stats, col_stats_str)

        self._print_missing_stats(removed_rows_stats)
        self.data_manager.commit()
        if self.data_manager.verbose > 0:
            built_time = str(datetime.timedelta(seconds=round(time.time() - build_start_time, 3))).rstrip('0')
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Build Completed in: {built_time}.")

    def _mark_samples_on_trees(self, indices: Iterable, force_resample_all, force_sensitivity_recalc,
                               is_removing: bool = False, ):
        for tree in self.trees:
            if tree.is_optimized_for_cleaning and force_resample_all is None:
                force_resample_all = -1
            tree._mark_samples_on_tree(indices=indices,
                                       is_removing=is_removing,
                                        force_resample_all=force_resample_all,
                                        force_sensitivity_recalc=force_sensitivity_recalc,
                                       )

    def _get_dirty_chunks(self):
        return list(
            {node.chunk_node_id for tree in self.trees for node in tree.get_dirty_leaves(True) if node.chunk_node_id})

    def _get_chunks_ids(self, with_buffer):
        return {node.chunk_node_id for tree in self.trees for node in tree.get_leaves(with_buffer=with_buffer)}

    def _should_rebuild_chunks(self, force_resample_all: Optional[int], force_sensitivity_recalc: Optional[int],
                               force_do_nothing: Optional[bool]):
        if force_do_nothing:
            return False

        # If the trees were built with sample_weight, don't rebuild chunks since sample_weight were not saved
        for tree in self.trees:
            if any([node.weighted_leaf for node in tree.tree[0]]):
                return False

        # if not self.save_all:
        #     return False
        for tree in self.trees:
            actual_min_level, actual_min_full_level = tree._get_actual_levels_for_update(
                force_resample_all=force_resample_all,
                force_sensitivity_recalc=force_sensitivity_recalc
            )
            if min(actual_min_level, actual_min_full_level) == 0:
                return True
        return False

    def _remove(self, indices):
        # Remove in the dataManager
        self.data_manager.remove(indices)

    def _replace(self, indices, X=None, y=None):
        # Replace in the dataManager
        self.data_manager.replace(indices, X=X, y=y)
        # Update buffer
        self.chunk_layer.update_buffer(indices, X=X, y=y)

    def _rebuild_leaves(self, force_resample_all, force_sensitivity_recalc):

        # Have the trees mark dirty nodes
        chunk_ids = self._get_dirty_chunks()
        # Rebuild dirty chunks
        chunk_nodes = self.chunk_layer.rebuild(chunk_ids)
        for chunk_node in chunk_nodes:
            for coreset in chunk_node.coresets:
                for group in self.tree_groups:
                    if coreset.params.chunk_id == group.group_id:
                        self._group_rebuild_leaf(chunk_node, group, coreset, force_resample_all,
                                                 force_sensitivity_recalc)
            if chunk_node.is_buffer():
                chunk_node.save(self.data_manager, save_all=self.save_all)

    def _update(self, force_resample_all, force_sensitivity_recalc, force_do_nothing):
        if force_do_nothing:
            return

        # Rebuild leaves if needed
        if self._should_rebuild_chunks(force_resample_all, force_sensitivity_recalc, force_do_nothing):
            self._rebuild_leaves(force_resample_all, force_sensitivity_recalc)

        # update trees
        for tree in self.trees:
            if tree.is_optimized_for_cleaning and force_resample_all is None:
                force_resample_all = -1
            tree._update(
                force_resample_all=force_resample_all,
                force_sensitivity_recalc=force_sensitivity_recalc,
                update_leaves=False
            )

    def update_targets(
            self,
            indices: Iterable,
            y: Iterable,
            force_resample_all: Optional[int],
            force_sensitivity_recalc: Optional[int],
            force_do_nothing: Optional[bool],
    ):
        """
        Updates the targets in the data-manager, the buffer and rebuild trees if needed
        """

        # Update samples
        self._replace(indices, y=y)

        # Mark dirty flag in all trees
        self._mark_samples_on_trees(indices, force_resample_all=force_resample_all,
                                    force_sensitivity_recalc=force_sensitivity_recalc)

        # Update trees and chunks
        self._update(force_resample_all, force_sensitivity_recalc, force_do_nothing)

    def update_features(
            self,
            indices: Iterable,
            X: np.ndarray,
            feature_names: Iterable,
            force_resample_all: Optional[int],
            force_sensitivity_recalc: Optional[int],
            force_do_nothing: Optional[bool],
    ):
        """
        Update features in the data-manager and in the buffer and then update all trees.
        """

        X = utils.process_features(X, self.data_manager, feature_names)

        # Update samples
        self._replace(indices, X=X)

        # Mark dirty flag in all trees
        self._mark_samples_on_trees(indices, force_resample_all=force_resample_all,
                                    force_sensitivity_recalc=force_sensitivity_recalc)

        # Update trees and chunks
        self._update(force_resample_all, force_sensitivity_recalc, force_do_nothing)

    def remove_samples(
            self,
            indices: Iterable,
            force_resample_all: Optional[int],
            force_sensitivity_recalc: Optional[int],
            force_do_nothing: Optional[bool]
    ):
        """
        Remove samples from all trees
        """

        # send telemetry for all trees (TODO: maybe send only for the first tree)
        # and removes the indices from the random samples
        for tree in self.trees:
            tree._samples_removed_telemetry_send(indices)
            tree._remove_random_sample_indices(indices)

        # Add indices to the removed indices list
        self._remove(indices)

        # Mark dirty flag in all trees
        self._mark_samples_on_trees(indices, is_removing=True,
                                    force_resample_all=force_resample_all,
                                    force_sensitivity_recalc=force_sensitivity_recalc)

        # Update trees and chunks
        self._update(force_resample_all, force_sensitivity_recalc, force_do_nothing)

    def remove_nodes(self, node_idxs: List[tuple]) -> None:
        # Get chunk ids of nodes.
        nodes = [list(self.trees)[0]._get_node(*node_idx, root_zero=False) for node_idx in node_idxs]
        chunk_node_ids = [node.chunk_node_id for node in nodes]
        # remove nodes from DataManager
        self.data_manager.remove_nodes(chunk_node_ids)

        # remove nodes from all trees.
        for tree in self.trees:
            tree.remove_nodes(node_idxs)

    def filter_out_samples(
            self,
            filter_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]],
            force_resample_all,
            force_sensitivity_recalc,
            force_do_nothing
    ):
        """
        Filter out samples in all trees.
        1. Fetch each chunk from the data manager and apply the filter function to get the indices to be excluded.
        2. Apply filtering also on the buffer in memory.
        3. Use the remove_samples method to apply the remove.
        """
        chunk_ids = self._get_chunks_ids(True)
        indices_for_remove = self.chunk_layer.filter_out_samples(filter_function, chunk_ids)
        self.remove_samples(
            indices_for_remove,
            force_resample_all=force_resample_all,
            force_sensitivity_recalc=force_sensitivity_recalc,
            force_do_nothing=force_do_nothing
        )

    def update_dirty(self, force_resample_all: Optional[int] = None, force_sensitivity_recalc: Optional[int] = None):
        self._update(force_resample_all, force_sensitivity_recalc, False)

    def is_dirty(self):
        if self.trees:
            return any(tree.is_dirty() for tree in self.trees)
        return False

    def get_max_level(self):
        if self.trees:
            return max(tree.get_max_level() for tree in self.trees)
        else:
            return 0

    def update_build_params(self):
        if self.chunk_layer.chunk_size is not None:
            # -1, 0, regular
            return

        try:
            # in case chunk_layer.chunk_corset_params is None or not iterable, or coreset_params is None
            dtype = next(iter(self.chunk_layer.chunk_coreset_params)).coreset_params.get("dtype", "float32")
        except Exception:
            dtype = 'float32'

        chunk_size, coreset_size_tree_type, _ = utils.calc_chunks_params(
            chunk_size=self.chunk_size,
            coreset_size=None,
            n_instances=self.data_manager.n_instances,
            buffer_size=self.chunk_layer.get_buffer_size(),
            n_features=self.data_manager.n_features_expected,
            n_classes=self.data_manager.n_classes,
            max_memory_gb=self.max_memory_gb,
            dtype=dtype
        )
        self.update_chunks_params(chunk_size, coreset_size_tree_type["training"])
