from ._base import CoresetBase
import numpy as np

from typing import Optional, Union, List
from numpy.random import Generator

from .coreset_lg import (
    sensitivity_unified,
    estimate_unified,
    union_unified,
    sensitivity_lg_lightweight,
    estimate_lightweight,
)


class CoresetDTC(CoresetBase):
    _coreset_type = "classification"
    _possible_sensitivities = ["unified", "lightweight", "lightweight_per_feature"]
    _possible_estimators = ["unified", "lightweight", "lightweight_per_feature"]
    _possible_unions = ["unified"]

    def __init__(
        self,
        *,
        algorithm: str = "unified",
        enable_estimation: bool = False,
        random_state: Union[int, Generator] = None,
        **sensitivity_kwargs,
    ):
        """Coreset for the Decision Trees classification task.

        Parameters
        ----------
        algorithm: str, default = "unified"
            sensitivity algorithm. One of ["unified", "lightweight", "lightweight_per_feature"]

        enable_estimation: bool, default = False
            True - estimation will be enabled. When the sensitivity is calculated, will compute all information necessary for estimation.
                The algorithm provided must be one of  ["unified", "lightweight", "lightweight_per_feature"]
            False - Estimation is disabled. Any attempt to estimate with this parameter false should raise an error.
            
        random_state: int or np.random.Generator
            int - creates a random generator with the `random_state` seed
            Generator - uses the given generator

        **sensitivity_kwargs: Key arguments
            parameters to be passed to the sensitivity function
        """
        super().__init__(random_state=random_state)
        self._algorithm = algorithm
        self.is_classification = True
        self.sensitivity_kwargs = sensitivity_kwargs
        self.enable_estimation = enable_estimation
        self.estimation_params_ = None

        # Set sensitivity
        if algorithm not in self._possible_sensitivities:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")
        if self.enable_estimation and algorithm not in self._possible_estimators:
            raise ValueError(
                f"For estimation, `algorithm` must be one of {self._possible_estimators}, found {algorithm}"
            )
        self._algorithm = algorithm

    def sensitivity(self, X, y=None, w=None, estimate: bool = False) -> np.ndarray:
        if self.algorithm == "unified":
            sensitivity_f = sensitivity_unified
        elif self.algorithm == "lightweight" or self.algorithm == "lightweight_per_feature":
            sensitivity_f = sensitivity_lg_lightweight
            if self.algorithm == "lightweight_per_feature":
                self.sensitivity_kwargs["per_feature"] = True
            if "class_weight" in self.sensitivity_kwargs:
                self.sensitivity_kwargs.pop("class_weight")
        else:
            raise ValueError(f"Sensitivity must be in {self._possible_sensitivities}")

        if self.algorithm in self._possible_estimators:
            self.sensitivity_kwargs["return_info"] = self.enable_estimation

        if estimate:
            # Estimation can happen only if sensitivity was computed before in the attribute estimation_params_
            self._check_estimation_requirements()
            if self.algorithm == "unified":
                sensitivities = estimate_unified(X, y, d_dict=self.estimation_params_, w=w)
            elif self.algorithm == "lightweight" or self.algorithm == "lightweight_per_feature":
                sensitivities = estimate_lightweight(
                    X=X,
                    w=w,
                    mu=self.estimation_params_["mu"],
                    w_sum=self.estimation_params_["w_sum"],
                    di_sum=self.estimation_params_["di_sum"],
                    per_feature=self.algorithm == "lightweight_per_feature",
                )
        else:
            res = sensitivity_f(X=X, y=y, w=w, **self.sensitivity_kwargs)
            # If estimation was enabled return and save information for estimation.
            # This is used to check if estimation is possible in _check_estimation_requirements()
            if self.enable_estimation:
                sensitivities, self.estimation_params_ = res
                self._estimation_algorithm_used = self.algorithm
            else:
                sensitivities = res
        return sensitivities

    def compute_sensitivities(self, X, y=None, w=None, estimate: bool = False):
        self.sensitivities = self.sensitivity(X, y, w, estimate=estimate) if X.shape[0] > 0 else np.ndarray([])
        return self

    def union(self, coresets: List["CoresetDTC"]) -> "CoresetDTC":
        """Updates Self estimation capabilities by combining a list of coresets.
        This method does not need the coresets to be fully built. It just needs `sens_info` to be available and their algorithm to match.
        This method will enable the newly built CoresetDTC to estimate sensitivities. 

        Parameters
        ----------
        coresets : List[CoresetDTC]

        Returns
        -------
        CoresetDTC
            Self    

        Raises
        ------
        NotImplementedError
            If the union is not implemented for the algorithms provided
        ValueError
            If the algorithm of the provided coresets do not match
        """
        if self.algorithm not in self._possible_unions:
            raise NotImplementedError(f"union for {self.algorithm} does not exist yet")
        else:
            if any(c.algorithm != coresets[0].algorithm for c in coresets) or any(
                c._estimation_algorithm_used != coresets[0]._estimation_algorithm_used for c in coresets
            ):
                raise ValueError("All provided coresets must have been prepared with the same sensitivity algorithm")
            if self.algorithm == "unified":
                self.estimation_params_ = union_unified([c.estimation_params_ for c in coresets])
            self.enable_estimation = True
            self._estimation_algorithm_used = self.algorithm
        return self
