from typing import Any, Dict, Iterator, List, Tuple, Optional, Union

import numpy as np
import pandas as pd
from pandas import CategoricalDtype
from sklearn.utils.extmath import weighted_mode

from .helpers import _get_inf_nan_indexes, _update_n_represents, get_feature_slice
from ..core.numpy_extra import unique
from ..core.sklearn_extra.array_encoder import WeightedArrayEncoder
from ..core.sklearn_extra._target_encoder import TargetEncoder
from ..core.sklearn_extra.column_transformer import WeightedColumnTransformer
from ..core.sklearn_extra.preprocessing import WeightedOHE
from ..core.coreset.common import is_percent, is_int
from ..utils import user_warning
from ..services.common import CategoricalEncoding, PreprocessingParams, CATEGORICAL_INFREQUENT

CAT_T = "c"


def preprocess_data_ohe(
    X,
    *,
    ohe_used_categories: Dict,
    te_used_categories: Dict,
    missing_values: Dict,
    removed_columns: List,
    categories_as_str: bool = True,
    columns_given_as_index: bool = False,
    copy=False,
):
    """
    TODO
     As of today, we only support OHE by employing the "get_dummies" below; however, for the TE/MIXED, we will need
     to do more effort and to actually Target-Encode the TE-group's features.
     As long as this support is not implemented, this method remains incomplete.
     Once we add this implementation, we will need to remove the NotImplementedError guard before calling this
     method in EstimationMixin.
    """
    # From orig to encoded
    if copy:
        X = X.copy()
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)

    # If columns were given as index remake the config as dictionaries
    if columns_given_as_index:
        ohe_used_categories = {X.columns[k]: v for k, v in ohe_used_categories.items()}
        te_used_categories = {X.columns[k]: v for k, v in te_used_categories.items()}
        missing_values = {X.columns[k]: v for k, v in missing_values.items()}
        removed_columns = [X.columns[k] for k in removed_columns]

    X.drop(columns=removed_columns, inplace=True)
    X.fillna(value=missing_values, inplace=True)
    cat_cols = [c for c in ohe_used_categories.keys() if c not in removed_columns]
    used_cols = [c for c in X.columns if c not in removed_columns]

    for col in cat_cols:
        if categories_as_str:
            X[col] = X[col].astype(str)
        else:
            # nan is still represented as str
            X[col] = X[col].fillna(value="nan")
        X[col] = X[col].where(X[col].isin(ohe_used_categories[col]), CATEGORICAL_INFREQUENT)
        X[col] = X[col].astype(pd.CategoricalDtype(categories=ohe_used_categories[col]))

    column_order = []
    for col in cat_cols:
        for category in ohe_used_categories[col]:
            column_order.append(f"{col}_{category}")
    for col in used_cols:
        if col not in ohe_used_categories:
            column_order.append(col)
    X_prep = pd.get_dummies(data=X, columns=cat_cols)
    X_prep = X_prep[column_order]
    return X_prep


class DataAutoProcessor:
    def __init__(
            self,
            X,
            y=None,
            weight=None,
            ind=None,
            props=None,
            feature_names: List = None,
            feature_types: List = None,
            categorical_features: List = None,
            array_features: List = None,
            categorical_threshold: Union[int, float, Dict[Any, Union[int, float]]] = None,
            cat_encoding_config: Dict = None,
            array_encoding_config: Dict = None,
            drop_rows_below: float = 0,
            drop_cols_above: float = 1,
            missing_replacement: list = None,
            is_classification: bool = True,
            missing_values_params: dict = None,
            calc_replacements: bool = False,
            lazy = False,
            class_weights: dict = None,
    ):

        # This should not copy data
        self.X = X
        self.y = y
        self.X_processed = X
        self.weight = weight
        self.ind = ind
        self.props = props
        self.feature_types = feature_types
        self.feature_names = feature_names
        self.feature_names_original = feature_names.copy() if feature_names else None
        self.categorical_features = categorical_features
        self.array_features = array_features if array_features is not None else []
        self.categorical_threshold = categorical_threshold
        self.cat_encoding_config = cat_encoding_config if cat_encoding_config is not None else {}
        self.array_encoding_config = array_encoding_config if array_encoding_config is not None else {}
        self.cat_features_idxs_ohe = None
        self.cat_features_idxs_te = None
        self.preprocessor = None
        self.drop_rows_below = drop_rows_below
        self.drop_cols_above = drop_cols_above
        self.missing_replacement = missing_replacement
        self.removed_rows = np.array([], dtype=int)
        self.removed_features = []
        self.is_classification = is_classification
        self.has_missing_values_params = True if missing_values_params is not None else False
        self.missing_values_params = {'features': {}} if missing_values_params is None else missing_values_params
        self.calc_replacements = calc_replacements
        self.n_represents_diff = {} if is_classification else 0
        self.class_weights = class_weights

        if not lazy:
            self._post_init(
                X=X,
                y=y,
                weight=weight,
                ind=ind,
                props=props,
                feature_names=feature_names,
                feature_types=feature_types,
                categorical_features=categorical_features,
                categorical_threshold=categorical_threshold,
                cat_encoding_config=cat_encoding_config
            )

    def _post_init(
            self,
            X,
            y=None,
            weight=None,
            ind=None,
            *,
            props=None,
            feature_names: List = None,
            feature_types: List = None,
            categorical_features: List = None,
            categorical_threshold: Union[
                int, float, Dict[Any, Union[int, float]]
            ] = None,
            cat_encoding_config=None,
    ):
        # When CategoricalEncoding is Nothing so we're in the Analytics use case, we need to consider all
        # columns as categorical.
        if self.cat_encoding_config and self.cat_encoding_config[CategoricalEncoding.ENCODING_METHOD_KEY] == CategoricalEncoding.NOTHING:
                categorical_features = list(range(X.shape[1]))

        if feature_names and categorical_features and feature_types is None:
            feature_types = [CAT_T if i in categorical_features else float for i in range(len(feature_names))]

        self.X, self.feature_names, self.feature_types = self._init_data(
            X, feature_names=feature_names, feature_types=feature_types
        )
        # If X was DataFrame - in the call before, it is implicitly converted to ndarray. If it does, we must convert
        # X_processed to it as well (rather, refresh the pointer to the new X).
        self.X_processed = self.X
        self.feature_types_original = self.feature_types.copy()
        self.feature_types = _find_categorical_types(
            self.X,
            feature_names=self.feature_names,
            feature_types=self.feature_types,
            categorical_features=categorical_features,
            categorical_threshold=categorical_threshold,
        )

        self.categorical_features = categorical_features
        self.categorical_threshold = categorical_threshold

        self.n_samples, self.n_features = _check_data_shape(self.X)

        self.y = self._init_labels(y)
        self.weight = self._init_weight(weight)
        self.ind = ind if ind is not None else self.ind
        self.props = props if props is not None else self.props
        self.cat_encoding_config = cat_encoding_config if cat_encoding_config is not None else self.cat_encoding_config

        return self

    @staticmethod
    def _init_data(X, feature_names: Optional[List], feature_types: Optional[List]) -> Tuple[np.ndarray, List, List]:

        # This function should not copy the data, rather return a pointer / handle to it
        # and some extra information
        if isinstance(X, np.ndarray):
            X_ = X
            _, d = X.shape
            if feature_names is None:
                # Columns can be numeric for indexing
                feature_names = list(range(d))
            if feature_types is None:
                feature_types = _detect_types_numpy(X)

        elif isinstance(X, pd.DataFrame):
            X_ = X.values
            if feature_names is None:
                # Should we make all columns str?
                feature_names = list(X.columns)
            if feature_types is None:
                feature_types = list(X.dtypes)

        return X_, feature_names, feature_types

    def _init_labels(self, y = None) -> Optional[np.ndarray]:
        return y if y is not None else self.y

    def _init_weight(self, weight = None) -> Optional[np.ndarray]:
        return weight if weight is not None else self.weight

    def clone(self):
        # TODO: Own the data. Will copy data
        raise NotImplementedError

    def __getitem__(self, index) -> "DataAutoProcessor":
        res = DataAutoProcessor(
            X=np.atleast_2d(self.X[index]),
            y=self.y[index] if self.y is not None else None,
            weight=self.weight[index] if self.weight is not None else None,
            props=self.props[index] if self.props is not None else None,
            feature_names=self.feature_names,
            feature_types=self.feature_types,
            categorical_features=self.categorical_features,
            array_features=self.array_features,
            categorical_threshold=self.categorical_threshold,
        )
        res.feature_types_original = self.feature_types_original

        return res

    def handle_missing_and_feature_encoding(self, sparse_threshold=0.01):
        if self.X.size == 0:
            return self.X
        self.handle_missing_values()
        transformed_data = self.handle_feature_encoding(sparse_threshold)
        return transformed_data

    def handle_missing_values(self):
        """
        Handle missing values in the dataset.
        Modifies the dataset (X and y) in place.
        The calls to the underlying methods must be done only once, in the following order: y, then X.
        """
        if self._is_y_provided():
            self._apply_missing_values_y()
        self._apply_missing_values_X()

    def handle_feature_encoding(self, sparse_threshold=0.01, predict_context: bool = False):
        """
        Encode categorical and array features.
        """
        cat_encoding_method, encoder_config_ohe, encoder_config_te, encoder_config_mixed, has_categories = self._cat_encoding_configs()

        if cat_encoding_method == CategoricalEncoding.NOTHING:
            return self.X_processed
        # "has_categories" can be True only (1) in prediction or in (2+3) fit with refine/resample contexts.
        # In prediction context, we don't expect y to be provided, but in fit with refine/resample, we do (for
        # supervised learning, of course).
        # In all three contexts, we don't expect weights to be present.
        # We don't have, at this point, a way to distinguish between the different contexts and to verify y was
        # provided only for refine/resample - and to raise an exception otherwise, in prediction context - but we can
        # verify that weight is not provided in all three contexts.
        if has_categories:
            if self.weight is not None and len(self.weight) > 0:
                raise ValueError("Unexpected weight in prediction/refine/resample context(s).")

        # Extract categorical feature columns (non numeric) while skipping array columns
        cat_features_idxs = self.categorical_features if has_categories else [
            i for i, t in enumerate(self.feature_types) if _is_categorical_dtype(t)
            and i not in (self.array_features if self.array_features else [])
        ]
        if has_categories:
            self.cat_features_idxs_ohe = encoder_config_ohe["cat_features_idxs"]
            self.cat_features_idxs_te = encoder_config_te["cat_features_idxs"]
        else:
            self.cat_features_idxs_ohe, self.cat_features_idxs_te = _categorical_features_encoding_split(
                cat_encoding_method,
                cat_features_idxs,
                encoder_config_mixed["favor_ohe_num_cats_thresh"],
                encoder_config_mixed["favor_ohe_vol_pct_thresh"],
                self.X_processed)

        # No point executing the transformer if no categorical columns exist.
        if (cat_features_idxs is None or len(cat_features_idxs) <= 0) and \
                (self.array_features is None or len(self.array_features) == 0):
            return self.X_processed

        transformers = []
        if cat_features_idxs is not None and len(cat_features_idxs) > 0:
            if cat_encoding_method in (CategoricalEncoding.OHE, CategoricalEncoding.MIXED) and not predict_context:
                init_encoder_config_ohe = {k: encoder_config_ohe[k] for k in encoder_config_ohe if k != "cat_features_idxs"}
                transformers.append(("cat_ohe", WeightedOHE(**init_encoder_config_ohe), self.cat_features_idxs_ohe))
            if cat_encoding_method in (CategoricalEncoding.TE, CategoricalEncoding.MIXED):
                # "cv" cannot be greater than the total number of samples or the number of members in each class
                # (i.e., there must exist at least one class for which the number of members is >= number of splits);
                # however, "cv" must also have at least the value of 2.
                # The implementation below should work for any input, except where we have exactly one member for
                # each class.
                # In this extremely rare case, seems like the only way to prevent an error is inside TargetEncoder's
                # fit_transform() method - which, upon having encountered such situation, will run fit() + transform(),
                # preventing the usage of CV whatsoever.
                config_val = encoder_config_te["cv"]
                cv_cands = [CategoricalEncoding.TE_DEFAULT_CV if config_val is None else config_val, self.X_processed.shape[0]]
                if self._is_y_provided():
                    _, class_counts = unique(self.y, return_counts=True)
                    cv_cands.extend(class_counts)
                cv = max(2, min(cv_cands))
                te_common = {
                    "cv": cv,
                    "random_state": encoder_config_te.get("random_state"),
                }
                te_pre_fit = {}
                if has_categories:
                    # Having categories means we should have all the other values as well, so exception should be
                    # raised if some values aren't found (therefore dictionary is accessed directly and not via "get").
                    te_pre_fit["categories"] = encoder_config_te["categories"]
                    te_pre_fit["target_type"] = encoder_config_te["target_type"]
                    te_pre_fit["pre_fit_classes"] = encoder_config_te["classes"]
                    te_pre_fit["pre_fit_target_mean"] = encoder_config_te["target_mean"]
                    te_pre_fit["pre_fit_encodings"] = encoder_config_te["encodings"]
                transformers.append(("cat_te", TargetEncoder(**{**te_common, **te_pre_fit}), self.cat_features_idxs_te))

        if self.array_features is not None and len(self.array_features) > 0:
            array_features_names = list(np.array(self.feature_names)[self.array_features])
            transformers.append(("array_enc", WeightedArrayEncoder(**self.array_encoding_config,
                                                                   array_columns=array_features_names),
                                 self.array_features))

        preprocessor = WeightedColumnTransformer(
            transformers=transformers,
            apply_sample_weight=[name for (name, _, _) in transformers] if not has_categories else None,
            remainder="passthrough",
            sparse_threshold=sparse_threshold
        )

        # TODO Future work:
        #  fit_transform vs. transform flow: the current design is probably not exactly fitting the work we do in
        #  practice with the OHE, and this especially becomes more apparent with the suggested treatment of
        #  "fit_transform" in the TE; our flow of always going through "fit_transform" is not optimal, and we may
        #  want to use a proper "transform" call because in either case we’re doing the so-called "fit" functional
        #  part in other places, preceding the call to data_preprocessed, already ("prepare_data_and_categories",
        #  to be precise). This architectural change will require rethinking about the WeightedColumnTransformer
        #  part as well, and introducing the "transform" flow in "data_preprocessed" as an option in addition to
        #  the "fit_transform", where we’d expect the "fit" part of a pre-existing encoder to be fully prepared
        #  ahead of time by our preprocessing code.

        # Check if we actually have y in the input (i.e., we're not exclusively in a transform-only context).
        # TE requires both X and an actual y to 'fit_transform' (supervised).
        # OHE requires only X to 'fit_transform' (unsupervised), but supports y as a parameter and ignores it.
        # Both encoders need only X in order to 'transform'.
        # So we decide on whether to pass y exclusively based on its existence.
        replacement_weights = self._calc_replacement_weights()
        replacement_weights = np.delete(replacement_weights, self.removed_rows) if \
            self.removed_rows is not None and self.weight is not None else replacement_weights
        if self._is_y_provided():
            y_removed = np.delete(self.y, self.removed_rows) if self.removed_rows is not None else self.y
            transformed_data = preprocessor.fit_transform(self.X_processed, y_removed, sample_weight=replacement_weights)
        else:
            transformed_data = preprocessor.fit_transform(self.X_processed, sample_weight=replacement_weights)
        self.preprocessor = preprocessor

        return transformed_data

    def get_processed_arrays(self):
        if self.removed_rows.size > 0:
            processed_y = np.delete(self.y, self.removed_rows) if self.y is not None else None
            processed_weight = np.delete(self.weight, self.removed_rows) if self.weight is not None else None
            processed_ind = np.delete(self.ind, self.removed_rows) if self.ind is not None else None
        else:
            processed_y = self.y
            processed_weight = self.weight
            processed_ind = self.ind

        return processed_y, processed_weight, processed_ind

    def get_generated_array_feature_names(self):
        return self._transformer_array().get_feature_names_out() if (self.array_features is not None
                                                                     and len(self.array_features) > 0) else []

    def get_generated_feature_names(self, non_existing_encoded_value, used_categories_names):
        """
        could be used after data_preprocessed,
        returns columns generated by OHE, TE and array encoding
        as example -[country_0.0, country_1.0, country_infrequent, gender_0.0, gender_1.0, age, salary, ...]
        categorical features are always going at first, array features second and numeric features - going after them
        (that is how OHE engine works)

        used_categories_names - list of original (not encoded) categorical feature values
        """

        feature_names = list(map(lambda el: str(el), self.feature_names))
        feature_names_original = list(map(lambda el: str(el), self.feature_names_original))

        numerical_feature_names = [f for i, f
                                   in enumerate(feature_names)
                                   if i not in (self.categorical_features if self.categorical_features else [])
                                   and i not in (self.array_features if self.array_features else [])
                                   ]

        array_features_names = self.get_generated_array_feature_names()

        if self.categorical_features is None or len(self.categorical_features) == 0:
            return array_features_names + numerical_feature_names

        cat_encoding_method, _, _, _, has_categories = self._cat_encoding_configs()

        out_cat_feature_names_ohe = []
        if cat_encoding_method in (CategoricalEncoding.OHE, CategoricalEncoding.MIXED) \
                and self._transformer_ohe() is not None:
            cat_features_names_ohe = np.array(feature_names)[self.cat_features_idxs_ohe].tolist()
            out_cat_feature_names_ohe = self._transformer_ohe().get_feature_names_out(cat_features_names_ohe)
            if not has_categories:
                # replace '_infrequent_sklearn' with own label ('_infrequent')
                # that could happen when ohe_encoder_config.get("categories") = None, that means OHE engine calc categories
                out_cat_feature_names_ohe = [str(f).replace('_infrequent_sklearn', '_infrequent')
                                             for f in out_cat_feature_names_ohe]
            else:
                # replace '_non_existing_encoded_value' with label ('_infrequent')
                # that could happen only when ohe_encoder_config.get("categories") != None
                out_cat_feature_names_ohe = [str(f).replace('_' + str(float(non_existing_encoded_value)), '_infrequent')
                                             for f in out_cat_feature_names_ohe]

            # decode "encoded" OHE feature names -
            # [Job_title_infrequent, Gender_0, Gender_1, Age] -> [Job_title_infrequent, Gender_Female, Gender_Male, Age]
            processed_features = set()
            for i, column_name in enumerate(out_cat_feature_names_ohe):
                if not column_name.endswith('_infrequent'):
                    # categorical encoded feature
                    feature_name = column_name.rsplit('_', 1)[0]

                    if feature_name not in processed_features:
                        # Compute category dictionary and process all columns for this feature_name
                        idx_str = str(feature_names_original.index(feature_name))
                        category = {v: k for k, v in used_categories_names[idx_str].items()}
                        category[0] = np.nan

                        for j, cn in enumerate(out_cat_feature_names_ohe):
                            if cn.rsplit('_', 1)[0] == feature_name and not cn.endswith('_infrequent'):
                                encoded_value_j = cn.split('_')[-1]
                                if int(float(encoded_value_j)) < len(category) + 4:
                                    replace_with_value = str(category[int(float(encoded_value_j))])
                                else:
                                    replace_with_value = 'nan'
                                out_cat_feature_names_ohe[j] = cn.replace(encoded_value_j, replace_with_value)

                        # Mark this feature_name as processed and delete the category dictionary
                        processed_features.add(feature_name)

        out_cat_feature_names_te = []
        if cat_encoding_method in (CategoricalEncoding.TE, CategoricalEncoding.MIXED) \
                and self._transformer_te() is not None:
            cat_features_names_te = np.array(feature_names)[self.cat_features_idxs_te].tolist()
            out_cat_feature_names_te = self._transformer_te().get_feature_names_out(cat_features_names_te)
            if not np.array_equal(cat_features_names_te, out_cat_feature_names_te):
                # If the arrays are different, the features have actually changed, and this can only happen for
                # multiclass classification. This indicates an internal implementation flow error.
                raise NotImplementedError("Unsupported Target Encoding for non-binary classification")

        # Comprehend output features list:
        # 1. Categorical OHE-transformed features (if applicable) go first.
        # 2. Categorical TE-transformed features (if applicable) go next.
        # 3. Array features transformed features (if applicable) go next.
        # 4. Numerical features (if applicable) go last.
        features_full_out = [*out_cat_feature_names_ohe, *out_cat_feature_names_te, *array_features_names, *numerical_feature_names]
        return features_full_out

    def get_auto_preprocessing_params_values(self):
        """
        could be used after data_preprocessed,
        returns preprocessing data generated by either of the OHE/TE/MIXED approach encoders.
        """
        preprocessing_params = PreprocessingParams(
            missing_values_params=self.missing_values_params,
        )

        if self.categorical_features is not None and len(self.categorical_features) > 0:

            cat_encoding_method, encoder_config_ohe, encoder_config_te, _, has_categories = self._cat_encoding_configs()

            if cat_encoding_method in (CategoricalEncoding.OHE, CategoricalEncoding.MIXED) \
                    and self._transformer_ohe() is not None:
                preprocessing_params.ohe_cat_features_idxs = self.cat_features_idxs_ohe.copy()
                if has_categories:
                    ohe_used_categories = encoder_config_ohe["categories"].copy()
                else:
                    # if categories were auto-detected we need some calculations for features that have 'infrequent' column
                    ohe_used_categories = []
                    for i, category in enumerate(self._transformer_ohe().categories_):
                        infrequent_cats = self._transformer_ohe().infrequent_categories_[i]
                        if infrequent_cats is not None:
                            # have infrequent column
                            # used_cat = detected by OHE categories minus categories marked as 'infrequent'
                            used_cat = np.array(sorted(list(set(category).difference(set(infrequent_cats)))))
                            # if there are 'infrequent' column, add it to result categories
                            used_cat = np.concatenate([used_cat.astype(object), [CATEGORICAL_INFREQUENT]])
                        else:
                            # there is no infrequent column
                            used_cat = category
                        ohe_used_categories.append(used_cat)
                preprocessing_params.ohe_used_categories = ohe_used_categories

            if cat_encoding_method in (CategoricalEncoding.TE, CategoricalEncoding.MIXED) \
                    and self._transformer_te() is not None:
                preprocessing_params.te_cat_features_idxs = self.cat_features_idxs_te.copy()
                if has_categories:
                    # Having categories means we should have all the other values as well, so exception should be
                    # raised if some values aren't found (therefore dictionary is accessed directly and not via "get").
                    preprocessing_params.te_used_categories = encoder_config_te["categories"]
                    preprocessing_params.te_target_type = encoder_config_te["target_type"]
                    preprocessing_params.te_classes = encoder_config_te["classes"]
                    preprocessing_params.te_target_mean = encoder_config_te["target_mean"]
                    preprocessing_params.te_encodings = encoder_config_te["encodings"]
                else:
                    te_transformer = self._transformer_te()
                    preprocessing_params.te_used_categories = te_transformer.categories_
                    preprocessing_params.te_target_type = te_transformer.target_type_
                    preprocessing_params.te_classes = te_transformer.classes_
                    preprocessing_params.te_target_mean = te_transformer.target_mean_
                    preprocessing_params.te_encodings = te_transformer.encodings_
        if self.array_features is not None and len(self.array_features) > 0:
            # assign the calculated labels per column
            preprocessing_params.ae_feature_classes = self._transformer_array().feature_classes_
        return preprocessing_params

    def _remove_features(self, features_to_remove):

        self.X_processed = np.delete(self.X_processed, features_to_remove, axis=1)

        cat_encoding_method, encoder_config_ohe, encoder_config_te, encoder_config_mixed, has_categories = self._cat_encoding_configs()
        if has_categories:
            cat_features_idxs_ohe = encoder_config_ohe["cat_features_idxs"]
            if cat_encoding_method in (CategoricalEncoding.OHE, CategoricalEncoding.MIXED):
                removed_cat_cols_ohe = [r for r in cat_features_idxs_ohe if r in features_to_remove]
                encoder_config_ohe["categories"] = [
                    r for i, r in enumerate(encoder_config_ohe["categories"]) if i not in removed_cat_cols_ohe
                ]

            cat_features_idxs_te = encoder_config_te["cat_features_idxs"]
            if cat_encoding_method in (CategoricalEncoding.TE, CategoricalEncoding.MIXED):
                removed_cat_cols_te = [r for r in cat_features_idxs_te if r in features_to_remove]
                encoder_config_te["categories"] = [
                    r for i, r in enumerate(encoder_config_te["categories"]) if i not in removed_cat_cols_te
                ]
                encoder_config_te["encodings"] = [
                    r for i, r in enumerate(encoder_config_te["encodings"]) if i not in removed_cat_cols_te
                ]

        # Remove from missing_replacement
        self.missing_replacement = [
            replacement for id, replacement in enumerate(self.missing_replacement)
            if id not in features_to_remove
        ]
        # Remove from self.feature_names, feature_types, categorical_features
        self.feature_names = [
            feature_name for id, feature_name in enumerate(self.feature_names)
            if id not in features_to_remove
        ]
        self.feature_types = [
            feature_type for id, feature_type in enumerate(self.feature_types)
            if id not in features_to_remove
        ]
        self.categorical_features = [
            feature_id for feature_id in self.categorical_features
            if feature_id not in features_to_remove
        ]
        self.categorical_features = [idx - sum(1 for removed_idx in features_to_remove if removed_idx < idx) for idx
                                     in self.categorical_features]

        if self.array_features is not None:
            self.array_features = [idx - sum(1 for removed_idx in features_to_remove if removed_idx < idx) for idx
                                   in self.array_features]

    def _is_y_provided(self) -> bool:
        return self.y is not None and len(self.y) > 0

    def _transformer_ohe(self):
        if self.cat_features_idxs_ohe is not None \
                and len(self.cat_features_idxs_ohe) > 0 \
                and self.preprocessor is not None \
                and 'cat_ohe' in [t[0] for t in self.preprocessor.transformers]:
            return self.preprocessor.named_transformers_.cat_ohe
        return None

    def _transformer_te(self):
        if self.cat_features_idxs_te is not None \
                and len(self.cat_features_idxs_te) > 0 \
                and self.preprocessor is not None \
                and 'cat_te' in [t[0] for t in self.preprocessor.transformers]:
            return self.preprocessor.named_transformers_.cat_te
        return None

    def _transformer_array(self):
        if self.array_features is not None \
                and len(self.array_features) > 0 \
                and self.preprocessor is not None \
                and 'array_enc' in [t[0] for t in self.preprocessor.transformers]:
            return self.preprocessor.named_transformers_.array_enc
        return None

    @staticmethod
    def _handle_inf(arr, arr_name="X"):
        mask = np.isinf(arr)
        if np.any(mask):
            user_warning(f"inf values detected in {arr_name}, replacing with nan")
        return mask

    def drop_indices(self, indices=None):
        # drop X
        self.X_processed = np.delete(self.X_processed, indices, axis=0)
        # Remove rows from self.y
        if self.y is not None and len(self.y) > 0:
            self._update_n_represents_diff(indices)

    def _update_w_ind_props(self, dropped_indices):
        # Remove rows from self.weight
        if self.weight is not None:
            self.weight = np.delete(self.weight, dropped_indices)
        # Remove rows from self.ind
        if self.ind is not None:
            self.ind = np.delete(self.ind, dropped_indices)
        # Remove rows from self.props
        if self.props is not None:
            self.props = np.delete(self.props, dropped_indices, axis=0)

    def _update_n_represents_diff(self, dropped_indices):
        if self.is_classification:
            ys_to_remove = self.y[dropped_indices]
            n_represents_diff = dict(zip(*np.unique(ys_to_remove, return_counts=True)))
        else:
            n_represents_diff = len(dropped_indices)
        self.n_represents_diff = _update_n_represents(self.n_represents_diff, n_represents_diff, self.is_classification)

    @staticmethod
    def adjust_array_features_mask(x_mask, array_features, X=None):
        for array_feature in array_features:
            if X is not None:
                # find the null values
                column_to_be_added = []
                for element in X[:, array_feature]:
                    column_to_be_added.append(element is None)
            else:
                column_to_be_added = np.array([False] * x_mask.shape[0])

            # # Adding column to array using append() method
            x_mask = np.insert(x_mask, array_feature, column_to_be_added, axis=1)
        return x_mask

    def _apply_missing_values_y(self):
        """
        Filter-out rows with missing y values in-place.
        Assumes:
            (1) y exists.
            (2) being called only once, and BEFORE handling X missing values.
        """
        # Get the indices of rows with missing values
        dropped_indices = _get_inf_nan_indexes(self.y)
        if dropped_indices:
            self._update_n_represents_diff(dropped_indices)
            self.y = np.delete(self.y, dropped_indices)
            # Remove rows from self.X
            self.X = np.delete(self.X, dropped_indices, axis=0)
            # Remove rows from self.weight, self.ind, self.props
            self._update_w_ind_props(dropped_indices)
            # There's an assumption here that we didn't process X yet, so the current method must be the first
            # thing called, only once (may never be called after doing any processing on X).
            self.X_processed = self.X

    def _apply_missing_values_X(self):
        """
        Fill missing feature values in the dataset in-place.
        Assumes:
            (1) being called only once, and AFTER handling y missing values.
        """

        inf_mask = self._handle_inf(self.X[:, [c for c in range(self.X.shape[1]) if c not in self.array_features]].astype(float) if self.array_features else self.X)
        if self.array_features:
            inf_mask = self.adjust_array_features_mask(inf_mask, self.array_features)

        if np.any(inf_mask):
            self.X[inf_mask] = np.nan

        if self.calc_replacements:
            self._calc_replacements()

        # If there are no missing values in the dataset, return the dataset as is
        missing_mask = np.isnan(self.X[:, [c for c in range(self.X.shape[1]) if c not in self.array_features]].astype(float) if self.array_features else self.X)
        if self.array_features:
            # adjust the mask to have the same columns as x
            missing_mask = self.adjust_array_features_mask(missing_mask, self.array_features, X=self.X)
        if not np.any(missing_mask):
            self.X_processed = self.X
            return

        # Column by column check if the missing values are more than missing_feature_threshold.
        # X is a numpy array
        if not self.has_missing_values_params:
            features_to_remove = []
            for column in range(self.X.shape[1]):

                if self.array_features is not None and column in self.array_features:
                    continue

                missing_percentage = missing_mask[:, column].mean()
                if missing_percentage > self.drop_cols_above or missing_percentage == 1.0:
                    features_to_remove.append(column)
        else:
            features_to_remove = self.missing_values_params.get('removed_features', [])
        # If there are features to remove we need to copy the original X and missing_mask to be able to revert
        # the changes later
        self.X_processed = self.X.copy() if features_to_remove else self.X

        # Remove the features marked for removal
        if features_to_remove:
            self._remove_features(features_to_remove)
            missing_mask = np.delete(missing_mask, features_to_remove, axis=1)

        # Check if we still have remaining features, if not raise an error.

        if self.X_processed.shape[1] == 0:
            raise ValueError("All features have been removed due to missing values.")

        # Check the percentage of rows with missing values, if it is more than the missing_row_threshold
        # then we need to replace the missing values. Else just drop the rows with missing values.
        # X is a numpy array
        percentage_rows_with_missing = missing_mask.mean()
        if percentage_rows_with_missing > self.drop_rows_below:
            if not features_to_remove:
                self.X_processed = self.X.copy()
            self.X_processed = self._make_replacements(missing_mask)
        else:
            # Get the indices of rows with missing values
            dropped_indices = np.where(np.any(missing_mask, axis=1))[0]
            if dropped_indices.size > 0:
                if not features_to_remove:
                    self.X_processed = self.X.copy()
                self.drop_indices(dropped_indices)
                # Collect data regarding removed rows
                self.removed_rows = np.concatenate([self.removed_rows, dropped_indices])

        # Check if we still have remaining features, if not raise an error.
        if self.X_processed.shape[0] == 0:
            raise ValueError("All samples have been dropped due to missing values.")

        # Collect data regarding removed features
        self.removed_features = features_to_remove
        if not self.has_missing_values_params:
            self.missing_values_params['removed_features'] = features_to_remove

    def _calc_replacements(self):
        for feature_id, replacement in enumerate(self.missing_replacement):
            if self.array_features is not None and feature_id in self.array_features:
                continue
            if feature_id in self.categorical_features:
                if replacement == 'take_most_common':
                    replacement_weights = self._calc_replacement_weights()
                    mode, _ = weighted_mode(self.X[:, feature_id], w=replacement_weights)
                    mode = mode[0]
                    self.missing_values_params['features'][feature_id] = mode
                elif replacement is not None:
                    self.missing_values_params['features'][feature_id] = replacement
            else:
                if replacement is None:
                    # Compute the weighted mean value
                    replacement_weights = self._calc_replacement_weights()
                    mask = ~np.isnan(self.X[:, feature_id])\
                        if not self.X.dtype == np.object_ else ~np.isnan(self.X[:, feature_id].astype(float))
                    mean = np.average(self.X[:, feature_id][mask], weights=replacement_weights[mask])\
                        if not self.X.dtype == np.object_ else np.average(self.X[:, feature_id][mask].astype(float),
                                                                          weights=replacement_weights[mask])
                    self.missing_values_params['features'][feature_id] = mean

    def _calc_replacement_weights(self):
        """Calculate weights based on class_weights and sample_weight if provided"""
        weights = self.weight if self.weight is not None else np.ones(self.X_processed.shape[0])
        weights = weights.astype(np.float32)
        if self.class_weights:
            for cls, cls_weight in self.class_weights.items():
                mask = (self.y == cls)
                weights[mask] = weights[mask] * cls_weight
        return weights

    def _make_replacements(self, missing_mask):
        """
        Make replacements for missing values in the dataset.
        :param missing_mask: mask of missing values
        :return: X processed
        """
        for feature_id, replacement in enumerate(self.missing_replacement):

            if np.any(missing_mask[:, feature_id]):
                if feature_id in self.categorical_features:
                    if replacement == 'take_most_common':
                        # compute most common value (weighted if we have self.weight)
                        if not self.has_missing_values_params:
                            replacement_weights = self._calc_replacement_weights()
                            mode, _ = weighted_mode(self.X_processed[:, feature_id], w=replacement_weights)
                            mode = mode[0]
                            self.missing_values_params['features'][feature_id] = mode
                        else:
                            mode = self.missing_values_params['features'][feature_id]
                        # replace missing values with most common value
                        self.X_processed[:, feature_id] = np.where(missing_mask[:, feature_id], mode, self.X_processed[:, feature_id])
                    elif replacement is not None:
                        # use replacement (encoded value for replacement is zero)
                        self.X_processed[:, feature_id] = np.where(
                            missing_mask[:, feature_id],
                            0,
                            self.X_processed[:, feature_id]
                        )
                    else:
                        # treat missing value as a separate value (encoded value for missing value is zero)
                        self.X_processed[:, feature_id] = np.where(
                            missing_mask[:, feature_id],
                            0,
                            self.X_processed[:, feature_id]
                        )

                elif self.array_features is not None and feature_id in self.array_features:
                    # replace the missing array values with an empty list
                    for missing_idx in np.where(missing_mask[:, feature_id])[0]:
                        self.X_processed[:, feature_id][missing_idx] = np.array([], dtype=np.int32)
                        # change the X because we cannot save nan and None to hdf5 vlarray
                        self.X[:, feature_id][missing_idx] = np.array([], dtype=np.int32)

                else:
                    if replacement is not None:
                        # use replacement
                        # Check if replacement is numeric else raise error
                        if not isinstance(replacement, (int, float)):
                            raise ValueError(
                                f"Replacement for feature index {feature_id} is not numeric."
                            )
                        self.X_processed[:, feature_id] = np.where(
                            missing_mask[:, feature_id],
                            replacement,
                            self.X_processed[:, feature_id]
                        )
                    else:
                        # use mean value (weighted)
                        if not self.has_missing_values_params or \
                                feature_id not in self.missing_values_params['features']:
                            # that is possible if when preprocessing train data we removed rows
                            # and on test data we do not want to remove rows

                            replacement_weights = self._calc_replacement_weights()
                            mask = ~np.isnan(self.X_processed[:, feature_id])\
                                if not self.X_processed.dtype == np.object_ else ~np.isnan(
                                self.X_processed[:, feature_id].astype(float))
                            mean = np.average(self.X_processed[:, feature_id][mask], weights=replacement_weights[mask])\
                                if not self.X_processed.dtype == np.object_ else np.average(
                                self.X_processed[:, feature_id][mask].astype(float), weights=replacement_weights[mask])

                            self.missing_values_params['features'][feature_id] = mean
                        else:
                            mean = self.missing_values_params['features'][feature_id]
                        self.X_processed[:, feature_id] = np.where(missing_mask[:, feature_id], mean, self.X_processed[:, feature_id])
        return self.X_processed

    def _cat_encoding_configs(self):
        cat_encoding_method = _validated_cat_encoding_method(self.cat_encoding_config)
        encoder_config_ohe = self.cat_encoding_config[CategoricalEncoding.OHE]
        encoder_config_te = self.cat_encoding_config[CategoricalEncoding.TE]
        encoder_config_mixed = self.cat_encoding_config[CategoricalEncoding.MIXED]
        if cat_encoding_method == CategoricalEncoding.MIXED:
            categories_ohe = encoder_config_ohe.get("categories")
            has_categories_ohe = categories_ohe is not None and len(categories_ohe) > 0
            categories_te = encoder_config_te.get("categories")
            has_categories_te = categories_te is not None and len(categories_te) > 0
            has_categories = has_categories_ohe or has_categories_te
        elif cat_encoding_method == CategoricalEncoding.NOTHING:
            has_categories = False
        else:  # OHE, TE
            categories = self.cat_encoding_config[cat_encoding_method].get("categories")
            has_categories = categories is not None and len(categories) > 0
        return cat_encoding_method, encoder_config_ohe, encoder_config_te, encoder_config_mixed, has_categories


def _validated_cat_encoding_method(cat_encoding_config: dict):
    if cat_encoding_config is None:
        raise ValueError(f"Categorical encoding config cannot be None.")
    cat_encoding_method = cat_encoding_config.get(CategoricalEncoding.ENCODING_METHOD_KEY)
    if cat_encoding_method is None:
        raise ValueError(f"Value under categorical encoding method key "
                         f"'{CategoricalEncoding.ENCODING_METHOD_KEY}' cannot be None.")
    if cat_encoding_method not in (CategoricalEncoding.OHE, CategoricalEncoding.TE, CategoricalEncoding.MIXED, CategoricalEncoding.NOTHING):
        raise ValueError(f"Unsupported categorical encoding method '{cat_encoding_method}'")
    return cat_encoding_method


def _categorical_features_encoding_split(cat_encoding_method: str,
                                         categorical_feature_idxs: Union[list, None],
                                         favor_ohe_num_cats_thresh: int,
                                         favor_ohe_vol_pct_thresh: float,
                                         dataset,
                                         return_unique_ohe_counts: bool = False):
    cat_feature_idxs_ohe = []
    cat_feature_idxs_te = []
    # the unique value counts for each ohe feature
    unique_ohe_counts = []

    if categorical_feature_idxs is not None and len(categorical_feature_idxs) > 0:
        if cat_encoding_method == CategoricalEncoding.OHE:
            cat_feature_idxs_ohe = categorical_feature_idxs.copy()
            if return_unique_ohe_counts:
                # get unique counts for each ohe feature
                unique_ohe_counts = [len(unique(get_feature_slice(dataset, cat_feature_idx)))
                                     for cat_feature_idx in cat_feature_idxs_ohe]
        elif cat_encoding_method == CategoricalEncoding.TE:
            cat_feature_idxs_te = categorical_feature_idxs.copy()
        elif cat_encoding_method == CategoricalEncoding.MIXED:
            favor_ohe_vol_thresh = int(dataset.shape[0] * favor_ohe_vol_pct_thresh)

            for cat_feature_idx in categorical_feature_idxs:
                feature_slice = get_feature_slice(dataset, cat_feature_idx)
                category_vals, category_counts = unique(feature_slice, return_counts=True)
                sorted_counts = [-category_count for category_count, _ in sorted(zip(-category_counts, category_vals))]
                ohe_cand = False
                running_n_samples = 0
                for i, category_count in enumerate(sorted_counts):
                    running_n_samples += category_count
                    if i + 1 > favor_ohe_num_cats_thresh:
                        break
                    if running_n_samples >= favor_ohe_vol_thresh:
                        ohe_cand = True
                        break
                if ohe_cand:
                    cat_feature_idxs_ohe.append(cat_feature_idx)
                    unique_ohe_counts.append(len(category_vals))
                else:
                    cat_feature_idxs_te.append(cat_feature_idx)
    if return_unique_ohe_counts:
        return cat_feature_idxs_ohe, cat_feature_idxs_te, unique_ohe_counts
    else:
        return cat_feature_idxs_ohe, cat_feature_idxs_te


def _check_data_shape(data) -> Tuple:
    if hasattr(data, "shape") and len(data.shape) != 2:
        raise ValueError("Please reshape the input data into 2-dimensional matrix.")
    return data.shape


def _detect_types_numpy(data: np.ndarray) -> List[type]:
    if data.size == 0:
        return []
    n, d = data.shape

    if data.dtype != object:
        return [data.dtype] * d
    # All elements in a column must have the same type.
    # To check this we compare all element's types to the first one's type.
    # This seems kinda inneficient for Python for loops, but np.vectorize does
    # not promise speed either way, and had some weird type behaviour with float types.
    types = []
    for col in range(d):
        # find first non-nan element in column without using isnan
        # (because it does not work with object arrays)
        typ0 = float
        for row in range(n):
            # check if the value is not np.nan and not None. parquet files can have None values
            # pd.notna can check if the value is not np.nan or None, but it does not work with array values
            if data[row, col] is not np.nan and data[row, col] is not None:
                if isinstance(data[row, col], np.ndarray):
                    typ0 = np.ndarray
                    break
                else:
                    if data[row, col] != float('inf') and data[row, col] != float('-inf'):
                        typ0 = type(data[row, col])
                    break
        types.append(typ0)
    return types


def _is_categorical_dtype(typ):
    # Q: Make this global const?
    cat_dtypes = [object, str, CAT_T]
    return isinstance(typ, CategoricalDtype) or typ in cat_dtypes


def _find_categorical_types(
        data,
        feature_names,
        feature_types,
        categorical_features,
        categorical_threshold
):
    # 1. Check and set the given categorical features
    if categorical_features is not None:
        if all(isinstance(c, int) for c in categorical_features):
            for c in categorical_features:
                feature_types[c] = CAT_T
        else:
            for c in categorical_features:
                feature_types[feature_names.index(c)] = CAT_T

    # 2. Check and set the default categorical-like features
    for i, typ in enumerate(feature_types):
        if _is_categorical_dtype(typ):
            feature_types[i] = CAT_T

    # 3. Check features under threshold and set them to a categorical type
    n_samples, n_features = _check_data_shape(data)

    # If the number of unique instances is lower than some threshold, feature is categorical
    # This function should not copy anything.
    def under(col_idx, threshold, typ):
        if not _is_categorical_dtype(typ) and not typ == bool:
            # Our unique is faster than np.unique.
            if len(unique(data[:, col_idx])) < threshold:
                feature_types[col_idx] = CAT_T

    if is_int(categorical_threshold, positive=True):
        for (j, typ) in enumerate(feature_types):
            under(j, categorical_threshold, typ)
    elif is_percent(categorical_threshold):
        for (j, typ) in enumerate(feature_types):
            under(j, int(n_samples * categorical_threshold), typ)
    elif isinstance(categorical_threshold, dict):
        for feat_name, threshold in categorical_threshold.items():
            j = feature_names.index(feat_name)
            if is_int(threshold, positive=True):
                under(j, threshold, feature_types[j])
            elif is_percent(threshold):
                under(j, int(n_samples * threshold), feature_types[j])
    elif categorical_threshold is not None:
        raise TypeError(
            f"`categorical_threshold` must be positive int, percent or dict, found {categorical_threshold}"
        )

    return feature_types
