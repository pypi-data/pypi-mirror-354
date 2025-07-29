from copy import deepcopy
import numpy as np
from typing import Optional, Union, Dict, List
from dataheroes.core.estimator._base import SensitivityEstimatorBase
from numpy.random import Generator
from dataheroes.core.numpy_extra import _to_python_obj, group_by_label
from dataheroes.core.coreset.coreset_lg import estimate_unified, estimate_unified_one
from dataheroes.core.coreset._base import CoresetBase


class SensitivityEstimatorUnified(SensitivityEstimatorBase):
    _expected_sensitivities: List[str] = ["unified"]
    _requires_classes: bool = True

    def __init__(
        self,
        d: Dict,
        sampling_ratios: dict,
        history: Optional[dict] = None,
        sliding_window_size: Optional[int] = None,
        adjust_threshold: int = 1_000_000,
        auto_adjust: bool = True,
        adjustment_strength: float = 0.1,
        adjust_history: Optional[dict] = None,
        random_state: Optional[Union[int, Generator]] = None,
    ):
        self.d = d
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

    @classmethod
    def from_sensitivities(
        cls,
        d: dict,
        sensitivities: np.ndarray,
        y: np.ndarray,
        percent: Union[float, dict] = 1,
        percent_step: float = 0.1,
        percent_n_steps: int = 5,
        sliding_window_size: Optional[int] = None,
        adjust_threshold: int = 1_000_000,
        auto_adjust: bool = True,
        adjustment_strength: float = 0.1,
        random_state: Optional[Union[int, Generator]] = None,
    ) -> "SensitivityEstimatorUnified":
        """Construct an estimator from a given array of senstivities and classes

        Parameters
        ----------
        d : dict
            dict with sensitivity information for estimation. Contains the D_inv matrices

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
        SensitivityEstimatorUnified
        """
        
        sensitivities_dict = group_by_label(sensitivities, labels=y)
        sampling_ratios = cls._tables_from_sensitivities(
            sensitivities_dict=sensitivities_dict,
            percent=percent,
            percent_step=percent_step,
            percent_n_steps=percent_n_steps,
            random_state=random_state,
            requires_classes=cls._requires_classes,
        )
        return cls(
            d=d,
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
    ) -> "SensitivityEstimatorUnified":
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
        SensitivityEstimatorUnified
        """
        
        coreset, sensitivities, y = cls._check_before_tables(coreset=coreset, sensitivities=sensitivities, y=y)
        # Delete D, we only need D_inv for estimation.
        d = deepcopy(coreset.estimation_params_)
        for c in d:
            del d[c]["D"]

        return cls.from_sensitivities(
            d=d,
            # sensitivities_dict=sens_dict,
            sensitivities=sensitivities,
            y=y,
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
        for c in list(data["d"].keys()):
            if isinstance(c, str) and c not in data["sampling_ratios"]["classes"]:
                if c.isdigit():
                    c_ = int(c)
                    assert c_ in data["sampling_ratios"]["classes"]
                    data["d"][c_] = data["d"].pop(c)
                elif c.replace(".", "").isdigit():
                    c_ = float(c)
                    assert c_ in data["sampling_ratios"]["classes"]
                    data["d"][c_] = data["d"].pop(c)
                else:
                    raise ValueError(f"Class {c} not in {data['sampling_ratios']['classes']}")
        return data

    def to_dict(self, as_lists: bool = True, include_adjust_history: bool = False) -> Dict:
        res = super().to_dict(as_lists=as_lists, include_adjust_history=include_adjust_history)
        if as_lists:
            res["d"] = _to_python_obj(deepcopy(self.d))
        return res

    @classmethod
    def from_dict(cls, data: Dict, as_arrays: bool = True) -> "SensitivityEstimatorUnified":
        if as_arrays:
            data = cls._to_arrays_dict(data=data)
            for c in data["sampling_ratios"]["classes"]:
                data["d"][c]["D_inv"] = np.array(data["d"][c]["D_inv"])
        return cls(**data)

    def estimate(self, X, y, w=None) -> np.ndarray:
        return estimate_unified(X, y, d_dict=self.d, w=w)

    def estimate_one(self, X, y, w=None) -> float:
        w = w if w is not None else 1
        return estimate_unified_one(X, y, d_dict=self.d, w=w)
