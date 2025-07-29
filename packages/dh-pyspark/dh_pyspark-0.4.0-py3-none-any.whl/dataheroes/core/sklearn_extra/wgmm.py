from sklearn.mixture import GaussianMixture
from sklearn.mixture._gaussian_mixture import _compute_precision_cholesky
from sklearn.utils import check_random_state
from sklearn.exceptions import ConvergenceWarning
from sklearn import cluster
import numpy as np

from ..sklearn_extra.wkmeans_plusplus import kmeans_plusplus_w
from ...utils import user_warning


class WeightedGaussianMixture(GaussianMixture):
    def _initialize_parameters(self, X, random_state,sample_weight=None):
        """Initialize the model parameters.
        Parameters
        ----------
        X : array-like of shape  (n_samples, n_features)
        random_state : RandomState
            A random number generator instance that controls the random seed
            used for the method chosen to initialize the parameters.
        """
        if sample_weight is None:
            sample_weight = np.ones(len(X))
        n_samples, _ = X.shape

        if self.init_params == "kmeans":
            resp = np.zeros((n_samples, self.n_components))
            label = (
                cluster.KMeans(
                    n_clusters=self.n_components, n_init=1, random_state=random_state
                )
                .fit(X,sample_weight=sample_weight)
                .labels_
            )
            resp[np.arange(n_samples), label] = 1
        elif self.init_params == "random":
            resp = random_state.uniform(size=(n_samples, self.n_components))
            resp /= resp.sum(axis=1)[:, np.newaxis]
        elif self.init_params == "random_from_data":
            resp = np.zeros((n_samples, self.n_components))
            p = 1/(sample_weight + np.finfo(resp.dtype).eps)
            p /= np.sum(p)
            indices = random_state.choice(
                n_samples, size=self.n_components, replace=False,p= p
            )
            resp[indices, np.arange(self.n_components)] = 1
        elif self.init_params == "k-means++":
            resp = np.zeros((n_samples, self.n_components))
            _, indices = kmeans_plusplus_w(
                X,
                self.n_components,
                random_state=random_state,
                w = sample_weight
            )
            resp[indices, np.arange(self.n_components)] = 1
        else:
            raise ValueError(
                "Unimplemented initialization method '%s'" % self.init_params
            )

        self._initialize(X, resp)
    def fit(self,X,y=None,sample_weight=None):

        """Estimate model parameters with the EM algorithm.
        The method fits the model ``n_init`` times and sets the parameters with
        which the model has the largest likelihood or lower bound. Within each
        trial, the method iterates between E-step and M-step for ``max_iter``
        times until the change of likelihood or lower bound is less than
        ``tol``, otherwise, a ``ConvergenceWarning`` is raised.
        If ``warm_start`` is ``True``, then ``n_init`` is ignored and a single
        initialization is performed upon the first call. Upon consecutive
        calls, training starts where it left off.
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            List of n_features-dimensional data instances. Each row
            corresponds to a single data point.
        y : Ignored
            Not used, present for API consistency by convention.
        Returns
        -------
        self : object
            The fitted mixture.
        """
        self.fit_predict(X, y, sample_weight)
        return self

    def fit_predict(self, X, y=None, sample_weight = None):
        """Estimate model parameters using X and predict the labels for X.
        The method fits the model n_init times and sets the parameters with
        which the model has the largest likelihood or lower bound. Within each
        trial, the method iterates between E-step and M-step for `max_iter`
        times until the change of likelihood or lower bound is less than
        `tol`, otherwise, a :class:`~sklearn.exceptions.ConvergenceWarning` is
        raised. After fitting, it predicts the most probable label for the
        input data instances.
        .. versionadded:: 0.20
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            List of n_features-dimensional data instances. Each row
            corresponds to a single data point.
        y : Ignored
            Not used, present for API consistency by convention.
        Returns
        -------
        labels : array, shape (n_samples,)
            Component labels.
        """
        if sample_weight is None:
            sample_weight = np.ones(len(X))
        sample_weight = np.array(sample_weight,dtype=np.float32)

        X = self._validate_data(X, dtype=[np.float64, np.float32], ensure_min_samples=2)
        if X.shape[0] < self.n_components:
            raise ValueError(
                "Expected n_samples >= n_components "
                f"but got n_components = {self.n_components}, "
                f"n_samples = {X.shape[0]}"
            )
        self._check_initial_parameters(X)

        # if we enable warm_start, we will have a unique initialisation
        do_init = not (self.warm_start and hasattr(self, "converged_"))
        n_init = self.n_init if do_init else 1

        max_lower_bound = -np.inf
        self.converged_ = False

        random_state = check_random_state(self.random_state)

        n_samples, _ = X.shape
        for init in range(n_init):
            self._print_verbose_msg_init_beg(init)

            if do_init:
                self._initialize_parameters(X, random_state,sample_weight=sample_weight)

            lower_bound = -np.inf if do_init else self.lower_bound_

            if self.max_iter == 0:
                best_params = self._get_parameters()
                best_n_iter = 0
            else:
                for n_iter in range(1, self.max_iter + 1):
                    prev_lower_bound = lower_bound

                    log_prob_norm, log_resp = self._e_step(X,sample_weight=sample_weight)
                    self._m_step(X, log_resp,sample_weight=sample_weight)
                    lower_bound = self._compute_lower_bound(log_resp, log_prob_norm)

                    change = lower_bound - prev_lower_bound
                    self._print_verbose_msg_iter_end(n_iter, change)

                    if abs(change) < self.tol:
                        self.converged_ = True
                        break

                self._print_verbose_msg_init_end(lower_bound)

                if lower_bound > max_lower_bound or max_lower_bound == -np.inf:
                    max_lower_bound = lower_bound
                    best_params = self._get_parameters()
                    best_n_iter = n_iter

        # Should only warn about convergence if max_iter > 0, otherwise
        # the user is assumed to have used 0-iters initialization
        # to get the initial means.
        if not self.converged_ and self.max_iter > 0:
            user_warning(
                "Initialization %d did not converge. "
                "Try different init parameters, "
                "or increase max_iter, tol "
                "or check for degenerate data." % (init + 1),
                ConvergenceWarning,
            )

        self._set_parameters(best_params)
        self.n_iter_ = best_n_iter
        self.lower_bound_ = max_lower_bound

        # Always do a final e-step to guarantee that the labels returned by
        # fit_predict(X) are always consistent with fit(X).predict(X)
        # for any value of max_iter and tol (and any random_state).
        _, log_resp = self._e_step(X,sample_weight)

        return log_resp.argmax(axis=1)


    def _e_step(self, X,sample_weight):
        """E step.
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
        Returns
        -------
        log_prob_norm : float
            Mean of the logarithms of the probabilities of each sample in X
        log_responsibility : array, shape (n_samples, n_components)
            Logarithm of the posterior probabilities (or responsibilities) of
            the point of each sample in X.
        """
        log_prob_norm, log_resp = self._estimate_log_prob_resp(X)
        return np.average(log_prob_norm,weights=sample_weight), log_resp

    def _m_step(self, X, log_resp,sample_weight):
        """M step.
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
        log_resp : array-like of shape (n_samples, n_components)
            Logarithm of the posterior probabilities (or responsibilities) of
            the point of each sample in X.
        """

        self.weights_, self.means_, self.covariances_ = _estimate_gaussian_parameters(
            X, np.exp(log_resp), self.reg_covar, self.covariance_type,sample_weight
        )

        self.weights_ /= self.weights_.sum()
        self.precisions_cholesky_ = _compute_precision_cholesky(
            self.covariances_, self.covariance_type
        )

def _estimate_gaussian_parameters(X, resp, reg_covar, covariance_type,sample_weight):
    """Estimate the Gaussian distribution parameters.
    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The input data array.
    resp : array-like of shape (n_samples, n_components)
        The responsibilities for each data sample in X.
    reg_covar : float
        The regularization added to the diagonal of the covariance matrices.
    covariance_type : {'full', 'tied', 'diag', 'spherical'}
        The type of precision matrices.
    Returns
    -------
    nk : array-like of shape (n_components,)
        The numbers of data samples in the current components.
    means : array-like of shape (n_components, n_features)
        The centers of the current components.
    covariances : array-like
        The covariance matrix of the current components.
        The shape depends of the covariance_type.
    """
    nk = np.sum(resp,axis=0) + 10 * np.finfo(resp.dtype).eps
    means = np.dot(np.multiply(resp, sample_weight[:, np.newaxis]).T, X)*len(X) / (nk[:, np.newaxis]*np.sum(sample_weight))
    means = np.dot(resp.T, X) / (nk[:, np.newaxis])
    
    covariances = {
        "full": _estimate_gaussian_covariances_full,
        "tied": _estimate_gaussian_covariances_tied,
        "diag": _estimate_gaussian_covariances_diag,
        "spherical": _estimate_gaussian_covariances_spherical,
    }[covariance_type](resp, X, nk, means, reg_covar,sample_weight)
    return nk, means, covariances

def _estimate_gaussian_covariances_full(resp, X, nk, means, reg_covar,sample_weight):
    """Estimate the full covariance matrices.
    Parameters
    ----------
    resp : array-like of shape (n_samples, n_components)
    X : array-like of shape (n_samples, n_features)
    nk : array-like of shape (n_components,)
    means : array-like of shape (n_components, n_features)
    reg_covar : float
    Returns
    -------
    covariances : array, shape (n_components, n_features, n_features)
        The covariance matrix of the current components.
    """
    n_components, n_features = means.shape
    covariances = np.empty((n_components, n_features, n_features))
    for k in range(n_components):
        diff = X - means[k]
        #covariances[k] = np.dot(sample_weight*resp[:, k] * diff.T, diff)*len(X) / (nk[k]*np.sum(sample_weight))
        covariances[k] = np.dot(resp[:, k] * diff.T, diff) / (nk[k])
        covariances[k].flat[:: n_features + 1] += reg_covar
    return covariances


def _estimate_gaussian_covariances_tied(resp, X, nk, means, reg_covar,sample_weight):
    """Estimate the tied covariance matrix.
    Parameters
    ----------
    resp : array-like of shape (n_samples, n_components)
    X : array-like of shape (n_samples, n_features)
    nk : array-like of shape (n_components,)
    means : array-like of shape (n_components, n_features)
    reg_covar : float
    Returns
    -------
    covariance : array, shape (n_features, n_features)
        The tied covariance matrix of the components.
    """
    avg_X2 = np.dot(np.dot(sample_weight,X).T, X)/np.sum(sample_weight)
    avg_means2 = np.dot(nk * means.T, means)
    covariance = avg_X2 - avg_means2
    covariance /= nk.sum()
    covariance.flat[:: len(covariance) + 1] += reg_covar
    return covariance


def _estimate_gaussian_covariances_diag(resp, X, nk, means, reg_covar,sample_weight):
    """Estimate the diagonal covariance vectors.
    Parameters
    ----------
    responsibilities : array-like of shape (n_samples, n_components)
    X : array-like of shape (n_samples, n_features)
    nk : array-like of shape (n_components,)
    means : array-like of shape (n_components, n_features)
    reg_covar : float
    Returns
    -------
    covariances : array, shape (n_components, n_features)
        The covariance vector of the current components.
    """
    avg_X2 = np.dot(resp.T, X * X) / nk[:, np.newaxis]
    avg_means2 = means**2
    avg_X_means = means * np.dot((sample_weight*resp).T, X) / nk[:, np.newaxis]
    return avg_X2 - 2 * avg_X_means + avg_means2 + reg_covar


def _estimate_gaussian_covariances_spherical(resp, X, nk, means, reg_covar,sample_weight):
    """Estimate the spherical variance values.
    Parameters
    ----------
    responsibilities : array-like of shape (n_samples, n_components)
    X : array-like of shape (n_samples, n_features)
    nk : array-like of shape (n_components,)
    means : array-like of shape (n_components, n_features)
    reg_covar : float
    Returns
    -------
    variances : array, shape (n_components,)
        The variance values of each components.
    """
    return _estimate_gaussian_covariances_diag(resp, X, nk, means, reg_covar,sample_weight).mean(1)


if __name__ == "__main__":
    def test1():
        X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
        gm1 = WeightedGaussianMixture(n_components=2, random_state=0,max_iter=300).fit(X,sample_weight=1*np.ones(len(X)))
        gm2 = WeightedGaussianMixture(n_components=2, random_state=0,max_iter=300).fit(X,sample_weight=2000*np.ones(len(X)))

        res = True
        if not np.allclose(gm1.means_,gm2.means_):
            print("Bad means")
            res =  False

        if not np.allclose(gm1.covariances_,gm2.covariances_):
            print("Bad covariances_")
            res = False
        return res

    def test2():
        n_iter = 100
        X = np.concatenate([np.array([[1, 2]]), np.array(100*[[14, 27]])],axis=0)
        gm1 = GaussianMixture(n_components=2, random_state=0,max_iter=n_iter).fit(np.concatenate([X]))
        
        X = np.concatenate([np.array([[1, 2]]), np.array([[14, 27]])],axis=0)
        gm2 = WeightedGaussianMixture(n_components=2, random_state=0,max_iter=n_iter).fit(X,sample_weight=[1,100])

        res = True
        if not np.allclose(gm1.means_,gm2.means_[::-1]):
            print("Bad means")
            print(gm1.means_,gm2.means_)
            res =  False

        if not np.allclose(gm1.covariances_,gm2.covariances_):
            print("Bad covariances_")
            res = False
        return res


    def test3():
        n_iter = 100
        rep = 100
        X1 = np.random.randn(100,2)
        X2 = np.random.randn(100,2)+190
        X = np.concatenate([X1,np.repeat(X2,rep,axis=0)],axis=0)
        gm1 = GaussianMixture(n_components=2, random_state=0,max_iter=n_iter).fit(np.concatenate([X]))
        
        X = np.concatenate([X1,X2],axis=0)
        w = np.ones(len(X))
        w[len(X1):] = rep
        gm2 = WeightedGaussianMixture(n_components=2, random_state=0,max_iter=n_iter).fit(X,sample_weight=w)

        
        
        res = True
        if not np.allclose(gm1.means_,gm2.means_):
            print("Bad means")
            print(gm1.means_,gm2.means_)
            res =  False

        if not np.allclose(gm1.covariances_,gm2.covariances_):
            print("Bad covariances_")
            print(gm1.covariances_,gm2.covariances_)
            res = False
        return res
    print("test1:")
    print(test1())
    print(17*"_")
    
    
    print("test3:")
    print(test2())
    print(17*"_")
    
    print("test3:")
    print(test3())
    print(17*"_")

