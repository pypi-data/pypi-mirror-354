import numpy as np
from sklearn.tree._tree import TREE_LEAF


def refine_tree(model, X, y, weights=None):
    if weights is None:
        weights = np.ones(len(y))

    leaf_ids = model.apply(X)
    node_idxs_dict = {}
    children = np.where(model.tree_.children_left == TREE_LEAF)[0]
    for t in children:
        node_idxs_dict[t] = np.where(leaf_ids == t)[0]

    for node, idxs in node_idxs_dict.items():
        if len(idxs) > 0:
            idxs = node_idxs_dict[node]
            targets_ = y[idxs]
            w_ = weights[idxs]
            model.tree_.value[node] = [np.average(targets_, weights=w_)]

    return model
