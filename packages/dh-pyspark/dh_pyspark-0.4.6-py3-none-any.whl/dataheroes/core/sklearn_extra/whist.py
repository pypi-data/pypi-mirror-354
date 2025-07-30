import numpy as np

def weighted_histogram(X, algorithm, **kwargs):
    """
    Coresets the data, predicts on the sampled indexes and
    applies a weighted np.bincount() with the computed weights

    Arguments
        X: {array-like} -- (n_samples, n_features) Data to histogram
        algorithm: {KMeans-like} -- An algorithm to compute the coreset
        algorithm_kwargs: {key arguments} -- Key that will be passed to the provided algorithm

    Returns
        h: {array-like} --  (n_centers, ) the computed histogram
    """
    X = np.array(X)
    cmodel = algorithm(**kwargs)
    cmodel.fit(X)
    idxs, weights = cmodel.idxs, cmodel.weights
    preds = cmodel.predict(X[idxs])
    h = np.bincount(preds, weights=weights)
    return h


def per_feature_weighted_histograms(X, algorithm, **kwargs):
    """
    Calls `weighted_histogram()` for each feature which:
    coresets the data, predicts on the sampled indexes and
    applies a weighted np.bincount() with the computed weights

    Arguments
        X: {array-like} -- (n_samples, n_features) Data to histogram
        algorithm: {KMeans-like} -- An algorithm to compute the coreset
        algorithm_kwargs: {key arguments} -- Key th2at will be passed to the provided algorithm

    Returns
        hs: {array-like} -- (n_features, n_centers) array of histogram
    """
    X = np.array(X)
    hs = []
    for feature in X.T:
        feature = feature[:, np.newaxis]
        h = weighted_histogram(feature, algorithm, **kwargs)
        hs.append(h)
    return np.array(hs)



def proj(P, kmeans):
    ind = kmeans.predict(P)
    P_tag = np.zeros_like(P)
    cluster_size = np.zeros(P.shape[0])
    for i in range(kmeans.n_clusters):
        temp_ind = np.where(ind == i)[0]
        cluster_size[temp_ind] = len(temp_ind)
        P_tag[temp_ind] = kmeans.cluster_centers_[i]
    return P_tag