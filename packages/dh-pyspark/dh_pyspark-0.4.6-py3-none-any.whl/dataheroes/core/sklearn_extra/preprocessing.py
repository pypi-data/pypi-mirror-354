import numpy as np
from contextlib import suppress

from .validation import _check_n_features, _check_feature_names

from .sklearn_1_5_1_mask.preprocessing._encoders import OneHotEncoder
from .sklearn_1_5_1_mask.utils._missing import is_scalar_nan
from .sklearn_1_5_1_mask.utils._encode import _check_unknown, _unique as _unique_sklearn, _NaNCounter


def _unique_weighted(y, w=None, return_counts: bool = False):
    """
    DH Specific note: replacement method for sklearn's `_unique`, which supports weights without crippling the
    execution speed/running times.
    """
    if w is None:
        return _unique_sklearn(y, return_counts=return_counts)

    classes = _unique_sklearn(y)

    if not return_counts:
        return classes

    frequencies = np.bincount(y.astype(np.int64), w, len(classes))
    return classes, np.array(frequencies[frequencies > 0])


def _get_counts_weighted(values, uniques, weights=None):
    """
    DH Specific note: the original line using sklearn's `_unique_np` replaced to use DH Specific `_unique_weighted`.

    Get the count of each of the `uniques` in `values`.

    The counts will use the order passed in by `uniques`. For non-object dtypes,
    `uniques` is assumed to be sorted and `np.nan` is at the end.
    """
    if values.dtype.kind in "OU":
        counter = _NaNCounter(values)
        output = np.zeros(len(uniques), dtype=np.int64)
        for i, item in enumerate(uniques):
            with suppress(KeyError):
                output[i] = counter[item]
        return output

    # unique_values, counts = _unique_np(values, return_counts=True)  # DH Specific: original line
    unique_values, counts = _unique_weighted(values, w=weights, return_counts=True)  # DH Specific: replacement line

    # Recorder unique_values based on input: `uniques`
    uniques_in_values = np.isin(uniques, unique_values, assume_unique=True)
    if np.isnan(unique_values[-1]) and np.isnan(uniques[-1]):
        uniques_in_values[-1] = True

    unique_valid_indices = np.searchsorted(unique_values, uniques[uniques_in_values])
    output = np.zeros_like(uniques, dtype=np.int64)
    output[uniques_in_values] = counts[unique_valid_indices]
    return output


class WeightedOHE(OneHotEncoder):
    """
    DH Specific note:

    Replacement class for OHE that supports sample weights -
    1. Override "_fit" (originally, in _BaseEncoder of the frozen local sklearn 1.5.1 version) to support weights.
       We override it here locally for OHE only, because in other encoders we support (namely, TargetEncoder), there
       is no need to add sample weight support in this specific method. This is so, because in order for the
       additional functionality added here to be effective, infrequent categories need to be turned on. However, they
       are turned on only via the passing of max_categories/min_frequency, params which are irrelevant for the
       TargetEncoder (and relevant only for the OHE), therefore, they cannot turn the infrequent categories on anyway.
       Hence, the conditions that require category counts involving sample weights, do not hold during the calls to
       "_fit" under the context of TargetEncoder, and the adaptation of the code for supporting weights in "_fit"
       below, for the TargetEncoder specifically, is not necessary - it is only necessary for the OHE. Therefore,
       it is added directly here, for OHE's sake only.
       In other words, DH Specific addition of sample weight support in "_fit" is necessary only to support
       infrequent categories, which are not a part of TargetEncoder's mechanism, and are used only by the OHE.
    2. Override "fit" (originally, in OneHotEncoder of the frozen local sklearn 1.5.1 version) to support weights
       when calling the overridden "_fit" just mentioned above.
    """
    def _fit(
            self,
            X,
            sample_weight=None,
            handle_unknown="error",
            force_all_finite=True,
            return_counts=False,
            return_and_ignore_missing_for_infrequent=False,
    ):
        self._check_infrequent_enabled()
        _check_n_features(estimator=self, X=X, reset=True)
        _check_feature_names(self, X, reset=True)
        X_list, n_samples, n_features = self._check_X(
            X, force_all_finite=force_all_finite
        )
        self.n_features_in_ = n_features

        if self.categories != "auto":
            if len(self.categories) != n_features:
                raise ValueError(
                    "Shape mismatch: if categories is an array,"
                    " it has to be of shape (n_features,)."
                )

        self.categories_ = []
        category_counts = []
        compute_counts = return_counts or self._infrequent_enabled

        for i in range(n_features):
            Xi = X_list[i]

            if self.categories == "auto":
                result = _unique_weighted(Xi, sample_weight, return_counts=compute_counts)
                if compute_counts:
                    cats, counts = result
                    category_counts.append(counts)
                else:
                    cats = result
            else:
                if np.issubdtype(Xi.dtype, np.str_):
                    # Always convert string categories to objects to avoid
                    # unexpected string truncation for longer category labels
                    # passed in the constructor.
                    Xi_dtype = object
                else:
                    Xi_dtype = Xi.dtype

                cats = np.array(self.categories[i], dtype=Xi_dtype)
                if (
                    cats.dtype == object
                    and isinstance(cats[0], bytes)
                    and Xi.dtype.kind != "S"
                ):
                    msg = (
                        f"In column {i}, the predefined categories have type 'bytes'"
                        " which is incompatible with values of type"
                        f" '{type(Xi[0]).__name__}'."
                    )
                    raise ValueError(msg)

                # `nan` must be the last stated category
                for category in cats[:-1]:
                    if is_scalar_nan(category):
                        raise ValueError(
                            "Nan should be the last element in user"
                            f" provided categories, see categories {cats}"
                            f" in column #{i}"
                        )

                if cats.size != len(_unique_weighted(cats)):
                    msg = (
                        f"In column {i}, the predefined categories"
                        " contain duplicate elements."
                    )
                    raise ValueError(msg)

                if Xi.dtype.kind not in "OUS":
                    sorted_cats = np.sort(cats)
                    error_msg = (
                        "Unsorted categories are not supported for numerical categories"
                    )
                    # if there are nans, nan should be the last element
                    stop_idx = -1 if np.isnan(sorted_cats[-1]) else None
                    if np.any(sorted_cats[:stop_idx] != cats[:stop_idx]):
                        raise ValueError(error_msg)

                if handle_unknown == "error":
                    diff = _check_unknown(Xi, cats)
                    if diff:
                        msg = (
                            "Found unknown categories {0} in column {1}"
                            " during fit".format(diff, i)
                        )
                        raise ValueError(msg)
                if compute_counts:
                    category_counts.append(_get_counts_weighted(Xi, cats, sample_weight))

            self.categories_.append(cats)

        output = {"n_samples": n_samples}
        if return_counts:
            output["category_counts"] = category_counts

        missing_indices = {}
        if return_and_ignore_missing_for_infrequent:
            for feature_idx, categories_for_idx in enumerate(self.categories_):
                if is_scalar_nan(categories_for_idx[-1]):
                    # `nan` values can only be placed in the latest position
                    missing_indices[feature_idx] = categories_for_idx.size - 1
            output["missing_indices"] = missing_indices

        if self._infrequent_enabled:
            self._fit_infrequent_category_mapping(
                n_samples,
                category_counts,
                missing_indices,
            )
        return output

    def fit(self, X, y=None, sample_weight=None):
        """
        Fit OneHotEncoder to X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data to determine the categories of each feature.

        y : None
            Ignored. This parameter exists only for compatibility with
            :class:`~sklearn.pipeline.Pipeline`.

        Returns
        -------
        self
            Fitted encoder.
        """
        self._fit(
            X,
            sample_weight=sample_weight,
            handle_unknown=self.handle_unknown,
            force_all_finite="allow-nan",
        )
        self._set_drop_idx()
        self._n_features_outs = self._compute_n_features_outs()
        return self
