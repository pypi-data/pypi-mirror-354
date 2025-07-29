# todo Igor 2024-09-04:
#  In this module, the apparently right thing to do in order to stay in line with the other preprocessing code is
#  to switch to using the local frozen sklearn mask as well as it is done elsewhere. For this purpose, we'll need
#  to expand the mask's base and introduce additional frozen source code; in addition, we will want to refresh the
#  implementation below with a source code based on the specific frozen sklearn version (1.5.1).
#  This wasn't necessary during the implementation of the Target Encoder feature and required extra work without
#  getting an adequate ROI - hence, the decision to adopt this approach was delayed to the future.
from itertools import chain
import sklearn
from typing import List
from sklearn import clone
from sklearn.compose import ColumnTransformer
from scipy import sparse
import numpy as np
from sklearn.utils import _safe_indexing
from .validation import _check_n_features, _check_feature_names, check_array

if sklearn.__version__ < "1.5.0":
    from sklearn.utils import _print_elapsed_time
else:
    from sklearn.utils._user_interface import _print_elapsed_time

from sklearn.preprocessing import FunctionTransformer
if sklearn.__version__ < "1.2.1":
    from sklearn.utils.fixes import delayed
    from joblib import Parallel
    
else:
    from sklearn.utils.parallel import Parallel, delayed

if sklearn.__version__ >= "1.2":
    from sklearn.utils._set_output import _get_output_config

_ERR_MSG_1DCOLUMN = (
    "1D data passed to a transformer that expects 2D data. "
    "Try to specify the column selection as a list of one "
    "item instead of a scalar."
)


def _check_X(X):
    """Use check_array only on lists and other non-array-likes / sparse"""
    if hasattr(X, "__array__") or sparse.issparse(X):
        return X
    return check_array(X, ensure_all_finite="allow-nan", dtype=object)


def _fit_transform_one(
    transformer, X, y, weight, message_clsname="", message=None, **fit_params
):
    """
    Fits ``transformer`` to ``X`` and ``y``. The transformed result is returned
    with the fitted transformer. If ``weight`` is not ``None``, the result will
    be multiplied by ``weight``.
    """
    with _print_elapsed_time(message_clsname, message):
        if hasattr(transformer, "fit_transform"):
            res = transformer.fit_transform(X, y, **fit_params)
        else:
            res = transformer.fit(X, y, **fit_params).transform(X)

    if weight is None:
        return res, transformer
    return res * weight, transformer


def _is_empty_column_selection(column):
    """
    Return True if the column selection is empty (empty list or all-False
    boolean array).

    """
    if hasattr(column, "dtype") and np.issubdtype(column.dtype, np.bool_):
        return not column.any()
    elif hasattr(column, "__len__"):
        return (
            len(column) == 0
            or all(isinstance(col, bool) for col in column)
            and not any(column)
        )
    else:
        return False


class WeightedColumnTransformer(ColumnTransformer):
    def __init__(
        self,
        transformers,
        *,
        remainder="drop",
        sparse_threshold=0.01,
        n_jobs=None,
        transformer_weights=None,
        verbose=False,
        verbose_feature_names_out=True,
        apply_sample_weight: List[str] = None
    ):
        self.apply_sample_weight = (
            apply_sample_weight if apply_sample_weight is not None else []
        )
        if sklearn.__version__ < "1.0":
            super().__init__(
                transformers,
                remainder=remainder,
                sparse_threshold=sparse_threshold,
                n_jobs=n_jobs,
                transformer_weights=transformer_weights,
                verbose=verbose,
            )
            self.verbose_feature_names_out = verbose_feature_names_out
        else:
            super().__init__(
                transformers,
                remainder=remainder,
                sparse_threshold=sparse_threshold,
                n_jobs=n_jobs,
                transformer_weights=transformer_weights,
                verbose=verbose,
                verbose_feature_names_out=verbose_feature_names_out,
            )

    def fit(self, X, y=None, sample_weight=None):
        """Fit all transformers using X.

        Parameters
        ----------
        X : {array-like, dataframe} of shape (n_samples, n_features)
            Input data, of which specified subsets are used to fit the
            transformers.

        y : array-like of shape (n_samples,...), default=None
            Targets for supervised learning.

        Returns
        -------
        self : ColumnTransformer
            This estimator.
        """
        # we use fit_transform to make sure to set sparse_output_ (for which we
        # need the transformed data) to have consistent output type in predict
        self.fit_transform(X, y=y, sample_weight=sample_weight)
        return self

    def fit_transform(self, X, y=None, sample_weight=None):
        """Fit all transformers, transform the data and concatenate results.

        Parameters
        ----------
        X : {array-like, dataframe} of shape (n_samples, n_features)
            Input data, of which specified subsets are used to fit the
            transformers.

        y : array-like of shape (n_samples,), default=None
            Targets for supervised learning.

        Returns
        -------
        X_t : {array-like, sparse matrix} of \
                shape (n_samples, sum_n_components)
            Horizontally stacked results of transformers. sum_n_components is the
            sum of n_components (output dimension) over transformers. If
            any result is a sparse matrix, everything will be converted to
            sparse matrices.
        """
        if sklearn.__version__ >= "1.0":
            _check_feature_names(estimator=self, X=X, reset=True)

        X = _check_X(X)
        # set n_features_in_ attribute
        _check_n_features(estimator=self, X=X, reset=True)
        self._validate_transformers()
        self._validate_column_callables(X)
        self._validate_remainder(X)

        result = self._fit_transform(
            X, y, _fit_transform_one, sample_weight=sample_weight
        )

        if not result:
            self._update_fitted_transformers([])
            # All transformers are None
            return np.zeros((X.shape[0], 0))

        Xs, transformers = zip(*result)

        # determine if concatenated output will be sparse or not
        if any(sparse.issparse(X) for X in Xs):
            nnz = sum(X.nnz if sparse.issparse(X) else X.size for X in Xs)
            total = sum(
                X.shape[0] * X.shape[1] if sparse.issparse(X) else X.size for X in Xs
            )
            density = nnz / total
            self.sparse_output_ = density < self.sparse_threshold
        else:
            self.sparse_output_ = False

        self._update_fitted_transformers(transformers)
        self._validate_output(Xs)
        self._record_output_indices(Xs)

        if 'n_samples' in self._hstack.__code__.co_varnames:
            return self._hstack(list(Xs), n_samples=Xs[0].shape[0])
        else:
            return self._hstack(list(Xs))

    def _fit_transform(
        self, X, y, func, sample_weight=None, fitted=False, column_as_strings=False
    ):
        """
        Private function to fit and/or transform on demand.

        Return value (transformers and/or transformed X data) depends
        on the passed function.
        ``fitted=True`` ensures the fitted transformers are used.
        """
        # if sklearn.__version__ < "1.0":
        #     transformers = list(self._iter(fitted=fitted, replace_strings=True))
        # else:
        transformers = list(
                self._iter(
                    fitted=fitted,
                    replace_strings=True,
                    column_as_strings=column_as_strings,
                )
            )
        try:
            return Parallel(n_jobs=self.n_jobs)(
                delayed(func)(
                    transformer=clone(trans) if not fitted else trans,
                    X=_safe_indexing(X, column, axis=1),
                    y=y,
                    weight=weight,
                    message_clsname="ColumnTransformer",
                    message=self._log_message(name, idx, len(transformers)),
                    sample_weight=sample_weight,
                )
                if name in self.apply_sample_weight
                else delayed(func)(
                    transformer=clone(trans) if not fitted else trans,
                    X=_safe_indexing(X, column, axis=1),
                    y=y,
                    weight=weight,
                    message_clsname="ColumnTransformer",
                    message=self._log_message(name, idx, len(transformers)),
                )
                for idx, (name, trans, column, weight) in enumerate(transformers, 1)
            )

        except ValueError as e:
            if "Expected 2D array, got 1D array instead" in str(e):
                raise ValueError(_ERR_MSG_1DCOLUMN) from e
            else:
                raise

    def _record_output_indices(self, Xs):
        """
        Record which transformer produced which column.
        """
        idx = 0
        self.output_indices_ = {}

        for transformer_idx, (name, _, _, _) in enumerate(
            self._iter(fitted=True, replace_strings=True)
        ):
            n_columns = Xs[transformer_idx].shape[1]
            self.output_indices_[name] = slice(idx, idx + n_columns)
            idx += n_columns

        # `_iter` only generates transformers that have a non empty
        # selection. Here we set empty slices for transformers that
        # generate no output, which are safe for indexing
        all_names = [t[0] for t in self.transformers] + ["remainder"]
        for name in all_names:
            if name not in self.output_indices_:
                self.output_indices_[name] = slice(0, 0)

    def _iter(self,
              fitted=False,
              replace_strings=False,
              column_as_strings=False,
              column_as_labels=False,
              skip_drop=False,
              skip_empty_columns=False):
        """
        Generate (name, trans, column, weight) tuples.

        If fitted=True, use the fitted transformers, else use the
        user specified transformers updated with converted column names
        and potentially appended with transformer for remainder.

        """
        if fitted:
            if sklearn.__version__ >= "1.2" and replace_strings:
                # Replace "passthrough" with the fitted version in
                # _name_to_fitted_passthrough
                def replace_passthrough(name, trans, columns):
                    if not hasattr(self, '_name_to_fitted_passthrough') or name not in self._name_to_fitted_passthrough:
                        return name, trans, columns
                    return name, self._name_to_fitted_passthrough[name], columns

                transformers = [replace_passthrough(*trans) for trans in self.transformers_]
            else:
                transformers = self.transformers_
        else:
            # interleave the validated column specifiers
            transformers = [
                (name, trans, column)
                for (name, trans, _), column in zip(self.transformers, self._columns)
            ]
            # add transformer tuple for remainder
            if self._remainder[2]:
                transformers = chain(transformers, [self._remainder])
        get_weight = (self.transformer_weights or {}).get

        if sklearn.__version__ >= "1.2":
            output_config = _get_output_config("transform", self)
        for name, trans, columns in transformers:
            if replace_strings:
                # replace 'passthrough' with identity transformer and
                # skip in case of 'drop'
                if trans == "passthrough":
                    if sklearn.__version__ >= "1.2":
                        trans = FunctionTransformer(
                            accept_sparse=True,
                            check_inverse=False,
                            feature_names_out="one-to-one",
                        ).set_output(transform=output_config["dense"])
                    else:
                        trans = FunctionTransformer(accept_sparse=True, check_inverse=False)
                elif trans == "drop":
                    continue
                elif _is_empty_column_selection(columns):
                    continue

            if column_as_strings:
                # Convert all columns to using their string labels
                columns_is_scalar = np.isscalar(columns)

                indices = self._transformer_to_input_indices[name]
                columns = self.feature_names_in_[indices]

                if columns_is_scalar:
                    # selection is done with one dimension
                    columns = columns[0]

            yield (name, trans, columns, get_weight(name))
