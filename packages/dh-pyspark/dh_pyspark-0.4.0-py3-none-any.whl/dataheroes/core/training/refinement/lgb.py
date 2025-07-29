from typing import Union
import ctypes
import lightgbm as lgb
import numpy as np


def lgb_set_leaf_output(self, tree_id: int, leaf_id: int, value: float) -> lgb.Booster:
    lgb.basic._safe_call(
        lgb.basic._LIB.LGBM_BoosterSetLeafValue(
            self.handle, ctypes.c_int(tree_id), ctypes.c_int(leaf_id), ctypes.c_double(value)
        )
    )
    return self


def refine_iteration(
    booster: lgb.Booster,
    X,
    y,
    weights=None,
    current_iteration: int = None,
):
    """
    Main function:
    Given a tree model and the data X, y, sets leaf values to the optimal values
    that are calculated by averaging all labels assigned
    to a leaf
    """
    if current_iteration is None:
        current_iteration = booster.current_iteration() - 1
    num_leaves = booster.dump_model(start_iteration=current_iteration, num_iteration=1)["tree_info"][0]["num_leaves"]
    lr = booster.params["learning_rate"]
    reg_lambda = booster.params["reg_lambda"]
    reg_alpha = booster.params["reg_alpha"]

    predicted_leaves = booster.predict(X, start_iteration=current_iteration, num_iteration=1, pred_leaf=True)
    if current_iteration == 0:
        targets = y
    else:
        targets = y - booster.predict(X, start_iteration=0, num_iteration=current_iteration)

    for leaf_id in range(num_leaves):
        idxs = np.where(predicted_leaves == leaf_id)[0]
        if len(idxs) > 0:
            targets_ = targets[idxs]
            w_ = weights[idxs] if weights is not None else None
            # TODO is this good?
            # remove all nan, inf and -inf values from targets
            targets_ = targets_[~(np.isnan(targets_) | np.isinf(targets_) | np.isneginf(targets_))]
            if len(targets_) >= 0:
                v = np.sum(targets_ if w_ is None else targets_ * w_)
                if v > reg_alpha:
                    v -= reg_alpha
                else:
                    v += reg_alpha
                v = v / (len(targets_) + reg_lambda) * lr
            else:
                v = 0
            if lgb.__version__ < "4.0.0":
                lgb_set_leaf_output(booster, tree_id=current_iteration, leaf_id=leaf_id, value=v)
            else:
                booster.set_leaf_output(
                    tree_id=current_iteration,
                    leaf_id=leaf_id,
                    value=v,
                )


def refine_iteration_clf(
    booster: lgb.Booster,
    X,
    y,
    weights=None,
    current_iteration: int = None,
):
    """
    Main function:
    Given a tree model and the data X, y, sets leaf values to the optimal values
    that are calculated by applying leaf_optimal_func to all labels assigned
    to a leaf
    """
    if current_iteration is None:
        current_iteration = booster.current_iteration() - 1
    tree_info = booster.dump_model(start_iteration=current_iteration, num_iteration=1)[
        "tree_info"
    ]
    num_leaves_all = [t["num_leaves"] for t in tree_info]
    num_trees = len(tree_info)

    lr = booster.params["learning_rate"]
    reg_lambda = booster.params["reg_lambda"]
    reg_alpha = booster.params["reg_alpha"]

    leaf_preds = booster.predict(
        X, start_iteration=current_iteration, num_iteration=1, pred_leaf=True
    )
    if leaf_preds.ndim == 1:
        leaf_preds = leaf_preds[:, None]
    if num_trees == 1:
        y_ohe = np.atleast_2d(y).T
        ct = 1
    else:
        y_ohe = np.eye(np.max(y) + 1)[y]
        ct = 2
    if current_iteration == 0:
        # softmax over n_classes
        p = 1 / 2 if num_trees == 1 else 1 / num_trees
        grad = p - y_ohe
        hess = ct * p * (1 - p) * np.ones_like(y_ohe)
    else:
        p = booster.predict(X, start_iteration=0, num_iteration=current_iteration)
        if p.ndim == 1:
            p = p[:, None]
        grad = p - y_ohe
        hess = ct * p * (1 - p)
    for tree_id in range(num_trees):
        for leaf_id in range(num_leaves_all[tree_id]):
            leaf_ids = np.where(leaf_preds[:, tree_id] == leaf_id)[0]
            g_sum = np.sum(grad[leaf_ids, tree_id])
            h_sum = np.sum(hess[leaf_ids, tree_id])
            if g_sum > reg_alpha:
                g_sum -= reg_alpha
            else:
                g_sum += reg_alpha
            v = -g_sum / (h_sum + reg_lambda) * lr
            if lgb.__version__ < "4.0.0":
                lgb_set_leaf_output(
                    booster,
                    tree_id=current_iteration * num_trees + tree_id,
                    leaf_id=leaf_id,
                    value=v,
                )
            else:
                booster.set_leaf_output(
                    tree_id=current_iteration * num_trees + tree_id,
                    leaf_id=leaf_id,
                    value=v,
                )

class RefinementCallbackLGB:
    def __init__(
        self, X, y, sample_weight=None, n_refinement_steps: Union[int, str] = "all", is_classification: bool = False
    ):
        self.X = X
        self.y = y
        self.weights = sample_weight
        self.n_refinement_steps = n_refinement_steps
        self.is_classification = is_classification

    def __call__(self, env):
        booster = env.model
        epoch = env.iteration
        if (
            self.n_refinement_steps == "all" or epoch < self.n_refinement_steps
        ) and epoch < env.model.current_iteration():
            if self.is_classification:
                # TODO don't clf refine outside binary clf
                refine_iteration_clf(booster, X=self.X, y=self.y, weights=self.weights, current_iteration=epoch)
            else:
                refine_iteration(booster, X=self.X, y=self.y, weights=self.weights, current_iteration=epoch)
