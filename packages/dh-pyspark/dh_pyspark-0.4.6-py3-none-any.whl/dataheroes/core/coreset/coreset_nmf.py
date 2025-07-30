from ._base import CoresetBase
from sklearn.decomposition import NMF
from time import time
import numpy as np


def dist_points_to_line_norm(p, l, norm_ord=4):
    """
    p - a set of points sparse Nxd
    l - a line from the origin
    return the distance of p to the closet point on line l
    """
    if type(p) == "scipy.sparse.csr.csr_matrix":
        p = p.todense()

    norm_p = np.linalg.norm(p, axis=1, ord=norm_ord)
    if len(l.shape) == 1:
        l = np.reshape(l, (1, -1))
    l /= np.linalg.norm(l, axis=1, ord=norm_ord)[:, np.newaxis]
    norm_porj = np.linalg.norm(p.dot(l.T), axis=1, ord=norm_ord)
    return (np.abs(-(norm_porj ** norm_ord) + norm_p ** norm_ord)) ** (1.0 / norm_ord)


def dist_points_to_line(p, l):
    """
    p - a set of points sparse Nxd
    l - a line from the origin
    return the euclidean distance of p to the closet point on line l
    """
    if type(p) == "scipy.sparse.csr.csr_matrix":
        p = p.todense()

    norm_p = np.linalg.norm(p, axis=1)
    if len(l.shape) == 1:
        l = np.reshape(l, [-1, 1]).T
    l /= np.linalg.norm(l, axis=1)[:, np.newaxis]
    norm_porj = np.linalg.norm(p.dot(l.T), axis=1)
    return np.sqrt(np.abs(-(norm_porj ** 2) + norm_p ** 2))


class CoresetNMF(CoresetBase):
    def __init__(self, k, coreset_size, replace=True, uniform=False, **nmf_kwargs):
        """
        Arguments
            k: {int} -- number of NMF components - Use 1
            coreset_size: {int} -- max number of samples
            replace: {bool}, default = True -- if coreset sampling is done with replacement
            uniform: {bool}, default = False -- if we should use uniform sampling
        """
        super().__init__(coreset_size, replace)
        self.k = k
        self.what_am_i = "nmf"
        self.model = NMF(n_components=k, **nmf_kwargs)

    def reweight_func(self, X, y=None):
        return X ** 0.5

    def sensitivity(self, X, y=None, w=None):
        if w is not None:
            X = self.w_dot_X(X=X, y=y, w=w)
        P = X
        k = self.k
        if P.shape[0] <= k:
            return np.ones(P.shape[0]) / P.shape[0], None
        nmf = NMF(n_components=k).fit(P)
        l_star = nmf.components_
        rho = 2.0
        alpha = 1.0

        l_star = np.atleast_2d(l_star)
        p_tag = P.dot(l_star.T)  # projection(P,l_star)
        u = np.mean(p_tag, axis=0)

        up1 = dist_points_to_line(P, l_star) ** rho
        down1 = np.sum(up1)
        up2 = np.linalg.norm(p_tag - u, axis=1) ** rho
        down2 = np.sum(up2)
        s_p = rho * alpha * up1 / down1 + (rho ** 2) * up2 / down2 + 2 * ((rho ** 2) * (1 + alpha)) / P.shape[0]

        return s_p

    def fit(self, X, y=None, w=None):
        """
        Samples and fits the data. Sets self.model to a sklearn PCA model
        Arguments
            X {array-like} -- (n_samples, n_features) feature array
            y Ignored -- not used
            w {array-like} -- (n_sampples, )  apriori weight array
            **nmf_kwargs -- arguments for sklearn NMF
        Returns
            {sklearn.decomposition.NMF} -- the model
        """
        # NOTE: Dict use is intended for trees-only (for now)
        if isinstance(X, dict):
            w = X["w"]
            X = X["X"]
            self.model.fit(X)
            return self.model

        # k = self.k
        t = time()
        idxs, w = self.sample(X, w=w, replace=self.replace)
        self.sample_time = time() - t
        X_ = X[idxs, :]
        X_ = self.w_dot_X(X_, w=w)
        self.model.fit(X_)
        return self.model

    def predict(self, X):
        """
        Predicts using the fitted model.
        Arguments:
            X {array-like} -- (n_samples, n_features) feature array
        Return
            {array-like} -- (n_samples, k) samples transformed over k components
        """
        return self.model.transform(X)

    def cost(self, X, y=None, w=None):
        """
        RMSE
        Argument
            X {array-like} -- (n_samples, n_features) feature array
        Return
            {float} -- RMSE
        """
        t = self.model.transform(X)
        t = self.model.inverse_transform(t)
        return np.sqrt(np.sum((X - t) ** 2))
