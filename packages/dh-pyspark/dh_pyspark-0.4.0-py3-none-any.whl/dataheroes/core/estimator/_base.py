from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Union, Dict, Any, List, Tuple
from numpy.random import Generator
from dataheroes.core.coreset._base import CoresetBase
from dataheroes.core.numpy_extra import check_random_state, _to_python_obj, group_by_label, normalize_probs
from copy import deepcopy
import pickle
import json
from pathlib import Path


class SensitivityEstimatorBase(ABC):
    """The base sensitivity estimator class. This class has the job of encompassing the estimation process.
    The goal of this class is to sample data in a streaming fashion such that at the end we will have around p% of the data sampled.
    The idea behing estimation is to build a sampling "table" where on rows we have sampling ratios and on columns percentiles.

    The table is built as follows:
    1. We gather some big array of sensitivities
    2. We compute percentiles of the big array of sensitivities.
    3. We sample p% sensitivities  from the big array.
    4. We see the percent of the sampled sensitivities that "land" between percentiles. These represent probabilities.
    The probabilities should sum up to p%

    The table estimates and samples as follows:
    1. We estimate the sensitivity of a new data point
    2. We see in what percentile it lands
    3. Using the corresponding probability, we sample it or not.

    Ex:
    1. We have 1_000_000 sensitivities
    2. We compute the percentiles, let's say [0, 50, 100, 150, ...]
    3. User wants in the end to sample 5% => we sample 20_000 sensitivities
    4. If 100 points land between [0, 50] => bucket will have 100 / (0.01 * 1_000_000) = 0.01
    If 1234 points land between [0, 50] => bucket will have 1234 / (0.01 * 1_000_000) = 0.1324
    ...

    Even if the user provides p% we will compute tables for more percentages, lower and higher than p%, in steps.
    The parameters for this are controlled by the user.

    The estimator has an adjustment mechanism that adjusts the "corresponding probability" based on history.
    Basically we try to "pull" the probability in the other direction.
    For example, if the user desired 5%, but we previously sampled only 4.2% the probability of the new samples is a weighted mean:
    probability_6% * 0.8 + probability_5% * 0.2.
    The strength of this adjustmenet can also be adjusted.

    The estimator can be serialized and deserialized into json.

    Note: The sampling tables are individual per class, for unsupervized we consider everything to have a default class.
    """

    _expected_sensitivities = []
    _DEFAULT_CLASS: Any = 0

    def __init__(
        self,
        sampling_ratios: dict,
        history: Optional[dict] = None,
        sliding_window_size: Optional[int] = None,
        adjust_threshold: int = 1_000_000,
        auto_adjust: bool = True,
        adjustment_strength: float = 0.1,
        adjust_history: Optional[dict] = None,
        random_state: Optional[Union[int, Generator]] = None,
    ):
        """Init method of the class.

        Parameters
        ----------
        **Any subclass specific parameters. Check subclass __init__ docstring

        sampling_ratios : dict
            Probability tables with all details

        history : Optional[dict], default=None
            History. Essential for the adjustment part of a working estimator.
            If empty it will be initialized as empty

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
            A history of adjustments (formulas, how much was sampled etc). Not essential for the estimator to work

        random_state : Optional[Union[int, Generator]], default=None
            Random state
        """
        self.sampling_ratios = sampling_ratios
        self.adjust_threshold = adjust_threshold
        self.auto_adjust = auto_adjust
        self.adjustment_strength = adjustment_strength
        self.sliding_window_size = sliding_window_size
        self.random_state = check_random_state(random_state)
        self.reset_history(history=history, adjust_history=adjust_history)

    @property
    @abstractmethod
    def _requires_classes(cls):
        raise NotImplementedError

    @property
    def _classes(self) -> List[Any]:
        return self.sampling_ratios["classes"]

    @property
    def n_seen_total(self) -> int:
        # Total seen over all classes
        if self.history is None:
            return 0
        return sum(self.history[c]["n_seen"] for c in self.history if c in self._classes)

    @property
    def n_sampled_total(self) -> int:
        # Total sampled over all classes
        if self.history is None:
            return 0
        return sum(self.history[c]["n_sampled"] for c in self.history if c in self._classes)

    @property
    def n_adjustments(self) -> int:
        return self.history["n_adjustments"]

    @staticmethod
    def _tables_from_sensitivities(
        sensitivities_dict: Dict[Any, np.ndarray],
        percent: Union[float, dict],
        percent_step: float,
        percent_n_steps: int,
        random_state: Union[int, Generator],
        requires_classes: bool,
    ) -> Dict:
        """Construct the sampling tables given the sensitivities.
        For a given percent `percent` we construct tables for it and adjacent percentages in range
        [percent - percent_step * percent_n_steps, percent + percent_step * percent_n_steps]

        Parameters
        ----------
        sensitivities_dict : Dict[Any, np.ndarray]
            The sensitivities in form {class: np.ndarray}

        percent : Union[float, dict]
            The expected percentage to be sampled

        percent_step : float
            The percentage step for other computed percentages.

        percent_n_steps : int
            How many percents left and right of `percent` to compute

        random_state : Union[int, Generator]
            Random state
        Returns
        -------
        Dict
            The sampling tables.
        """
        random_state = check_random_state(random_state)
        sampling_ratios = {}
        # The percent is unique for all classes
        sampling_ratios["classes"] = _to_python_obj(list(sensitivities_dict.keys()))
        sampling_ratios["tables"] = {c: {} for c in sampling_ratios["classes"]}
        if isinstance(percent, dict) and not requires_classes:
            raise ValueError("This estimator cannot receive percent as a dictionary")
        for c, c_sens in sensitivities_dict.items():
            if isinstance(percent, (float, int)):
                sampling_ratios["tables"][c]["target_percent"] = percent
            elif isinstance(percent, dict):
                if c not in percent:
                    raise ValueError(
                        f"Percent dictionary must contain all classes. Clases found: {set(sampling_ratios['classes'])}, percent keys: {set(percent.keys())}"
                    )
                sampling_ratios["tables"][c]["target_percent"] = percent[c]

            target_percent = sampling_ratios["tables"][c]["target_percent"]
            # c = int(c)
            # Compute percentiles for the given array of sensitivities
            percentiles = np.percentile(c_sens, np.arange(0, 100))
            percentiles[0] = 0  # sensitivities can start from 0.
            # Compute the percentages left and right of `percent`
            percents = _to_python_obj(
                np.round(
                    np.arange(
                        target_percent - percent_step * percent_n_steps,
                        target_percent + percent_step * (percent_n_steps + 1),
                        percent_step,
                    ),
                    8,
                )
            )
            # Only keep ones above 0.
            percents = [p for p in percents if p > 0]
            sampling_ratios["tables"][c]["percents"] = percents
            sampling_ratios["tables"][c]["percentiles"] = percentiles
            sampling_ratios["tables"][c]["s_max"] = np.max(percentiles) - 1e-20
            # The initial adjusment formula 1 * percent + 0 * percent
            sampling_ratios["tables"][c]["formula"] = [[1, target_percent], [0, target_percent]]
            # For each percent we sample p%, and put the values into percentile "buckets".
            for perc in percents:
                perc = float(perc)
                s_ = random_state.choice(
                    c_sens, size=int(perc / 100 * len(c_sens)), p=normalize_probs(c_sens), replace=False
                )
                t = np.zeros(100)
                denom = int(0.01 * len(c_sens))
                # denom = 0.01 * len(c_sens)
                if denom != 0:
                    for i, (p1, p2) in enumerate(zip(percentiles, percentiles[1:])):
                        t[i] = np.sum(np.logical_and(s_ >= p1, s_ < p2)) / denom
                    t[-1] = np.sum(s_ >= percentiles[-1]) / denom
                    sampling_ratios["tables"][c][perc] = t
                # When we have few samples we might encounter denom equal to 0. In this case we assign equal probabilities.
                else:
                    sampling_ratios["tables"][c][perc] = np.ones_like(t) / len(t)
        return sampling_ratios

    @classmethod
    def _check_before_tables(cls, coreset: CoresetBase, sensitivities: Optional[np.ndarray], y: Optional[np.ndarray]):
        """method that checks if the coreset, sensitivities and classes are correct before computing the sampling tables

        Parameters
        ----------
        coreset : CoresetBase
            Given coreset

        sensitivities : Optional[np.ndarray]
            Given sensitivities

        y : Optional[np.ndarray]
            Given classes. Will be set to _DEFAULT_CLASS and ignored if the estimator does not require classes

        Returns
        -------
        coreset, sensitivities, y
            y might be modified and set to _DEFAULT_CLASS

        Raises
        ------
        ValueError
        """
        if not coreset.enable_estimation:
            raise ValueError("The coreset was not built for estimation")
        if coreset.algorithm not in cls._expected_sensitivities:
            raise ValueError(f"Expected algorithm one of {cls._expected_sensitivities}, found {coreset.algorithm}")
        elif coreset.estimation_params_ is None:
            raise ValueError("No sensitivity information is available for estimation. Please build the coreset first.")
        if coreset._coreset_type == "classification" and cls._requires_classes:
            if sensitivities is not None and y is None or y is not None and sensitivities is None:
                raise ValueError("Both `sensitivities` and `y` must be provided.")
            if sensitivities is not None and y is not None:
                sensitivities = np.asarray(sensitivities)
                y = np.asarray(y)
                if len(sensitivities) != len(y):
                    raise ValueError("The length of `sensitivities` and `y` must be the same.")
            if sensitivities is None and y is None:
                sensitivities = coreset.sensitivities
                y = coreset._decode_classes(coreset.y)
        else:
            if sensitivities is None:
                sensitivities = coreset.sensitivities
            # Consider all sensitivities as part from a class.
            y = np.full(len(sensitivities), fill_value=cls._DEFAULT_CLASS)
        return coreset, sensitivities, y

    @classmethod
    def _check_y(cls, y: Union[Any, np.ndarray], length: Optional[int] = None) -> Union[Any, np.ndarray]:
        """Checks y before estimating a new value. If length is None, y should be a single value, otherwise y should be an array

        Parameters
        ----------
        y : Union[Any, np.ndarray]
            The class or array of classes, can be None

        length : Optional[int], default=None
            If given, and we don't require classes we will return an array of the given length with the default class


        Returns
        -------
        Union[Any, np.ndarray]
            The array of classes / class

        Raises
        ------
        ValueError
            if y is not provided and is required or if it's not 1-dimensional
        """
        if cls._requires_classes and y is None:
            raise ValueError(f"clsses y must be provided for {cls.__name__}")
        if cls._requires_classes and y is not None:
            if isinstance(y, np.ndarray):
                if y.ndim != 1:
                    raise ValueError("y must be 1-dimensional")
            return y
        if not cls._requires_classes:
            if length is None:
                return cls._DEFAULT_CLASS
            else:
                return np.full(length, fill_value=cls._DEFAULT_CLASS)

    def reset_history(self, history: Optional[dict] = None, adjust_history: Optional[dict] = None):
        """Resets the history and adjustment history if they are given as None.

        Parameters
        ----------
        history : Optional[dict], default=None
            The history that consists of n_seen, n_sampled in total and per batch.

        adjust_history : Optional[dict], default=None
            The detailed history, usually used for debugging and statistics.
        """
        # self.history keeps just the sliding window history.
        # self.adjust_history keeps the full history
        # self.adjust_history are not neeeded for the adjustment to work, they're just statistics.
        self.adjust_history = {}
        if history is None:
            self.history = {}
            self.history["n_adjustments"] = 0
            for c in self._classes:
                self.history[c] = {
                    "n_seen": 0,
                    "n_sampled": 0,
                    "n_seen_batch": 0,
                    "n_sampled_batch": 0,
                    "n_seen_per_batch": [],
                    "n_sampled_per_batch": [],
                }
        else:
            self.history = history
        if adjust_history is None:
            for c in self._classes:
                self.adjust_history[c] = {
                    "target_percents": [],
                    "formulas": [],
                    "hist_percents": [],
                    "n_seen_per_batch": [],
                    "n_sampled_per_batch": [],
                }
        else:
            self.adjust_history = adjust_history

    @classmethod
    def _key_to_class(cls, data: dict) -> dict:
        """Utility method that converts the dictionary keys to actual classes in json ser/de.
        Json does not allow for non-string keys, therefore integers / floats will be converted to strings.
        However, our algorithms should work with int / float keys.
        This method goes through the tables and converts the keys to int / floats, if they were initially int / floats.
        Note that we also saved percents as keys, so this method is also needed to convert them.

        Parameters
        ----------
        data : dict
            state dictionary

        Returns
        -------
        dict
            adjusted state dictionary

        Raises
        ------
        ValueError
            If a class is found that was not in the original list
        """
        # For all found classes
        for c in list(data["sampling_ratios"]["tables"].keys()):
            # If we find a string key that isn't in our saved classes
            if isinstance(c, str) and c not in data["sampling_ratios"]["classes"]:
                # We check if it's digit or float
                if c.isdigit():
                    c_ = int(c)
                    # We check if the conversion is in the classes (it should be if working correctly)
                    assert c_ in data["sampling_ratios"]["classes"]
                    # We replace
                    data["sampling_ratios"]["tables"][c_] = data["sampling_ratios"]["tables"].pop(c)
                    data["history"][c_] = data["history"].pop(c)
                    if "adjust_history" in data:
                        data["adjust_history"][c_] = data["adjust_history"].pop(c)
                elif c.replace(".", "").isdigit():
                    c_ = float(c)
                    assert c_ in data["sampling_ratios"]["classes"]
                    data["sampling_ratios"]["tables"][c_] = data["sampling_ratios"]["tables"].pop(c)
                    data["history"][c_] = data["history"].pop(c)
                    if "adjust_history" in data:
                        data["adjust_history"][c_] = data["adjust_history"].pop(c)
                else:
                    raise ValueError(f"Class {c} not in {data['sampling_ratios']['classes']}")
                keys_to_convert = {}
                for key in data["sampling_ratios"]["tables"][c_]:
                    if key.replace(".", "").isdigit():
                        keys_to_convert[key] = float(key)
                for str_key, float_key in keys_to_convert.items():
                    data["sampling_ratios"]["tables"][c_][float_key] = data["sampling_ratios"]["tables"][c_].pop(
                        str_key
                    )
        return data

    @classmethod
    def _to_arrays_dict(cls, data: dict) -> dict:
        """Utility method that tranforms lists in the state dictionary to np arrays.
        Used when we load from json

        Parameters
        ----------
        data : dict
            state dictionary

        Returns
        -------
        dict
            state dictionary
        """
        for c in data["sampling_ratios"]["classes"]:
            data["sampling_ratios"]["tables"][c]["percents"] = np.array(
                data["sampling_ratios"]["tables"][c]["percents"]
            )
            data["sampling_ratios"]["tables"][c]["percentiles"] = np.array(
                data["sampling_ratios"]["tables"][c]["percentiles"]
            )
            for perc in data["sampling_ratios"]["tables"][c]["percents"]:
                # Probably saved to json and became string
                if perc not in data["sampling_ratios"]["tables"][c]:
                    data["sampling_ratios"]["tables"][c][float(perc)] = np.array(
                        data["sampling_ratios"]["tables"][c].pop(str(perc))
                    )
                else:
                    data["sampling_ratios"]["tables"][c][float(perc)] = np.array(
                        data["sampling_ratios"]["tables"][c][perc]
                    )
        return data

    def to_dict(self, as_lists: bool = True, include_adjust_history: bool = False) -> Dict:
        """method that serializes the estimator into a dictionary

        Parameters
        ----------
        as_lists : bool, default=True
            If the np arrays should be converted to lists

        include_adjust_history : bool, default=False
            If the adjustment history should be included (not necessary for the algorithm to work, useful for debugging)


        Returns
        -------
        Dict
            state dict
        """
        sampling_ratios = self.sampling_ratios.copy()
        res = {
            "sampling_ratios": deepcopy(sampling_ratios),
            "history": deepcopy(self.history),
            "auto_adjust": self.auto_adjust,
            "adjust_threshold": self.adjust_threshold,
            "adjustment_strength": self.adjustment_strength,
            "sliding_window_size": self.sliding_window_size,
        }
        if include_adjust_history:
            res["adjust_history"] = self.adjust_history
        if as_lists:
            res = _to_python_obj(res)
        return res

    @classmethod
    def from_dict(cls, data: Dict, as_arrays: bool = True) -> "SensitivityEstimatorBase":
        """method that constructs an estimator from a dictionary

        Parameters
        ----------
        data : Dict
            state dictionary

        as_arrays : bool, default=True
            if the lists should be converted to arrays


        Returns
        -------
        Estimator class
        """
        if as_arrays:
            data = cls._to_arrays_dict(data=data)
        return cls(**data)

    def save(
        self,
        file: Union[str, Path],
        include_adjust_history: bool = False,
        as_json: bool = False,
        return_filepath: bool = False,
    ):
        """Method that serializes the estimator to a file. If the given path ends in .json it will be serialized as json.
        Otherwise it will be pickled

        Parameters
        ----------
        file : Union[str, Path]
            filepath

        include_adjust_history : bool, default=False
            If the adjustment history should be included (not necessary for the algorithm to work, useful for debugging)
        """
        filepath = Path(file)
        directory = filepath.parent
        if not directory.exists():
            print(f"{directory} does not exist. Creating {directory}")
        directory.mkdir(parents=True, exist_ok=True)

        if as_json:
            filepath = filepath.with_suffix(".json")
            with open(filepath, "w") as f:
                json.dump(self.to_dict(as_lists=True, include_adjust_history=include_adjust_history), f, indent=4)
        else:
            with open(filepath, "wb") as f:
                pickle.dump(self, f)
        return self, filepath if return_filepath else self

    @classmethod
    def load(cls, file: Union[str, Path]) -> "SensitivityEstimatorBase":
        """Method that deserializes the estimator from a file. If the given path ends in .json it will be deserialized from a json file.

        Parameters
        ----------
        file : Union[str, Path]
            filepath

        Returns
        -------
        Estimator
        """
        file = Path(file)
        if file.suffix == ".json":
            with open(file, "r") as f:
                data = json.load(f)
            data = cls._key_to_class(data)
            return cls.from_dict(data=data, as_arrays=True)
        else:
            with open(file, "rb") as f:
                est = pickle.load(f)
            return est

    def update(self, *, sampling_ratios: Optional[dict] = None, history: Optional[dict] = None):
        """Method that should update internal parameters for a working estimator

        Parameters
        ----------
        sampling_ratios : dict, default=None
            tables dictionary

        history : dict, default=None
            history for adjustment

        """
        if sampling_ratios is not None:
            self.sampling_ratios = sampling_ratios
        if history is not None:
            self.history = history

    @abstractmethod
    def estimate(self, X, y= None, w= None) -> np.ndarray:
        """Estimate sensitivities for new data points. This doc is from the abstract method in the base class.
        The method should be implemented in the child classes for the estimator to work. 

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            Features

        y : Optional[np.ndarray] of shape (n_samples, ), default=None
            Classes
            
        w : Optional[np.ndarray] of shape (n_samples, ), default=None
            sample weights

        Returns
        -------
        np.ndarray of shape (n_samples, )
            estimated sensitivities

        """
        # Implemented in child classes based on flavor
        raise NotImplementedError

    @abstractmethod
    def estimate_one(self, X: np.ndarray, y: Optional[Any] = None, w: Optional[float] = None) -> float:
        """Estimate sensitivities for a single new data point. This doc is from the abstract method in the base class.
        The method should be implemented in the child classes for the estimator to work. 

        Parameters
        ----------
        X : np.ndarray of shape (n_features, )
            Features

        y : Optional[Any], default=None
            Class
            
        w : Optional[float], default=None
            sample weight

        Returns
        -------
        float
            estimated sensitivity
        """
        # Implemented in child classes based on flavor
        raise NotImplementedError

    def _get_prob(self, y, percentile: Union[Any, np.ndarray]):
        """Method that gets the probability of a class or many, given the array of percentiles or a single one or many,
        based on the weighted formula.

        Parameters
        ----------
        y : Union[Any, np.ndarray]
            one class or an array of classes

        percentile : Union[Any, np.ndarray]
            one percentile or an array of percetiles

        Returns
        -------
        Float, or np.ndarray[float]
            returning probability / probabilities
        """

        ((ratio_min, percent_min), (ratio_max, percent_max)) = self.sampling_ratios["tables"][y]["formula"]
        prob = (
            ratio_min * self.sampling_ratios["tables"][y][percent_min][percentile]
            + ratio_max * self.sampling_ratios["tables"][y][percent_max][percentile]
        )
        return prob

    def estimate_proba(
        self, X, y=None, w=None, return_stats: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, ...]]:
        """Method that estimates the probabilities of new samples. It returns the probability, but can also return the corresponding percentiles
        and sensitivities if desired.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            features array

        y : Optional[np.ndarray] of shape (n_samples, ), default=None
            classes

        w : np.ndarray of shape (n_samples, ), default=None
            sample weight array

        return_stats : bool, default=False
            If the return should include the percentiles and sensitivities for each sample

        Returns
        -------
        np.ndarray or Tuple[np.ndarray] depending on what is expected to return
        """
        y = self._check_y(y, length=len(X))
        # Estimate sensitivities
        sens = self.estimate(X=X, y=y, w=w)
        probs = np.zeros_like(sens)
        percentiles = np.zeros_like(sens)
        for c in self._classes:
            percent = self.sampling_ratios["tables"][c]["target_percent"]
            assert (
                percent in self.sampling_ratios["tables"][c].keys()
            ), f"percent must be in {self.sampling_ratios[c].keys()}"
            c_idxs = np.where(y == c)[0]
            # For each sensitivity in s[c_indxs], find the position in the percentile scores array to insert to keep the array sorted.
            # For 100 percentiles, this is equivalent to finding the percentile.
            # searchsorted will always return >=1, because the first percentile is 0,
            # so we subtract 1 to get the correct position in the ratios array
            c_percentiles = np.searchsorted(self.sampling_ratios["tables"][c]["percentiles"], sens[c_idxs]) - 1
            probs[c_idxs] = self._get_prob(c, percentile=c_percentiles)
            percentiles[c_idxs] = c_percentiles
        weights = 1 / probs
        return (probs, percentiles, sens, weights) if return_stats else probs

    def estimate_proba_one(self, X, y=None, w=None, return_stats: bool = False) -> Union[float, Tuple[float, ...]]:
        """Method that estimates the probabilities of a new sample. It returns the probability, but can also return the corresponding percentilee
        and sensitivity if desired.

        Parameters
        ----------
        X : np.ndarray of shape (n_features, )
            features array

        y : Optional[Any], default=None

        w : Optional[float], default=None

        return_stats : bool, default=False
            If the return should include the percentiles and sensitivities

        Returns
        -------
        float or Tuple[float], depending on what was requested.
        """
        y = self._check_y(y)
        percent = self.sampling_ratios["tables"][y]["target_percent"]
        assert (
            percent in self.sampling_ratios["tables"][y].keys()
        ), f"percent must be in {self.sampling_ratios['tables'][y].keys()}"
        s = self.estimate_one(X, y, w)
        percentile = int(np.searchsorted(self.sampling_ratios["tables"][y]["percentiles"], s) - 1)
        # prob = self.sampling_ratios[y][percent][percentile]
        prob = self._get_prob(y=y, percentile=percentile)
        weight = 1 / prob
        return (prob, percentile, s, weight) if return_stats else prob

    def sample(self, X, y=None, w=None, return_stats: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, Dict]]:
        """Method that samples new samples. It can return stats like the probability, percentile and sensitivity for each sample
        This function also auto adjusts if auto_adjust is True.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            features array

        y : Optional[np.ndarray] of shape (n_samples, ), default=None
            classes

        w : np.ndarray of shape (n_samples, ), default=None
            sample weight array

        return_stats : bool, default=False
            If to return a dictionary with statistics

        Returns
        -------
        np.ndarray[bool] or np.ndarray[bnol] dictionary of statistics if return_stats is True
        """

        # An important thing is that this function modifies the history, so it must split the data
        # into before and after adjustment_threshold and sliding_window_size
        y = self._check_y(y, length=len(X))

        # Function that updates estimates and updates the history. Written to avoid code duplication
        def _select_update(X, y, w):
            probs, percentiles, sens, weights = self.estimate_proba(X=X, y=y, w=w, return_stats=True)
            mask = self.random_state.random(size=len(probs)) < probs
            if self._requires_classes:
                mask_dict = group_by_label(mask, y)
            else:
                mask_dict = {0: mask}
            for c, m in mask_dict.items():
                self.history[c]["n_seen"] += len(m)
                self.history[c]["n_sampled"] += np.sum(m)
                self.history[c]["n_seen_batch"] += len(m)
                self.history[c]["n_sampled_batch"] += np.sum(m)
            return probs, percentiles, sens, weights, mask

        n_new = len(X)
        next_threshold = (self.n_adjustments + 1) * self.adjust_threshold
        # Arrays to keep the results in.
        probs = np.zeros(n_new)
        percentiles = np.zeros(n_new)
        sens = np.zeros(n_new)
        weights = np.zeros(n_new)
        mask = np.zeros(n_new, dtype=bool)
        if w is None:
            w = np.ones(n_new)

        # We need to split the data into before and after adjustment_threshold
        if self.auto_adjust and self.n_seen_total + n_new >= next_threshold:
            # This function selects and updates result arrays and history given a start and an end
            def _select_update_idx(X, y, w, start, end):
                Xi, yi, wi = X[start:end], y[start:end], w[start:end]
                probsi, percentilesi, sensi, weightsi, maski = _select_update(Xi, yi, wi)
                sens[start:end] = sensi
                probs[start:end] = probsi
                percentiles[start:end] = percentilesi
                weights[start:end] = weightsi
                mask[start:end] = maski

            # Before adjustment threshold, update and adjust
            n_split0 = next_threshold - self.n_seen_total
            _select_update_idx(X, y, w, start=0, end=n_split0)
            self.adjust()

            # Next splits, update and adjust
            n_remaining = n_new - n_split0
            q, r = divmod(n_remaining, self.adjust_threshold)
            i = 0
            while i < q:
                _select_update_idx(
                    X, y, w, start=n_split0 + i * self.adjust_threshold, end=n_split0 + (i + 1) * self.adjust_threshold
                )

                self.adjust()
                i += 1

            assert n_split0 + i * self.adjust_threshold + r == n_new
            if r != 0:
                _select_update_idx(
                    X, y, w, start=n_split0 + i * self.adjust_threshold, end=n_split0 + i * self.adjust_threshold + r
                )
        else:
            # If we are under the threshold, just select and update
            probs, percentiles, sens, weights, mask = _select_update(X, y, w)
        self.check_sliding_window()
        if return_stats:
            return mask, {"probs": probs, "percentiles": percentiles, "sensitivities": sens, "weights": weights}
        else:
            return mask

    def sample_one(self, X, y=None, w=None, return_stats: bool = False) -> Union[bool, Tuple[bool, Dict]]:
        """Method that samples new samples. It can return stats like the probability, percentile and sensitivity for each sample
        This function also auto adjusts if auto_adjust is True.

        Parameters
        ----------
        X : np.ndarray of shape (n_sampels, )

        y : Optional[Any], default=None

        w : Optional[float], default=None

        return_stats : bool, default=False
            If to return probability, perenctile and sensitivity

        Returns
        -------
        bool or bool, dict if return_stats = True
        """
        y = self._check_y(y)
        prob, percentile, sens, weight = self.estimate_proba_one(X=X, y=y, w=w, return_stats=True)
        res = self.random_state.random() < prob
        self.history[y]["n_seen"] += 1
        self.history[y]["n_seen_batch"] += 1
        if res:
            self.history[y]["n_sampled"] += 1
            self.history[y]["n_sampled_batch"] += 1
        if self.auto_adjust and self.n_seen_total % self.adjust_threshold == 0:
            self.adjust()
        self.check_sliding_window()
        if return_stats:
            return res, {"prob": prob, "percentile": percentile, "sensitivity": sens, "weight": weight}
        else:
            return res

    def check_sliding_window(self):
        """Cut the history if the number of samples exceeds the sliding window."""
        if self.sliding_window_size is not None:
            while self.n_seen_total > self.sliding_window_size:
                classes = [c for c in self.history if c in self._classes]
                for c in classes:
                    self.history[c]["n_seen"] -= self.history[c]["n_seen_per_batch"].pop(0)
                    self.history[c]["n_sampled"] -= self.history[c]["n_sampled_per_batch"].pop(0)

    def adjust(self):
        """The adjustment mechanism
        The main idea is that if we're off with e%, to pull with e% * adjustment_strength in the other direction
        So we prepare a formula of shape [[ratio_min, percent_min], [ratio_max, percent_max]] and the computed probability would be
        the ratio_min * probability corresponding to percent_min and the ratio_max * probability corresponding to percent_max.
        So if the desired probability is 5% and we sampled 4.2% we would have a new target percent 5.8
        [[0.2 5], [0.8, 6]]
        """
        self.check_sliding_window()
        self.history["n_adjustments"] += 1
        classes = [c for c in self.history if c in self._classes]
        for c in classes:
            target_percent = self.sampling_ratios["tables"][c]["target_percent"]
            # Current percent - 5%
            hist_percent = self.history[c]["n_sampled"] / max(self.history[c]["n_seen"], 1) * 100
            # New target percent on the other side of initial target percent 5.8
            new_target_percent = target_percent + (target_percent - hist_percent) * (1 + self.adjustment_strength)
            percents = np.array(self.sampling_ratios["tables"][c]["percents"])
            # Get the 2 closest percents to the new target percent 5, 6
            if new_target_percent in percents:  
                percent_min = new_target_percent  
                percent_max = new_target_percent  
                ratio_min = 1  
                ratio_max = 0  
            else:  
                pos = np.searchsorted(percents, new_target_percent, side = "left")  
                if pos == 0:  
                    ratio_min = 0  
                    ratio_max = 1  
                    percent_min = percents[0]  
                    percent_max = percents[0]  
                elif pos >= len(percents):  
                    ratio_min = 1  
                    ratio_max = 0  
                    percent_min = percents[-1]  
                    percent_max = percents[-1]  
                else:  
                    percent_min = percents[pos - 1]  
                    percent_max = percents[pos]  
                    # Compute the ratios [0.2, 0.8]  
                    ratio_min = (percent_max - new_target_percent) / (percent_max - percent_min)  
                    ratio_max = 1 - ratio_min  
                assert percent_max >= percent_min, "Something went wrong when computing the adjustment"  

            # Add everything to history and adjust_history
            new_formula = [[ratio_min, percent_min], [ratio_max, percent_max]]
            self.sampling_ratios["tables"][c]["formula"] = new_formula

            self.history[c]["n_seen_per_batch"].append(self.history[c]["n_seen_batch"])
            self.history[c]["n_sampled_per_batch"].append(self.history[c]["n_sampled_batch"])
            self.history[c]["n_seen_batch"] = 0
            self.history[c]["n_sampled_batch"] = 0

            self.adjust_history[c]["hist_percents"].append(hist_percent)
            self.adjust_history[c]["target_percents"].append(new_target_percent)
            self.adjust_history[c]["formulas"].append(new_formula)
            self.adjust_history[c]["n_seen_per_batch"].append(self.history[c]["n_seen_batch"])
            self.adjust_history[c]["n_sampled_per_batch"].append(self.history[c]["n_sampled_batch"])

    def __eq__(self, other):
        return self.to_dict(as_lists=True, include_adjust_history=True) == other.to_dict(
            as_lists=True, include_adjust_history=True
        )
