import numpy as np

from ..coreset.common import w_dot_X


class WSVD:

    def __init__(self, k=2):
        self.k = k
        pass

    def fit(self, X, y=None, sample_weight=None):
        """
        Samples and fits the data. Sets self.model to the V components as a np.array
        Arguments
            X {array-like} -- (n_samples, n_features) feature array
            y Ignored -- not used
            w {array-like} -- (n_sampples, )  apriori weight array
        Returns
            {np.array} -- the V components
        """
        w = sample_weight
        _, _, V_T = np.linalg.svd(w_dot_X(X, w=w), full_matrices=False)
        self.model = V_T[0: self.k, :]
        return self

    def predict(self, X):
        """
        Predicts using the fitted model.
        Arguments:
            X {array-like} -- (n_samples, n_features) feature array
        Return
            {array-like} -- (n_samples, k+1) samples svd-reduced over the V component
        """
        return X.dot(self.model.T)

    def cost(self, X, y=None):
        if isinstance(X, dict):
            X = X["X"]
        return np.linalg.norm(X - (self.predict(X)).dot(self.model))

    def score(self, X, y=None):
        return -self.cost(X, y)