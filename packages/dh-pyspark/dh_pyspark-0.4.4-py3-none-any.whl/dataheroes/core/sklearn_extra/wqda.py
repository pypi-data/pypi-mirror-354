from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.utils.multiclass import check_classification_targets
import numpy as np
from typing import List


class WQDA(QuadraticDiscriminantAnalysis):
    def fit(self, X, y, sample_weight=None, norm_S=None):
        """Fit the model according to the given training data and parameters.

        Arguments
            X: {array-like} of shape (n_samples, n_features) --
                Training vector, where n_samples is the number of samples and
                n_features is the number of features.

            y: {array-like} of shape (n_samples,) -- Target values (integers)

            w: {array-like} of shape (n_samples,) -- Sample weights

            norm_S: list of len (n_classes) -- The normalizing factor for S**2.
                When using coresets it should be the number of samples per class in the original dataset

        Returns
            self: {WQDA}
        """
        w = sample_weight
        X, y = self._validate_data(X, y)
        check_classification_targets(y)
        if w is None:
            w = np.ones(len(y))  # /len(y)
        w = w / np.sum(w) * len(w)
        self.classes_, y = np.unique(y, return_inverse=True)
        n_samples, n_features = X.shape
        n_classes = len(self.classes_)
        if n_classes < 2:
            raise ValueError("The number of classes has to be greater than" " one; got %d class" % (n_classes))
        if self.priors is None:
            self.priors_ = np.bincount(y) / float(n_samples)
        else:
            self.priors_ = self.priors
        # Validate norm list. TODO make them into Exceptions
        if norm_S is not None:
            assert isinstance(norm_S, (dict, List, np.ndarray, np.generic)), "`norm_S` must be list or np.array or a dictionary"
            assert len(norm_S) == n_classes, "The length of `norm_S` must be the same as the number of classes"
            if isinstance(norm_S, dict):
                norm_S = [norm_S[c] for c in self.classes_]

        cov = None
        store_covariance = self.store_covariance
        if store_covariance:
            cov = []
        means = []
        scalings = []
        rotations = []
        for ind in range(n_classes):
            Xg = X[y == ind, :]
            wg = w[y == ind]
            if norm_S is not None:
                norm = norm_S[ind]
            else:
                norm = None

            # Calculate mean
            meang = np.average(Xg, axis=0, weights=wg)
            means.append(meang)
            if len(Xg) == 1:
                raise ValueError(
                    "y has only 1 sample in class %s, covariance " "is ill defined." % str(self.classes_[ind])
                )
            # Center
            Xgc = Xg - meang
            # Reweight
            Xgc = np.multiply(Xgc, wg[:, np.newaxis])
            # Xgc = U * S * V.T
            _, S, Vt = np.linalg.svd(Xgc, full_matrices=False)
            # rank = np.sum(S > self.tol)

            # Removed this. Not sure what causesd this but it spammed
            # if rank < n_features:
            #     warnings.warn("Variables are collinear")
            if norm is not None:
                S2 = (S ** 2) / (norm - 1)
            else:
                S2 = (S ** 2) / (np.sum(wg) - 1)
            S2 = ((1 - self.reg_param) * S2) + self.reg_param
            if self.store_covariance or store_covariance:
                # cov = V * (S^2 / (n-1)) * V.T
                cov.append(np.dot(S2 * Vt.T, Vt))
            scalings.append(S2)
            rotations.append(Vt.T)
        if self.store_covariance or store_covariance:
            self.covariance_ = cov
        self.means_ = np.asarray(means)
        self.scalings_ = scalings
        self.rotations_ = rotations
        return self
