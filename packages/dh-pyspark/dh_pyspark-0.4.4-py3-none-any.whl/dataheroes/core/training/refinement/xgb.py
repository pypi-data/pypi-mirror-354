from typing import List, Union
import json
import numpy as np
from scipy.special import softmax
from datetime import date, datetime, timedelta
import xgboost as xgb


class NpEncoder(json.JSONEncoder):
    """
    Encoding of many numpy types is not supported by json library - specifically, we've had a failure on np.float32.
    We use one of the solutions suggested online to support JSON encoding.
    This solution strives to cover all types, but we may reduce it to handle only the float32 type - if we want to
    be more conservative (until we encounter a failure with a new type).
    What we use is taken from here: https://codetinkering.com/numpy-encoder-json/
    See more details here:
    https://github.com/numpy/numpy/issues/16432
    https://ellisvalentiner.com/post/serializing-numpyfloat32-json/
    https://stackoverflow.com/questions/53082708/typeerror-object-of-type-float32-is-not-json-serializable
    https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
    https://bobbyhadz.com/blog/python-typeerror-object-of-type-int64-is-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.floating, np.complexfloating)):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.string_):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return str(obj)
        return super(NpEncoder, self).default(obj)


def get_split_conditions(booster: xgb.Booster, tree_idx: int) -> List:
    b_raw = booster.save_raw(raw_format="json")
    b_json = json.loads(b_raw)
    return b_json["learner"]["gradient_booster"]["model"]["trees"][tree_idx]["split_conditions"]


def set_split_conditions(
    split_conditions: List[float],
    booster: xgb.Booster,
    tree_idx: int,
    copy: bool = False,
) -> xgb.Booster:
    b_raw = booster.save_raw(raw_format="json")
    b_json = json.loads(b_raw)
    old_sc = b_json["learner"]["gradient_booster"]["model"]["trees"][tree_idx]["split_conditions"]
    if len(old_sc) != len(split_conditions):
        raise ValueError("Length of old split conditions must match the length of new split conditions")
    b_json["learner"]["gradient_booster"]["model"]["trees"][tree_idx]["split_conditions"] = split_conditions

    if copy:
        return xgb.Booster(model_file=bytearray(json.dumps(b_json, cls=NpEncoder).encode()))
    else:
        booster.load_model(bytearray(json.dumps(b_json, cls=NpEncoder).encode()))
        return booster


def refine_iteration(
    booster: xgb.Booster,
    dmatrix: xgb.DMatrix,
    current_iteration: int = None,
):
    """
    Main function:
    Given a tree model and the data X, y, sets leaf values to the optimal values
    that are calculated by applying leaf_optimal_func to all labels assigned
    to a leaf
    """
    if current_iteration is None:
        # current_iteration = booster.best_iteration
        current_iteration = booster.num_boosted_rounds() - 1
    weights = dmatrix.get_weight()
    y = dmatrix.get_label()
    if len(weights) == 0:
        weights = np.ones(len(y))
    # Get last tree
    config = json.loads(booster.save_config())
    if xgb.__version__ >= "2.0.0":
        lr = np.float32(config["learner"]["gradient_booster"]["tree_train_param"]["learning_rate"])
        reg_alpha = np.float32(config["learner"]["gradient_booster"]["tree_train_param"]["reg_alpha"])
        reg_lambda = np.float32(config["learner"]["gradient_booster"]["tree_train_param"]["reg_lambda"])
    else:
        updater = config["learner"]["gradient_booster"]["updater"]
        if "grow_colmaker" in updater:
            lr = np.float32(updater["grow_colmaker"]["train_param"]["learning_rate"])
            reg_alpha = np.float32(updater["grow_colmaker"]["train_param"]["reg_alpha"])
            reg_lambda = np.float32(updater["grow_colmaker"]["train_param"]["reg_lambda"])
        elif "grow_quantile_histmaker" in updater:
            lr = np.float32(updater["grow_quantile_histmaker"]["train_param"]["learning_rate"])
            reg_alpha = np.float32(updater["grow_quantile_histmaker"]["train_param"]["reg_alpha"])
            reg_lambda = np.float32(updater["grow_quantile_histmaker"]["train_param"]["reg_lambda"])
        else:
            raise ValueError("Can't find hyperparameters")
            # warnings.warn("Can't find hyperparameters, using default")
            lr = 0.3
            reg_alpha = 0
            reg_lambda = 1
    subbooster = booster[current_iteration]
    if xgb.__version__ >= "1.6.0":
        b_json = json.loads(subbooster.save_raw(raw_format="json"))
    else:
        raise ValueError("Refinement not supported on versions older than 1.6.0")
    trees = b_json["learner"]["gradient_booster"]["model"]["trees"]
    last_tree = trees[-1]  # equiv to trees[0] when a booster contains 1 tree
    children = [i for i in range(len(last_tree["parents"])) if i not in last_tree["parents"]]
    base_score = np.float32(b_json["learner"]["learner_model_param"]["base_score"])

    leaf_ids = subbooster.predict(dmatrix, pred_leaf=True)
    node_idxs_dict = {}
    for t in children:
        node_idxs_dict[t] = np.where(leaf_ids == t)[0]

    if current_iteration == 0:
        targets = y - base_score
    else:
        targets = y - booster.predict(dmatrix, iteration_range=(0, current_iteration))
    for node, idxs in node_idxs_dict.items():
        if len(idxs) > 0:
            idxs = node_idxs_dict[node]
            targets_ = targets[idxs]
            w_ = weights[idxs]
            # TODO is this good?
            # remove all nan, inf and -inf values from targets
            targets_ = targets_[~(np.isnan(targets_) | np.isinf(targets_) | np.isneginf(targets_))]
            v = np.sum(targets_ if w_ is None else targets_ * w_)
            if v > reg_alpha:
                v -= reg_alpha
            else:
                v += reg_alpha
            v = v / (len(targets_) + reg_lambda) * lr
            last_tree["split_conditions"][node] = v

    # Set values
    new_sc = last_tree["split_conditions"]
    set_split_conditions(split_conditions=new_sc, booster=booster, tree_idx=current_iteration, copy=False)


def refine_iteration_clf(
    booster: xgb.Booster,
    dmatrix: xgb.DMatrix,
    current_iteration: int = None,
):
    """
    Main function:
    Given a tree model and the data X, y, sets leaf values to the optimal values
    that are calculated by applying leaf_optimal_func to all labels assigned
    to a leaf
    """
    if current_iteration is None:
        # current_iteration = booster.best_iteration
        current_iteration = booster.num_boosted_rounds() - 1
    weights = dmatrix.get_weight()
    y = dmatrix.get_label().astype(int)
    if len(weights) == 0:
        weights = np.ones(len(y))
    # Get last tree
    config = json.loads(booster.save_config())
    if xgb.__version__ >= "2.0.0":
        lr = np.float32(config["learner"]["gradient_booster"]["tree_train_param"]["learning_rate"])
        reg_alpha = np.float32(config["learner"]["gradient_booster"]["tree_train_param"]["reg_alpha"])
        reg_lambda = np.float32(config["learner"]["gradient_booster"]["tree_train_param"]["reg_lambda"])
    else:
        updater = config["learner"]["gradient_booster"]["updater"]
        if "grow_colmaker" in updater:
            lr = np.float32(updater["grow_colmaker"]["train_param"]["learning_rate"])
            reg_alpha = np.float32(updater["grow_colmaker"]["train_param"]["reg_alpha"])
            reg_lambda = np.float32(updater["grow_colmaker"]["train_param"]["reg_lambda"])
        elif "grow_quantile_histmaker" in updater:
            lr = np.float32(updater["grow_quantile_histmaker"]["train_param"]["learning_rate"])
            reg_alpha = np.float32(updater["grow_quantile_histmaker"]["train_param"]["reg_alpha"])
            reg_lambda = np.float32(updater["grow_quantile_histmaker"]["train_param"]["reg_lambda"])
        else:
            raise ValueError("Can't find hyperparameters")
            # warnings.warn("Can't find hyperparameters, using default")
            lr = 0.3
            reg_alpha = 0
            reg_lambda = 1

    subbooster = booster[current_iteration]
    b_json = json.loads(subbooster.save_raw(raw_format="json"))
    trees = b_json["learner"]["gradient_booster"]["model"]["trees"]
    leaves_all = [[i for i in range(len(tree["parents"])) if i not in tree["parents"]] for tree in trees]

    # (n_samples, n_boosters, n_trees, 1)
    # where n_boosters = 1 because subbooster is a single booster iteration and n_trees = n_classes
    leaf_preds = subbooster.predict(dmatrix, pred_leaf=True, strict_shape=True)
    leaf_preds = leaf_preds[:, 0, :, 0]
    if len(trees) == 1: # binary classification
        y_ohe = np.atleast_2d(y).T
        ct = 1
    else:
        y_ohe = np.eye(np.max(y) + 1)[y]
        ct = 2
    if current_iteration == 0:
        # softmax over n_classes
        base_score_p = 1 / 2 if len(trees) == 1 else 1 / len(trees)
        grad = base_score_p - y_ohe
        hess = ct * base_score_p * (1 - base_score_p) * np.ones_like(y_ohe)
    else:
        # (n_samples, n_trees)
        if len(trees) > 1:
            p = softmax(booster[:current_iteration].predict(dmatrix, output_margin=True, strict_shape = True), axis = 1)
        else:
            p = booster[:current_iteration].predict(dmatrix, strict_shape=True)  # probabilities
        grad = p - y_ohe
        hess = ct * p * (1 - p)
    # Computing for all trees at once doesn't work, because trees might have diferent structures
    sc_all = [trees[i]["split_conditions"] for i in range(len(trees))]
    for i, (tree, leaves) in enumerate(zip(trees, leaves_all)):
        for leaf in leaves:
            leaf_ids = np.where(leaf_preds[:, i] == leaf)[0]
            g_sum = grad[leaf_ids, i].sum()
            if g_sum > reg_alpha:
                g_sum -= reg_alpha
            else:
                g_sum += reg_alpha
            # g_sum = g_sum - reg_alpha * np.sign(g_sum - reg_alpha)
            h_sum = hess[leaf_ids, i].sum()
            sc_all[i][leaf] = -g_sum / (h_sum + reg_lambda) * lr

    b_json = json.loads(booster.save_raw(raw_format="json"))
    for i, sc in enumerate(sc_all):
        b_json["learner"]["gradient_booster"]["model"]["trees"][current_iteration * len(trees) + i][
            "split_conditions"
        ] = sc
    booster.load_model(bytearray(json.dumps(b_json, cls=NpEncoder).encode()))


class RefinementCallbackXGB(xgb.callback.TrainingCallback):
    def __init__(
        self, dmatrix, model_params, n_refinement_steps: Union[int, str] = "all", is_classification: bool = False
    ):
        self.dmatrix = dmatrix
        self.model_params = model_params
        self.n_refinement_steps = n_refinement_steps
        self.is_classification = is_classification
        super().__init__()

    def after_iteration(self, model, epoch, evals_log):
        if self.n_refinement_steps == "all" or epoch < self.n_refinement_steps and epoch < model.num_boosted_rounds():
            if self.is_classification:
                refine_iteration_clf(
                    model,
                    self.dmatrix,
                    current_iteration=epoch,
                )
            else:
                refine_iteration(
                    model,
                    self.dmatrix,
                    current_iteration=epoch,
                )
        model.set_param(self.model_params)
