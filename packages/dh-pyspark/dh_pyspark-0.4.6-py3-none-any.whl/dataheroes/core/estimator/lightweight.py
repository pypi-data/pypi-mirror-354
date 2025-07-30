from copy import deepcopy
import numpy as np
from typing import Optional, Union, Dict, List
from dataheroes.core.coreset.coreset_kmeans import estimate_lightweight
from dataheroes.core.estimator._base import SensitivityEstimatorBase
from numpy.random import Generator
from dataheroes.core.numpy_extra import _to_python_obj
from dataheroes.core.coreset._base import CoresetBase
import warnings


class SensitivityEstimatorLightweight(SensitivityEstimatorBase):
    _expected_sensitivities: List[str] = ["lightweight", "lightweight_per_feature"]
    _requires_classes: bool = False

    def __init__(
        self,
        mu: np.ndarray,
        di_sum: Union[np.ndarray, float],
        w_sum: Union[np.ndarray, float],
        sampling_ratios: dict,
        history: Optional[dict] = None,
        sliding_window_size: Optional[int] = None,
        adjust_threshold: int = 1_000_000,
        auto_adjust: bool = True,
        adjustment_strength: float = 0.1,
        adjust_history: Optional[dict] = None,
        random_state: Optional[Union[int, Generator]] = None,
    ):
        self.mu = mu
        self.di_sum = di_sum
        self.w_sum = w_sum
        super().__init__(
            sampling_ratios=sampling_ratios,
            history=history,
            sliding_window_size=sliding_window_size,
            adjust_threshold=adjust_threshold,
            auto_adjust=auto_adjust,
            adjustment_strength=adjustment_strength,
            adjust_history=adjust_history,
            random_state=random_state,
        )
        self.sampling_ratios = sampling_ratios

    @property
    def per_feature(self) -> bool:
        """Check if lightweight is per feature"""
        return isinstance(self.di_sum, (np.ndarray, list))

    @classmethod
    def from_sensitivities(
        cls,
        mu,
        di_sum,
        w_sum,
        sensitivities: np.ndarray,
        y: Optional[np.ndarray] = None,
        percent: Union[float, dict] = 1,
        percent_step: float = 0.1,
        percent_n_steps: int = 5,
        sliding_window_size: Optional[int] = None,
        adjust_threshold: int = 1_000_000,
        auto_adjust: bool = True,
        adjustment_strength: float = 0.1,
        random_state: Optional[Union[int, Generator]] = None,
    ) -> "SensitivityEstimatorLightweight":
        """Construct an estimator from a given array of senstivities and classes

        Parameters
        ----------
        mu : np.ndarray
            Sensitivity information  mean

        di_sum : Union[np.ndarray, float]
            Sens info distance sum

        w_sum : Union[np.ndarray, float]
            Sensitivity information weight sum

        sensitivities : np.ndarray of shape (n_samples, )
            Sensitivities to build the estimation tables on.

        y : Optional[np.ndarray], default=None
            For compatibility, not used

        percent : Union[float, dict]
            The experceted percentage to be sampled

        percent_step : float
            The percentage step for other computed percentages.

        percent_n_steps : int
            How many percents left and right of `percent` to compute

        sliding_window_size : Optional[int], default=None
            How much history to be kept for adjustment

        adjust_threshold : int, default=1_000_000
            After how many samples should we adjust

        auto_adjust : bool, default=True
            True - Adjustment will be done automatically
            False - Adjustment will be done manually by calling .adjust()

        adjustment_strength : float, default=0.1
            How strong the adjustment should be

        adjust_history : Optional[dict], default=None
            A history of adjustments (formulas, how muich was sampled etc). Not essential for the estimator to work

        random_state : Optional[Union[int, Generator]], default=None
            Random state

        Returns
        -------
        SensitivityEstimatorLightweight
        """
        sensitivities_dict = {cls._DEFAULT_CLASS: sensitivities}
        sampling_ratios = cls._tables_from_sensitivities(
            sensitivities_dict=sensitivities_dict,
            percent=percent,
            percent_step=percent_step,
            percent_n_steps=percent_n_steps,
            random_state=random_state,
            requires_classes=cls._requires_classes,
        )
        return cls(
            mu=mu,
            di_sum=di_sum,
            w_sum=w_sum,
            sampling_ratios=sampling_ratios,
            auto_adjust=auto_adjust,
            adjust_threshold=adjust_threshold,
            adjustment_strength=adjustment_strength,
            sliding_window_size=sliding_window_size,
            random_state=random_state,
        )

    @classmethod
    def from_coreset(
        cls,
        coreset: CoresetBase,
        sensitivities: Optional[np.ndarray] = None,
        y: Optional[np.ndarray] = None,
        percent: Union[float, dict] = 1,
        percent_step: float = 0.1,
        percent_n_steps: int = 5,
        sliding_window_size: Optional[int] = None,
        adjust_threshold: int = 1_000_000,
        auto_adjust: bool = True,
        adjustment_strength: float = 0.1,
        random_state: Optional[Union[int, Generator]] = None,
    ) -> "SensitivityEstimatorLightweight":
        """Construct an estimator from a Coreset. If sensitivities and coreset is not given, it will be constructed from the ones in the coreset.

        Parameters
        ----------
        coreset : CoresetBase
            Coreset from which to build the estimator from

        sensitivities : np.ndarray of shape (n_samples, )
            Sensitivities to build the estimation tables on.

        y : Optional[np.ndarray], default=None
            For compatibility, not used

        percent : Union[float, dict]
            The experceted percentage to be sampled

        percent_step : float
            The percentage step for other computed percentages.

        percent_n_steps : int
            How many percents left and right of `percent` to compute

        sliding_window_size : Optional[int], default=None
            How much history to be kept for adjustment

        adjust_threshold : int, default=1_000_000
            After how many samples should we adjust

        auto_adjust : bool, default=True
            True - Adjustment will be done automatically
            False - Adjustment will be done manually by calling .adjust()

        adjustment_strength : float, default=0.1
            How strong the adjustment should be

        adjust_history : Optional[dict], default=None
            A history of adjustments (formulas, how muich was sampled etc). Not essential for the estimator to work

        random_state : Optional[Union[int, Generator]], default=None
            Random state

        Returns
        -------
        SensitivityEstimatorLightweight
        """
        
        if y is not None:
            warnings.warn("y will be ignored in lightweight estimator. Provide it as class 0 in other functions")
        coreset, sensitivities, y = cls._check_before_tables(coreset=coreset, sensitivities=sensitivities, y=y)
        info = deepcopy(coreset.estimation_params_)
        # sens_dict = group_by_label(sensitivities, labels=y)
        return cls.from_sensitivities(
            mu=info["mu"],
            di_sum=info["di_sum"],
            w_sum=info["w_sum"],
            sensitivities=sensitivities,
            y=y,
            # sensitivities_dict=sens_dict,
            percent=percent,
            percent_step=percent_step,
            percent_n_steps=percent_n_steps,
            sliding_window_size=sliding_window_size,
            adjust_threshold=adjust_threshold,
            auto_adjust=auto_adjust,
            adjustment_strength=adjustment_strength,
            random_state=random_state,
        )

    @classmethod
    def _key_to_class(cls, data: dict) -> dict:
        super()._key_to_class(data=data)
        return data

    def to_dict(self, as_lists: bool = True, include_adjust_history: bool = False) -> Dict:
        res = super().to_dict(as_lists=as_lists, include_adjust_history=include_adjust_history)
        if as_lists:
            res["mu"] = _to_python_obj(self.mu)
            res["di_sum"] = _to_python_obj(self.di_sum)
            res["w_sum"] = _to_python_obj(self.w_sum)
        return res

    @classmethod
    def from_dict(cls, data: Dict, as_arrays: bool = True) -> "SensitivityEstimatorLightweight":
        if as_arrays:
            data = cls._to_arrays_dict(data=data)
            data["mu"] = np.asarray(data["mu"])
            if isinstance(data["di_sum"], list):
                data["di_sum"] = np.asarray(data["di_sum"])
            if isinstance(data["w_sum"], list):
                data["w_sum"] = np.asarray(data["w_sum"])
        return cls(**data)

    def estimate(self, X, y=None, w=None) -> np.ndarray:
        return estimate_lightweight(
            X, w=w, mu=self.mu, w_sum=self.w_sum, di_sum=self.di_sum, per_feature=self.per_feature
        )

    def estimate_one(self, X, y=None, w=None) -> float:
        w = w if w is not None else 1.0
        return estimate_lightweight(
            X, w=w, mu=self.mu, w_sum=self.w_sum, di_sum=self.di_sum, per_feature=self.per_feature
        )[0]
