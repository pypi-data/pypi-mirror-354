import copy
import io
import os
import pathlib
import pickle
import sys
from dataclasses import dataclass
from datetime import datetime
from time import time
from math import ceil
from typing import Tuple, Union, Optional, Iterator, Type, Callable, Any, Iterable, Dict, List
from uuid import uuid4

import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from networkx.drawing.nx_pydot import graphviz_layout
from sklearn.utils import check_array

from dataheroes.core.types import CoresetSampleParams, CoresetSampleParamsClassification
from dataheroes.data.storage.storage_manager import StorageManager

from . import utils
from .chunk_layer import ChunkSensitivitiesParams, ChunkNode, ChunkLayer
from .common import TreeParams, ScoringFailCodes, BUFFER_NODE_ID
from .. import CoresetDTC
from .utils import process_features, evaluate_max_batch_size
from ..common import to_ndarray, weight_processing
from ..coreset._base import CoresetBase, unique
from ..coreset.common import fairness_policy_adaptor_cleaning, is_int, is_percent
from ..numpy_extra import delete_and_shift, expand_and_select, filter_missing_and_inf, isin_select
from ..coreset.coreset_lg import CoresetLG
from ..helpers import align_arrays_by_key
from ...configuration import DataHeroesConfiguration
from ...data.common import Dataset
from ...data.data_auto_processor import DataAutoProcessor
from ...data.helpers import _update_n_represents
from ...data.manager import DataManagerT
from ...utils import check_feature_for_license, add_telemetry_attribute, user_warning
from ...common import ThreadPoolManager


DATA_MIX_THRESHOLD_DEFAULT = 0.75
MAX_RATIO_CORESET_SIZE_TO_CHUNK_SIZE = 0.6

class TreeOptimizedFor:
    training = 'training'
    cleaning = 'cleaning'

    valid_values = training, cleaning

    @staticmethod
    def check(optimized_for):
        # keep if we want to go back to this implementation
        if isinstance(optimized_for, str):
            # optimized_for = [s.strip() for s in optimized_for.split(',')]
            optimized_for = [optimized_for]
        else:
            optimized_for = list(set(optimized_for))
            if len(optimized_for) != 1:
                raise ValueError(f"optimized_for must be one of {TreeOptimizedFor.valid_values}, got {optimized_for}")

        for v in optimized_for:
            if v not in TreeOptimizedFor.valid_values:
                raise ValueError(f"optimized_for must be one of {TreeOptimizedFor.valid_values}, got {v}")
        return optimized_for


@dataclass
class Node:
    """
    NOTES
        1. Tree is constructed like a list- of lists
        => [[leaf level], [one above], ..., [root level]]
        Therefore, leaves are at self.tree[0] and  root at self.tree[-1]
        2. We identify a node by the level and its index
        3. A node is a dict with 3 keys:
            - "indexes" - indexes of feature / feature-label pair. These are used to query the database
            - "weights" - the corresponding weights
            - "n_represents" - the number of samples each node represents.
                               Might be a dict or list of tuples for multiclass.
    """

    # TODO def __init__ to auto transform to numpy array?
    indexes: np.ndarray
    weights: np.ndarray
    n_represents: Union[dict, int, list]
    # Sum of the sample weights used during build. If weights were not used, it's equal to n_represents. 
    sum_orig_weights: Union[dict, float, list] = None
    # Contains all indexes that were used to build this node
    build_indexes: np.ndarray = None
    # Contains indexes randomly sampled for validation purposes
    random_sample_indexes: np.ndarray = None
    # Contains indexes that the coreset used. node.preprocessed_indexes[cset.idxs] should be used.
    # ("good" indexes, that were not dropped by the preprocessing)
    preprocessed_indexes: np.ndarray = None
    model: Any = None
    model_err: str = None
    model_id: str = None
    metadata: Union[list, dict] = None
    coreset: CoresetBase = None
    dirty: bool = False
    # Is true if the node is a leaf and the build used sample weights.
    weighted_leaf: bool = False
    node_id: Any = None
    chunk_node_id: Any = None
    coreset_size: int = None
    statistics: pd.DataFrame = None

    def to_dict_lists(self, allow_pickle=True):

        def f_array(v):
            if v is not None:
                return v.tolist() if not allow_pickle and not isinstance(v, list) else v

        def dict_to_list(data: dict):
            # The key (label) can be int or some other non string type. Since json forces key to be string
            #   convert dictionary to a list of (key. value) tuple.
            # Since both keys and values in the dictionary can be some numpy type, convert them to simple type.
            #   Note that dict.keys() and dict.values() are asure to be in the same order.
            return list(zip(
                np.array(list(data.keys())).tolist(),
                np.array(list(data.values())).tolist()
            ))

        result = {
            "indexes": f_array(self.indexes),
            "weights": f_array(self.weights),
            "metadata": self.metadata,
            "coreset": self.coreset.to_dict(to_list=not allow_pickle),
            "dirty": self.dirty,
            "weighted_leaf": self.weighted_leaf,
            "build_indexes": f_array(self.build_indexes),
            "preprocessed_indexes": f_array(self.preprocessed_indexes),
            "random_sample_indexes": f_array(self.random_sample_indexes),
            'node_id': self.node_id,
            'chunk_node_id': self.chunk_node_id,
            'coreset_size': self.coreset_size,
        }

        result['n_represents'] = dict_to_list(self.n_represents) \
            if isinstance(self.n_represents, dict) else self.n_represents
        result['sum_orig_weights'] = dict_to_list(self.sum_orig_weights) \
            if isinstance(self.sum_orig_weights, dict) else self.sum_orig_weights

        result['statistics'] = pickle.dumps(self.statistics) if self.statistics is not None else None

        return result

    def __post_init__(self):
        self.node_id = self.node_id or uuid4().hex
        # n_represents dictionary was converted to a list when saving.
        # We should return it back to a dictionary.
        if isinstance(self.n_represents, list):
            self.n_represents = dict(self.n_represents)
        if isinstance(self.sum_orig_weights, list):
            self.sum_orig_weights = dict(self.sum_orig_weights)
        if self.sum_orig_weights is None:
            self.sum_orig_weights = self.n_represents

    @property
    def n_represents_total(self):
        return sum(self.n_represents.values()) if isinstance(self.n_represents, dict) else self.n_represents


    def clear(self) -> None:
        # empty all appropriate arrays (indexes, weights, etc.). 
        # don't mark node as dirty since we already modify the coreset at this step
        self.build_indexes = np.array([], dtype=np.int64)
        self.indexes = np.array([], dtype=np.int64)
        self.preprocessed_indexes = np.array([], dtype=np.int64)
        self.random_sample_indexes = np.array([], dtype=np.int64)
        self.weights = np.array([])
        if isinstance(self.n_represents, dict):
            for key in self.n_represents.keys():
                self.n_represents[key] = 0
        else:
            self.n_represents = 0
        if isinstance(self.sum_orig_weights, dict):
            for key in self.sum_orig_weights.keys():
                self.sum_orig_weights[key] = 0
        else:
            self.sum_orig_weights = 0
        if self.statistics is not None:
            self.statistics["count"] = 0

        # make coreset be empty
        self.coreset.clear()

        self.dirty=False
        

    def is_empty(self):
        """
        Returns True if there is no data in the ChunkNode
        """
        return len(self.indexes) == 0

    # to avoid collecting user's data on telemetry
    def __str__(self):
        return f"Node(len(indexes)={len(self.indexes)}, len(build_indexes)={len(self.build_indexes)})" \
               f" {self.n_represents=}"


class CoresetTree:
    """
    Tree based coreset data structure.

    Methods:

        read_data(self, start = 0, end = None) -- Reads data from the database from `start` to `end`

        fit(self,level=0) -- fits the model

        add_sample(self, X, y=None) -- Adds sample to tree

        get_coreset(self, level=0, verbose=False) -- Gets data from the level

        remove_sample(self, ind)

        replace(self, X, ind, y=None)

        kfold(self,k,cost)


    """

    tree_params_cls = TreeParams

    def __init__(
        self,
        *,
        coreset_cls: Type[CoresetBase],
        sample_params: CoresetSampleParams = None,
        chunk_size: int = None,
        coreset_params: dict = None,
        data_manager: DataManagerT = None,
        leaf_factor: int = 2,
        tree_data=None,
        num_cores: int = 1,
        model_train_function: Callable[[np.ndarray, np.ndarray, np.ndarray], Any] = None,
        model_train_function_params: dict = None,
        optimized_for: str = TreeOptimizedFor.training,
        max_memory_gb: int = None,
        is_mutable_coreset_size=None,
        save_all: bool = None,
        is_multitree: bool = False,
        build_w_estimation: bool = False,
        _DH_DEBUG_MODE: bool = False,
    ):
        """

        Arguments:
            chunk_size: {int} -- leaf level sample size.
                0: leaves are created based on the input data batch separation.

            coreset_size: {int | list} -- coreset_size when sampling. List for multiclass

            buffer_size: {int} -- Buffer Size for memory

            sample_all: {list[bool]} -- A list of booleans that flag which classes to sample everything from

            sampling_list: {int} --  a list of coreset functions (Only the first is used for now)

            database: {TreeDatabase | dict} -- database to connect | a schema to init the TreeDatabase.

            leaf_factor: {int} -- How many children / node

            num_cores: {int} -- number of cores to use

            optimized_for: str, one of 'training', 'cleaning'

            max_memory_gb: int, optional
                maximum memory in GB allowed.

            is_mutable_coreset_size: bool, Optional
                when true, coreset_size may change based on the data
            
            is_multitree: {bool} -- Idicates if the tree manger is used (the tree is not standalone)

            save_all: {bool}
                when true, save all samples to database (not only selected ones)

        NOTES
        1. Tree is constructed like a list- of lists
        => [[leaf level], [one above], ..., [root level]]
        Therefore, leaves are at self.tree[0] and  root at self.tree[-1]
        2. We identify a node by the level and its index
        """
        self.coreset_cls = coreset_cls

        if sample_params is None:
            sample_params = CoresetSampleParamsClassification() if self.is_classification else CoresetSampleParams()
        if optimized_for == TreeOptimizedFor.cleaning:
            sample_params.deterministic_size = 1.0
            # As long as CoresetDTC imitates CoresetLG sensitivity functionality, it needs to have the same treatment
            # as CoresetLG. Once CoresetDTC stands on its own, we'll need to revisit this section here.
            if coreset_cls in (CoresetLG, CoresetDTC) and coreset_params.get("algorithm", "") == "unified":
                coreset_params["solver"] = "cleaning"
        coreset_size = sample_params.coreset_size
        save_all = save_all if save_all is not None else False
        if is_mutable_coreset_size is None:
            if coreset_size:
                is_mutable_coreset_size = False
            else:
                is_mutable_coreset_size = True

        self.tree_params = self.tree_params_cls(
            chunk_size=chunk_size,
            num_cores=num_cores,
            leaf_factor=leaf_factor,
            model_train_function=model_train_function,
            model_train_function_params=model_train_function_params,
            optimized_for=optimized_for,
            max_memory_gb=max_memory_gb,
            is_mutable_coreset_size=is_mutable_coreset_size,
            save_all=save_all,
        )

        self.sample_params = sample_params
        self.coreset_params = coreset_params
        self.data_manager = data_manager
        self._calculated_coreset_size = None

        # Tree = a list of lists
        # leaves are at self.trees[0], root self.trees[-1]
        # we identify a node by the level and its index
        self.tree: List[List[Node]] = [[]]
        # self.removed_indexes = np.array([])
        self.buffer_node = None
        self._nodes_cache = dict()
        # get_cleaning_samples array of seen indexes and last tree level
        self.seen_cleaning_samples = np.array([])
        if tree_data:
            self._load_tree_data(tree_data)

        self.tree_id = uuid4().hex
        # LeafLayer
        self.is_multitree = is_multitree
        self.chunk_layer = None
        self._removed_features = dict()

        self.size = 0
        self.build_w_estimation = build_w_estimation

        self._DH_DEBUG_MODE = _DH_DEBUG_MODE

        # Internal states
        # self.is_classification = self.coreset_cls._coreset_type == "classification"
        self._is_multi_coreset_size = (
            isinstance(self.sample_params, CoresetSampleParamsClassification)
            and self.sample_params.class_size is not None
        )

        if not self.is_classification:
            if self._is_multi_coreset_size:
                raise ValueError("Multi coreset size is allowed for classification tasks only")
            # Sample all can never be here due to how SampleParams is constructed
            # if self.sample_params.sample_all is not None:
            # raise ValueError("`sample_all` is allowed only in classification tasks")

    def _init_chunks_layer(self):
        cor_params = ChunkSensitivitiesParams(coreset_params=self.coreset_params, coreset_cls=self.coreset_cls,
                                              coreset_size=self.coreset_size)
        return ChunkLayer(
            chunk_coreset_params=[cor_params], parent=self, chunk_size=self.chunk_size, data_manager=self.data_manager
        )

    def _remove(self, indexes):
        self.data_manager.remove(indexes)
        # indexes_data_type = np.array(indexes).dtype
        # self.removed_indexes = np.unique(np.concatenate([self.removed_indexes, indexes]).astype(indexes_data_type))

    def get_params(self):
        return {"sample_params": self.sample_params.to_dict(), **self.tree_params.to_dict()}

    # MARK: Tree Properties
    @property
    def is_mutable_coreset_size(self):
        v = self.tree_params.is_mutable_coreset_size
        return False if v is False else True

    @is_mutable_coreset_size.setter
    def is_mutable_coreset_size(self, value):
        self.tree_params.is_mutable_coreset_size = value

    @property
    def n_features(self):
        return self.data_manager.n_features

    @property
    def n_instances(self):
        return self.data_manager.n_instances

    @property
    def n_classes(self):
        return self.data_manager.n_classes

    @property
    def optimized_for(self):
        return self.tree_params.optimized_for

    @property
    def save_all(self):
        return self.tree_params.save_all

    @property
    def max_memory_gb(self):
        return self.tree_params.max_memory_gb

    @property
    def chunk_size(self):
        return self.tree_params.chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        if value is not None:
            value = int(value)
        self.tree_params.chunk_size = value

    def is_simple_chunk_size(self):
        return utils.is_simple_chunk_size(self.chunk_size)

    @property
    def model_train_function(self):
        return self.tree_params.model_train_function

    @property
    def model_train_function_params(self):
        return self.tree_params.model_train_function_params

    @property
    def num_cores(self):
        return self.tree_params.num_cores

    @property
    def leaf_factor(self):
        return self.tree_params.leaf_factor

    @property
    def coreset_size(self):
        return self.sample_params.coreset_size

    @coreset_size.setter
    def coreset_size(self, v):
        if v is not None:
            v = int(v)
        if isinstance(self.sample_params, CoresetSampleParamsClassification) and self.sample_params.class_size is not None and v < sum(self.sample_params.class_size.values()):
            v = sum(self.sample_params.class_size.values())  
        self.tree_params.coreset_size = v
        self.sample_params.coreset_size = v

    @property
    def class_size(self):
        return self.sample_params.class_size if hasattr(self.sample_params, "class_size") else None

    @property
    def is_optimized_for_cleaning(self):
        return self.tree_params.optimized_for == TreeOptimizedFor.cleaning

    @property
    def is_optimized_for_training(self):
        return self.tree_params.optimized_for != TreeOptimizedFor.cleaning

    @property
    def fair(self):
        # TODO Daci: We could assert we are in classification case here.
        return self.sample_params.fair if hasattr(self.sample_params, "fair") else None

    @property
    def buffer(self):
        return self.chunk_layer.get_buffer()

    @property
    def is_classification(self):
        return self.coreset_cls._coreset_type == "classification"

    def get_buffer_size(self) -> int:
        return self.chunk_layer.get_buffer_size()

    def is_empty(self) -> bool:
        """
        Return True if tree has no samples
        """
        return self.tree is None or len(self.tree) == 0 or len(self.tree[0]) == 0

    def get_tree_data(self, level=None, allow_pickle=True):

        # Verify that there is data
        if (not self.tree[0] or not self.tree[0][0]) and not self.buffer_node:
            return None

        models = list()

        # Set meta/ take one node as a representative to decide on dtypes.
        rep_node = self.tree[0][0] if self.tree[0] else self.buffer_node
        meta = dict(
            indexes_dtype=rep_node.indexes.dtype.str,
            weights_dtype=rep_node.weights.dtype.str
        )
        data = dict()

        def _to_dict(node):
            d = node.to_dict_lists(allow_pickle)
            if node.model:
                model_id = node.model_id or uuid4().hex
                models.append((model_id, node.model))
                d['model_id'] = model_id
            return d

        for level, nodes in enumerate(self.tree):
            data[level] = []
            for node in nodes:
                data[level].append(_to_dict(node))

        buffer_node = _to_dict(self.buffer_node) if self.buffer_node else None
        return dict(
            data=data,
            meta=meta,
            buffer_node=buffer_node,
            models=models,
            seen_cleaning_samples=self.seen_cleaning_samples.tolist(),
            # removed_indexes=self.removed_indexes.tolist()
        )

    def get_max_level(self):
        """
        Return the maximal level of the coreset tree. Level 0 is the head of the tree.
        Level 1 is the level below the head of the tree, etc.
        """
        if self.is_empty():
            return 0
        else:
            return max(len(self.tree) - 1, 0)

    def _load_tree_data(self, data: dict):
        meta = data['meta']
        tree_data = data['data']
        buffer_node = data.get('buffer_node')
        models = dict(data.get('models', []))
        seen_cleaning_samples = data.get('seen_cleaning_samples')
        # removed_indexes = data.get('removed_indexes', [])

        results = []

        def to_node(node_dict):
            node = Node(**node_dict)
            node.weights = np.array(node.weights, dtype=meta['weights_dtype'])
            node.indexes = np.array(node.indexes, dtype=meta['indexes_dtype'])
            node.build_indexes = np.array(node.build_indexes, dtype=meta['indexes_dtype'])
            node.n_represents = np.array(node.n_represents) if isinstance(node.n_represents,
                                                                          (list, tuple)) else node.n_represents
            # If node wasn't saved with sum_orig_weights, use n_represents as a default
            if node.sum_orig_weights is None:
                node.sum_orig_weights = node.n_represents
            node.model = models.get(node_dict.get('model_id'))
            node.coreset = self.coreset_cls.from_dict(
                node_dict.get('coreset', dict()),
                **(self.coreset_params or dict())
            )
            node.statistics = pickle.loads(node_dict.get('statistics')) if node_dict.get('statistics') else None
            return node

        for level in sorted(tree_data.keys()):
            nodes = tree_data[level]
            results.append([to_node(node) for node in nodes])

        self.tree = results
        self.buffer_node = to_node(buffer_node) if buffer_node else None
        self.seen_cleaning_samples = np.array(seen_cleaning_samples, dtype=meta['indexes_dtype'])
        # self.removed_indexes = np.array(removed_indexes, dtype=meta['indexes_dtype'])

    def _get_node(
            self,
            level: int,
            index: int,
            root_zero: bool
    ) -> Node:
        """
        Get node based on the level of the tree and the index in the tree list.
        Negative index returns buffer node.
        """
        if index < 0:
            return self.buffer_node
        tree = self.tree[::-1] if root_zero else self.tree
        return tree[level][index]

    @staticmethod
    def _is_buffer_node(node_id):
        """check if input node_id is the buffer node_id"""
        return node_id == BUFFER_NODE_ID

    def _init_n_represents(self):
        """returns 0 or a ndarray of number of classes zeroes for classification sampling"""
        if self.is_classification:
            return {}
        else:
            return 0

    @staticmethod
    def _add_n_represents(n_rep1, n_rep2):
        """
        Returns the result of applying a + operation between two n_reps.
        When n_reps are dictionaries the result a union of keys.
        """
        if isinstance(n_rep1, dict):
            return {k: n_rep1.get(k, 0) + n_rep2.get(k, 0) for k in set(n_rep1) | set(n_rep2)}
        else:
            return n_rep1 + n_rep2

    @staticmethod
    def _divide_n_represents(n_rep, denominator):
        """
        Returns the result of dividing n_rep by denominator.
        When n_rep is a dictionary, each value is divided by the denominator.
        """
        if isinstance(n_rep, dict):
            return {k: v / denominator for k, v in n_rep.items()}
        else:
            return n_rep / denominator

    def get_tree_sum_build_indexes(self, level=0):
        """
        Returns the sum of build_indexes of all nodes in the tree.
        """
        nodes, _, _, buffer = self.get_all_nodes_at_some_generalised_level(level=level)
        total_build_indexes = sum([len(node.build_indexes) for node in nodes])
        if buffer is not None:
            total_build_indexes += len(buffer.build_indexes)
        return total_build_indexes

    def _reset_tree(self):
        self.tree = [[]]

    def _read_data(self) -> Iterable:
        datasets = self.data_manager.read_data(self.chunk_size)
        return datasets

    def _update_chunks_params(self, chunk_size, coreset_size):
        self.chunk_size = chunk_size
        if not self.is_multitree:
            self.chunk_layer.chunk_size = chunk_size

        if (
            self.coreset_size is None
            and isinstance(self.sample_params, CoresetSampleParamsClassification)
            and self.sample_params.class_size
        ):
            return
        if coreset_size is not None and self.is_mutable_coreset_size and self.coreset_size is None:
            self.coreset_size = coreset_size
        # Edge case where existing coreset_size is smaller than the sum of class_size.
        # This is also forced in the setter of self.coreset_size but since it's not called when self.coreset_size
        # already exists we need to check it here too.  
        if (
            is_int(self.coreset_size)
            and isinstance(self.sample_params, CoresetSampleParamsClassification)
            and self.sample_params.class_size is not None
            and self.coreset_size < sum(self.sample_params.class_size.values())
        ):
            v = sum(self.sample_params.class_size.values())
            self.tree_params.coreset_size = v
            self.sample_params.coreset_size = v

        if utils.is_simple_chunk_size(self.chunk_size):
            self.is_mutable_coreset_size = False

    def add_buffer_node(self, chunk_node: ChunkNode, coreset=None, random_sample_indexes=None):

        # this update is for building the tree without the service.
        self.update_build_params()

        if chunk_node is not None:
            coreset = coreset or chunk_node.coresets[0]
            node = self._create_leaf_node(
                dataset=chunk_node.dset,
                coreset=coreset,
                chunk_node_id=chunk_node.node_id,
                node_id=BUFFER_NODE_ID,
                random_sample_indexes=random_sample_indexes
            )
            chunk_node.add_indices(node.indexes)
            if not self.is_multitree:
                chunk_node.save(self.data_manager, save_all=self.save_all)
            self.buffer_node = node
        else:
            self.buffer_node = None

    def add_leaf(self, chunk_node: ChunkNode, coreset=None, random_sample_indexes=None, leaf_index=None):

        self.update_build_params()

        # TODO Dacian: Why do we default to the first coreset here? seems error prone.
        coreset = coreset or chunk_node.coresets[0]
        node = self._create_leaf_node(
            dataset=chunk_node.dset,
            coreset=coreset,
            chunk_node_id=chunk_node.node_id,
            random_sample_indexes=random_sample_indexes
        )

        # Add selected samples to chunk_node
        chunk_node.add_indices(node.indexes)
        if not self.is_multitree:
            chunk_node.save(self.data_manager, save_all=self.save_all)

        # If leaf_factor is a factor of the tree we need to build the tree
        if self.data_manager.n_jobs is not None and self.data_manager.n_jobs > 1:
            # we should add all missed leaf nodes up to current index - as empty values (node=None)
            # besides this when adding new nodes
            # we should create all corresponding farther nodes (up to the root), =None as well
            with ThreadPoolManager().lock:
                while len(self.tree[0]) < leaf_index + 1:
                    # update self.tree with None nodes
                    self.tree[0].append(None)
                    # 0 is the leaf level. All new nodes go to the leaves
                    if len(self.tree[0]) % self.leaf_factor == 0:
                        self._update_tree(add_empty=True)
            #  replace None with real node objects as soon as they will be calculated
            self.tree[0][leaf_index] = node

            dtype = self.coreset_params.get('dtype', 'float32') if self.coreset_params else 'float32'

            def _create_parent_node(father_level, father_idx):
                f_node = self._create_father_node(father_level, self.leaf_factor * father_idx)
                self.tree[father_level][father_idx] = f_node

            def _check_if_children_exist(node_level, node_idx):
                max_batch_size = evaluate_max_batch_size(
                    n_features=self.data_manager.n_features_expected, available=True, dtype=dtype
                )
                if max_batch_size < self.chunk_size and ThreadPoolManager().has_running_tasks():
                    return False
                assert node_level > 0
                first_child_idx = self.leaf_factor * node_idx
                child_nodes = [first_child_idx + i for i in range(self.leaf_factor)]
                children_level = node_level - 1
                for child_node_idx in child_nodes:
                    if self.tree[children_level][child_node_idx] is None:
                        return False
                return True
            nodes_for_queue = utils.get_parent_nodes_for_leaf(leaf_factor=self.leaf_factor, leaf_index=leaf_index)
            for node_for_queue in nodes_for_queue:
                node_father_level, node_father_idx = node_for_queue
                ThreadPoolManager().add_to_queue(
                    _create_parent_node,          # callable
                    _check_if_children_exist,   # condition (also callable)
                    node_father_level + 1,
                    # args for callables
                    node_father_level,
                    node_father_idx)
        else:
            self.tree[0].append(node)
            # 0 is the leaf level. All new nodes go to the leaves
            if len(self.tree[0]) % self.leaf_factor == 0:
                self._update_tree()
        return node

    def _build(self, datasets: Iterator[tuple] = None):
        datasets = datasets or self._read_data()
        self.chunk_layer = self._init_chunks_layer()
        chunk_nodes = self.chunk_layer.process(datasets, create_buffer=True)
        for chunk_node in chunk_nodes:
            if chunk_node.is_buffer():
                self.add_buffer_node(chunk_node)
            else:
                self.add_leaf(chunk_node)
        self._clear_node_data_cache()
        self.data_manager.commit()
        self.finish_build(self.chunk_layer.build_params)

    def _run_build_telemetry(self):
        # telemetry
        number_of_leaf_nodes = len(self.tree[0]) if self.tree and len(self.tree) > 0 else 0
        add_telemetry_attribute("tree._build.number_of_leaf_nodes", number_of_leaf_nodes)
        _, heads = self._traverse_tree()
        print_lines = []
        self._traverse_orphans(heads=heads, print_lines=print_lines)
        self._traverse_buffer(heads=heads, print_lines=print_lines)
        heads_representation = '\n'.join([line for line in print_lines if "head" in line])
        add_telemetry_attribute("tree._build.heads_representation", heads_representation)

    def _print_removed_features(self):
        if self._removed_features is None:
            return
        total_nodes = len(self._removed_features)
        feature_count = {}  # To count how many nodes each feature is dropped in

        # Count the occurrences of each feature being dropped
        for node_features in self._removed_features.values():
            for feature in node_features:
                if feature in feature_count:
                    feature_count[feature] += 1
                else:
                    feature_count[feature] = 1

        # Print the percentages
        feature_stats = "Feature removal stats:\n"
        for feature, count in feature_count.items():
            percentage = (count / total_nodes) * 100
            to_print = f"Feature '{feature}' has been dropped in {percentage:.2f}% of nodes"
            feature_stats += to_print + "\n"
        add_telemetry_attribute("tree._build.missing_removed_features_prints", feature_stats)

    def finish_build(
            self,
            tree_build_params: dict = None,
            missing_removed_stats: str = '0%',
            missing_cols_stats: str = '',
    ):
        self._run_build_telemetry()
        self._print_removed_features()
        if self.data_manager.data_params.seq_column is not None:
            self._check_tree_is_sequential()

        tree_build_params['coreset_size'] = self.coreset_size
        add_telemetry_attribute("tree._build.tree_build_params", str(tree_build_params))
        add_telemetry_attribute("tree._build.data_params", str(self.data_manager.data_params))
        add_telemetry_attribute("tree._build.missing_removed_rows", missing_removed_stats)
        add_telemetry_attribute("tree._build.missing_cols_stats", missing_cols_stats)
        if tree_build_params['number_of_samples'] > 100_000_000:
            check_feature_for_license("build data exceed 100M")
        if self.is_classification:
            # telemetry - tree._build.n_represents_percent
            n_represents_leaves = {}
            for node in self.tree[0]:
                n_represents_leaves = {key: n_represents_leaves.get(key, 0) + node.n_represents.get(key, 0)
                                       for key in set(n_represents_leaves) | set(node.n_represents)}
            # buffer too
            if self.buffer_node:
                n_represents_leaves = {key: n_represents_leaves.get(key, 0) + self.buffer_node.n_represents.get(key, 0)
                                       for key in set(n_represents_leaves) | set(self.buffer_node.n_represents)}
            n_represents_leaves_total = sum([n_represents_leaves[c] for c in n_represents_leaves])
            n_represents_percent = {key: n_represents_leaves.get(key) / n_represents_leaves_total
                                    for key in n_represents_leaves}
            # format output considering requirements
            n_represents_percent_str_representation = ''
            for class_name in sorted(list(n_represents_percent)):
                n_represents_percent_str_representation += f"'{class_name}': {n_represents_percent[class_name]:.4f}, "
            n_represents_percent_str_representation = "{" + n_represents_percent_str_representation.rstrip(", ") + "}"
            add_telemetry_attribute("tree._build.n_represents_percent", n_represents_percent_str_representation)

    def update_build_params(self):

        if (
            self.coreset_size is None
            and isinstance(self.sample_params, CoresetSampleParamsClassification)
            and self.sample_params.class_size
        ):
            return

        # no point to calculate chunk size and update if we have no data
        if self.n_instances or self.get_buffer_size():
            chunk_size, coreset_size_tree_type, _ = utils.calc_chunks_params(
                chunk_size=self.chunk_size,
                coreset_size=self.coreset_size,
                n_instances=self.n_instances,
                buffer_size=self.get_buffer_size(),
                n_features=self.data_manager.n_features_expected,
                n_classes=self.n_classes,
                max_memory_gb=self.max_memory_gb,
                dtype=self.coreset_params.get("dtype", "float32") if self.coreset_params else "float32",
                class_size_exists=isinstance(self.sample_params, CoresetSampleParamsClassification)
                and self.sample_params.class_size is not None,
            )
            self._update_chunks_params(chunk_size, coreset_size_tree_type[self.optimized_for])

    def build(self, datasets: Iterator[Dataset] = None):
        self._reset_tree()
        self._build(datasets)

    def partial_build(self, datasets: Iterator[Dataset] = None):
        self.buffer_node = None
        self._build(datasets)

    def get_by_index(self, ind, *arrays, with_props=False, with_removed=False):
        return self._get_by_index(ind, *arrays, with_props=with_props, with_removed=with_removed)

    def _get_by_index(self, ind, *arrays, with_props=False, with_removed=False):
        """
        Fetch X and y based on input ind by calling data manager get_by_index.

        Parameters
        ----------
        ind: array like
            identifiers of the required items
        arrays: array like args, optional
            addition related arrays (e.g.  w) for them active masking need to be applied as well.

        Returns
        -------
        ind, X,y, props, *arrays

        Important implementation notes:
        {ind, w} input params are provided in some order - define it as order A.
        The provided ind is applied on DataManager to return {indices, X, y} that were actually found in the DB,
        but these are returned from the DM in a different order, call it order B.
        Some elements of ind may be missing from what the DM returns - hence we use the active_indices mask on {ind, w}.
        Lastly, before we return the {ind, X, y, w}, we need to sync them to match one of the orders - otherwise
        {ind, w} won't match {X, y}.
        Henceforth, we reorder {X, y} according to the original order of the {ind, w} parameters, therefore returning
        (possibly partial to the input) {ind, w} to the caller, which is matching the original order A, with {X, y}
        reordered to match them in the same order.
        Eventually, {ind, X, y, w} quadruplet is returned in all sync, matching the original params order A.
        """
        dataset = self.data_manager.get_by_index(ind, with_props=with_props, with_removed=with_removed)
        if len(arrays) > 0:
            arrays, ind = isin_select(*arrays, idxs=ind, test_idxs=dataset[0], return_index=True)
        # If ind is empty, after expand_and_select we lose the nr of columns of X. We recover them after the call.
        X_shape = dataset.X.shape
        dataset = expand_and_select(*dataset, sel_idxs=ind, orig_idxs=dataset[0])
        if dataset[1].shape != X_shape and len(dataset[1]) == 0:
            dataset[1] = np.zeros((0, X_shape[1]))
        dataset = Dataset(*dataset)
        if arrays:
            return dataset, *arrays
        else:
            return dataset

    def _get_by_nodes(self, nodes, with_props=False):
        """
        Fetch X and y based on input nodes by calling data manager get_by_node.
        Parameters
            nodes:
                array like
                identifiers of the required nodes
        Returns
            ind, X,y, props *arrays
        """
        try:
            return self.data_manager.get_by_nodes([n.chunk_node_id for n in nodes], with_props=with_props)
        except NotImplementedError:
            indexes = np.concatenate([n.build_indexes for n in nodes])
            return self._get_by_index(indexes, with_props=with_props)

    def _init_coreset(self) -> CoresetBase:
        coreset_params = self.coreset_params or {}
        coreset = self.coreset_cls(**coreset_params)
        return coreset

    def _build_coreset(
        self,
        X,
        y,
        w=None,
        new_state=None,
        coreset_size=None,
        coreset=None,
        keep_selected_only=False,
        is_buffer=False,
        is_leaf=False,
        n_represents=None,
        children_nodes: Optional[List[Node]] = None,
    ) -> Tuple[CoresetBase, Union[int, dict], list]:
        coreset = coreset or self._init_coreset()
        if keep_selected_only:
            coreset.keep_selected_only = True
        if is_buffer:
            coreset.safe_mode = True
        coreset_size = coreset_size if coreset_size is not None else self.coreset_size

        # for case of buffer node, change coreset_size in proportion to number of samples
        if (
            coreset_size
            and self.is_simple_chunk_size()
            and len(X) < self.chunk_size
            and is_buffer
            and not self.is_empty()
        ):
            coreset_size = ceil(coreset_size * len(X) / self.chunk_size)
            if self.is_classification and self.sample_params.sample_all is not None:
                # to avoid exception in choice_classification
                classes, counts = unique(filter_missing_and_inf(y), return_counts=True)  # get classes
                classes_counts = dict(zip(classes, counts))
                total_counts = sum(classes_counts.get(c, 0) for c in self.sample_params.sample_all)
                coreset_size = max(coreset_size, total_counts)

        # if self.is_classification and self.sample_params.sample_all is not None:
        #     sample_kwargs['sample_all'] = self.sample_all

        new_state = new_state.coreset if new_state else None
        cat_encoding_config = self.data_manager.cat_encoding_config_clear()
        dap = DataAutoProcessor(
            X=X,
            y=y,
            weight=None if self.is_optimized_for_cleaning else w,
            categorical_features=self.data_manager.data_params_internal.categorical_features_,
            array_features=self.data_manager.data_params_internal.array_features_,
            feature_names=[f.name for f in self.data_manager.data_params.features],
            cat_encoding_config=cat_encoding_config,
            array_encoding_config=self.data_manager.array_encoding_config(),
            missing_replacement=self.data_manager.data_params_internal.aggregated_missing_replacements,
            drop_rows_below=self.data_manager.data_params.drop_rows_below,
            drop_cols_above=self.data_manager.data_params.drop_cols_above,
            is_classification=self.is_classification,
        )
        X_processed = dap.handle_missing_and_feature_encoding()
        if n_represents:
            if dap.n_represents_diff:
                n_represents = _update_n_represents(n_represents, dap.n_represents_diff, self.is_classification)
        else:
            if self.is_classification:
                n_represents = dict(zip(*np.unique(dap.y, return_counts=True))) if dap.y is not None else dict()
            else:
                n_represents = len(X_processed)

        children_coresets = (
            [node.coreset for node in children_nodes]
            if children_nodes is not None and len(children_nodes) > 0
            else None
        )
        y_processed, weight_processed, _ = dap.get_processed_arrays()

        # We don't want to pass class_weight to any level above the leaf level Coresets as we'll be "double counting" it,
        # meaning taking it into account multiple times, once per level.
        class_sample_kwargs = copy.deepcopy(self.sample_params).to_dict()
        if not is_leaf and not is_buffer:
            class_sample_kwargs.pop("class_weight", None)
        if coreset_size != self.coreset_size and isinstance(self.sample_params, CoresetSampleParamsClassification) and self.sample_params.sample_all is not None: 
            # class_sample_kwargs.update(class_size = None)
            if len(unique(y_processed)) == len(self.sample_params.sample_all):
                coreset_size = None
        class_sample_kwargs.update(
            coreset_size=coreset_size, fair=self.optimized_for if self.fair is None else self.fair
        )
        coreset.build(
            X=X_processed,
            y=y_processed,
            w=weight_processed,
            new_state=new_state,
            from_coresets=children_coresets if self.build_w_estimation else None,
            **class_sample_kwargs,
        )
        # we need at least one sample!
        if len(coreset.idxs) == 0 and X.shape[0] > 0:
            coreset.idxs = np.array([0])
            coreset.w = np.array([1.])
            coreset.weights = np.array([1.])
        new_indexes = self._map_to_original_indexes(coreset, dap, X)

        return coreset, n_represents, dap.removed_features, dap.removed_rows, new_indexes

    def _rebuild_coreset(self, coreset, X, y, w=None, new_state=None, *, coreset_size=None, idxs_removed,
                         is_buffer=False, is_leaf=False, n_represents=None, **sample_kwargs):

        coreset_size = coreset_size if coreset_size is not None else self.coreset_size
        new_state = new_state.coreset if new_state else None
        if is_buffer:
            coreset.safe_mode = True
        cat_encoding_config = self.data_manager.cat_encoding_config_clear()
        dap = DataAutoProcessor(
            X=X,
            y=y,
            weight=None if self.is_optimized_for_cleaning else w,
            categorical_features=self.data_manager.data_params_internal.categorical_features_,
            array_features=self.data_manager.data_params_internal.array_features_,
            array_encoding_config=self.data_manager.array_encoding_config(),
            feature_names=[f.name for f in self.data_manager.data_params.features],
            cat_encoding_config=cat_encoding_config,
            missing_replacement=self.data_manager.data_params_internal.aggregated_missing_replacements,
            drop_rows_below=self.data_manager.data_params.drop_rows_below,
            drop_cols_above=self.data_manager.data_params.drop_cols_above,
        )
        # X_processed in rebuild may be differen from X_processed in build
        # We need to adjust for the differences
        X_processed = dap.handle_missing_and_feature_encoding()
        if dap.n_represents_diff:
            n_represents = _update_n_represents(n_represents, dap.n_represents_diff, self.is_classification)
        t = idxs_removed.copy()
        # dap.removed_rows is in [0, len(X_rebuild) - 1]
        # idxs_removed is in [0, len(X_build) - 1]
        # We need idxs_removed in [0, len(X_build_processed)].
        # For this we shift up dap.removed_rows in [0, len(X_build)] and then
        # we shift idxs_removed in [0, len(X_build_processed)]
        # removed_rows_build = shift_indexes(dap.removed_rows, idxs_removed, down = False)
        # removed_rows_build = np.setdiff1d(removed_rows_build, idxs_removed)
        # idxs_removed = delete_and_shift(idxs_removed, removed_rows_build)

        y_processed, weight_processed, _ = dap.get_processed_arrays()

        class_sample_kwargs = copy.deepcopy(self.sample_params).to_dict()
        if not is_leaf and not is_buffer:
            class_sample_kwargs.pop("class_weight", None)
        class_sample_kwargs.update(
            coreset_size=coreset_size, fair=self.optimized_for if self.fair is None else self.fair
        )
        coreset.rebuild(
            X=X_processed,
            y=y_processed,
            w=weight_processed,
            new_state=new_state,
            idxs_removed=idxs_removed,
            random_state=coreset.random_state,
            **class_sample_kwargs,
        )
        new_indexes = self._map_to_original_indexes(coreset, dap, X)

        return n_represents, new_indexes

    def _train_node_model(self, X_full, y_full, w_coreset, coreset_indices_mask) -> Tuple[Any, Any]:
        if self.model_train_function:
            X_coreset = X_full[coreset_indices_mask]
            y_coreset = y_full[coreset_indices_mask] if y_full is not None else None
            try:
                return self.model_train_function(X_coreset, y_coreset, w_coreset,
                                                 **(self.model_train_function_params or dict())), None
            except BaseException as e:
                return None, str(e)
        else:
            return None, None

    def _create_leaf_node(
            self, dataset: Union[Tuple[np.ndarray], Dataset],
            coreset: Optional[ChunkNode] = None,
            node_id=None,
            chunk_node_id=None,
            random_sample_indexes=None
    ) -> Node:
        """
        Create a new leaf node from input indices, X, y, sample_weight.

        Parameters
        ----------
        dataset: tuple
            indices, X, y, sample_weight *
        node_id: optional
            unique identifier representing the node

        Returns
        -------
        Node

        """
        # TODO Dacian : Any reeason we have this?  redeclaration here?
        prepared_dataset = Dataset(*dataset)
        indices, X, y, sample_weight, props = (
            prepared_dataset.ind,
            prepared_dataset.X,
            prepared_dataset.y,
            prepared_dataset.sample_weight,
            prepared_dataset.props,
        )

        coreset_size = self._compose_coreset_size(self.coreset_size, len(X))
        # create a new coreset node
        # TODO Dacian: This should take a dataset object if we have them.
        node = self._coreset_it(
            ind=indices,
            X=X,
            y=y,
            w=sample_weight,
            props=props,
            chunk_node=coreset,
            node_id=node_id,
            chunk_node_id=chunk_node_id,
            is_leaf=True,
            is_buffer=(node_id == BUFFER_NODE_ID),
            coreset_size=coreset_size,
        )

        node.random_sample_indexes = random_sample_indexes

        # set node metadata
        node.metadata = self.data_manager.get_node_metadata(prepared_dataset, node.indexes)
        return node

    def _create_father_node(self, father_level, fs_idx) -> Node:
        """
        Create a new father node from its direct children.

        Parameters
        ----------
        father_level: int
            the level in the tree new father node be positioned.
        fs_idx: int
            index in self.tree[level - 1] that represents the first son of the father

        Returns
        -------
        Node

        """
        ind_, w_, sum_orig_weights, n_represents, nodes = self._all_my_sons(father_level, fs_idx)
        # Check if data is sequential
        if self.data_manager.data_params.seq_column is not None:
            self._check_data_is_sequential(nodes)
        datasets = []
        missing = []
        for node in nodes:
            dataset = self._get_node_data_from_cache(node.node_id, remove=True)
            if dataset:
                datasets.append(dataset)
            else:
                missing.append((node.indexes, node.weights))
        if missing:
            with ThreadPoolManager().dm_lock:
                dataset, w = self._get_by_index(*tuple(map(np.concatenate, zip(*missing))), with_props=True)
            # Get missing data from data manger in a single call.
            datasets.append(
                # self._get_by_index(*tuple(map(np.concatenate, zip(*missing))))
                (dataset.ind, dataset.X, dataset.y, w, dataset.props)
            )

        # Combine all dataset into a single dataset
        ind, X, y, w, props = tuple(np.concatenate(d, axis=0) if d[0] is not None else None for d in zip(*datasets))

        coreset_sizes = [node.coreset_size for node in nodes]
        if all(coreset_sizes):
            coreset_size = int(sum(coreset_sizes) / self.leaf_factor)
        else:
            coreset_size = None

        # create a new coreset node
        node = self._coreset_it(ind=ind, X=X, y=y, w=w, props=props, n_represents=n_represents, coreset_size=coreset_size, children_nodes=nodes)
        # overwrite sum_orig_weights to the sum of the children nodes
        node.sum_orig_weights = sum_orig_weights
        # set node metadata
        node.metadata = self.data_manager.get_node_metadata((ind, X, y), node.indexes,
                                                            [n.metadata for n in nodes if n.metadata])

        return node

    def _update_tree(self, add_empty=False):
        """
        Used when multiple nodes / levels are removed and a stubbed tree is left.
        Go through an arbitrary tree and build up the parents wherever possible.
        """
        if len(self.tree) == 0:
            # nothing to update, the tree is empty
            return

        level = 0

        # add levels as needed
        while len(self.tree[0]) >= self.leaf_factor ** len(self.tree):
            self.tree.append([])

        # iterate until the second to last level
        for level_idx in range(len(self.tree) - 1):
            level = self.tree[level_idx]
            nr_nodes = len(level)

            # Calculate the idxs of orphans whose parents can be computed
            expected_parents = nr_nodes // self.leaf_factor
            actual_parents = len(self.tree[level_idx + 1])
            assert expected_parents >= actual_parents
            eligible_orphans = (expected_parents - actual_parents) * self.leaf_factor
            first_orphan = actual_parents * self.leaf_factor
            last_orphan = first_orphan + eligible_orphans

            # If expected_parents == actual_parents then first_orphen == last_orphan == 1 and the for is skipped
            for node_idx in range(first_orphan, last_orphan, self.leaf_factor):
                father = None if add_empty else self._create_father_node(level_idx + 1, node_idx)
                self.tree[level_idx + 1].append(father)

    def _all_my_sons(self, level: int, fs_idx: int) -> Tuple[np.ndarray, np.ndarray, Union[int, list], list]:
        """
        helper function.
        Collects data from all my sons.

        Input:
            level: {int} - father level
            fs_idx: {int} - index in self.tree[level - 1] that represents the first son of the father

        Return:
            {list} -- concatenated idxs of the sons
            {list} -- concatenated weights of the sons
            n_represents_: {int | list} -- summed number of represented nodes by the father
        """
        assert level > 0, "Leaf level has no sons"
        sons_level = level - 1
        idxs = np.array([], dtype=int)
        w = np.array([])
        sum_orig_weights = self._init_n_represents()
        n_represents_ = self._init_n_represents()

        nodes = self.tree[sons_level][fs_idx: fs_idx + self.leaf_factor]

        for son in nodes:
            idxs = np.concatenate([idxs, son.indexes], axis=0)
            w = np.concatenate([w, son.weights], axis=0)
            n_represents_ = self._add_n_represents(n_represents_, son.n_represents)
            sum_orig_weights = self._add_n_represents(sum_orig_weights, son.sum_orig_weights)
        return idxs, w, sum_orig_weights, n_represents_, nodes

    def _coreset_it(
            self,
            ind: np.ndarray,
            X: np.ndarray,
            y: np.ndarray,
            w: Optional[np.ndarray] = None,
            props: Optional[np.ndarray] = None,
            chunk_node: Optional[ChunkNode] = None,
            node_id=None,
            chunk_node_id=None,
            is_leaf=False,
            is_buffer=False,
            n_represents: Optional[Union[int, dict]] = None,
            coreset_size=None,
            children_nodes: Optional[List[Node]] = None,
    ) -> Node:
        """
        Helper function.
        Grab data from database and coreset it.

        Input:
            ind: {array-like} -- indices
            X: {array-like} -- features
            y: {array-like} -- target
            w: {array-like}, default = None -- weights for the indices
            n_represents: {int | np.ndarray}, default None -- number of samples the father represents
            node_id: optional
            is_leaf: optional - and indication if the required node is a leaf.
            is_buffer: optional - and indication if the required node is buffer.

        Return:
            {Node} -- Node with indexes, weights and number of represented samples
        """

        keep_selected_only = is_leaf and not self.save_all and not self._is_buffer_node(chunk_node_id)

        # if we get no data create and return empty node
        if X is None or len(X) == 0:
            node = Node(
                weights=np.array([]),
                indexes=np.array([], dtype=int),
                sum_orig_weights=self._init_n_represents(),
                n_represents=self._init_n_represents(),
                node_id=node_id,
                chunk_node_id=chunk_node_id,
                coreset_size=coreset_size,
            )
            node = self._compute_node_statistics(node, X, props, children_nodes, is_leaf)
            return node

        # Sample indices and weights for the node
        coreset, n_represents, removed_features, removed_rows, new_indexes = self._build_coreset(
            X,
            y,
            w,
            chunk_node,
            keep_selected_only=keep_selected_only,
            is_leaf=is_leaf,
            is_buffer=is_buffer,
            n_represents=n_represents,
            coreset_size=coreset_size,
            children_nodes=children_nodes,
        )
        _, _w = coreset.get_index_weights()
        _ind = new_indexes
        if self.is_optimized_for_cleaning:
            # We're not using weights, initialize them to 1
            _w = np.ones_like(_w)
            # coreset.weights = _w  # Weights inside the coreset are kept as the original values

        # Create father node with the sampled data and return it
        model, e_str = self._train_node_model(X, y, _w, _ind)

        # Calculate sum_orig_weights
        if w is None:
            sum_orig_weights = n_represents
        else:
            if self.is_classification:
                sum_orig_weights = {}
                for class_name in np.unique(y):
                    mask = (y == class_name)
                    sum_orig_weights[class_name] = np.sum(w[mask])
            else:
                sum_orig_weights = np.sum(w)

        weighted_leaf = True if w is not None and is_leaf else False

        indexes = np.array(ind)[list(_ind)]
        build_indexes = np.array(indexes) if keep_selected_only else ind
        preprocessed_indexes = np.setdiff1d(build_indexes, ind[removed_rows])
        node = Node(
            indexes=indexes,
            weights=_w,
            sum_orig_weights=sum_orig_weights,
            n_represents=n_represents,
            model=model,
            model_err=e_str,
            coreset=coreset,
            build_indexes=build_indexes,
            preprocessed_indexes=preprocessed_indexes,
            node_id=node_id,
            chunk_node_id=chunk_node_id,
            coreset_size=coreset_size,
            weighted_leaf=weighted_leaf,
        )

        self._removed_features[node.node_id] = removed_features

        self._add_node_data_to_cache(node.node_id, _ind, X, y, _w, ind, props)
        node = self._compute_node_statistics(node, X, props, children_nodes, is_leaf)
        return node

    def _compute_node_statistics(self, node, X, props, children_nodes, is_leaf):
        if is_leaf:
            node.statistics = self.data_manager.get_node_statistics(X, props)
        else:
            children_statistics = [child.statistics for child in children_nodes if child.statistics is not None]
            if children_statistics:
                # Merge statistics
                node.statistics = pd.concat(children_statistics)
                # Sum the counts
                node.statistics = node.statistics.groupby('seq').sum().reset_index()
            else:
                node.statistics = None
        return node

    def _add_node_data_to_cache(self, node_id, ind, X, y, w, indices, props):
        X = X[ind]
        y = y[ind] if y is not None else y
        indices = indices[ind]
        props = props[ind] if props is not None else props
        self._nodes_cache[node_id] = (indices, X, y, w, props)

    def _remove_node_data_from_cache(self, node_id):
        self._nodes_cache.pop(node_id, None)

    def _get_node_data_from_cache(self, node_id, remove=True):
        return self._nodes_cache.get(node_id) if not remove else self._nodes_cache.pop(node_id, None)

    def _clear_node_data_cache(self):
        self._nodes_cache = dict()

    def is_dirty(self) -> bool:
        """
        Returns: if tree have "dirty" nodes
        """
        for level in self.tree:
            for node in level:
                if node.dirty:
                    return True
        if self.chunk_layer.has_buffer() and self.buffer_node.dirty:
            return True
        return False

    def _get_parent(self, level_idx, node_idx, as_idx = False):
        """
        Return parent node object based on child level and child index.
        Return None if child has no parent

        Parameters
        ----------
        level_idx: int
        node_idx: int

        Returns
        -------
        Node or None
        """
        tree = self.tree

        p_level_idx = level_idx + 1

        # root has not parent
        if p_level_idx >= len(self.tree):
            return None

        fs_idx = node_idx // self.leaf_factor

        # orphan node (last) has no parent
        if fs_idx >= len(tree[p_level_idx]):
            return None
        if as_idx:
            return p_level_idx, fs_idx
        else:
            return tree[p_level_idx][fs_idx]

    def get_children(self, level, node_idx, root_zero=False, as_idx=False) -> Union[Iterable[Node], Iterable[Tuple]]:
        """
        Get the children of the node identified by level and node_idx
        level: {int} -- level of the node
        node_idx: {int} -- index in the level
        root_zero: {bool}, default=False -- If True then the root is at 0'th levevl
        """
        if root_zero:
            tree = self.tree[::-1]
            if level == len(tree) - 1:
                return []
            children_level = level + 1
        else:
            tree = self.tree
            if level == 0:
                return []
            children_level = level - 1

        if children_level < 0:
            raise IndexError("Negative index")

        fs_idx = self.leaf_factor * node_idx if node_idx != 0 else 0
        if as_idx:
            children_idxs = range(fs_idx, fs_idx + self.leaf_factor)
            return list(zip([children_level]*len(children_idxs), children_idxs))
        else:
            children = tree[children_level][fs_idx: fs_idx + self.leaf_factor]
            return children

    def _where_is_node(self, node_id, root_zero=False):
        """
        Returns the position of the node in the tree
        """
        tree = self.tree[::-1] if root_zero else self.tree
        # use list comprehension to find the node and next
        if node_id == BUFFER_NODE_ID:
            return -1, 0
        (level, node_idx) = next((level_idx, node_idx) for level_idx, level in enumerate(tree)
                                 for node_idx, node in enumerate(level) if node is not None and node.node_id == node_id)

        return level, node_idx

    def _get_actual_levels_for_update(self, force_sensitivity_recalc, force_resample_all):
        if len(self.tree) > 0:
            tree_level_count = len(self.tree)
        elif self.buffer_node:
            # only one level, with only one buffer node
            tree_level_count = 1
        else:
            tree_level_count = 0

        # actual_min_level_to_do_replacement - 0 = leaf level, 1 = one above leaf, and so on
        if self.is_empty():
            actual_min_level_to_do_replacement = 0
        elif force_sensitivity_recalc == -1:
            actual_min_level_to_do_replacement = 0
        elif force_sensitivity_recalc is None and self.save_all:
            actual_min_level_to_do_replacement = 0
        elif force_sensitivity_recalc is None and not self.save_all:
            actual_min_level_to_do_replacement = 1
        else:
            actual_min_level_to_do_replacement = tree_level_count - force_sensitivity_recalc - 1

        # actual_min_level_to_full_replacement - 0 = leaf level, 1 = one above leaf, and so on
        if force_resample_all == -1:
            actual_min_level_to_do_full_replacement = 0 if self.save_all else 1
        elif force_resample_all is None:
            # we will hardly have so huge trees, that means no force resample at all
            actual_min_level_to_do_full_replacement = 2 ** 100
        else:
            actual_min_level_to_do_full_replacement = tree_level_count - force_resample_all - 1

        if actual_min_level_to_do_replacement < 0 or actual_min_level_to_do_full_replacement < 0:
            raise RuntimeError("No resampling below leaf level")

        return actual_min_level_to_do_replacement, actual_min_level_to_do_full_replacement

    def _process_node_resampling(self, node, new_indexes, new_weights,
                                 force_resample_all: bool = False, build_indexes=None, X=None, y=None,
                                 children=None,
                                 is_root: bool = False):
        if is_root:
            number_of_replaced = sum(~np.isin(new_indexes, node.indexes))
            percent_of_replaced = round(100 * number_of_replaced / len(node.indexes), 2) if len(node.indexes) > 0 else 0
            add_telemetry_attribute("Root samples replaced",
                                    str({"count": number_of_replaced,
                                         "% on the root node": percent_of_replaced
                                         }))

        node.indexes = new_indexes
        if self.is_optimized_for_cleaning:
            # We're not using weights, initialize them to 1
            node.weights = np.ones_like(new_weights)
        else:
            node.weights = new_weights
        node.build_indexes = build_indexes

        model, e_str = self._train_node_model(X, y, node.weights, node.coreset.idxs)
        node.model = model
        node.model_err = e_str
        children_metadata = [n.metadata for n in children if n.metadata] if children else None
        node.metadata = self.data_manager.get_node_metadata((build_indexes, X, y), node.indexes, children_metadata)
        node.dirty = False

    def remove_samples(self,
                       indices: Iterable,
                       force_resample_all: Optional[int],
                       force_sensitivity_recalc: Optional[int],
                       force_do_nothing: Optional[bool]
                       ):
        """
        Remove samples from the tree

        Parameters
        ----------
        indices: list of instances to be removed
        force_resample_all:
            do force resample starting from level=force_resample_all, regarding:
                0 = root level
                len(tree)-1 = leaf level
                None = no force resample
                -1 = same as leaf level
        force_sensitivity_recalc:
            Force the recalculation of the sensitivity and partial resampling of the affected nodes,
            based on the coreset's quality, starting from level=force_sensitivity_recalc.
            None - If self.save_all=False - one level above leaf node level. If self.save_all=True - leaf level
            0 - The head of the tree, 1 - The level below the head of the tree,
            len(tree)-1 = leaf level, -1 - same as leaf level.
        force_do_nothing
        """

        # telemetry field "Samples removed"
        self._samples_removed_telemetry_send(indices)

        # update list of removed indexes without duplicates
        self._remove(indices)

        # Mark dirty flag
        self._mark_samples_on_tree(indices=indices, is_removing=True)

        # Update trees and chunks
        self._update(force_resample_all, force_sensitivity_recalc, force_do_nothing)

    def remove_nodes(self, node_idxs: List[tuple]) -> None:
        # Go through the tree and remove all node data
        for node_idx in node_idxs:
            node = self._get_node(*node_idx, root_zero=False)
            node.clear()
            # mark parents as dirty to update them and their coresets in self.resolve_tree()
            self._mark_parents_dirty_recursive(node_idx)

        self.resolve_tree()

    def _mark_parents_dirty_recursive(self, node_idx: tuple):
        # recursively mark parents as dirty up to the root
        parent_idx = self._get_parent(*node_idx, as_idx=True)
        if parent_idx is None:
            return
        parent = self._get_node(*parent_idx, root_zero=False)
        if not parent.dirty:
            parent.dirty = True
            self._mark_parents_dirty_recursive(parent_idx)

    def resolve_tree(self) -> None:
        # Step 1: Decide parent nodes based on children: empty, copy of single child or recompute based on full children
        self._recompute_parents_after_node_removal()

        # Step 2: Prune tree if a part of it is not needed anymore (root is zero or has only one full child left)
        # Heads level indexes are generated with root_zero = True
        heads = self._get_tree_heads(get_empty=True)
        heads_idxs = list(heads.keys())
        # Convert level_idx to root_zero = False
        heads_idxs = [(len(self.tree)-head[0]-1, head[1]) for head in heads]
        root_level_idx = len(self.tree) - 1
        node_idxs_to_remove = self._get_nodes_to_prune_after_removal(heads_idxs, level_idx=root_level_idx)
        self._prune_nodes(node_idxs_to_remove)
        self._remove_empty_levels()

        # Step 3: Rebuild the tree if there are pairs of orphans that can have parents.
        self._update_tree()

    def _recompute_parents_after_node_removal(self) -> None:
        # Handle parent nodes from level leaf+1 upwards.
        for level_idx, level in enumerate(self.tree):
            for node_idx, node in enumerate(level):
                # Leaves are not dirty since they were already emptied. Children will not be None.
                if node.dirty:
                    children, _, full_children, nr_full_children = \
                        self._analyze_full_children(level_idx, node_idx, root_zero=False)
                    if nr_full_children == 0:
                        # Make the node empty if all children are empty.
                        node.clear()
                    elif nr_full_children == 1:
                        # Make the node a copy of the child if only one child is left.
                        child_clone = copy.deepcopy(full_children[0])
                        # The node_id must be distinct for each node in the tree
                        child_clone.node_id = node.node_id
                        self.tree[level_idx][node_idx] = child_clone
                    else:
                        # Recompute the parent node if more than one child is left.
                        first_child_idx = self._where_is_node(children[0].node_id)[1]
                        self.tree[level_idx][node_idx] = self._create_father_node(level_idx, first_child_idx)

    def _get_nodes_to_prune_after_removal(self, heads_idxs: List[tuple], level_idx: int) -> List[tuple]:
        if level_idx < 0:
            return heads_idxs

        # List of heads which should be removed. Acts like a clone of heads_idxs.
        idxs_to_remove = []
        debated_idxs = []
        for head_idx in heads_idxs:
            if head_idx[0] != level_idx:
                # We don't inspect this head yet, keep in the list for the future
                idxs_to_remove.append(head_idx)
            else:
                _, _, _, nr_full_children = \
                    self._analyze_full_children(*head_idx, root_zero=False)
                if nr_full_children is None:
                    if self._get_node(*head_idx, root_zero=False).is_empty():
                        # Reached a full leaf node. Can happen in case of orphan leaves. Don't remove.
                        idxs_to_remove.append(head_idx)
                    continue
                # If a node has one child left, we must check if it should be kept after parsing all heads_idxs
                if nr_full_children == 1:
                    debated_idxs.append(head_idx)
                # Heads with no full children are removed
                elif nr_full_children == 0:
                    idxs_to_remove.append(head_idx)
                    # Its children are now heads and should also be inspected.
                    children_idxs = self.get_children(*head_idx, root_zero=False, as_idx=True)
                    idxs_to_remove.extend(children_idxs)
                else:
                    # Reached a head that has more than one child. It will not be removed.
                    # Because of this, its children don't become heads so we don't inspect them.
                    pass

        # Heads with one child are in debated_idxs. If they have neighbours to their right that are not to be removed
        # the head can't be removed since the neighbour will slide left and become the parent of their remaining child
        for debated_idx in debated_idxs:
            # Get a list of all neighbours to the right
            level_idx = debated_idx[0]
            right_neighbour_idxs = list(zip([level_idx] * len(self.tree[level_idx]), # level_idxs of curent head
                            range(debated_idx[1] + 1, len(self.tree[level_idx]))))   # node_idxs to the right of curent head
            # Check that all right-hand neighbours are to be removed.
            if all([(right_neighbour_idx in idxs_to_remove) or (right_neighbour_idx in debated_idxs)
                    for right_neighbour_idx in right_neighbour_idxs]):
                idxs_to_remove.append(debated_idx)
                children_idxs = self.get_children(*debated_idx, root_zero=False, as_idx=True)
                idxs_to_remove.extend(children_idxs)

        # Finished checking all heads at this level, go a level down the tree.
        # The idxs_to_remove list becomes the new head_idx list
        return self._get_nodes_to_prune_after_removal(idxs_to_remove, level_idx-1)

    def _prune_nodes(self, node_idxs: List[tuple]):
        # Create a list of lists of indexes like:
        # [[4, 5, 6, 7, 8, 9],  # remove nodes 4, 5, 6, 7, 8, 9 at level 0.
        #  [2, 3, 4],           # remove nodes 2, 3, 4 at level 1.
        #  [1, 2],              # remove nodes 1, 2 at level 2.
        #  [0]]                 # remove node 0 at level 3.
        idxs_to_remove = []
        for level_idx in range(len(self.tree)):
            idxs = [n_idx for lv_idx, n_idx in node_idxs if lv_idx == level_idx]
            idxs_to_remove.append(idxs)

        # Go level by level and keep only good nodes at each level.
        for level_idx, (nodes_to_remove, level) in enumerate(zip(idxs_to_remove, self.tree)):
            level = [node for idx, node in enumerate(level) if idx not in nodes_to_remove]
            self.tree[level_idx] = level

    def _analyze_full_children(self, level_idx: int, node_idx: int, root_zero: bool=False):
        children = self.get_children(level_idx, node_idx, root_zero=root_zero)
        if not children:
            return None, None, None, None
        children = np.array(children)
        children_are_full = [not child.is_empty() for child in children]
        full_children = children[children_are_full]
        nr_full_children = sum(children_are_full)
        return children, children_are_full, full_children, nr_full_children

    def _remove_empty_levels(self):
        self.tree = [level for level in self.tree if len(level) > 0]

    def _replace(self, indices, X=None, y=None):
        # Replace in the dataManager
        self.data_manager.replace(indices, X=X, y=y)
        # Update buffer
        self.chunk_layer.update_buffer(indices, X=X, y=y)

    def _update(self, force_resample_all, force_sensitivity_recalc, force_do_nothing=False, update_leaves=True):
        if force_do_nothing:
            return

        actual_min_level_to_do_replacement, actual_min_level_to_do_full_replacement = \
            self._get_actual_levels_for_update(
                force_resample_all=force_resample_all,
                force_sensitivity_recalc=force_sensitivity_recalc,
            )

        self._process_samples_on_tree(
            actual_min_level_to_do_replacement=actual_min_level_to_do_replacement,
            actual_min_level_to_do_full_replacement=actual_min_level_to_do_full_replacement,
            force_do_nothing=force_do_nothing,
        )

    def update_targets(self,
                       indices: Iterable,
                       y: Iterable,
                       force_resample_all: Optional[int],
                       force_sensitivity_recalc: Optional[int],
                       force_do_nothing: Optional[bool],
                       ):
        """
        Remove samples from the tree

        Parameters
        ----------
        indices: list of instances to be updated
        y: list of new targets values len(y)=len(indices) otherwise - exception
        force_resample_all:
            do force resample starting from level=force_resample_all, regarding:
                0 = root level
                len(tree)-1 = leaf level
                None = no force resample
                -1 = same as leaf level
        force_sensitivity_recalc:
                Force the recalculation of the sensitivity and partial resampling of the affected nodes,
                based on the coreset's quality, starting from level=force_sensitivity_recalc.
                None - If self.save_all=False - one level above leaf node level. If self.save_all=True - leaf level
                0 - The head of the tree, 1 - The level below the head of the tree,
                len(tree)-1 = leaf level, -1 - same as leaf level.
        force_do_nothing
        """

        # probably it's not the best idea to read and pass X/y when only one of them is changing,
        # but it gives a very simple implementation and not crucial for performance
        # when there is not a lot of changes, that rather a typical situation

        self._replace(indices, y=y)

        # Mark samples on tree
        self._mark_samples_on_tree(indices=indices)

        # Update tree
        self._update(force_resample_all, force_sensitivity_recalc, force_do_nothing)

    def update_dirty(self,
                     force_resample_all: Optional[int],
                     force_sensitivity_recalc: Optional[int]
                     ):
        """
        update "dirty" samples on the tree
        Parameters
        ----------
        force_resample_all:
            do force resample starting from level=force_resample_all, regarding:
                0 = root level
                len(tree)-1 = leaf level
                None = no force resample
                -1 = same as leaf level
        force_sensitivity_recalc:
            Force the recalculation of the sensitivity and partial resampling of the affected nodes,
            based on the coreset's quality, starting from level=force_sensitivity_recalc.
            None - If self.save_all=False - one level above leaf node level. If self.save_all=True - leaf level
            0 - The head of the tree, 1 - The level below the head of the tree,
            len(tree)-1 = leaf level, -1 - same as leaf level.
        """
        self._update(force_resample_all, force_sensitivity_recalc)

    def filter_out_samples(
            self,
            filter_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]],
            force_resample_all,
            force_sensitivity_recalc,
            force_do_nothing
    ):
        """
        Remove samples from the tree, selection via function

        Parameters
        ----------
        filter_function
        force_resample_all
        force_sensitivity_recalc
        force_do_nothing
        """

        chunk_ids = [node.chunk_node_id for node in self.get_leaves(True)]
        indexes_for_remove = self.chunk_layer.filter_out_samples(filter_function, chunk_ids)

        self.remove_samples(
            indices=indexes_for_remove,
            force_resample_all=force_resample_all,
            force_sensitivity_recalc=force_sensitivity_recalc,
            force_do_nothing=force_do_nothing
        )

    def update_features(self,
                        indices: Iterable,
                        X: Iterable,
                        feature_names: Iterable,
                        force_resample_all: Optional[int],
                        force_sensitivity_recalc: Optional[int],
                        force_do_nothing: Optional[bool]
                        ):
        """
        Remove samples from the tree

        Parameters
        ----------
        indices: list of instances to be updated
        X: list of new features values, X.shape(0)=len(indices) otherwise - exception
        feature_names: list of feature names to update X.shape(1)=len(feature_names) otherwise - exception
        force_resample_all:
            do force resample starting from level=force_resample_all, regarding:
                0 = root level
                len(tree)-1 = leaf level
                None = no force resample
                -1 = same as leaf level
        force_sensitivity_recalc:
            Force the recalculation of the sensitivity and partial resampling of the affected nodes,
            based on the coreset's quality, starting from level=force_sensitivity_recalc.
            None - If self.save_all=False - one level above leaf node level. If self.save_all=True - leaf level
            0 - The head of the tree, 1 - The level below the head of the tree,
            len(tree)-1 = leaf level, -1 - same as leaf level.
        force_do_nothing
        """
        X = process_features(X, self.data_manager, feature_names)

        # Update samples
        self._replace(indices, X=X)

        # Mark samples on tree
        self._mark_samples_on_tree(indices=indices)

        # Update trees and chunks
        self._update(force_resample_all, force_sensitivity_recalc, force_do_nothing)

    def rebuild_leaf(self, chunk_node: ChunkNode, coreset, actual_min_level_to_do_replacement,
                     actual_min_level_to_do_full_replacement):
        """
        Rebuild leaf node
        """
        if chunk_node.is_buffer():
            leaf_node = self.buffer_node
            node_index = -1
            is_buffer_node = True
            dset = None
        else:
            for node_index, l in enumerate(self.tree[0]):
                if l.chunk_node_id == chunk_node.node_id:
                    leaf_node = l
                    is_buffer_node = False
                    dset = chunk_node.dset
        result = self._process_samples_on_node(0, node_index, leaf_node,
                                               actual_min_level_to_do_replacement=actual_min_level_to_do_replacement,
                                               actual_min_level_to_do_full_replacement=actual_min_level_to_do_full_replacement,
                                               force_do_nothing=False,
                                               is_buffer_node=is_buffer_node,
                                               chunk_node=coreset,
                                               dset=dset
                                               )
        if chunk_node.is_buffer() and result:
            chunk_node.add_indices(leaf_node.indexes)
            if not self.is_multitree:
                chunk_node.save(self.data_manager, self.save_all)

    def _remove_random_sample_indices(self, indices):
        """
        Removes indices from the random samples.

        Parameters
        ----------
        indices: list
            A list of indices.
        -------
            -
        """
        leaves = self.get_leaves(with_buffer=True)
        indices_set = set(indices)
        for leaf in leaves:
            if leaf.random_sample_indexes is not None:
                random_sample_indexes_set = set(leaf.random_sample_indexes)
                filtered_random_sample_indexes_set = random_sample_indexes_set - indices_set.intersection(
                    random_sample_indexes_set)
                filtered_random_sample_indexes_list = list(filtered_random_sample_indexes_set)
                filtered_random_sample_indexes_list.sort()
                leaf.random_sample_indexes = np.array(filtered_random_sample_indexes_list)

    def _process_samples_on_node(self,
                                 level_index,
                                 node_index,
                                 node,
                                 actual_min_level_to_do_replacement: int,
                                 actual_min_level_to_do_full_replacement: int,
                                 force_do_nothing: Optional[bool],
                                 is_buffer_node=False,
                                 chunk_node=None,
                                 dset=None
                                 ) -> bool:

        def _get_child_indexes(child):
            return child.build_indexes if child.coreset.keep_selected_only else child.build_indexes[child.coreset.idxs]

        if force_do_nothing or (level_index < actual_min_level_to_do_replacement
                                and level_index < actual_min_level_to_do_full_replacement):
            return False
        else:
            do_full_resampling = (level_index >= actual_min_level_to_do_full_replacement)
            if level_index > 0:
                # ordinal leaf above leaf level
                children = self.get_children(level_index, node_index)
                children_indexes: np.ndarray = np.concatenate([child.indexes for child in children])
                children_weights: np.ndarray = np.concatenate([child.weights for child in children])
                dataset, children_weights = self._get_by_index(children_indexes, children_weights, with_removed=True)
                children_indexes, X, y = dataset[:3]
                # Index in the original build array, to remove samples that changed in the sons
                idxs_removed = np.where(~np.isin(node.build_indexes, children_indexes))[0]
                removed_rows_orig = np.setdiff1d(node.build_indexes, node.preprocessed_indexes)
                removed_rows_orig = np.where(np.isin(node.build_indexes, removed_rows_orig))[0]
                idxs_removed = delete_and_shift(idxs_removed, removed_rows_orig)
            else:
                # If leafs were built with weights, we can't update them since we don't save sample_weight
                if node.weighted_leaf:
                    node.dirty = False
                    return True

                children = None
                # leaf or buffer node
                if dset is not None:
                    children_indexes, X, y = dset[:3]
                elif is_buffer_node:
                    children_indexes, X, y = self.chunk_layer.get_buffer()[:3]
                else:
                    children_indexes, X, y = self._get_by_nodes([node])[:3]

                # persists_mask = ~np.isin(children_indexes, self.removed_indexes)
                # children_indexes = children_indexes[persists_mask]
                # X = X[persists_mask]
                # if y is not None:
                #     y = y[persists_mask]
                children_weights = None
                idxs_removed = np.where(~np.isin(node.build_indexes, children_indexes))[0]
                removed_rows_orig = np.setdiff1d(node.build_indexes, node.preprocessed_indexes)
                removed_rows_orig = np.where(np.isin(node.build_indexes, removed_rows_orig))[0]
                idxs_removed = delete_and_shift(idxs_removed, removed_rows_orig)

            if do_full_resampling:
                _, n_represents, _, _, new_indexes = self._build_coreset(
                    X=X,
                    y=y,
                    coreset=node.coreset,
                    coreset_size=node.coreset_size,
                    new_state=chunk_node,
                )
            else:
                n_represents, new_indexes = self._rebuild_coreset(
                    coreset=node.coreset,
                    coreset_size=node.coreset_size,
                    n_represents=node.n_represents,
                    X=X, y=y, w=children_weights, new_state=chunk_node,
                    idxs_removed=idxs_removed,
                    is_buffer=is_buffer_node, is_leaf=(level_index == 0)
                )

            node.n_represents = n_represents
            coreset_indexes_in_X, weights = node.coreset.get_index_weights()
            coreset_indexes_in_X = new_indexes
            self._process_node_resampling(
                node=node,
                new_indexes=np.array(children_indexes)[list(coreset_indexes_in_X)],
                new_weights=weights,
                build_indexes=children_indexes,
                X=X,
                y=y,
                children=children,
                force_resample_all=do_full_resampling,
                is_root=level_index == len(self.tree) - 1
            )

        return True

    def _process_samples_on_tree(self,
                                 actual_min_level_to_do_replacement: int,
                                 actual_min_level_to_do_full_replacement: int,
                                 force_do_nothing: Optional[bool]
                                 ):
        # iterate levels from leaf to root (level_index=0 - leaf level)
        for level_index, level in enumerate(self.tree):
            for node_index, node in enumerate(level):
                if node.dirty:
                    modified = self._process_samples_on_node(
                        level_index=level_index,
                        node_index=node_index,
                        node=node,
                        actual_min_level_to_do_replacement=actual_min_level_to_do_replacement,
                        actual_min_level_to_do_full_replacement=actual_min_level_to_do_full_replacement,
                        force_do_nothing=force_do_nothing
                    )
                    # after modifying a node, need to update its parent.
                    # set the parent.dirty flag so that it will be processed in the next level.
                    if modified:
                        parent = self._get_parent(level_index, node_index)
                        if parent:
                            parent.dirty = True
        if self.buffer_node and self.buffer_node.dirty:
            self._process_samples_on_node(
                level_index=0,
                node_index=0,
                node=self.buffer_node,
                actual_min_level_to_do_replacement=actual_min_level_to_do_replacement,
                actual_min_level_to_do_full_replacement=actual_min_level_to_do_full_replacement,
                force_do_nothing=force_do_nothing,
                is_buffer_node=True
            )

    def _samples_removed_telemetry_send(self, indices):
        if len(self.tree) > 0:
            total_samples = sum([len(n.indexes) for n in self.tree[0]])
            total_samples_removed = sum([len(np.isin(n.indexes, indices)) for n in self.tree[0]])
            if self.chunk_layer.has_buffer():
                total_samples += len(self.buffer_node.indexes)
                total_samples_removed += len(np.isin(self.buffer_node.indexes, indices))

            remove_samples_params = {"count": total_samples_removed,
                                     "% on the tree": round(100 * total_samples_removed /
                                                            total_samples, 2)}
            add_telemetry_attribute("Samples removed", str(remove_samples_params))

    def _mark_samples_on_node(self, node, level_index, node_index, indices, is_removing, is_buffer):
        if np.isin(node.build_indexes, indices).any():
            if is_removing:
                persist_mask = ~np.isin(node.indexes, indices)
                node.indexes = node.indexes[persist_mask]
                node.weights = node.weights[persist_mask]
            # update metadata
            if node.metadata:
                if is_buffer:
                    dataset = self.chunk_layer.get_buffer()
                elif level_index == 0:
                    dataset = self.data_manager.get_by_nodes([node.chunk_node_id])
                else:
                    dataset = self.data_manager.get_by_index(node.build_indexes)
                if level_index > 0:
                    children = self.get_children(level_index, node_index)
                    node.metadata = self.data_manager.get_node_metadata((dataset.ind, dataset.X, dataset.y),
                                                                        node.indexes,
                                                                        [n.metadata for n in children if
                                                                         n.metadata])
                else:
                    node.metadata = self.data_manager.get_node_metadata((dataset.ind, dataset.X, dataset.y),
                                                                        node.indexes)
            node.dirty = True

    def get_leaves(self, with_buffer=False, include_empty=False) -> Iterable[Node]:
        """Return tree leaves - level 0 and the buffer node if required """
        nodes = []
        if not self.is_empty():
            nodes.extend(self.tree[0])
        if with_buffer and self.buffer_node:
            nodes.append(self.buffer_node)
        if not include_empty:
            nodes = [node for node in nodes if not node.is_empty()]
        return nodes

    def get_dirty_leaves(self, with_buffer=False, include_empty=False) -> Iterable[Node]:
        """
        Get all nodes with dirty flag set to True
        Returns
        -------
        """
        return [node for node in self.get_leaves(with_buffer, include_empty) if node.dirty]

    def _mark_samples_on_tree(self,
                              indices: Iterable,
                              is_removing: bool = False,
                              force_resample_all: Optional[int] = None,
                              force_sensitivity_recalc: Optional[int] = None
                              ):
        """
        if node is affected:
            set dirty=true
            if is_removing=True, remove from node.indexes
        """
        min_level, min_level_full = \
            self._get_actual_levels_for_update(
                force_resample_all=force_resample_all,
                force_sensitivity_recalc=force_sensitivity_recalc
            )
        # mark dirty all nodes that will either be fully or partially resampled
        min_lvl = min(min_level, min_level_full)

        # iterate levels from leaf to root (level_index=0 - leaf level)
        for level_index, level in enumerate(self.tree):
            if level_index >= min_lvl:
                for node_index, node in enumerate(level):
                    self._mark_samples_on_node(
                        node=node, level_index=level_index, node_index=node_index, indices=indices,
                        is_removing=is_removing, is_buffer=False)

        if self.buffer_node:
            self._mark_samples_on_node(
                node=self.buffer_node, level_index=0, node_index=0, indices=indices,
                is_removing=is_removing, is_buffer=True)

    def _get_tree_heads(self, with_buffer=True, get_empty=False):
        # Traverse the tree to generate heads (main tree root + orphan roots + buffer).
        _, heads = self._traverse_tree(get_empty=get_empty)
        self._traverse_orphans(heads=heads, get_empty=get_empty)
        if with_buffer:
            self._traverse_buffer(heads=heads)
        return heads

    def get_coreset(
            self,
            level: int = 0,
            verbose: bool = False,
            inverse_class_weight: bool = True,
            seq_from: Any = None,
            seq_to: Any = None,
            purpose: str = None,
    ):
        """
        Produce a coreset from the tree based on the given tree level.
        Alternative 4: Union of all the head CoreSets into a shared pool.
        Return this shared pool.
        Whole idea of ownership percentage is discarded and weights are not altered.
        Input:
            level: {int} -- tree level to use; higher levels produces bigger sample sizes.
            verbose: {bool} -- indicate if to print detail debug information during the process.
            inverse_class_weight: {bool}, default=True -- If True then inverse class weight is used.
            seq_from: {datetime | str}, default=None -- The start sequence to filter samples by.
            seq_to: {datetime | str}, default=None -- The end sequence to filter samples by.
            purpose: {str}, default=None -- Purpose of getting the coreset, it's used for seq_column
                in order to decide if we should raise a userWarning or not.

        Return:
            {dict}: Node dictionary containing the sampled instances and their weights.
        """
        data_mix_threshold = float(DataHeroesConfiguration().get_param_str("data_mix_threshold") or
                                   DATA_MIX_THRESHOLD_DEFAULT)

        seq_from, seq_to = self._transform_seq_params(seq_from, seq_to)

        max_level = self.get_max_level()
        if level > max_level:
            user_warning(
                f'The requested level does not exist. '
                f'get_coreset returned samples for the maximal'
                f' available level {max_level}'
            )
            level = max_level
        # Flush buffer, if relevant.
        # self.chunk_layer._get_from_buffer()

        # Reverse it => level 0 = root, last level = leaves.
        tree = self.tree[::-1]

        heads = self._get_tree_heads()

        # Exclude heads which are above wanted level
        due = {key: val for key, val in heads.items() if key[0] >= level}

        perfectly_balanced = len(due) == 1

        if verbose:
            print(f'{level=} [heads only] due={self._verbose_due(due)} ({perfectly_balanced=})')

        # Add nodes which are on the wanted level
        due.update({(level, node_idx): node.n_represents for node_idx, node in enumerate(tree[level])})

        if verbose:
            print(f'{level=} [heads + level nodes] due={self._verbose_due(due)} ({perfectly_balanced=})')

        # Create response data pool, empty for now
        pool_ind, pool_w, = np.array([]), np.array([])
        pool_n_rep = self._init_n_represents()
        pool_orig_weights = self._init_n_represents()

        seq_params = [seq_from, seq_to]
        seq_operators = [False, False]
        selected_nodes = self.compute_seq_nodes(due, seq_params, seq_operators, data_mix_threshold, purpose) if seq_from or seq_to else \
            [self._get_node(row, col, root_zero=True) for row, col in due.keys()]
        # Loop through heads and add X, Y and W to our response data pool
        for node in selected_nodes:

            pool_ind = np.concatenate([pool_ind, node.indexes]) if pool_ind.size != 0 else node.indexes
            pool_w = np.concatenate([pool_w, node.weights]) if pool_w.size != 0 else node.weights
            pool_n_rep = self._add_n_represents(pool_n_rep, node.n_represents)
            pool_orig_weights = self._add_n_represents(pool_orig_weights, node.sum_orig_weights)

        # Return empty coreset for empty data
        if len(pool_ind) == 0:
            print("Returning empty coreset")
            nr_features = len(self.data_manager.features_cols)
            return {
                'ind': np.array([], dtype=np.int32),
                'X': np.zeros(shape = (0, nr_features)),
                'y': np.array([]),
                'w': np.array([]),
                'n_represents': self._init_n_represents(),
                'props': np.array([]),
            }
        if self._DH_DEBUG_MODE:
            positions = [{self._where_is_node(node.node_id, root_zero=True): len(node.indexes)} for node in selected_nodes]
            print(f"Selected nodes are: {positions}, Total index sum: {sum([list(pos.values())[0] for pos in positions])}")
        dataset, w = self._get_by_index(pool_ind, pool_w, with_props=True)
        res = {
            'ind': dataset.ind,
            'X': dataset.X,
            'y': dataset.y,
            'w': w,
            'n_represents': pool_n_rep,
            'props': dataset.props,
        }

        if verbose:
            print(f'------> final coreset size: {len(res["ind"])}')
            c_final = set()
            c_final.update(res["ind"])

            n_rep_sum = {} if self.is_classification else 0
            for value_tuple in due.values():
                n_rep_sum = self._add_n_represents(n_rep_sum, value_tuple)

            for due_key in due:
                access_level = due_key[0]
                access_node_idx = due_key[1]
                n_rep = due[due_key]
                # n_rep for classification should be sorted to make test assignments simpler
                if self.is_classification:
                    n_rep_classes = list(n_rep.keys())
                    n_rep_classes.sort()
                    n_rep = {i: n_rep[i] for i in n_rep_classes}

                if self.is_classification:
                    node_pct = sum(list(n_rep.values())) / sum(list(n_rep_sum.values()))
                else:
                    node_pct = n_rep / n_rep_sum

                c_node = set()
                if access_node_idx >= 0:  # Regular node in tree (either under the root or an orphan sub-tree).
                    node = tree[access_level][access_node_idx]
                    c_node.update(node.indexes)
                else:  # Buffer.
                    if self.chunk_layer.has_buffer():
                        idx_buff = self.chunk_layer.get_buffer()[0]
                        c_node.update(idx_buff)
                    elif self.buffer_node:
                        idx_buff = self.buffer_node.indexes
                        c_node.update(idx_buff)
                c_intersect = c_final.intersection(c_node)
                node_pct_actual = len(c_intersect) / len(c_final)
                print(f'------> {level=} ---node[{access_level},{access_node_idx}]: {n_rep=} '
                      f'{node_pct=:.5f} {node_pct_actual=:.5f} ({len(c_intersect)=} {len(c_node)=} {len(c_final)=})')

        if purpose != 'analytics':
            res["w"] = weight_processing(
                w=res["w"],
                sum_orig_weights=pool_orig_weights,
                y=res['y'],
                class_weight=self.coreset_params.get("class_weight", None),
                is_classification=self.is_classification,
                inverse_class_weight=inverse_class_weight
            )
        return res

    def compute_seq_nodes(self, nodes, seq_params, seq_operators, data_mix_threshold, purpose=None):
        result = self._compute_seq_nodes(nodes, seq_params, seq_operators, data_mix_threshold)
        if purpose is not None and (result['total'] != result['selected'] or result['leftout'] != 0):
            user_warning(f"Performing {purpose} on a Coreset representing {result['total']} data instances. "
                         f"{result['extra'] / result['total'] * 100:.2f}% of the included data falls outside of the "
                         f"defined sequences. "
                         f"{result['leftout'] / result['total'] * 100:.2f}% of the data was excluded since it was "
                         f"part of chunks including other data. "
                         f"Use `chunk_by=True` for the `seq_column` or adjust the `seq_column` granularity or adjust "
                         f"the `data_mix_threshold` parameter in the config file to control this behavior.")
        if self._DH_DEBUG_MODE:
            print("FINISHED, returning selected nodes")
        return result['nodes']

    def _compute_seq_nodes(self, nodes, seq_params, seq_operators, data_mix_threshold, result=None):
        """
        From the initial list of nodes, check if each node contains samples within the given time range. Also works with
        simple strings or ints.
        If so and the % of samples is greater than data_mix_threshold, check node's children.
        If the node has no children or none of the children have samples in % greater than data_mix_threshold,
        add it to the list of nodes to be returned.
        If the node has children, call this function recursively on the children.

        Parameters:
        - nodes (list): The initial list of nodes to be processed.
        - seq_params: List of two elements: seq_from and seq_to.
        - seq_operators: List of two boolen values, will determine if the comparison is strict or not.
        - data_mix_threshold (float): The threshold percentage for considering nodes.

        Returns:
        list: A list of nodes that meet the specified conditions.
        """

        def check_samples_within_range(node, seq_from, seq_from_strict, seq_to, seq_to_strict):
            """
            Checks if the node contains samples within the given time range. Also works with simple strings or ints.
            """
            # if the node has no samples, zero percent of the samples are in range
            if node.statistics['count'].sum() == 0:
                return 0.

            df = node.statistics.copy()
            if seq_from is not None:
                df = df[df["seq"] > seq_from] if seq_from_strict else df[df["seq"] >= seq_from]

            if seq_to is not None:
                df = df[df["seq"] < seq_to] if seq_to_strict else df[df["seq"] <= seq_to]

            return df['count'].sum() / node.statistics['count'].sum()

        seq_from, seq_to = seq_params
        seq_from_strict, seq_to_strict = seq_operators

        # make sure we have node objects and not positions
        nodes = [self._get_node(*node, root_zero=True) if isinstance(node, tuple) else node for node in nodes]
        result = {
            'nodes': [],
            'total': 0,
            'selected': 0,
            'leftout': 0,
            'extra': 0,
        } if result is None else result

        for node in nodes:
            row, col = self._where_is_node(node.node_id, root_zero=True)
            # Check if the node contains samples within the given time range
            perc = check_samples_within_range(node, seq_from, seq_from_strict, seq_to, seq_to_strict)
            n_rep = node.n_represents_total
            if perc == 1:
                if self._DH_DEBUG_MODE:
                    print(f"SELECTED -> Node ({row}, {col}) ({node.statistics['seq'].min().date()}, {node.statistics['seq'].max().date()}) contains all samples within the given time range (range: {seq_from} - {seq_to})")
                result['nodes'].append(node)
                result['selected'] += n_rep
                result['total'] += node.n_represents_total
            elif perc == 0:
                # Means that none of the samples are within range, so none of the children are either
                if self._DH_DEBUG_MODE:
                    print(f"NOT SELECTED -> Node ({row}, {col}) ({node.statistics['seq'].min().date()}, {node.statistics['seq'].max().date()}) contains no samples within the given time range (range: {seq_from} - {seq_to})"
                          f" so we're not checking its children.")
                continue
            else:
                if self._DH_DEBUG_MODE:
                    print(f"NOT SELECTED -> Node ({row}, {col}) ({node.statistics['seq'].min().date()}, {node.statistics['seq'].max().date()}) contains {perc * 100:.2f}% of samples within the given time range (range: {seq_from} - {seq_to})")
                children = self.get_children(row, col, root_zero=True) if row != -1 else None
                if children:
                    # Recursively call this function on the children
                    children_positions = [self._where_is_node(child.node_id, root_zero=True) for child in children]
                    self._compute_seq_nodes(children_positions, seq_params, seq_operators, data_mix_threshold, result)
                else:
                    if perc >= data_mix_threshold:
                        result['nodes'].append(node)
                        result['total'] += node.n_represents_total
                        result['selected'] += int(n_rep * perc)
                        result['extra'] += int(n_rep * (1 - perc))
                    else:
                        result['leftout'] += int(n_rep * perc)
        return result

    def _check_tree_is_sequential(self):
        heads = [self._get_node(*node, root_zero=True) for node in self._get_tree_heads()]  # includes buffer
        self._check_data_is_sequential(heads, root_zero=True)

    def _check_data_is_sequential(self, nodes, root_zero=False):
        """
        Checks that each node's minimum is greater than the maximum of the previous node
        """
        for i in range(len(nodes) - 1):
            left_node_max = nodes[i].statistics["seq"].max()
            right_node_min = nodes[i + 1].statistics["seq"].min()
            if left_node_max > right_node_min:
                left_node_pos = self._where_is_node(nodes[i].node_id, root_zero=root_zero)
                right_node_pos = self._where_is_node(nodes[i + 1].node_id, root_zero=root_zero)
                if root_zero:
                    raise ValueError(f"Provided data is not sequential between head node {left_node_pos[1]} on level {left_node_pos[0]} and "
                                     f"head node {right_node_pos[1]} on level {right_node_pos[0]}")
                else:
                    raise ValueError(f"Provided data is not sequential for father node {left_node_pos[1]} on "
                                     f"{left_node_pos[0]} level(s) above the leaf level Coresets.")
        return True

    def get_cleaning_samples(
            self,
            size: int = None,
            class_size: Dict[Any, int] = None,
            classes: list = None,
            sample_all: list = None,
            ignore_indices: Iterable = None,
            select_from_indices: Iterable = None,
            select_from_function: Callable[
                [Iterable, Iterable, Union[Iterable, None], Union[Iterable, None]], Iterable[Any]] = None,
            ignore_seen_samples: bool = True,
            max_tree_level: int = 4,
    ) -> Dict:
        """
        Returns indices of cleaning samples order by importance. Useful for identifying miss-labeled instances.
        At least one of size, class_size must be provided. Must be called after build.
        Parameters
        ----------
        size: int, optional
            Number of samples to return.
            When class_size is provided, remaining samples are taken from classes not appearing in class_size dictionary.
        class_size: dict {class: int or "all" or "any"}, optional.
            Controls the number of samples to choose for each class.
            int: return at most size
            "all": return all samples.
        classes: array-like, optional.
            classes to consider.
        sample_all: list, optional.
            Classes from which to retrieve all samples.
        ignore_indices: array-like, optional.
            An array of indices to ignore when selecting cleaning samples.
        select_from_indices: array-like, optional.
             An array of indices to include when selecting cleaning samples.
        select_from_function: array-like, optional.
             Filter results by function. Function should accept 3 parameters as input: indices, X, y and return
             a list(iterator) of indices
        ignore_seen_samples: bool, optional, default False.
             Exclude already seen indices and set seen flag on any returned indices.
        max_tree_level: int, optional, default 4.
             How many tree levels to go down.
        Returns
        -------
        Dict:
            indices: array-like[int].
                cleaning samples indices.
            X: array-like[int].
                X array
            y: array-like[int].
                y array
            importance: array-like[float].
                The cleaning value. High value is more important.
        """

        def gather_level_samples(level_no, level):
            """
            Gathers samples from a specific level in the tree.

            Args:
                level_no (int): The level to gather samples from.
                level (list): The list of nodes at the specified level.

            Returns:
                tuple: A tuple containing the last level indexes and level labels as NumPy arrays.

            Notes:
                - The function gathers samples from the specified level and constructs two NumPy arrays:
                  `last_level_indexes` contains the concatenated indexes from the nodes at or above the specified level,
                  and `level_y` contains the concatenated labels from the nodes at or above the specified level.
            """

            # Exclude heads which are above wanted level
            due = {key: val for key, val in heads.items() if key[0] >= level_no}
            # Add nodes which are on the wanted level
            due.update({(level_no, node_idx): node
                        for node_idx, node in enumerate(level)})

            last_level_indexes = np.array([])
            level_y = np.array([])
            if buffer_tree:
                buffer = self.buffer
                last_level_indexes = buffer.ind
                if buffer.y is not None:
                    level_y = buffer.y
                return last_level_indexes, level_y

            for _, node in due.items():
                # Indices in this node
                node_ind = node.indexes

                if last_level_indexes.size == 0:
                    last_level_indexes = node_ind
                else:
                    last_level_indexes = np.concatenate([last_level_indexes, node_ind])

                if self.is_classification:
                    node_y = node.coreset.get_y_decoded_selected()
                    if level_y.size == 0:
                        level_y = node_y
                    else:
                        level_y = np.concatenate([level_y, node_y])
            return last_level_indexes, level_y

        def add_to_pool(pool_ind, pool_y, pool_x, pool_props, ind, y, x, props):
            """
            Adds new samples to an existing pool of data.

            Args:
                pool_ind (numpy.ndarray): Existing pool of sample indexes.
                pool_y (numpy.ndarray): Existing pool of sample labels.
                pool_x (numpy.ndarray): Existing pool of sample features.
                pool_props (numpy.ndarray): Existing pool of sample props.
                ind (numpy.ndarray): New sample indexes to add to the pool.
                y (numpy.ndarray): New sample labels to add to the pool.
                x (numpy.ndarray): New sample features to add to the pool.
                props (numpy.ndarray): New sample props to add to the pool.

            Returns:
                tuple: A tuple containing the updated pool indexes, labels, and features as NumPy arrays.
            """

            # Add new level indexes to pool
            if pool_ind.size == 0:
                pool_ind = ind
            else:
                pool_ind = np.concatenate([
                    pool_ind, ind
                ])

            if pool_y.size == 0:
                pool_y = y
            else:
                pool_y = np.concatenate([
                    pool_y, y
                ])
            if pool_x.size == 0:
                pool_x = x
            else:
                pool_x = np.concatenate([
                    pool_x, x
                ])
            if pool_props.size == 0:
                pool_props = props
            else:
                pool_props = np.concatenate([
                    pool_props, props
                ])
            return pool_ind, pool_y, pool_x, pool_props

        import numpy as np

        def normalize_importance(targets, sensitivities):
            """
            Normalize the importance values separately for each class.

            Args:
                targets (numpy.ndarray): Array of target classes.
                sensitivities (numpy.ndarray): Array of sensitivity values.

            Returns:
                numpy.ndarray: Array of normalized importance values.

            """
            # Get unique classes from the targets array
            classes = np.unique(filter_missing_and_inf(targets))

            # Normalize importance separately for each class
            normalized_importance = np.zeros_like(sensitivities)
            for class_val in classes:
                class_indices = np.where(targets == class_val)[0]
                class_sensitivities = sensitivities[class_indices]
                max_importance = np.max(class_sensitivities)

                if max_importance > 0:
                    normalized_importance[class_indices] = class_sensitivities / max_importance

            return normalized_importance

        def apply_filters(ind, y):
            """
            Apply filters to the given arrays.

            Args:
                ind (numpy.ndarray): Array of sample indexes.
                y (numpy.ndarray): Array of sample labels.

            Returns:
                tuple or None: A tuple containing the filtered indexes, features, and labels,
                or None if no samples remain.

            Notes:
                - The function applies a series of filters to the input arrays `ind` and `y`.
                - If any of the filters result in an empty set of samples, the function returns None.
                - The function modifies the input arrays based on the applied filters and returns the filtered results.
            """

            # Restrict only to `classes` if argument was passed (only available in classification)
            if classes:
                calc = np.isin(y, classes)
                ind = ind[calc]
                if len(y) > 0:
                    y = y[calc]

            # Restrict only to select_from_indices
            if select_from_indices is not None:
                calc = np.isin(ind, select_from_indices)
                ind = ind[calc]
                if len(y) > 0:
                    y = y[calc]

            # Remove ignored indices
            if ignore_indices is not None:
                calc = ~np.isin(ind, ignore_indices)
                ind = ind[calc]
                if len(y) > 0:
                    y = y[calc]

            if ind.size == 0:
                return None

            if ignore_seen_samples:
                # Filter already seen indexes
                calc = ~np.isin(ind, self.seen_cleaning_samples, assume_unique=True)
                ind = ind[calc]
                if len(y) > 0:
                    y = y[calc]

            if ind.size == 0:
                return None

            if select_from_function:
                if buffer_tree:
                    all_ind, X, Y = self.buffer[:3]

                    if self.is_classification:
                        _, (ind, y) = align_arrays_by_key((all_ind,), (ind, y))
                    else:
                        _, (ind,) = align_arrays_by_key((all_ind,), (ind,))
                    mask = np.isin(all_ind, ind)
                    ind = ind[mask]
                    x = X[mask]
                    y = Y[mask]
                    props = self.buffer.props[mask] if self.buffer.props is not None else None
                else:
                    dataset = self.get_by_index(ind, with_props=True)
                    ind = dataset.ind
                    x = dataset.X
                    y = dataset.y
                    props = dataset.props

                # Filter by filter function
                ind_after_filter = select_from_function(ind, x, y, props)
                if ind_after_filter is None:
                    return None
                ind_after_filter = check_array(ind_after_filter, ensure_2d=False, ensure_min_samples=0)
                # Check size
                if ind_after_filter.size == 0:
                    return None
                calc = np.isin(ind, ind_after_filter)
                x = x[calc]
                y = y[calc]
                if props is not None and len(props) > 0:
                    props = props[calc]
            else:
                x = np.array([])
                props = np.array([])
                ind_after_filter = ind

            return ind_after_filter, x, y, props

        check_feature_for_license("get_cleaning_samples")

        if ignore_indices is not None:
            ignore_indices = np.array(ignore_indices)

        # Reverse it => level 0 = root, last level = leaves.
        tree = self.tree[::-1]

        buffer_tree = len(tree[-1]) == 0

        # Traverse the tree to generate heads (main tree root + orphan roots + buffer).
        _, heads = self._traverse_tree()
        self._traverse_orphans(heads=heads)
        self._traverse_buffer(heads=heads)
        # Get actual nodes, not dicts
        heads = {key: self._get_node(key[0], key[1], True) for key in heads.keys()}

        visited_indexes = np.array([])  # All samples we've checked

        size = None if all([class_size, size]) and size - sum(class_size.values()) <= 0 else \
            size - sum(class_size.values()) if all([class_size, size]) \
                else size

        # Sample all
        sample_all_idx = np.array([])
        sample_all_y = np.array([])
        sample_all_x = np.array([])
        sample_all_props = np.array([])

        if sample_all:
            last_lvl_nodes = [node for node_idx, node in enumerate(tree[-1])]
            if self.buffer_node:
                last_lvl_nodes.append(self.buffer_node)
            for node in last_lvl_nodes:
                if buffer_tree:
                    node_ind = self.buffer[0]
                    node_y = self.buffer[2]
                else:
                    node_ind = node.indexes
                    node_y = node.coreset.get_y_decoded_selected()

                calc = np.isin(node_y, sample_all)
                node_ind = node_ind[calc]
                node_y = node_y[calc]

                if sample_all_idx.size == 0:
                    sample_all_idx = node_ind
                    sample_all_y = node_y
                else:
                    sample_all_idx = np.concatenate([sample_all_idx, node_ind])
                    sample_all_y = np.concatenate([sample_all_y, node_y])

            sample_all_results = apply_filters(sample_all_idx, sample_all_y)
            if sample_all_results:
                sample_all_idx, sample_all_x, sample_all_y, sample_all_props = sample_all_results

            visited_indexes = sample_all_idx

        # Pool for class size
        selected_idx = np.array([], dtype=int)
        selected_y = np.array([])
        selected_X = np.array([])
        selected_props = np.array([])

        satisfied_size = False if size else True
        satisfied_classes = {cls: False for cls in class_size.keys()} if class_size else {'ok': True}

        for level_no, level in enumerate(tree[:max_tree_level + 1]):
            level_ind, level_y = gather_level_samples(level_no, level)
            # Filter only those which have not been already fetched in the previous levels
            # Do this in order not to query database for same indices every time
            calc = ~np.isin(level_ind, visited_indexes, assume_unique=True)
            level_ind = level_ind[calc]
            if level_y.size > 0:
                level_y = level_y[calc]
            # Update level indexes
            if visited_indexes.size == 0:
                visited_indexes = level_ind
            else:
                visited_indexes = np.concatenate([visited_indexes, level_ind])
            # Apply rest of the filters
            level_results = apply_filters(level_ind, level_y)
            if level_results:
                level_ind, level_x, level_y, level_props = level_results

                if buffer_tree:
                    selected_idx, selected_X, selected_y, selected_props = level_ind, level_x, level_y, level_props
                    break
                if class_size:
                    for current_class in class_size.keys():
                        if not satisfied_classes[current_class]:
                            calc = np.isin(level_y, [current_class])
                            new_class_ind = level_ind[calc]
                            new_class_y = np.array([])
                            new_class_x = np.array([])
                            new_class_props = np.array([])
                            if level_y.size > 0:
                                new_class_y = level_y[calc]
                            if level_x.size > 0:
                                new_class_x = level_x[calc]
                            if level_props.size > 0:
                                new_class_props = level_props[calc]

                            selected_idx, selected_y, selected_X, selected_props = add_to_pool(
                                selected_idx, selected_y, selected_X, selected_props,
                                new_class_ind, new_class_y, new_class_x, new_class_props
                            )

                            # Check conditions
                            count = np.count_nonzero(selected_y == current_class)
                            satisfied_classes[current_class] = count >= class_size[current_class]

                if size:
                    extra = 0 if not class_size else sum(class_size.values())
                    satisfied_size = selected_idx.size >= (size + extra)

                    if not satisfied_size:
                        new_size_ind = level_ind if not class_size else np.setdiff1d(level_ind, selected_idx)
                        new_size_y = level_y if not class_size else np.setdiff1d(level_y, selected_y)
                        new_size_x = level_x if not class_size else np.setdiff1d(level_x, selected_X)
                        new_size_props = level_props if not class_size else np.setdiff1d(level_props, selected_props)
                        selected_idx, selected_y, selected_X, selected_props = add_to_pool(
                            selected_idx, selected_y, selected_X, selected_props,
                            new_size_ind, new_size_y, new_size_x, new_size_props,
                        )
                        satisfied_size = selected_idx.size >= (size + extra)

            if satisfied_size and all(satisfied_classes.values()):
                break

        # Join sample_all with the rest of the pool:
        if sample_all_idx.size != 0:
            selected_idx = np.concatenate([selected_idx, sample_all_idx])
            selected_y = np.concatenate([selected_y, sample_all_y])
            selected_X = np.concatenate([selected_X, sample_all_x])
            selected_props = np.concatenate([selected_props, sample_all_props])

        if selected_idx.size != 0:

            if selected_X.size == 0:  # No filter was passed -> we didn't fetch the X
                if buffer_tree:
                    if self.is_classification:
                        _, (selected_idx, selected_y) = align_arrays_by_key((self.buffer[0],),
                                                                            (selected_idx, selected_y))
                    else:
                        _, (selected_idx,) = align_arrays_by_key((self.buffer[0],), (selected_idx,))

                    mask = np.isin(self.buffer[0], selected_idx)
                    selected_X = self.buffer[1][mask]
                    if self.buffer.props:
                        selected_props = self.buffer[3][mask]
                else:
                    dataset = self.get_by_index(selected_idx, with_props=True)
                    selected_idx = dataset.ind
                    selected_X = dataset.X
                    selected_y = dataset.y if dataset.y is not None else np.array([])
                    selected_props = dataset.props

            # If size was provided, use the policy adapter to tell us how these samples should be dispersed
            if size and self.is_classification:
                # We need to exclude from the calculation np.nan, np.inf, -np.inf
                filtered_y = selected_y[~pd.isna(selected_y) & (selected_y != float('inf')) &
                                        (selected_y != float('-inf'))]
                unique, counts = np.unique(filtered_y, return_counts=True)
                available_samples = dict(zip(unique, counts))
                # Remove sample_all classes from available samples
                if sample_all:
                    available_samples = {k: v for k, v in available_samples.items() if k not in sample_all}
                # If class size is provided, deduce the counts for each class unless there are fewer
                # samples for that class already, in which case, remove the key altogether
                if class_size:
                    for k, v in class_size.items():
                        if available_samples[k] - v > 0:
                            available_samples[k] -= v
                        else:
                            del available_samples[k]

                class_size_from_size = fairness_policy_adaptor_cleaning(size, available_samples)
                class_size = {key: class_size.get(key, 0) + class_size_from_size.get(key, 0) for
                              key in
                              set(class_size) | set(class_size_from_size)} if class_size else class_size_from_size

            only_size = size and not class_size and not sample_all

            if only_size:
                if self.is_classification:
                    # take first element destructuring syntax
                    coreset, *_ = self._build_coreset(selected_X, selected_y, coreset_size=size)
                    important_indices = coreset.idxs
                    final_sensitivities = coreset.get_sensitivities_selected()
                else:
                    # Kmeans practical fails otherwise, will return less than size.
                    coreset, *_ = self._build_coreset(selected_X, selected_y)
                    result = coreset.get_cleaning_samples(size=size)
                    important_indices, final_sensitivities = result
            else:
                coreset, *_ = self._build_coreset(selected_X, selected_y)
                important_indices, final_sensitivities = coreset.get_cleaning_samples(
                    class_size=class_size,
                    sample_all=sample_all,
                )

            final_indices = selected_idx[important_indices]
            final_X = selected_X[important_indices]
            if selected_y.size > 0:
                final_y = selected_y[important_indices]
            else:
                final_y = np.array([], dtype=int)
            final_props = None
            if selected_props is not None and len(selected_props) > 0:
                final_props = selected_props[important_indices]

            # Add returned indexes to seen cleaning samples
            if ignore_seen_samples:
                self.seen_cleaning_samples = np.concatenate([self.seen_cleaning_samples, final_indices])

            # Normalise sensitivities
            if self.is_classification:
                final_sensitivities = normalize_importance(final_y, final_sensitivities)
            else:
                # Normalize by max value disregarding the class
                final_sensitivities = normalize_importance(np.zeros_like(final_sensitivities), final_sensitivities)

            result = {'idx': final_indices,
                      'X': final_X,
                      'y': final_y,
                      'props': final_props,
                      'importance': final_sensitivities
                      }

        else:
            result = {'idx': np.array([]),
                      'X': np.array([]),
                      'y': np.array([]),
                      'props': np.array([]),
                      'importance': np.array([])
                      }

        return result

    def set_seen_indication(self,
                            seen_flag: bool = True,
                            indices: Iterable = None,
                            ):
        """
        Set samples as 'seen' or 'unseen'. Not providing an indices list defaults to setting the flag on all
        samples.

        Parameters
        ----------
        seen_flag: bool
            Set 'seen' or 'unseen' flag
        indices: array like
            Set flag only on provided list of indices. Defaults to all indices.
        """
        check_feature_for_license("get_cleaning_samples")
        if indices is None:
            if not seen_flag:
                # Case when the user resets seen flags for all samples.
                self.seen_cleaning_samples = np.array([], dtype=int)
                return
            # Go to bottom-most level
            node_indexes = [node.build_indexes for node in self.tree[0] if node.build_indexes is not None]
            if node_indexes:
                indices = np.concatenate(node_indexes)
                buffer = self.buffer_node
                if buffer:
                    indices = np.concatenate([indices, buffer.build_indexes])
            else:
                indices = self.chunk_layer.get_buffer()[0]
        else:
            indices = np.array(indices)
            if not (indices >= 0).all():
                raise ValueError("Passed indices must be greater or equal to zero")

        if indices.size > 0:
            if seen_flag:
                self.seen_cleaning_samples = np.unique(np.concatenate([self.seen_cleaning_samples, indices]))
            else:
                self.seen_cleaning_samples = self.seen_cleaning_samples[
                    ~np.isin(self.seen_cleaning_samples, indices)]

    def explain(self,
                X: Iterable,
                model_scoring_function: Callable[[np.ndarray, Any], float]) -> Tuple[Union[list, dict], str, str]:
        """
        Prepare explainability path using provided unlabeled example and model scoring function.

        Parameters
        ----------
        X: array like
            unclassified sample in an array of shape (1, n_attributes) (there must be exactly one sample).
        model_scoring_function: callable[[array like, any], float]
            model scoring function which gets the X and the node's train model as params and returns a score in
            the range of [0,1]; this function drives the building of the explainability path.

        Returns
        -------
        metadata:
            selected leaf's metadata
        explanation:
            free text explaining the built explainability path
        node identifier:
            str
        """
        X = to_ndarray(X)
        best_head_score, best_head_selected_leaf, explanation = self._explain(X, model_scoring_function)
        leaf_level = best_head_selected_leaf[0]
        leaf_index = best_head_selected_leaf[1]
        leaf_metadata = self._get_node(leaf_level, leaf_index, True).metadata
        leaf_id_str = self._node_id_str(False, leaf_level, leaf_index)
        return leaf_metadata, explanation, leaf_id_str

    def get_all_nodes_at_some_generalised_level(self, level):
        """
        Get the nodes, together with their levels and indices.
        Returns all nodes at the indicated level, and also the heads of all
        orphans situated at lower levels. The buffer, if it exists, is also returned.

        Parameters
        ----------
        level (int): The level from which we want to return the nodes.

        Returns
        ----------
        nodes: list of Nodes
            List of nodes
        nodes_levels: list of ints
            List of nodes' levels
        nodes_indexes: list of ints
            List of nodes' indices
        buffer_node: Node
            The buffer node
        """
        # Get the nodes with levels and indices
        levels, indexes, nodes, buffer_node = self._get_level_nodes(
            level=level, include_orphans_heads=True, return_buffer=True
        )
        return nodes, levels, indexes, buffer_node

    def _get_level_nodes(self, level, include_orphans_heads: bool, exclude_empty = True, return_buffer: bool = False):
        """
        Get the level, index and node information for all the nodes at some level.

        Parameters
        ----------
        level: int
            The level from which we extract the nodes' infromation.
        include_orphans_heads: bool
            A flag to indicate if the orphans' heads located
            at a higher level should be included
        exclude_empty: bool
            A flag to indicate if empty nodes should be omitted
        Returns
        ----------
        levels_indexes: list of tuples (int, int, Node)
            Lists containing the level, index and the corresponding node objects.
        """

        # Reverse the tree => level 0 = root, last level = leaves.
        tree = self.tree[::-1]

        # Get the levels, indices and nodes.
        levels = list()
        indexes = list()
        nodes = list()
        if include_orphans_heads:
            # Traverse the tree to generate heads (main tree root + orphan roots).
            _, heads = self._traverse_tree()
            self._traverse_orphans(heads=heads)
            for head_tuple in heads:
                head_level = head_tuple[0]
                if head_level > level:
                    levels.append(head_tuple[0])
                    indexes.append(head_tuple[1])
                    nodes.append(tree[head_tuple[0]][head_tuple[1]])
        if level >= len(tree):
            raise ValueError(
                f'The provided level value is too big. Please select for the `level` parameter a value value between 0 and {len(tree) - 1}.')
        for idx, node in enumerate(tree[level]):
            levels.append(level)
            indexes.append(idx)
            nodes.append(node)

        if exclude_empty:
            non_empty_idxs = self._non_empty_nodes_indexes(nodes)
            levels = [levels[idx] for idx in non_empty_idxs]
            indexes = [indexes[idx] for idx in non_empty_idxs]
            nodes = [nodes[idx] for idx in non_empty_idxs]

        if return_buffer:
            return levels, indexes, nodes, self.buffer_node
        return levels, indexes, nodes

    def _non_empty_nodes_indexes(self, nodes: list) -> np.ndarray:
        return np.where([not node.is_empty() for node in nodes])[0]

    def get_chunk_data_for_nodes(self, init_level: int, init_index: int, n_features_out: int=None, random_sample_percentage: float=None) -> Dataset:
        """
        Get the data from which a node has been constructed.
        If the data is to large to fit into the memory, a random sample
        will be used.
        When no random sample percentage is provided, the percentage is computed
        based on the available memory.

        Parameters
        ----------
        n_features_out: int
            Number of features.
        init_level:  int
            The level of the node.
        init_index: int
            The index of the node.
        Returns
        ----------
        Dataset
        The data (features and labels)
        """
        n_features_out = n_features_out or self.n_features
        # If the node is the buffer, get the data and exit
        # By convention, here the buffer is at level -1 (the index is ignored)
        leaves = self.get_node_corresponding_leaves(init_level, init_index)
        if init_level == -1:
            data = self.data_manager.get_by_index(self.buffer_node.random_sample_indexes)
            assert isinstance(data, Dataset)
            return data
        if random_sample_percentage is None:
            random_sample_percentage = self.get_random_sample_percentage(n_features_out, [init_level], [init_index])
        if random_sample_percentage < 1:
            chunks_dataset = self._get_random_sample(leaves, random_sample_percentage)
        else:
            chunks_indices = []
            for leaf in leaves:
                chunks_indices.extend(leaf.random_sample_indexes)
            chunks_dataset = self._get_by_index(np.array(chunks_indices))
        assert isinstance(chunks_dataset, Dataset)
        return chunks_dataset

    def get_random_sample_percentage(self, n_features_out, validation_nodes_levels, validation_nodes_indexes) -> float:
        """
        Compute the percentage of random samples that can be taken from the leaves of the nodes.
        Parameters
        ----------
        features_out
        validation_nodes_levels
        validation_nodes_indexes

        """
        n_features_out = n_features_out or self.n_features
        dtype = self.coreset_params.get('dtype', 'float32') if self.coreset_params else 'float32'
        max_data_size_in_memory = evaluate_max_batch_size(n_features_out, available=True, dtype=dtype)
        all_leaves = []
        for level, index in zip(validation_nodes_levels, validation_nodes_indexes):
            if (level == -1):
                # If level is -1, this is the buffer node 
                all_leaves.append(self.buffer_node)
            else:
                # Otherwise, it is a regular or orphan node
                all_leaves.extend(self.get_node_corresponding_leaves(level, index))
        total_data_size = self._total_chunk_data_size(all_leaves)
        sample_random_percentage = max_data_size_in_memory / float(total_data_size) if total_data_size != 0 else 1.0
        return sample_random_percentage

    def get_node_corresponding_leaves(self, level, index):
        group_size = self.leaf_factor ** (len(self.tree) - level - 1)
        return self.tree[0][group_size * index: group_size * (index + 1)]

    @staticmethod
    def _total_chunk_data_size(leaves):
        """
        Computes the size of the saved chunks data.
        Parameters
        ----------
        leaves:  list of Nodes
            A list of tree nodes (they must be leaves).
        Returns
        ----------
        total_data_size:  int
            The size of the saved data (random sample)
        """
        total_data_size = 0
        for leaf in leaves:
            if leaf.random_sample_indexes is not None:
                total_data_size += len(leaf.random_sample_indexes)
        return total_data_size

    def _get_random_sample(self, leaves, leaf_sample_percentage):
        """
        Get random samples from leaves' chunks.
        The leaves' chunks data can be the full build dataset
        or a random sample.
        Parameters
        ----------
        leaves:  list of Nodes
            A list of tree nodes (they must be leaves).
        leaf_sample_percentage: float
            Percentage of data instances to be sampled from each leaf.
            The values are between 0 and 1 (0 and 1 are excluded).
        Returns
        ----------
        random_sample:  ndarrays
            The random sample
        """
        if not (leaf_sample_percentage > 0 and leaf_sample_percentage < 1):
            raise ValueError(
                f'leaf_sample_percentage must be a float between 0 and 1 (0 and 1 are excluded). The provided value was {leaf_sample_percentage}.')
        random_sample_indices = []
        rng = np.random.default_rng()
        for node in leaves:
            if node.random_sample_indexes is not None:
                node_random_sample_size = len(node.random_sample_indexes)
                chunk_sample_size = int(leaf_sample_percentage * node_random_sample_size)
                # Sample without replacement data indices
                random_chunks_data_indices = rng.choice(node.random_sample_indexes, size=chunk_sample_size,
                                                        replace=False,
                                                        shuffle=False)
                random_sample_indices.extend(random_chunks_data_indices)
        if len(random_sample_indices) > 0:
            random_sample = self._get_by_index(np.array(np.array(random_sample_indices)))
        else:
            random_sample = np.array([])
        return random_sample

    def _explain(self, X: np.ndarray, model_scoring_function: Callable[[np.ndarray, Any], float]):
        if not self.model_train_function:
            raise ValueError("Tree is not supporting explainability feature")

        if not model_scoring_function:
            raise ValueError("Model scoring function is not provided")

        if X is None or len(X) != 1:
            raise ValueError("X is expected to contain only one sample")

        # Traverse the tree to generate heads (main tree root + orphan roots + buffer).
        _, heads = self._traverse_tree()
        self._traverse_orphans(heads=heads)
        self._traverse_buffer(heads=heads)

        head_levels = []
        head_node_indices = []
        head_scores = []
        head_selected_leaves = []
        head_explanations = ["---------- Explanation Start ----------"]
        for head_tuple in heads:
            head_level = head_tuple[0]
            head_node_idx = head_tuple[1]
            head_score, head_selected_leaf, head_explanation = self._explain_node(head_level, head_node_idx, X,
                                                                                  model_scoring_function)
            head_levels.append(head_level)
            head_node_idx_str = self._node_idx_str(head_node_idx)
            head_node_indices.append(head_node_idx_str)
            head_scores.append(head_score)
            head_selected_leaves.append(head_selected_leaf)
            head_explanations.append(f"==> Explaining head [{head_levels[-1]}.{head_node_indices[-1]}]:")
            head_explanations.append(f"{head_explanation}\n")

        best_head_idx = np.argmax(head_scores)
        head_explanations.append(f"Selected head: [{head_levels[best_head_idx]}.{head_node_indices[best_head_idx]}]")
        head_explanations.append(
            f"Selected leaf: [{head_selected_leaves[best_head_idx][0]}.{self._node_idx_str(head_selected_leaves[best_head_idx][1])}]")
        head_explanations.append(f"Best score: {max(0, head_scores[best_head_idx])}")
        head_explanations.append("---------- Explanation End ----------")
        complete_explanation = "\n".join(head_explanations)
        return max(0, head_scores[best_head_idx]), head_selected_leaves[best_head_idx], complete_explanation

    def _explain_node(
            self,
            node_level: int,
            node_idx: int,
            X: np.ndarray,
            model_scoring_function: Callable[[np.ndarray, Any], float],
            precomputed_score: Union[float, int] = None,
    ):

        indent = " " * 10
        prefix = indent * node_level + f"chosen node [{node_level}.{self._node_idx_str(node_idx)}]: "

        if node_idx < 0:  # Buffer
            buffer_node = self.buffer_node
            if buffer_node:
                score, e_str = self._score_model(X, buffer_node, model_scoring_function)
                explanation = prefix + f"{self._score_str(score, e_str)} (buffer)"
                return score, (node_level, node_idx), explanation
            else:
                raise ValueError("Buffer present but buffer node could not be provided")

        node = self._get_node(node_level, node_idx, True)
        children = self.get_children(node_level, node_idx, root_zero=True)
        if len(children) == 0:  # leaf
            score, e_str = self._score_model(X, node, model_scoring_function)
            explanation = prefix + f"{self._score_str(score, e_str)} (leaf)"
            return score, (node_level, node_idx), explanation
        else:
            score, e_str = precomputed_score, None
            if score is None:
                # This condition is fulfilled only for head nodes, at the beginning of head path exploration.
                # It is not necessary for the explainability function, as head's score has no influence on
                # the outcome whatsoever - but we include it here for completeness purposes (as well as the
                # precomputed score for a non-head node, which we use as-is, instead of recomputing it, to save
                # redundant (same) score calculation time).
                score, e_str = self._score_model(X, node, model_scoring_function)
            explanation = prefix + f"{self._score_str(score, e_str)}"
            children_node_indices = []
            children_scores = []
            child_level = node_level + 1
            for child_idx, _ in enumerate(children):
                child_node_idx = child_idx + node_idx * self.leaf_factor
                child_node = self._get_node(child_level, child_node_idx, True)
                child_score, child_e_str = self._score_model(X, child_node, model_scoring_function)
                child_prefix = indent * child_level + f"evaluating node [{child_level}.{child_node_idx}]: "
                child_explanation = child_prefix + f"{self._score_str(child_score, child_e_str)}"
                explanation = explanation + "\n" + child_explanation
                children_node_indices.append(child_node_idx)
                children_scores.append(child_score)
            best_child_idx = np.argmax(children_scores)
            best_child_node_idx = children_node_indices[best_child_idx]
            best_child_score, best_child_selected_leaf, best_child_explanation = self._explain_node(
                child_level, best_child_node_idx, X, model_scoring_function, children_scores[best_child_idx])
            explanation = explanation + "\n" + best_child_explanation
            return best_child_score, best_child_selected_leaf, explanation

    @staticmethod
    def _score_model(
            X: np.ndarray, node: Node, model_scoring_function: Callable[[np.ndarray, Any], float]
    ) -> Tuple[float, Any]:
        if node.model is None:
            return ScoringFailCodes.train_model_absent.code, node.model_err
        try:
            score = model_scoring_function(X, node.model)
            if score < 0:
                return ScoringFailCodes.function_score_too_low.code, str(score)
            elif score > 1:
                return ScoringFailCodes.function_score_too_high.code, str(score)
            return score, None
        except BaseException as e:
            return ScoringFailCodes.function_call_failed.code, str(e)

    @staticmethod
    def _score_str(score: float, e_str: str = None) -> str:
        if score < 0:
            e_string = ''
            if e_str is not None:
                e_string += f': {e_str}'
            return ScoringFailCodes.code_to_message.get(int(score)) + e_string
        return str(f'{score=}')  # str(...) enclosure is necessary to prevent failures on the CI/CD pipeline.

    def print(self):
        """
        Print the tree's string representation.
        """
        print(self.to_string())

    def to_string(self):
        """
        Return:
            {str} -- String representation of the tree, separated visually to the 3 main components: main tree, orphan sub-trees and buffer.
        """
        header_str = f'==================== {self._tree_desc_header()} ===================='
        print_lines = [header_str]
        _, heads = self._traverse_tree(print_lines=print_lines)
        orphans_str_prefix = "-------------------- Orphans: "
        orphans_str = orphans_str_prefix + (len(header_str) - len(orphans_str_prefix)) * "-"
        print_lines.append(orphans_str)
        self._traverse_orphans(heads=heads, print_lines=print_lines)
        buffer_str_prefix = "-------------------- Buffer: "
        buffer_str = buffer_str_prefix + (len(header_str) - len(buffer_str_prefix)) * "-"
        print_lines.append(buffer_str)
        self._traverse_buffer(heads=heads, print_lines=print_lines)
        footer_str = "=" * len(header_str)
        print_lines.append(footer_str)
        s = "\n".join(print_lines)
        return s

    def plot(
        self, path: Optional[Union[str, os.PathLike]] = None, name: str = None
    ) -> Optional[Union[str, os.PathLike]]:
        """
        Produce a tree graph plot.
        If path is provided, save the figure to path.

        Note: to allow more different styling options to various groups displayed in the plot, different group styles
        of nodes and edges need to be added *separately* and defined with their own style; see more at
        https://networkx.org/documentation/latest/auto_examples/drawing/plot_weighted_graph.html#sphx-glr-auto-examples-drawing-plot-weighted-graph-py

        Input:
            path: {str} -- Path to a local or cloud directory (AWS S3, Google Cloud Platform Storage and Azure Storage supported). If specified, plot is saved to this location.
            name: {str} -- file name, optional.

        Output:
            full path of the saved image or None if path is not provided.
        """
        G = nx.DiGraph()
        _, heads = self._traverse_tree(graph=G)
        self._traverse_orphans(graph=G, heads=heads)
        self._traverse_buffer(graph=G, heads=heads)

        edges = G.edges()
        edge_colors = [G[u][v]['color'] for u, v in edges]
        edge_widths = [G[u][v]['width'] for u, v in edges]

        # todo There must be a more elegant way to do that.
        node_colors = list(dict(G.nodes.data('node_color')).values())
        node_sizes = list(dict(G.nodes.data('node_size')).values())

        dpi = 300
        max_size_inches = int(2 ** 16 / dpi) - 1  # limitation is 2^16 dots
        # Automatically calculate the figure size (in inches) based on our best-practice experience.
        # Height:
        num_plot_tree_levels = len(self.tree) + 1  # with the redundancy of leaf representation.
        height_per_tree_level = 2.4  # based on the (32, 12) plot size which looks great for up to 4-level tree.
        # 8.0 is the magic number below which things get screwed; we may need to play with it in the future.
        plot_height = min(max(8.0, height_per_tree_level * num_plot_tree_levels), max_size_inches)
        # Width:
        num_leaves = len(self.tree[0]) + 1  # +1 is for the buffer
        width_per_leaf = 2  # based on the (32, 12) plot size which looks great for up to 4-level tree.
        # 16.0 is the magic number below which things get screwed; we may need to play with it in the future.
        plot_width = min(max(16.0, width_per_leaf * num_leaves), max_size_inches)

        pos = graphviz_layout(G, prog="dot")
        plt.figure(figsize=(plot_width, plot_height))
        plt.title(self._tree_desc_header())
        nx.draw(G,
                pos=pos,
                font_size=9,
                font_color='midnightblue',
                node_color=node_colors,
                edge_color=edge_colors,
                width=edge_widths,
                node_size=node_sizes,
                node_shape='s',
                with_labels=True,
                style='solid',
                arrows=True)
        name = name + '.png' if name and not name.endswith('.png') else name
        f_name = name or 'tree_plot_' + str(round(time() * 1000)) + '_' + self._tree_desc_header() + '.png'

        full_path = None
        if path is not None:
            storage_manager = StorageManager()
            if not storage_manager.is_dir(path):
                raise FileNotFoundError(f"Path {path} doesn't exist or is not a directory")

            full_path = storage_manager.joinpath(path, f_name)
            # TODO:
            #  define the formula for deciding on the DPI such that on one hand the file size will be minimal
            #  and on the other hand text will be readable when zooming in.
            #  For now dpi parameter is not sent as the image file size can get very big and may cause rendering issues,
            #  for example with the background.
            buffer = io.BytesIO()
            plt.savefig(buffer, bbox_inches='tight')
            storage_manager.dump_bytes(buffer.getvalue(), full_path)
            full_path = (
                pathlib.Path(full_path)
                if storage_manager.is_local(full_path)
                else full_path
            )
        return full_path

    def safe_plot(
        self, path: Optional[Union[str, os.PathLike]] = None, name: str = None
    ) -> Optional[Union[str, os.PathLike]]:
        try:
            return self.plot(path, name)
        except FileNotFoundError as e:
            err_msg = f"Plotting failed: {str(e)}"
            if "'dot'" in err_msg or '"dot"' in err_msg:
                err_msg += " [HINT: Graphviz 'dot' executable not found in the OS path]"
            print(err_msg, file=sys.stderr)
            return

    def _traverse_tree(self, level: int = 0, node_idx: int = 0, is_orphan_head: bool = False, print_lines: list = None,
                       graph: nx.DiGraph = None, father_graph_node_str: str = None, get_empty: bool = False):
        """
        Main tree traversal method. Collects heads data, and optionally, print lines and graph data.

        IMPORTANT: in traversal/presentation methods, the tree is reversed.

        Input:
            level: {int} -- Node's level.
            node_idx: {int} -- Node's index.
            is_orphan_head: {bool} -- Indication if the node is an orphan head.
            print_lines: {list | array} -- Optional collector for string description lines.
            graph: {DiGraph} -- Optional graph collector for tree plotting.
            father_graph_node_str {str} : Identifier of the father node.

        Return:
            {dict} -- Dictionary of (level, node_idx) tuple to n_represents of collected heads.
            {set} -- Set of already visited (level, node_idx) tuples, to prevent duplication.
        """
        tree = self.tree[::-1]
        visited = set()
        heads = {}
        if len(tree) == 0 or len(tree[level]) == 0:
            return visited, heads

        node = tree[level][node_idx]
        is_head = (level == 0 and node_idx == 0) or is_orphan_head
        node_id_str = self._node_id_str(is_head, level, node_idx)
        if print_lines is not None:
            print_line = self._generate_print_line(is_head, level, node, node_id_str)
            print_lines.append(print_line)

        visited.add((level, node_idx))
        if is_head and (not node.is_empty() or get_empty):
            heads[(level, node_idx)] = node.n_represents

        graph_n_rep_str = None
        graph_node_str = None
        if graph is not None:
            graph_n_rep_str, graph_node_str = self._graph_strs(node, node_id_str)
            self._add_plot_standard_node(graph=graph, node=graph_node_str, is_head=is_head)
            if is_orphan_head:
                self._add_plot_hidden_nodes(graph=graph, node_to=graph_node_str, node_id=node_id_str, level=level)
            if father_graph_node_str is not None:
                self._add_plot_standard_edge(graph=graph, node_from=father_graph_node_str, node_to=graph_node_str)

        children = self.get_children(level, node_idx, root_zero=True)
        if len(children) == 0 and graph is not None:
            graph_leaf_str = f"{node_id_str}.leaf\n#samples={graph_n_rep_str}"
            self._add_plot_leaf(graph=graph, node_from=graph_node_str, leaf_to=graph_leaf_str)

        for child_idx, _ in enumerate(children):
            child_visited, child_heads = self._traverse_tree(print_lines=print_lines, level=level + 1,
                                                             node_idx=child_idx + node_idx * self.leaf_factor,
                                                             graph=graph, father_graph_node_str=graph_node_str)
            visited.update(child_visited)
            heads.update(child_heads)

        return visited, heads

    def _traverse_orphans(self, heads: dict, print_lines: list = None, graph: nx.DiGraph = None, get_empty: bool = False):
        """
        Orphans traversal method. Collects (adds to) heads data, and optionally, print lines and graph data.
        Identifies orphans in the main tree structure, and calls the main traversal method to explore son nodes.

        IMPORTANT: in traversal/presentation methods, the tree is reversed.

        Input:
            heads: {dict} -- Dict of (level, node_idx) tuple to n_represents of collected heads.
            print_lines: {list | array} -- Optional collector for string description lines.
            graph: {DiGraph} -- Optional graph collector for tree plotting.
        """
        tree = self.tree[::-1]
        visited = set()

        for level in range(len(tree)):
            # Orphan sub-tree access at each level --> tree[level][self.leaf_factor ** level:]
            for orphan_node_idx in range(self.leaf_factor ** level, len(tree[level])):
                if (level, orphan_node_idx) not in visited:  # Orphan head found.
                    orphan_head_visited, orphan_head = self._traverse_tree(print_lines=print_lines, level=level,
                                                                           node_idx=orphan_node_idx,
                                                                           is_orphan_head=True, graph=graph, get_empty=get_empty)
                    visited.update(orphan_head_visited)
                    heads.update(orphan_head)

    def _traverse_buffer(self, heads: dict, print_lines: list = None, graph: nx.DiGraph = None):
        """
        Buffer traversal method. Collects (adds to) heads data, and optionally, print lines and graph data.
        Buffer is considered as a (partially sized) leaf-level node.

        IMPORTANT: in traversal/presentation methods, the tree is reversed.

        Input:
            heads: {dict} -- Dict of (level, node_idx) tuple to n_represents of collected heads.
            print_lines: {list | array} -- Optional collector for string description lines.
            graph: {DiGraph} -- Optional graph collector for tree plotting.
        """
        tree = self.tree[::-1]

        buffer_node = self.buffer_node
        if buffer_node and not buffer_node.is_empty():
            level = len(tree) - 1
            node_idx = -1
            node_id_str = self._node_id_str(True, level, node_idx)
            heads[(level, node_idx)] = buffer_node.n_represents
            if print_lines is not None:
                print_line = self._generate_print_line(True, level, buffer_node, node_id_str)
                print_lines.append(print_line)
                idxs_buffer = self.chunk_layer.get_buffer()[
                    0] if self.chunk_layer.has_buffer() else 'only buffer node available'
                print_lines.append(f'{idxs_buffer=}')
            if graph is not None:
                _, graph_node_str = self._graph_strs(buffer_node, node_id_str)
                self._add_plot_buffer_node(graph=graph, node_buffer=graph_node_str)
                self._add_plot_hidden_nodes(graph=graph, node_to=graph_node_str, node_id=node_id_str, level=level)

    def _verbose_due(self, due: dict) -> str:
        """
        Return "due" verbose representation in a representable way for a human-readable print out.
        """
        pretty_due = {}
        for k, n_rep in due.items():
            pretty_due[k] = self._to_n_represents_str(n_represents=n_rep, multiline=False) \
                if isinstance(n_rep, dict) else n_rep
        return str(pretty_due)

    def _tree_desc_header(self):
        """
        Return:
            {str} -- Textual description of the tree to be used in print, plot and plot file-name.
        """
        coreset_size = (
            sum(self.sample_params.class_size.values())
            if isinstance(self.sample_params, CoresetSampleParamsClassification)
            and self.sample_params.class_size is not None
            else self.coreset_size
        )
        return f"{self.optimized_for} tree, {self.coreset_cls.__name__}, " f"coreset_size={coreset_size}, chunk_size={self.chunk_size}"

    def _to_n_represents_str(self, n_represents: int or dict, multiline: bool):
        """
        Input:
            n_represents: {int | dict} -- number of samples represented.
            multiline: {bool} -- Indicate if to split the output to multiple lines.

        Return:
            {str} -- n_represents formatted as a string for presentation in print and plot methods.
        """
        if self.is_classification:
            s = str(sum(n_represents.values())) + '=' + ('\n' if multiline else '') + '('
            for i, k in enumerate(sorted(n_represents.keys())):
                if i > 0:
                    s += '\n' if multiline else ','
                s += f'{k}={str(n_represents[k])}'
                if multiline and i < len(n_represents) - 1:
                    s += ','
            s += ')'
            return s
        else:
            return str(n_represents)

    @staticmethod
    def _node_idx_str(node_idx: int):
        """
        Return textual node index representation.
        """
        return str(node_idx) if node_idx >= 0 else "buffer"

    @staticmethod
    def _node_id_str(is_head: bool, level: int, node_idx: int) -> str:
        """
        Return textual node Id representation.
        """
        node_idx_str = CoresetTree._node_idx_str(node_idx)
        return f'{level}.{node_idx_str}{(".head" if is_head else "")}'

    def _generate_print_line(self, is_head: bool, level: int, node: Node, node_id_str: str):
        """
        Generate print line for the tree printing functionality.
        """
        num_spaces = 10
        spaces_str = (" " * num_spaces * level + "(head)\n" if is_head else "") + " " * num_spaces * level
        min_max_idx_str = ""  # Indices are not necessarily numeric
        if node.indexes.dtype == np.float64 or node.indexes.dtype == np.int64:
            min_max_idx_str = f' [min_idx={node.indexes.min()}, max_idx={node.indexes.max()}]' if len(node.indexes) else ""

        node_str = f' --- c_size={node.indexes.shape[0]}{min_max_idx_str}, ' \
                   f'n_represents={self._to_n_represents_str(node.n_represents, multiline=False)}'
        model_str = ''
        if self.model_train_function:
            model_str = ', model=' + ('OK' if node.model is not None else f'ABSENT ({node.model_err})')
        print_line = spaces_str + node_id_str + node_str + model_str
        return print_line

    def _graph_strs(self, node: Node, node_id_str: str):
        """
        Generate graph strings to be used for graph plotting.
        """
        graph_n_rep_str = self._to_n_represents_str(node.n_represents, multiline=True)
        graph_model_str = ''
        if self.model_train_function:
            graph_model_str = ' ' + ('[M]' if node.model is not None else '[N/A]')
        graph_node_str = f'{node_id_str}{graph_model_str}\nc_size={node.indexes.shape[0]}\nn_rep={graph_n_rep_str}'
        return graph_n_rep_str, graph_node_str

    @staticmethod
    def _add_plot_standard_node(graph: nx.DiGraph, node: str, is_head: bool = False):
        """
        Add a standard node to tree graph.
        """
        if is_head:
            col = 'lightslategrey'
        else:
            col = 'lightsteelblue'
        graph.add_node(node, node_color=col, node_size=5000)

    @staticmethod
    def _add_plot_standard_edge(graph: nx.DiGraph, node_from: str, node_to: str):
        """
        Add a standard edge to tree graph.
        """
        if nx.__version__ < "2.8.6":
            graph.add_edge(node_from, node_to, color='black', width='1.5')
        else:
            graph.add_edge(node_from, node_to, color='black', width=1.5)

    @staticmethod
    def _add_plot_leaf(graph: nx.DiGraph, node_from: str, leaf_to: str):
        """
        Add a leaf to tree graph.
        """
        graph.add_node(leaf_to, node_color='pink', node_size=2500)
        if nx.__version__ < "2.8.6":
            graph.add_edge(node_from, leaf_to, color='red', width='0.5')
        else:
            graph.add_edge(node_from, leaf_to, color='red', width=0.5)

    @staticmethod
    def _add_plot_buffer_node(graph: nx.DiGraph, node_buffer: str):
        """
        Add a buffer node to tree graph.
        """
        graph.add_node(node_buffer, node_color='mediumturquoise', node_size=5000)

    @staticmethod
    def _add_plot_hidden_nodes(graph: nx.DiGraph, node_to: str, node_id: str, level: int):
        """
        Add hidden level nodes leading to a node outside the main tree (either orphan node or buffer node).
        """
        for hidden_node_level in range(0, level):
            hidden_from = str(hidden_node_level) + ".hidden.\n" + node_id
            graph.add_node(hidden_from, node_color='gainsboro', node_size=500)
            if hidden_node_level == level - 1:
                hidden_to = node_to
            else:
                hidden_to = str(hidden_node_level + 1) + ".hidden.\n" + node_id
                graph.add_node(hidden_to, node_color='gainsboro', node_size=500)

            if nx.__version__ < "2.8.6":
                graph.add_edge(hidden_from, hidden_to, color='gainsboro', width='0.5')
            else:
                graph.add_edge(hidden_from, hidden_to, color='gainsboro', width=0.5)

    @staticmethod
    def _map_to_original_indexes(coreset, dset, original_X):
        """
        Map coreset indexes to original indexes.
        """
        if len(original_X) == 0:
            return np.array([], dtype=coreset.idxs.dtype)
        if dset.removed_rows is not None:
            mask_X_processed = np.ones(len(original_X), dtype=bool)
            mask_X_processed[dset.removed_rows] = False
            new_indexes = np.where(mask_X_processed)[0][coreset.idxs]
        else:
            new_indexes = coreset.idxs
        return new_indexes

    @staticmethod
    def _compose_coreset_size(coreset_size, n_samples):
        """
        Compose coreset size.
        """
        warning_msg = lambda size, max_val: f"Provided coreset_size is too big: {size}. It will be capped to {max_val}"
        if is_percent(coreset_size):
            if coreset_size > MAX_RATIO_CORESET_SIZE_TO_CHUNK_SIZE:
                user_warning(warning_msg(coreset_size, MAX_RATIO_CORESET_SIZE_TO_CHUNK_SIZE))
            return int(n_samples * min(coreset_size, MAX_RATIO_CORESET_SIZE_TO_CHUNK_SIZE))
        elif is_int(coreset_size, positive=True):
            max_val = int(MAX_RATIO_CORESET_SIZE_TO_CHUNK_SIZE * n_samples)
            if coreset_size > max_val:
                user_warning(warning_msg(coreset_size, max_val))
            return min(coreset_size, max_val)
        elif coreset_size is not None:
            raise ValueError(f"Invalid coreset size: {coreset_size}")

    def _transform_seq_params(self, seq_from, seq_to):

        datetime_format = self.data_manager.data_params_internal.seq_datetime_format
        if datetime_format:
            try:
                seq_from = datetime.strptime(seq_from, datetime_format) if seq_from and datetime_format else None
                seq_to = datetime.strptime(seq_to, datetime_format) if seq_to and datetime_format else None
            except TypeError:
                if (isinstance(seq_from, datetime) or seq_from is None) and \
                   (isinstance(seq_to, datetime) or seq_to is None) :
                    pass
                else:
                    raise ValueError
            except ValueError:
                raise ValueError(
                    "When `seq_column` is datetime, `seq_from` and `seq_to` must both be either datetime "
                    "or string in the provided datetime format."
            )

        if seq_from is not None and seq_to is not None and seq_from > seq_to:
            raise ValueError("`seq_to` value must be greater than or equal to `seq_from`.")

        return seq_from, seq_to
