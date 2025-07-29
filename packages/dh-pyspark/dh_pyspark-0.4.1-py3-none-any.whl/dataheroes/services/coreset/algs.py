import os

import numpy as np
from typing import Iterable, Tuple, Union

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.cluster import KMeans

from .._coreset_service_base import DataManagerT
from ...core.coreset import CoresetLG, CoresetDTC, CoresetSVD, CoresetPCA, CoresetKMeans, CoresetReg
from ...core.sklearn_extra import WSVD, WPCA, kmeans_plusplus_w

from ._base import CoresetService
from ..common import CoresetParamsSVD, CoresetParamsPCA, CoresetParamsKMeans, CoresetParamsLR, CoresetParamsLG, \
    CoresetParamsDTC, CoresetParams
from ...data import DataParams
from ...utils import telemetry
from .. import helpers


class CoresetServiceSVD(CoresetService):
    coreset_cls = CoresetSVD
    coreset_params_cls = CoresetParamsSVD
    model_cls = WSVD

    _is_supervised = False


class CoresetServiceClassification(CoresetService):
    is_classification = True
    _is_supervised = True

    @telemetry
    def get_coreset(self, inverse_class_weight: bool = True) -> Tuple[Iterable, Iterable]:
        """Return the indexes and weights. If  `class_weights` is provided and `inverse_class_weight = True`
        the weights will be divided by the class weights, therefore requiring the user to pass
        `class_weights` again the `fit` function.

        Parameters:
            inverse_class_weight: boolean, default True
                True - return weights / class_weights
                False - return weights as they are.


        Returns:
            Tuple[Iterable, Iterable]
                idxs, weights
        """
        idxs, weights = super().get_coreset()
        coreset_params = self.coreset_params.to_dict()
        if inverse_class_weight and "class_weight" in coreset_params and coreset_params["class_weight"] is not None:
            cw = coreset_params["class_weight"]
            # Get classes
            y_encoded = self.coreset.y_encoded[idxs]  # Select only the indexes
            y = self.coreset._decode_classes(y_encoded)

            # Adjust weights with the inverse of what was provided
            cw = np.array([cw.get(yi, 1.0) for yi in y])
            weights = weights / cw

        return idxs, weights


class CoresetServiceLG(CoresetServiceClassification):
    coreset_cls = CoresetLG
    coreset_params_cls = CoresetParamsLG
    model_cls = LogisticRegression


class CoresetServiceDTC(CoresetServiceClassification):

    coreset_cls = CoresetDTC
    coreset_params_cls = CoresetParamsDTC

    @telemetry
    def __init__(self, *, data_manager: DataManagerT = None, data_params: Union[DataParams, dict] = None,
                 coreset_size: Union[int, dict, float] = 0.05, coreset_params: Union[CoresetParams, dict] = None,
                 sample_all: Iterable = None, working_directory: Union[str, os.PathLike] = None,
                 cache_dir: Union[str, os.PathLike] = None):
        if helpers.is_xgb_installed():
            from xgboost import XGBClassifier
            self.model_cls = XGBClassifier
        elif helpers.is_lgb_installed():
            from lightgbm import LGBMClassifier
            self.model_cls = LGBMClassifier
        elif helpers.is_catboost_installed():
            from catboost import CatBoostClassifier
            self.model_cls = CatBoostClassifier
        else:
            self.model_cls = GradientBoostingClassifier
        super().__init__(data_manager=data_manager,
                         data_params=data_params,
                         coreset_size=coreset_size,
                         coreset_params=coreset_params,
                         sample_all=sample_all,
                         working_directory=working_directory,
                         cache_dir=cache_dir)


class CoresetServicePCA(CoresetService):
    """Subclass of CoresetService for PCA"""

    coreset_cls = CoresetPCA
    model_cls = WPCA
    coreset_params_cls = CoresetParamsPCA

    _is_supervised = False


class CoresetServiceKMeans(CoresetService):
    """Subclass of CoresetService for KMeans"""

    coreset_cls = CoresetKMeans
    model_cls = KMeans
    coreset_params_cls = CoresetParamsKMeans

    _is_supervised = False

    def _fit_internal(
        self, X, y, weights, model=None, params=None, preprocessing_info: dict = None, sparse_threshold: float = None, n_clusters=None, **model_params
    ):
        initial_centers, _ = kmeans_plusplus_w(
            X=X, n_clusters=n_clusters, w=weights, random_state=model_params.get("random_state")
        )
        model = self.model_cls(n_clusters=n_clusters, n_init=1, **model_params) if model is None else model
        model.set_params(init=initial_centers)
        # Not for all modeling classes' "fit" method, the sample weights are in the 3rd positional argument (Catboost,
        # for example); however, the name of the argument for all of them - as far as we know - is called
        # "sample_weight" - and that's why we specifically use the named argument for weights.
        model.fit(X, y, sample_weight=weights)
        return model


class CoresetServiceLR(CoresetService):
    """Subclass of CoresetService for linear regression"""

    coreset_cls = CoresetReg
    model_cls = LinearRegression
    coreset_params_cls = CoresetParamsLR

    _is_supervised = True
