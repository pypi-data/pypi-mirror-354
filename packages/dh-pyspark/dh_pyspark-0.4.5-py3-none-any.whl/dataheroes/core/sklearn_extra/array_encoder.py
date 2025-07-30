import warnings
from collections import defaultdict

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.utils.validation import check_is_fitted

from dataheroes.core.numpy_extra import check_same_length, unique as unique_extra
from dataheroes.core.sklearn_extra.sklearn_1_5_1_mask.base import TransformerMixin, BaseEstimator


class WeightedArrayEncoder(TransformerMixin, BaseEstimator):
    """
    An binary encoder for array columns.
    Utilizing MultiLabelBinarizer per column with pre-calculated labels.
    The labels for the MultiLabelBinarizer are calculated with max categories and min frequency application.
    """
    def __init__(self, min_frequency: float = None, max_categories: int = None, array_columns: list = None,
                 feature_classes: dict = None, sparse_output: bool = False):
        """
        Parameters:
            min_frequency: min frequency per label.
            max_categories: max limit for the number of array labels.
            array_columns: array column names used for generating output column names.
            feature_classes: a dict of classes used for encoding.
            sparse_output
        """
        self.min_frequency = min_frequency
        self.max_categories = max_categories
        self.array_columns = array_columns
        # these labels are passed by the constructor when labels are known
        self.feature_classes = feature_classes
        self.sparse_output = sparse_output

    def fit(self, X, y=None, sample_weight=None):

        if not isinstance(X, np.ndarray):
            raise TypeError('X must be a numpy array')

        if X.ndim != 2:
            raise ValueError(f"Expected a 2D array, but got {X.ndim}D array instead.")

        if X.shape[0] == 0:
            raise ValueError("Cannot fit an encoder with an empty dataset.")

        check_same_length(X, sample_weight, allow_None=True)

        # this means that we received labels in the constructor
        # and no need to calculate them
        if self.feature_classes is not None:
            self.feature_classes_ = self.feature_classes
            return self

        # iterate through the X columns, and for each column compute the labels to encode
        # on labels we need to apply max categories and min frequencies if set
        # if max categories and min frequencies are not defined we take all labels
        # for max categories we take N most popular
        # the calculated classes are stored in feature_classes dict as
        # {column_index: [list of classes],..}

        # these are calculated labels by fit
        self.feature_classes_ = {}
        apply_constraints = self.max_categories is not None or self.min_frequency is not None

        for i in range(X.shape[1]):

            # if weights are equal or None and the concatenated result of the values in the column is an int array
            # the faster approach to use the bin count based unique.
            # if the weights are not equal we will use the bucket based approach where we iterate on the column
            # stack the weights in a dict where the key is the unique value
            if sample_weight is None or np.all(np.asarray(sample_weight) == sample_weight[0]):
                # concatenate all the arrays in column to a single array
                # this is memory consuming
                x_values = np.concatenate(X[:, i])
                # if x_values is int dtype it means that all values are valid, and we don't need to check them
                # and in this case the bin count based unique is faster
                if np.issubdtype(x_values.dtype, np.integer):
                    labels, counts = self._get_bin_unique(x_values, sample_weight, apply_constraints)
                else:
                    labels, counts = self._get_bucket_unique(X[:, i], sample_weight)
            else:
                # for unequal weights the bucket approach is faster
                labels, counts = self._get_bucket_unique(X[:, i], sample_weight)

            if apply_constraints:
                label_counts = list(zip(labels, counts))
                total = sum(counts)
                # filter max categories, take self.max_categories labels
                if self.max_categories is not None and len(label_counts) > self.max_categories:
                    label_counts = label_counts[:self.max_categories]

                # filter min frequency
                if self.min_frequency:
                    # if min_frequency given as int convert it to a relative value
                    relative_frequency = self.min_frequency * total if isinstance(self.min_frequency,
                                                                                  float) else self.min_frequency
                    label_counts = [(label, counts) for label, freq in label_counts if freq >= relative_frequency]
                labels = [label for label, freq in label_counts]

            # add labels to the feature classes dict
            # this dict will be used in transform for encoding columns
            # also it is saved in preprocessing_data for predict
            self.feature_classes_[i] = sorted(labels)
        return self

    @staticmethod
    def _get_bin_unique(x_values, w=None, apply_constraints: bool = False):
        # get unique values and counts with the bin count
        if apply_constraints:
            labels, counts = unique_extra(x_values, return_counts=True)
            # since all weights are equal we can multiply counts by the weight
            if w is not None:
                counts = counts * w[0]
            # order high to low of (label, frequency) tuples, based on frequency
            labels, counts = zip(*sorted(zip(labels, counts), key=lambda x: (-x[1], x[0])))
        else:
            labels, counts = list(unique_extra(x_values)), None
        return labels, counts

    @staticmethod
    def _get_bucket_unique(column_data, w=None):
        # iterate on the column and populate unique values dict,
        # where the unique value are the key and the accumulated weights are the value
        # {unique_value: sum(weights), ...}
        unique_weighted = defaultdict(int)
        for sample_idx, arr in enumerate(column_data):
            if arr is not None:
                w_value = w[sample_idx] if w is not None else 1
                # if the array is np.integer it means that all values are valid
                if isinstance(arr, np.ndarray) and np.issubdtype(arr.dtype, np.integer):
                    for arr_val in arr:
                        unique_weighted[arr_val] += w_value
                else:
                    for arr_val in arr:
                        # collect all the possible values and stack weights
                        # drop None, nan array values that come from [1, None, nan] ...
                        if arr_val is not None and not (isinstance(arr_val, float) and np.isnan(arr_val)):
                            unique_weighted[arr_val] += w_value
        sorted_list = sorted(unique_weighted.items(), key=lambda x: (-x[1], x[0]))
        # unpack to 2 lists, labels, counts
        return zip(*sorted_list)

    def fit_transform(self, X, y=None, sample_weight=None):
        return self.fit(X, sample_weight=sample_weight).transform(X)

    def transform(self, X):
        check_is_fitted(self, 'feature_classes_')
        result = []
        with warnings.catch_warnings():
            # ignore UserWarning for ignored labels
            warnings.simplefilter("ignore", UserWarning)
            for i in range(X.shape[1]):
                # generate the array([[1,0,1],[0,1,0],[0,0,1]]) columns
                mlb = MultiLabelBinarizer(classes=self.feature_classes_[i])
                result.append(mlb.fit_transform(X[:, i]))
        return np.concatenate(result, axis=1) if not self.sparse_output else csr_matrix(np.concatenate(result, axis=1))

    def get_feature_names_out(self, input_features=None):

        check_is_fitted(self, 'feature_classes_')
        array_columns = self.array_columns if input_features is None else input_features

        if len(array_columns) != len(self.feature_classes_):
            raise ValueError(
                "input_features should have length equal to number of "
                f"features ({len(self.feature_classes_)}), got {len(input_features)}")

        columns = []
        for column_name, column_index in zip(array_columns, self.feature_classes_):
            columns.extend([f'{column_name}_{i}' for i in range(len(self.feature_classes_[column_index]))])
        return columns
