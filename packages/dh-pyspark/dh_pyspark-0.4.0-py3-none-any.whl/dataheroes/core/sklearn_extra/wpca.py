from math import sqrt
from sklearn.decomposition import PCA
from sklearn.decomposition._pca import _infer_dimension
from scipy.sparse import issparse
from scipy.sparse.linalg import svds
import numpy as np
import numbers
from scipy import linalg
from sklearn.utils.extmath import randomized_svd, svd_flip, stable_cumsum
from sklearn.utils import check_random_state
from sklearn.utils._arpack import _init_arpack_v0
import sklearn

import numbers
from math import sqrt

import numpy as np
from scipy import linalg
from scipy.sparse import issparse
from scipy.sparse.linalg import svds
from sklearn.decomposition import PCA
from sklearn.decomposition._pca import _infer_dimension
from sklearn.utils import check_random_state
from sklearn.utils._arpack import _init_arpack_v0
from sklearn.utils.extmath import randomized_svd, stable_cumsum, svd_flip


class WPCA(PCA):
    def fit(self, X, y=None, sample_weight=None, norm_S=None):
        """Fit the model with X
        Arguments
            X {array-like} -- (n_samples, n_features) feature array
            y Ignored -- not used
            w {array-like} -- (n_samples, )  weight array
        Returns
            {WPCA} -- fitted model
        """
        self._fit(X, sample_weight, norm_S)
        return self

    def fit_transform(self, X, y=None, w=None):
        """
        Fit the model with X and apply the dimensionality reduction on X.
        Arguments
            X: {array-like} of shape (n_samples, n_features) --
                Training data, where n_samples is the number of samples
                and n_features is the number of features.

            y: Ignored

        Returns
            X_new: {ndarray} of shape (n_samples, n_components) -- Transformed values.
        """
        U, S, Vt = self._fit(X, w)
        U = U[:, : self.n_components_]

        if self.whiten:
            # X_new = X * V / S * sqrt(n_samples) = U * sqrt(n_samples)
            U *= sqrt(X.shape[0] - 1)
        else:
            # X_new = X * V = U * S * Vt * V = U * S
            U *= S[: self.n_components_]

        return U

    def _fit(self, X, w=None, norm_S=None):
        """Dispatch to the right submethod depending on the chosen solver."""

        # Raise an error for sparse input.
        # This is more informative than the generic one raised by check_array.
        if issparse(X):
            raise TypeError(
                "PCA does not support sparse input. See "
                "TruncatedSVD for a possible alternative."
            )

        X = self._validate_data(
            X, dtype=[np.float64, np.float32], ensure_2d=True, copy=self.copy
        )

        # Set weights to 1 if no weights are provided. Also make them the same dtype as X
        if w is None:
            w = np.ones(len(X), dtype=X.dtype)
        else:
            assert len(w) == len(
                X
            ), "Weights provided must be the same length as the data X"
            w = np.array(w, dtype=X.dtype)

        # Handle n_components==None
        if self.n_components is None:
            n_components = min(X.shape) - 1
        else:
            n_components = self.n_components

        return self._fit_full(X, w, n_components, norm_S)
        # Handle svd_solver

    def _fit_full(self, X, w, n_components, norm_S=None):
        """Fit the model by computing full SVD on X."""
        n_samples, n_features = X.shape

        if n_components == "mle":
            if n_samples < n_features:
                raise ValueError(
                    "n_components='mle' is only supported " "if n_samples >= n_features"
                )
        elif not 0 <= n_components <= min(n_samples, n_features):
            raise ValueError(
                "n_components=%r must be between 0 and "
                "min(n_samples, n_features)=%r with "
                "svd_solver='full'" % (n_components, min(n_samples, n_features))
            )
        elif n_components >= 1:
            if not isinstance(n_components, numbers.Integral):
                raise ValueError(
                    "n_components=%r must be of type int "
                    "when greater than or equal to 1, "
                    "was of type=%r" % (n_components, type(n_components))
                )

        if w is None:
            w = np.ones(n_samples)
        #         # Center
        #         X -= self.mean_
        #         # Reweight
        #         X = np.multiply(X, w[:, np.newaxis])

        #         U, S, Vt = linalg.svd(X, full_matrices=False)
        #         # flip eigenvectors' sign to enforce deterministic output
        #         U, Vt = svd_flip(U, Vt)
        # this might be faster than the one below
        self.mean_ = np.dot(w, X) / np.sum(w)
        # self.mean_ = np.average(X, axis = 0, weights=w)
        X_c = X - self.mean_
        # C = np.cov(X_c, rowvar=False, fweights=w)
        C = (X_c * w[:, np.newaxis]).T @ X_c / (np.sum(w) - 1)

        evals, evecs = np.linalg.eigh(C)
        # Flip order to descending
        evals = evals[::-1]
        evecs = evecs[:, ::-1]
        # Compute singular values
        S = np.sqrt(np.abs(evals) * (np.sum(w) - 1))

        # print(np.all(np.isclose(C2 @ evecs2, evecs2 @ np.diag(evals2))))

        Vt = evecs.T
        U = (X_c @ Vt.T) / S
        U, Vt = svd_flip(U, Vt)

        components_ = Vt

        # Get variance explained by singular values
        if norm_S is not None:
            explained_variance_ = (S ** 2) / (norm_S - 1)
        else:
            explained_variance_ = (S ** 2) / (np.sum(w) - 1)
        total_var = explained_variance_.sum()
        explained_variance_ratio_ = explained_variance_ / total_var
        singular_values_ = S.copy()  # Store the singular values.

        # Postprocess the number of components required
        if n_components == "mle":
            n_components = _infer_dimension(explained_variance_, n_samples)
        elif 0 < n_components < 1.0:
            # number of components for which the cumulated explained
            # variance percentage is superior to the desired threshold
            # side='right' ensures that number of features selected
            # their variance is always greater than n_components float
            # passed. More discussion in issue: #15669
            ratio_cumsum = stable_cumsum(explained_variance_ratio_)
            n_components = np.searchsorted(ratio_cumsum, n_components, side="right") + 1
        # Compute noise covariance using Probabilistic PCA model
        # The sigma2 maximum likelihood (cf. eq. 12.46)
        if n_components < min(n_features, n_samples):
            self.noise_variance_ = explained_variance_[n_components:].mean()
        else:
            self.noise_variance_ = 0.0

        self.n_samples_ = n_samples
        self.n_features_in_ = n_features
        self.components_ = components_[:n_components]
        self.n_components_ = n_components
        self.explained_variance_ = explained_variance_[:n_components]
        self.explained_variance_ratio_ = explained_variance_ratio_[:n_components]
        self.singular_values_ = singular_values_[:n_components]

        return U, S, Vt

    def get_covariance(self):
        components_ = self.components_
        exp_var = self.explained_variance_
        if self.whiten:
            components_ = components_ * np.sqrt(exp_var[:, np.newaxis])
        exp_var_diff = np.maximum(exp_var - self.noise_variance_, 0.0)
        cov = np.dot(components_.T * exp_var_diff, components_)
        cov.flat[:: len(cov) + 1] += self.noise_variance_  # modify diag inplace
        return cov

    def get_corrcoef(self):
        c = self.get_covariance()
        try:
            d = np.diag(c)
        except ValueError:  # scalar covariance
            # nan if incorrect value (nan, inf, 0), 1 otherwise
            return c / c
        return c / sqrt(np.multiply.outer(d, d))
