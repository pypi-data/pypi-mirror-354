import itertools
import time
from dataclasses import dataclass
from typing import Iterable, Union, Optional, Any, List, Tuple, Iterator
from uuid import uuid4

import numpy as np

from dataheroes.utils import colored
from .utils import evaluate_max_batch_size
from ..coreset._base import CoresetBase
from ..helpers import align_arrays_by_key
from ..numpy_extra import filter_missing_and_inf
from ...data.common import Dataset
from ...data.manager import DataManagerT
from . import utils
from ...data.data_auto_processor import DataAutoProcessor
from ...common import ThreadPoolManager

BUFFER_NODE_ID = 'buffer'


@dataclass
class ChunkSensitivitiesParams:
    coreset_params: dict = None
    coreset_cls: Any = None
    coreset_size: int = 10
    chunk_id: Any = None


@dataclass
class ChunkSensitivities:
    coreset: dict = None
    params: ChunkSensitivitiesParams = None
    removed_rows: np.ndarray = None
    n_features: int = None


def exclude_removed(removed, indices, dataset=None):
    """
    Exclude removed indices from the given indices and dataset.

    Args:
        removed: A list or array-like object containing the indices to be removed.
        indices: The original indices from which to exclude the removed indices.
        dataset: A tuple or list containing arrays or None representing the dataset.

    Returns:
        Tuple: A tuple containing the updated indices and the updated dataset (if provided).

    The function creates a mask to exclude the removed indices from the given indices. If a dataset is provided,
    it applies the mask to the dataset, updating the corresponding arrays.

    If no dataset is provided, only the indices are returned.

    Example:
        removed = [2, 5, 7]
        indices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        dataset = (array1, array2, array3)  # Arrays representing the dataset

        new_indices, new_dataset = exclude_removed(removed, indices, dataset)

        # new_indices: [1, 3, 4, 6, 8, 9]
        # new_dataset: (updated_array1, updated_array2, updated_array3)
    """

    mask = None
    if removed is not None and len(removed) > 0:
        mask = ~np.isin(indices, removed)
        if np.any(mask):
            indices = indices[mask]
    if dataset is not None:
        if mask is not None:
            dataset = Dataset(*[arr[mask] if arr is not None else None for arr in dataset])
        return indices, dataset

    return indices


class ChunkNode:
    """
    A class for creating chunk nodes.

    Parameters
    ----------
    dset : Dataset
        The dataset to build the coreset from.
    params : Iterable[ChunkSensitivitiesParams]
        A list of parameters to build the coreset.
    node_id : str, optional
        A unique identifier for the node, by default None.
    """

    def __init__(self,
                 dset: Dataset,
                 params: Iterable[ChunkSensitivitiesParams],
                 node_id=None,
                 tree_build_params: dict = None,
                 data_manager: DataManagerT = None,
                 ):
        self.params = list(params)
        self.dset = dset
        self.node_id = node_id or uuid4().hex
        self.tree_build_params = tree_build_params
        self.indices = np.array([], dtype=int)
        self.sensitivities = []
        self.coresets: List[ChunkSensitivities] = []
        self.data_manager = data_manager

    def is_empty(self):
        """
        Returns True if there is no data in the ChunkNode
        """
        return len(self.dset.X) == 0

    def is_buffer(self):
        """
        Returns True if the node_id is the BUFFER_NODE_ID.
        """
        return self.node_id == BUFFER_NODE_ID

    def build(self):
        """
        Builds the coreset.

        Returns
        -------
        ChunkNode
            The ChunkNode object.
        """
        for cor_params in self.params:
            coreset_params = cor_params.coreset_params or {}
            coreset = cor_params.coreset_cls(**coreset_params)
            if self.is_buffer():
                coreset.safe_mode = True
            cat_encoding_config = self.data_manager.cat_encoding_config_clear()
            class_weights = None
            if cor_params.coreset_params:
                class_weights = cor_params.coreset_params.get("class_weight", None)
            dap = DataAutoProcessor(
                X=self.dset.X,
                y=self.dset.y,
                weight=self.dset.sample_weight,
                ind=self.dset.ind,
                props=self.dset.props,
                categorical_features=self.data_manager.data_params_internal.categorical_features_,
                array_features=self.data_manager.data_params_internal.array_features_,
                feature_names=[f.name for f in self.data_manager.data_params.features],
                cat_encoding_config=cat_encoding_config,
                array_encoding_config=self.data_manager.array_encoding_config(),
                missing_replacement=self.data_manager.data_params_internal.aggregated_missing_replacements,
                drop_rows_below=self.data_manager.data_params.drop_rows_below,
                drop_cols_above=self.data_manager.data_params.drop_cols_above,
                class_weights=class_weights,
            )
            X_processed = dap.handle_missing_and_feature_encoding(sparse_threshold=0.01)
            # self.dset is a NamedTuple (immutable), so we need to replace the fields with the new values

            self.dset = self.dset._replace(
                X=dap.X,
                y=dap.y,
                sample_weight=dap.weight,
                ind=dap.ind,
                props=dap.props,
            )

            y_processed, w_processed, _ = dap.get_processed_arrays()

            coreset.compute_sensitivities(
                X=X_processed,
                y=y_processed,
                w=w_processed,
            )
            chunk_sensi = ChunkSensitivities(
                coreset=coreset.to_dict(with_important=True, use_keep_selected_only=False),
                params=cor_params,
                removed_rows=dap.removed_rows,
                n_features=len(dap.feature_names),
            )
            self.coresets.append(chunk_sensi)
        return self

    def save(self, data_manager: DataManagerT, save_all=False):
        """
        Saves the selected samples asynchronously.

        Parameters
        ----------
        data_manager : object
            The data manager object.
        """
        data_manager.save_selected_samples_async(self.dset,
                                                 self.indices if not save_all else None,
                                                 self.node_id,
                                                 is_buffer=self.node_id == BUFFER_NODE_ID
                                                 )

    def add_indices(self, indices):
        """
        Adds indices to the node.

        Parameters
        ----------
        indices : numpy.ndarray
            An array of indices.
        """
        if self.indices is None:
            self.indices = indices
        else:
            self.indices = np.concatenate([self.indices, indices])


class ChunkLayer:
    """
    A chunk layer for incremental learning.

    This layer divides the dataset into chunks of samples and performs incremental learning on each chunk.

    Args:
        data_manager: A data manager instance that provides access to the dataset.
        chunk_corset_params: An iterable of `ChunkSensitivitiesParams` objects, each containing the parameters for
            building a coreset on a chunk of data. Default is `None`.
        chunk_size: The maximum size of a chunk. If `None`, the entire dataset is treated as a single chunk.
            Default is `None`.
    """

    def __init__(
        self,
        data_manager: DataManagerT,
        chunk_coreset_params: Iterable[ChunkSensitivitiesParams] = None,
        chunk_size: Optional[int] = None,
        parent: Optional[Any] = None,
        chunk_index: int = None,
    ):
        self.build_params = None
        self.chunk_coreset_params = chunk_coreset_params
        self.buffer: Optional[Dataset] = None
        self.chunk_size = chunk_size
        self.data_manager = data_manager
        self.parent = parent
        self.chunk_index = 0 if chunk_index is None else chunk_index

    def has_buffer(self) -> bool:
        """
        Checks if there is a buffer available.

        Returns:
            bool: True if there is a buffer available and not empty, False otherwise.
        """
        return self.buffer is not None and self.buffer[1].shape[0] > 0

    def get_buffer(self) -> Union[Dataset, None]:
        """
        returns unhandled instances.

        Returns
        -------
        a list of numpy arrays

        """
        if self.has_buffer():
            removed_indices = self.data_manager.get_removed()
            _, buffer = exclude_removed(removed_indices, self.buffer.ind, self.buffer)
            return buffer
        else:
            return None

    def set_buffer(self, buffer: Union[List[np.ndarray], Tuple[np.ndarray]] = None):
        """
        set tree's internal buffer of unhandled instances

        Parameters
        ----------
        buffer: list of numpy ndarrays

        Returns
        -------

        """
        self.buffer = Dataset(*buffer) if buffer is not None else None

    def _make_consistent_sample_weight(self, dataset):
        if dataset.sample_weight is not None and self.buffer.sample_weight is None:
            self.buffer = self.buffer._replace(sample_weight = np.ones(self.buffer.X.shape[0], dtype=dataset.sample_weight.dtype))
        elif dataset.sample_weight is None and self.buffer.sample_weight is not None:
            dataset = dataset._replace(sample_weight = np.ones(dataset.X.shape[0], dtype=self.buffer.sample_weight.dtype))
        return dataset

    def _add_to_buffer(self, dataset):
        """
        Adds the given dataset to the buffer.

        Args:
            dataset: The dataset to be added to the buffer.
        """
        if self.has_buffer():
            dataset = self._make_consistent_sample_weight(dataset)            
            self.buffer = tuple((np.concatenate((b, d)) if d is not None else b) for b, d in zip(self.buffer, dataset))
        else:
            self.buffer = tuple(dataset)

        self.buffer = Dataset(*self.buffer)

        # this call covers the following case:
        # when the chunk size is None, and we can not build a 4 leaf tree from the initial n_instances
        # and the calculated default corset size, all the data goes to the buffer node and chunk size remains None.
        # when the partial build is called with new data, the buffer + new data is not enough to build a tree,
        # so the chunk size is calculated and saved.
        # for example: n_instances = 100k, n_features=100, default coreset_size=0.3*100k=30000, chunk_size=None
        # build: cannot build (4 leaf) tree -> all data goes to buffer node.
        # partial build: n_instances = 100k, buffer_node = 100k (total 200k) -> can build (4 leaf) tree,
        # calculating and saving chunk size.
        self.parent.update_build_params()

    def remove_from_buffer(self, indices):
        if self.has_buffer():
            _, buffer = exclude_removed(indices, self.buffer.ind, self.buffer)
            self.set_buffer(buffer)

    def _rebuild_node(self, dset: Dataset, node_id):
        return ChunkNode(
            dset=dset, params=self.chunk_coreset_params, node_id=node_id, data_manager=self.data_manager
        ).build()

    def _create_node(self, dset, node_id=None, leaf_node_index=None) -> ChunkNode:
        """
        Creates a new ChunkNode object.

        Args:
            dset: The dataset used to build the ChunkNode.
            node_id: Optional parameter specifying the ID of the new ChunkNode.
            leaf_node_index: Optional parameter specifying the chunk index for verbose, can be None for buffer node.
        Returns:
            ChunkNode: A new ChunkNode object.
        """
        t = time.time()
        chunk_node = ChunkNode(
            dset=dset, params=self.chunk_coreset_params, node_id=node_id, data_manager=self.data_manager
        ).build()
        chunk_build_time = time.time() - t
        if self.data_manager.verbose > 0 and leaf_node_index is not None:
            self._print_progress(chunk_build_time, leaf_node_index)
        return chunk_node

    def _print_progress(self, chunk_build_time, leaf_node_index):
        """
        print progress in case n_instances is not None:
        2024-04-01 14:10:37 Completed 19 out of 100 chunks, (chunk was built in 0.003 seconds)
        else:
        2024-04-01 14:10:37 Completed 19 chunks, (chunk was built in 0.003 seconds)
        chunk build time is printed in yellow
        Args:
            chunk_build_time: time it took to build a chunk in seconds
        """
        chunks = ""
        if self.data_manager.n_instances is not None and self.build_params.get("chunk_size", 0) > 0:
            # incase we have more chunks than expected data instances we no longer print the "out of" part
            if leaf_node_index + 1 <= self.data_manager.n_instances // self.build_params["chunk_size"]:
                chunks = f" out of {self.data_manager.n_instances // self.build_params['chunk_size']} chunks"
        ct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(
            f"{ct} Completed chunk #{leaf_node_index + 1}{chunks}, "
            f"{colored(f'(chunk was built in {chunk_build_time:.3f} seconds)', 'yellow')}"
        )

    def get_buffer_size(self) -> int:
        """
        Returns the size of the buffer.

        Returns:
            int: The size of the buffer.
        """
        # TODO Daci: There might exist datasets that have ind but no X, y, etc. See Dataset definition
        return self.buffer[1].shape[0] if self.has_buffer() else 0

    def create_buffer_node(self, after_create_leaf_node=None):
        """
        Creates a new ChunkNode object using the data stored in the buffer.

        Returns:
            Union[None, ChunkNode]: A new ChunkNode object if there is a buffer available, None otherwise.
        """
        if self.has_buffer():
            dset = Dataset(*self.buffer)
            node = self._create_node(dset, BUFFER_NODE_ID)
            if after_create_leaf_node:
                after_create_leaf_node(node, None)
            return node
        return None

    def _get_from_buffer(self, after_create_leaf_node=None):
        """
        Generator that moves data from buffer to CoreSet tree if the length of buffer is greater than chunk_size.
        If the buffer has not enough elements to form a chunk according to the chunk_size, no node will be yielded.
        If the chunk_size is set to 0, the whole buffer will be consumed for creating a single coreset node.

        Yields:
            ChunkNode: A ChunkNode object that contains coreset information computed from the chunk of data
            in the buffer.
        """
        if utils.is_simple_chunk_size(self.chunk_size) or self.chunk_size == 0:
            ignore_chunk_size = self.chunk_size == 0

            try:
                # in case chunk_corset_params is None or its not iterable, or coreset_params is None
                dtype = next(iter(self.chunk_coreset_params)).coreset_params.get("dtype", "float32")
            except Exception:
                dtype = 'float32'

            while self.has_buffer() and (ignore_chunk_size or self.buffer[1].shape[0] >= self.chunk_size):

                if ignore_chunk_size:
                    buffer = self.buffer
                    self.buffer = None
                else:
                    buffer = Dataset(*tuple(a[: self.chunk_size] if a is not None else None for a in self.buffer))
                    self.buffer = Dataset(*tuple(a[self.chunk_size:] if a is not None else None for a in self.buffer))

                # noinspection PyTypeChecker
                if self.data_manager.n_jobs is not None and self.data_manager.n_jobs > 1:
                    def _create_leaf_node(buff, leaf_node_index):
                        chunk_node = self._create_node(buff, leaf_node_index=leaf_node_index)
                        if after_create_leaf_node is not None:
                            after_create_leaf_node(chunk_node, leaf_node_index)

                    def _check_memory_available(buff, leaf_node_index):

                        max_batch_size = evaluate_max_batch_size(n_features=buff.X.shape[1], available=True,
                                                                 dtype=dtype)
                        if max_batch_size < buff.X.shape[0] and ThreadPoolManager().has_running_tasks():
                            return False
                        return True

                    ThreadPoolManager().add_to_queue(
                        _create_leaf_node,     # callable
                        _check_memory_available,  # condition
                        0,                 # priority
                        # args for task callable
                        buffer, self.chunk_index)
                    self.chunk_index += 1
                    yield None  # no matter what we yield here, node is handled by _create_leaf_node
                else:
                    node = self._create_node(buffer, leaf_node_index=self.chunk_index)
                    if after_create_leaf_node is not None:
                        after_create_leaf_node(node, None)
                    self.chunk_index += 1
                    if self.build_params:
                        pass
                    yield node

    def process(self, dsets: Iterator = None, create_buffer=True, is_classification=False, after_create_leaf_node=None):
        """
        Process input datasets by adding them to the internal buffer and creating coreset nodes from the buffered data.

        Args:
            dsets (List[Dataset]): A list of input datasets to be processed.
            create_buffer (bool, optional): Whether to create a buffer node from the remaining data in the buffer
                after processing all input datasets. Defaults to True.
            is_classification (bool, optional): Whether the task is classification. Defaults to False.
            after_create_leaf_node: callable to be executed after node leaf creation
        Yields:
            ChunkNode: A coreset node created from the buffered data.

        Returns:
            None

        Raises:
            LicenseError: If the total size of the processed data exceeds 100MB.


        """
        size_bytes = 0
        number_of_features_orig = 0
        number_of_samples = 0
        targets_unique = np.array([])
        for dset in dsets:
            dset = Dataset(*dset)
            if dset.y is not None and is_classification:
                conc = np.concatenate([targets_unique, dset.y])
                targets_unique = np.unique(filter_missing_and_inf(conc))
            size_bytes += sum([d.size * d.itemsize for d in dset if d is not None])
            number_of_features = dset.X.shape[1]
            if dset.orig is not None:
                number_of_features_orig = dset.orig.shape[1]
            number_of_samples += len(dset.ind)

            self._add_to_buffer(dset)

            self.build_params = {
                "number_of_features": number_of_features,
                "number_of_features_orig": number_of_features_orig,
                "number_of_samples": number_of_samples,
                "chunk_size": self.chunk_size,
                "targets_unique_count": len(targets_unique),
                "size_bytes": size_bytes,
                "size_MB": str(size_bytes / 2 ** 20)
            }
            for node in self._get_from_buffer(after_create_leaf_node):
                yield node

        if create_buffer and self.has_buffer():
            yield self.create_buffer_node(after_create_leaf_node)

    def update_buffer(self, indices, X=None, y=None):
        if not self.has_buffer():
            return

        _, (indices, X, y) = align_arrays_by_key((self.buffer.ind,), (indices, X, y))
        mask = np.isin(self.buffer.ind, indices)
        if y is not None:
            self.buffer.y[mask] = y
        if X is not None:
            self.buffer.X[mask] = X

    def rebuild(self, chunk_ids: List[str]):
        for chunk_id in chunk_ids:
            if chunk_id == BUFFER_NODE_ID:
                dset = self.get_buffer()
            else:
                dset = self.data_manager.get_by_nodes([chunk_id])
            node = self._rebuild_node(dset, chunk_id)
            yield node

    def filter_out_samples(self, filter_function, node_ids, with_buffer=True):
        indexes_for_remove = np.array([])

        # TODO: what if data manager does not support get_by_nodes (SQLite)???
        #   in this case we need the build_indexes from the nodes.
        #   probably some end2end tests will fail
        datasets = map(lambda node_id: self.data_manager.get_by_nodes([node_id], with_props=True), node_ids)
        if with_buffer and self.has_buffer():
            itertools.chain(datasets, [self.buffer])
        for dset in datasets:
            filtered_ind = filter_function(dset.ind, dset.X, dset.y, dset.props)
            if len(filtered_ind) > 0:
                indexes_for_remove = np.concatenate([indexes_for_remove, filtered_ind])

        return indexes_for_remove
