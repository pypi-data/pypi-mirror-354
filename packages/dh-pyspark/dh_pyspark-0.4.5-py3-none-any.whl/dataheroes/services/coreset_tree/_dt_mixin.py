from typing import Optional, Union, Iterable, Callable, Any, Tuple, Dict, List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from ._mixin import ResampleMixin, RefinementMixin
from ..helpers import get_model_name
from ...utils import telemetry

# LGBM / XGB Default number of estimators
N_ESTIMATORS_DEFAULT = 100


class DTMixin(ResampleMixin, RefinementMixin):

    def _fit_internal(
        self,
        X,
        y,
        weights,
        model=None,
        params: Dict = None,
        preprocessing_info: Dict = None,
        sparse_threshold: float = 0.01,
        model_fit_params: Dict = None,
        **model_params,
    ):
        model_params = model_params or dict()
        model_fit_params = model_fit_params or dict()

        # Adjust and get model info
        model_cls_name = get_model_name(model if model is not None else self.model_cls)

        if model_cls_name in ["XGBRegressor", "XGBClassifier"]:
            if model_params.get("tree_method") is None:
                # if user did not set any, use "hist" to avoid possible usage of slower "exact"
                model_params["tree_method"] = "hist"

        if model is None:
            model = self.model_cls(**model_params)
        else:
            model.set_params(**model_params)

        # Get and filter refine and sample based on library and version
        assert "refine" in self.fit_params and "resample" in self.fit_params and "tree_idx" in self.fit_params
        refine = self.fit_params.get("refine", False)
        resample = self.fit_params.get("resample", False)
        tree_idx = self.fit_params.get("tree_idx")
        tree = self.trees[tree_idx]

        model_lib = "other"
        if model_cls_name in ["XGBRegressor", "XGBClassifier"]:
            model_lib = "xgb"
        elif model_cls_name in ["LGBMRegressor", "LGBMClassifier"]:
            model_lib = "lgb"
        elif model_cls_name in ["DecisionTreeRegressor"]:
            model_lib = "sklearn"
        is_clf_booster = model_cls_name in ["XGBClassifier", "LGBMClassifier"]
        if model_lib == "xgb":
            import xgboost as xgb

            if xgb.__version__ >= "1.6.0" and refine:
                from dataheroes.core.training.refinement.xgb import (
                    RefinementCallbackXGB,
                    refine_iteration,
                    refine_iteration_clf,
                )
            else:
                refine = False
        elif model_lib == "lgb":
            import lightgbm as lgb

            if lgb.__version__ >= "3.0.0":
                if refine:
                    from dataheroes.core.training.refinement.lgb import RefinementCallbackLGB, refine_iteration, \
                        refine_iteration_clf
            else:
                refine = False
                resample = False
        elif model_lib == "sklearn":
            resample = False
        else:
            refine = False
            resample = False

        # Refinement and resampling
        if refine:
            X_ref, y_ref, w_ref = self._get_refinement_data(
                tree_idx, model, params, preprocessing_info=preprocessing_info, sparse_threshold=sparse_threshold
            )
            tree_sum_build_indexes = tree.get_tree_sum_build_indexes()
            coreset_size = tree._compose_coreset_size(tree.coreset_size, tree_sum_build_indexes)
            n_refinement_rounds = self._n_refinement_rounds(coreset_size, tree_sum_build_indexes)
            # check if the booster is binary. We'll use y_ref, because it's supposed to be bigger.
            if is_clf_booster:
                is_binary_booster = len(np.unique(y_ref)) == 2
            # check if X_ref is a DataFrame and has categorical columns
            if model_lib == "xgb":
                enable_categorical = (
                        isinstance(X_ref, pd.DataFrame) and len(X_ref.select_dtypes(include="category").columns) > 0
                )
                # Future notice: if XGB's fit fails on feature_names which weren't found, it may be because
                # dmatrix_ref.feature_names is None, while the X is DF and it has column names automatically given
                # to it.
                # If this happens, it may be because until some change was implemented, we were always passing both X
                # and (producing) X_ref as ndarrays; however, maybe X has for some reason been passed as DF. If it did,
                # we may want to revert to making sure it is passed as ndarray - but if we want to retain it as DF,
                # we can, in the init of DMatrix below, pass "feature_names=X.columns.tolist()".
                dmatrix_ref = xgb.DMatrix(data=X_ref, label=y_ref, weight=w_ref, enable_categorical=enable_categorical)
        if resample:
            n_estimators = model.n_estimators if model.n_estimators is not None else N_ESTIMATORS_DEFAULT
            model.set_params(n_estimators=1)
            rounds = min(self._n_resampling_rounds(), n_estimators)
            level = int(params.get("level", 0)) if params is not None else 0
            resample_data = self._get_resample_training_data(
                tree_idx=tree_idx,
                n_iter=rounds,
                level=level,
                model=model,
                params=params,
                preprocessing_info=preprocessing_info,
                sparse_threshold=sparse_threshold,
            )

            def f_fit(model, X, y, w, init_model=None):
                if model_lib == "xgb":
                    # y = y.astype(np.int32)
                    return model.fit(X, y, sample_weight=w, xgb_model=init_model)
                elif model_lib == "lgb":
                    return model.fit(X, y, sample_weight=w, init_model=init_model)
                else:
                    raise ValueError("Unknown model library")

            for i in range(rounds):
                if i == 0:
                    X_fit, y_fit, w_fit = X, y, weights
                else:
                    # account for the first round
                    X_fit, y_fit, w_fit = self._get_resample_iteration_data(resample_data, i - 1)
                # Fit model
                assert model_lib in ["xgb", "lgb"], "Unknown model library"
                model = f_fit(model, X_fit, y_fit, w_fit, init_model=model if i > 0 else None)
                if refine and i < n_refinement_rounds:
                    if model_lib == "xgb":
                        if is_clf_booster:
                            refine_iteration_clf(model.get_booster(), dmatrix_ref, current_iteration=i)
                        else:
                            refine_iteration(model.get_booster(), dmatrix_ref, current_iteration=i)
                    elif model_lib == "lgb":
                        if is_clf_booster:
                            if is_binary_booster:
                                refine_iteration_clf(model.booster_, X_ref, y_ref)
                            else:
                                raise ValueError("Refinement for multi-class LGBMClassifier is not supported.")
                        else:
                            # TODO lightgbm might skip iterations?
                            refine_iteration(model.booster_, X_ref, y_ref)
            if n_estimators - rounds > 0:
                model.set_params(n_estimators=n_estimators - rounds)
                f_fit(model, X_fit, y_fit, w_fit, init_model=model)
            model.set_params(n_estimators=n_estimators)
        elif refine:
            # Special treatment for refinement with callbacks, when possible
            if model_lib == "xgb":
                model_params = model.get_params()
                # Using callbacks may be faster and more accurate.
                cb = RefinementCallbackXGB(
                    dmatrix=dmatrix_ref,
                    model_params=model_params,
                    n_refinement_steps=n_refinement_rounds,
                    is_classification=is_clf_booster,
                )
                if hasattr(model, "callbacks") and model.callbacks is None:
                    model.set_params(callbacks=[cb])
                else:
                    model.callbacks.append(cb)
                model.fit(X=X, y=y, sample_weight=weights, **model_fit_params)
                model.callbacks.pop()
                if len(model.callbacks) == 0:
                    model.callbacks = None
            elif model_lib == "lgb":
                # use callback
                if is_clf_booster and not is_binary_booster:
                    raise ValueError("Refinement for multi-class LGBMClassifier is not supported.")
                cb = RefinementCallbackLGB(
                    X=X_ref, y=y_ref, n_refinement_steps=n_refinement_rounds, is_classification=is_clf_booster
                )
                model.fit(X=X, y=y, sample_weight=weights, callbacks=[cb], **model_fit_params)
            elif model_lib == "sklearn":
                from dataheroes.core.training.refinement.sklearn import refine_tree

                model.fit(X=X, y=y, sample_weight=weights, **model_fit_params)
                model = refine_tree(model, X_ref, y_ref, w_ref)
        else:
            model.fit(X, y, sample_weight=weights, **model_fit_params)

        return model

    def _set_fit_params(self, **params):
        if not hasattr(self, "fit_params"):
            self.fit_params = {}
        enhancement = params.get("enhancement", 0)
        if enhancement == 0:
            resample, refine = False, False
        elif enhancement == 1:
            resample, refine = False, True
        elif enhancement == 2:
            resample, refine = True, False
        elif enhancement == 3:
            resample, refine = True, True
        else:
            raise ValueError(f"`enhancement` must be a value from [0, 1, 2, 3], found {enhancement}")

        self.fit_params.update({"resample": resample, "refine": refine, "tree_idx": params.get("tree_idx", 0)})

    @telemetry
    def fit(
        self,
        tree_idx: int = 0,
        level: int = 0,
        seq_from: Any = None,
        seq_to: Any = None,
        enhancement: int = 0,
        model: Any = None,
        preprocessing_stage: Union[str, None] = None,
        sparse_threshold: float = 0.01,
        model_fit_params: Optional[dict] = None,
        **model_params,
    ):
        """
        Fit a model on the coreset tree.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted. 
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: Defines the depth level of the tree from which the coreset is extracted.
                Level 0 returns the coreset from the head of the tree with around coreset_size samples.
                Level 1 returns the coreset from the level below the head of the tree with around twice of the samples compared to level 0, etc.
                If the passed level is greater than the maximal level of the tree, the maximal available level is used.
            seq_from: string/datetime, optional
                The starting sequence of the training set.
            seq_to: string/datetime, optional
                The ending sequence of the training set.
            enhancement: int (0-3), optional, default 0 (no enhancement).
                Enhance the default decision tree based training.
                Can improve the strength of the model, but will increase the training run time.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                Default: instantiate the service model class using input model_params.
            preprocessing_stage: string, optional, default `user` when CatBoost is used, `auto` otherwise.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            model_fit_params: dict, optional, default None.
                Parameters passed to the model's fit function.
            model_params: Model hyperparameters kwargs.
                Input when instantiating default model class.

        Returns:
            Fitted estimator.
        """
        self._set_fit_params(enhancement=enhancement, tree_idx=tree_idx)
        preprocessing_stage = self._get_default_preprocessing_stage(preprocessing_stage, model)
        return super().fit(
            tree_idx=tree_idx,
            level=level,
            seq_from=seq_from,
            seq_to=seq_to,
            model=model,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            model_fit_params=model_fit_params,
            **model_params,
        )

    @telemetry
    def grid_search(
        self,
        param_grid: Union[Dict[str, List], List[Dict[str, List]]],
        tree_indices: Optional[List[int]] = None,
        level: Optional[int] = None,
        validation_method: str = "cross validation",
        model: Any = None,
        model_fit_params: Optional[dict] = None,
        scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
        refit: bool = True,
        verbose: int = 0,
        preprocessing_stage: Union[str, None] = None,
        sparse_threshold: float = 0.01,
        enhancement: int = 0,
        error_score: Union[str, float, int] = np.nan,
        validation_size: float = 0.2,
        seq_train_from: Any = None,
        seq_train_to: Any = None,
        seq_validate_from: Any = None,
        seq_validate_to: Any = None,
        n_jobs: int = None,
    ) -> Union[Tuple[Dict, pd.DataFrame, BaseEstimator], Tuple[Dict, pd.DataFrame]]:
        """
        A method for performing hyperparameter selection by grid search, using the coreset tree.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            param_grid: dict or list of dicts.
                Dictionary with parameters names (str) as keys and lists of parameter settings to try as values, or a list of such dictionaries, in which case the grids
                spanned by each dictionary in the list are explored. This enables searching over any sequence of parameter settings.
            tree_indices:
                Defines the indices of the trees on which the grid search will be performed. By default, grid search is run on all trees.
            level: int, optional.
                The level of the tree on which the training and validation will be performed.
                If None, the best level will be selected.
            validation_method: str, optional.
                Indicates which validation method will be used. The possible values are 'cross validation', 'hold-out validation' and 'seq-dependent validation'.
                If 'cross validation' is selected, the process involves progressing through folds. We first train and validate all hyperparameter
                combinations for each fold, before moving on to the subsequent folds.
            model: A Scikit-learn compatible model instance, optional.
                The model class needs to implement the usual scikit-learn interface.
            model_fit_params: dict, optional, default None.
                Parameters passed to the model's fit function.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            refit: bool, optional.
                If True, retrain the model on the whole coreset using the best found hyperparameters, and return the model.
            verbose: int, optional.
                Controls the verbosity: the higher, the more messages.
                    >=1 : the computation time for each fold and parameter candidate is displayed;
                    >=2 : the score is also displayed;
                    >=3 : starting time of the computation is also displayed.
            preprocessing_stage: string, optional, default `user` when CatBoost is used, `auto` otherwise.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            enhancement: int (0-3), optional, default 0 (no enhancement).
                Enhance the default decision tree based training.
                Can improve the strength of the model, but will increase the training run time.
            error_score: "raise" or numeric, optional.
                Value to assign to the score if an error occurs in model training. If set to "raise", the error is raised. If a numeric value is given,
                FitFailedWarning is raised. This parameter does not affect the refit step, which will always raise the error.
            validation_size: float, optional, default 0.2.
                The size of the validation set, as a percentage of the training set size for hold-out validation.
            seq_train_from: Any, optional.
                The starting sequence of the training set for seq-dependent validation.
            seq_train_to: Any, optional.
                The ending sequence of the training set for seq-dependent validation.
            seq_validate_from: Any, optional.
                The starting sequence number of the validation set for seq-dependent validation.
            seq_validate_to: Any, optional.
                The ending sequence number of the validation set for seq-dependent validation.
            n_jobs: int, optional.
                Default: number of CPUs. Number of jobs to run in parallel during grid search.

        Returns:
            A dict with the best hyperparameters setting, among those provided by the user. The keys are the hyperparameters names, while the dicts' values are the hyperparameters values.
            The tree index of the Coreset tree on which the best hyperparameters where found. 
            A Pandas DataFrame holding the score for each hyperparameter combination and fold. For the 'cross validation' method the average across all folds for each hyperparameter combination is included too. 
            If refit=True, the retrained model is also returned.                
        """
        self._set_fit_params(enhancement=enhancement)
        preprocessing_stage = self._get_default_preprocessing_stage(preprocessing_stage, model)
        return super().grid_search(
            param_grid=param_grid,
            tree_indices=tree_indices,
            level=level,
            validation_method=validation_method,
            model=model,
            model_fit_params=model_fit_params,
            scoring=scoring,
            refit=refit,
            verbose=verbose,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            error_score=error_score,
            validation_size=validation_size,
            seq_train_from=seq_train_from,
            seq_train_to=seq_train_to,
            seq_validate_from=seq_validate_from,
            seq_validate_to=seq_validate_to,
            n_jobs=n_jobs,
        )

    @telemetry
    def cross_validate(
        self,
        tree_idx: int = 0,
        level: Optional[int] = None,
        model: Any = None,
        scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
        return_model: bool = False,
        verbose: int = 0,
        preprocessing_stage: Union[str, None] = None,
        sparse_threshold: float = 0.01,
        enhancement: int = 0,
        model_fit_params: Optional[dict] = None,
        **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        Method for cross-validation on the coreset tree.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional.
                The level of the tree on which the training and validation will be performed.
                If None, the best level will be selected.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                The model class needs to implement the usual scikit-learn interface.
                Default: instantiate the service model class using input model_params.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            return_model: bool, optional.
                If True, the trained model is also returned.
            verbose: int, optional.
                Controls the verbosity: the higher, the more messages.
                    >=1 : the computation time for each fold is displayed;
                    >=2 : the score is also displayed;
                    >=3 : starting time of the computation is also displayed.
            preprocessing_stage: string, optional, default `user` when CatBoost is used, `auto` otherwise.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            enhancement: int (0-3), optional, default 0 (no enhancement).
                Enhance the default decision tree based training.
                Can improve the strength of the model, but will increase the training run time.
            model_fit_params: dict, optional, default None.
                Parameters passed to the model's fit function.
            model_params: kwargs, optional.
                The hyper-parameters of the model. If not provided, the default values are used.

        Returns:
            A list of scores, one for each fold. If return_model=True, a list of trained models is also returned (one model for each fold).
        """
        self._set_fit_params(enhancement=enhancement)
        preprocessing_stage = self._get_default_preprocessing_stage(preprocessing_stage, model)

        return super().cross_validate(
            tree_idx=tree_idx,
            level=level,
            model=model,
            scoring=scoring,
            return_model=return_model,
            verbose=verbose,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            model_fit_params=model_fit_params,
            **model_params,
        )

    @telemetry
    def holdout_validate(
        self,
        tree_idx: int = 0,
        level: Optional[int] = None,
        validation_size: float = 0.2,
        model: Any = None,
        model_fit_params: Optional[dict] = None,
        scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
        return_model: bool = False,
        verbose: int = 0,
        preprocessing_stage: Union[str, None] = None,
        sparse_threshold: float = 0.01,
        enhancement: int = 0,
        **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        A method for hold-out validation on the coreset tree.
        The validation set is always the last part of the dataset.
        This function is only applicable in case the coreset tree was optimized_for `training`.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional.
                The level of the tree on which the training and validation will be performed.
                If None, the best level will be selected.
            validation_size: float, optional.
                The percentage of the dataset that will be used for validating the model.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                The model class needs to implement the usual scikit-learn interface.
                Default: instantiate the service model class using input model_params.
            model_fit_params: dict, optional, default None.
                Parameters passed to the model's fit function.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            return_model: bool, optional.
                If True, the trained model is also returned.
            verbose: int, optional.
                Controls the verbosity: the higher, the more messages.
                    >=1 : the training and validation time is displayed;
                    >=2 : the validation score is also displayed;
                    >=3 : starting time of the computation is also displayed.
            preprocessing_stage: string, optional, default `user` when CatBoost is used, `auto` otherwise.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            enhancement: int (0-3), optional, default 0 (no enhancement).
                Enhance the default decision tree based training.
                Can improve the strength of the model, but will increase the training run time.
            model_params: kwargs, optional.
                The hyper-parameters of the model. If not provided, the default values are used.

        Returns:
            The validation score. If return_model=True, the trained model is also returned.
        """
        self._set_fit_params(enhancement=enhancement)
        preprocessing_stage = self._get_default_preprocessing_stage(preprocessing_stage, model)
        return super().holdout_validate(
            tree_idx=tree_idx,
            level=level,
            validation_size=validation_size,
            model=model,
            model_fit_params=model_fit_params,
            scoring=scoring,
            return_model=return_model,
            verbose=verbose,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            **model_params,
        )

    @telemetry
    def seq_dependent_validate(
        self,
        tree_idx: int = 0,
        level: int = None,
        seq_train_from: Any = None,
        seq_train_to: Any = None,
        seq_validate_from: Any = None,
        seq_validate_to: Any = None,
        model: Any = None,
        scoring: Union[str, Callable[[BaseEstimator, np.ndarray, np.ndarray], float]] = None,
        return_model: bool = False,
        verbose: int = 0,
        preprocessing_stage: Union[str, None] = None,
        sparse_threshold: float = 0.01,
        enhancement: int = 0,
        model_fit_params: Optional[dict] = None,
        **model_params,
    ) -> Union[List[float], Tuple[List[float], List[BaseEstimator]]]:
        """
        The method allows to train and validate on a subset of the Coreset tree, according to the `seq_column` defined
        in the `DataParams` structure passed to the init.
        This function is only applicable in case the coreset tree was optimized_for `training`.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional.
                The level of the tree from which the search for the best matching nodes starts. Nodes closer to the
                leaf level than the specified level, may be selected to better match the provided seq parameters.If
                None, the search starts from level 0, the head of the tree.
                If None, the best level will be selected.
            seq_train_from: Any, optional.
                The starting sequence of the training set.
            seq_train_to: Any, optional.
                The ending sequence of the training set.
            seq_validate_from: Any, optional.
                The starting sequence number of the validation set.
            seq_validate_to: Any, optional.
                The ending sequence number of the validation set.
            model: A Scikit-learn compatible model instance, optional.
                When provided, model_params are not relevant.
                The model class needs to implement the usual scikit-learn interface.
                Default: instantiate the service model class using input model_params.
            scoring: callable or string, optional.
                If it is a callable object, it must return a scalar score. The signature of the call is (model, X, y),
                where model is the ML model to be evaluated, X is the data and y is the ground truth labeling.
                For example, it can be produced using [sklearn.metrics.make_scorer](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html).
                If it is a string, it must be a valid name of a Scikit-learn [scoring method](https://scikit-learn.org/stable/modules/model_evaluation.html)
                If None, the default scorer of the current model is used.
            return_model: bool, optional.
                If True, the trained model is also returned.
            verbose: int, optional.
                Controls the verbosity: the higher, the more messages.
                    >=1 : The number of hyperparameter combinations to process at the start and the time it took, best hyperparameters found and their score at the end.
                    >=2 : The score and time for each hyperparameter combination.
            preprocessing_stage: string, optional, default `user` when CatBoost is used, `auto` otherwise.<br/><br/>
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including one-hot-encoding,
                converting Boolean fields to numeric, etc.
            sparse_threshold: float, optional, default 0.01. Creates a sparse matrix from the features (X),
                if the data density after preprocessing is below sparse_threshold, otherwise, will create an array.
                (Applicable only for preprocessing_stage='auto').
            enhancement: int (0-3), optional, default 0 (no enhancement).
                Enhance the default decision tree based training.
                Can improve the strength of the model, but will increase the training run time.
            model_fit_params: dict, optional, default None.
                Parameters passed to the model's fit function.
            model_params: kwargs, optional.
                The hyper-parameters of the model. If not provided, the default values are used.

        Returns:
            The validation score. If return_model=True, the trained model is also returned.
        """
        self._set_fit_params(enhancement=enhancement)
        preprocessing_stage = self._get_default_preprocessing_stage(preprocessing_stage, model)
        return super().seq_dependent_validate(
            tree_idx=tree_idx,
            level=level,
            seq_train_from=seq_train_from,
            seq_train_to=seq_train_to,
            seq_validate_from=seq_validate_from,
            seq_validate_to=seq_validate_to,
            model=model,
            model_fit_params=model_fit_params,
            scoring=scoring,
            return_model=return_model,
            verbose=verbose,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            **model_params,
        )