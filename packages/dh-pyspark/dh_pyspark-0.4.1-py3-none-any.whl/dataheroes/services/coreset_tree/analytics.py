import hashlib
import os
import random
import shutil
from pathlib import Path
from typing import Union, Iterable, Callable, Any, Tuple

import numpy as np
import pandas as pd

from ._base import CoresetTreeService, DataManagerT
from ._mixin import CoresetTreeServiceUnsupervisedMixin
from ..common import CoresetParams, CategoricalEncoding, DataTuningParamsClassification
from ...core.coreset import CoresetAnalytics
from ...core.helpers import aggregate_children
from ...data import DataParams
from ...utils import telemetry, check_feature_for_license, unsupported_method_in
from dataheroes.core.tree import TreeOptimizedFor


SAMPLING_METHODS = {
    1: {  # Method 1
        100_000_000: {0.005: 0.0002, 0.01: 0.0005, 0.025: 0.0005, 0.05: 0.0010, 0.1: 0.0020, 0.15: 0.0030, 0.2: 0.0040, 0.3: 0.0050, 0.4: 0.0080},
        10_000_000: {0.005: 0.0005, 0.01: 0.0010, 0.025: 0.0010, 0.05: 0.0020, 0.1: 0.0050, 0.15: 0.0100, 0.2: 0.0200, 0.3: 0.0500, 0.4: 0.1000},
        1_000_000: {0.005: 0.0010, 0.01: 0.0020, 0.025: 0.0050, 0.05: 0.0100, 0.1: 0.0150, 0.15: 0.0200, 0.2: 0.0500, 0.3: 0.1100, 0.4: 0.3500},
        100_000: {0.005: 0.0050, 0.01: 0.0100, 0.025: 0.0100, 0.05: 0.0200, 0.1: 0.0500, 0.15: 0.1000, 0.2: 0.3600, 0.3: 0.9500, 0.4: 1.0000},
        10_000: {0.005: 0.0250, 0.01: 0.0500, 0.025: 0.0850, 0.05: 0.2000, 0.1: 0.5000, 0.15: 1.0000, 0.2: 1.0000, 0.3: 1.0000, 0.4: 1.0000},
        0: {0.005: 0.0250, 0.01: 0.0500, 0.025: 0.3000, 0.05: 0.5000, 0.1: 1.0000, 0.15: 1.0000, 0.2: 1.0000, 0.3: 1.0000, 0.4: 1.0000}
    },
    2: {  # Method 2
        100_000_000: {0.005: 0.0010, 0.01: 0.0020, 0.025: 0.0070, 0.05: 0.0100, 0.1: 0.0300, 0.15: 0.0500, 0.2: 0.0700, 0.3: 0.1300, 0.4: 0.1900},
        10_000_000: {0.005: 0.0025, 0.01: 0.0050, 0.025: 0.0100, 0.05: 0.0200, 0.1: 0.0500, 0.15: 0.0800, 0.2: 0.1100, 0.3: 0.1700, 0.4: 0.2800},
        1_000_000: {0.005: 0.0050, 0.01: 0.0100, 0.025: 0.0350, 0.05: 0.0500, 0.1: 0.1000, 0.15: 0.1500, 0.2: 0.2000, 0.3: 0.4400, 0.4: 0.5000},
        100_000: {0.005: 0.0100, 0.01: 0.0300, 0.025: 0.0500, 0.05: 0.0700, 0.1: 0.1500, 0.15: 0.2000, 0.2: 0.5000, 0.3: 0.6500, 0.4: 0.8000},
        10_000: {0.005: 0.0120, 0.01: 0.0300, 0.025: 0.0700, 0.05: 0.1000, 0.1: 0.3500, 0.15: 0.5000, 0.2: 0.7000, 0.3: 0.8000, 0.4: 0.9000},
        0: {0.005: 0.0120, 0.01: 0.0300, 0.025: 0.0500, 0.05: 0.2000, 0.1: 0.3000, 0.15: 0.5000, 0.2: 0.6500, 0.3: 0.8000, 0.4: 0.8500}
    },
    3: {  # Method 3 (testing purposes)
        100_000_000: {0.005: 0.0002, 0.01: 0.0005, 0.025: 0.0005, 0.05: 0.0010, 0.1: 0.0020},
        10_000_000: {0.005: 0.0005, 0.01: 0.0010, 0.025: 0.0010, 0.05: 0.0020, 0.1: 0.0050},
        1_000_000: {0.005: 0.0025, 0.01: 0.0050, 0.025: 0.0050, 0.05: 0.0075, 0.1: 0.0100},
        100_000: {0.005: 0.0050, 0.01: 0.0100, 0.025: 0.0100, 0.05: 0.0200, 0.1: 0.0200},
        10_000: {0.005: 0.0250, 0.01: 0.0500, 0.025: 0.0850, 0.05: 0.2000, 0.1: 0.5000},
        0: {0.005: 0.0250, 0.01: 0.0500, 0.025: 0.3000, 0.05: 0.5000, 0.1: 1.0000}
    }
}

# Constant for maximum number of samples to include in the sample probability
MAX_SAMPLES = 30_000_000


def get_sampling_prob(freq, method=1):

    sample_prob = SAMPLING_METHODS.get(method, SAMPLING_METHODS[1])
    sample_prob_len = len(sample_prob)
    # Iterate over thresholds to find the correct range for the frequency
    for idx, (threshold, percents) in enumerate(sample_prob.items()):
        if freq > threshold:
            return sample_prob_len - idx - 1
    return 0


def prepare_sampling_probs(sampling_probs):

    prepared_probs = []
    for prob in sampling_probs:
        prepared_prob = f"{prob}.{random.randint(1000, 9999)}"
        prepared_probs.append(prepared_prob)

    return np.array(prepared_probs).reshape(-1, 1)  # Return as a 2D array with 1 column


def arrange_probs(data, separator="|"):

    arranged_data = []
    for row in data:
        # Concatenate all fields in the row with the separator
        concatenated_row = separator.join(map(str, row))
        # Compute MD5 hash of the concatenated string
        arranged_obj = hashlib.md5(concatenated_row.encode())
        arranged_data.append(arranged_obj.hexdigest())

    return np.array(arranged_data).reshape(-1, 1)  # Return as a 2D array with 1 column


def prepare_probability_data(method_number):
    data = SAMPLING_METHODS.get(method_number)
    if not data:
        raise ValueError("Invalid method number.")

    prepared_data = {}
    probabilities = [str(prob).rstrip('0').rstrip('.') for prob in data[next(iter(data))]]

    # Initialize the dictionary keys without modifying it during iteration
    for prob_str in probabilities:
        no1 = random.uniform(0, 1)
        prepared_data[f"{prob_str}_rand"] = [no1]
        prepared_data[f"{prob_str}_prepared"] = [float(prob_str) / no1]

    for group, prob_values in sorted(data.items()):
        for prob, original_value in prob_values.items():
            prob_str = str(prob).rstrip('0').rstrip('.')
            no1 = random.uniform(0, 1)
            prepared_data[f"{prob_str}_rand"].append(no1)
            prepared_data[f"{prob_str}_prepared"].append(original_value / no1)

    return pd.DataFrame(prepared_data).rename(columns=lambda _: '', index=None)


class CoresetTreeServiceAnalytics(
    CoresetTreeServiceUnsupervisedMixin, CoresetTreeService
):

    _coreset_cls = CoresetAnalytics
    _coreset_params_cls = CoresetParams
    _data_tuning_params_cls = DataTuningParamsClassification

    @telemetry
    def __init__(
        self,
        *,
        data_manager: DataManagerT = None,
        data_params: Union[DataParams, dict] = None,
        data_tuning_params: Union[DataTuningParamsClassification, dict] = None,
        n_instances: int = None,
        max_memory_gb: int = None,
        n_classes: int = None,
        optimized_for: Union[list, str] = TreeOptimizedFor.training,
        chunk_size: int = None,
        chunk_by: Union[Callable, str, list] = None,
        coreset_params: Union[CoresetParams, dict] = None,
        working_directory: Union[str, os.PathLike] = None,
        cache_dir: Union[str, os.PathLike] = None,
        node_train_function: Callable[[np.ndarray, np.ndarray, np.ndarray], Any] = None,
        node_train_function_params: dict = None,
        node_metadata_func: Callable[
            [Tuple[np.ndarray], np.ndarray, Union[list, None]], Union[list, dict, None]
        ] = None,
        chunk_sample_ratio: float = None,
        model_cls: Any = None,
    ):
        check_feature_for_license("analytics")
        self.model_cls = None

        if type(data_params) is dict:
            data_params = {CategoricalEncoding.ENCODING_METHOD_KEY: CategoricalEncoding.NOTHING, **data_params}
        elif isinstance(data_params, DataParams):
            data_params.cat_encoding_method = CategoricalEncoding.NOTHING
        elif data_params is None:
            data_params = {CategoricalEncoding.ENCODING_METHOD_KEY: CategoricalEncoding.NOTHING}

        super().__init__(
            data_manager=data_manager,
            data_params=data_params,
            n_instances=n_instances,
            max_memory_gb=max_memory_gb,
            n_classes=n_classes,
            optimized_for=optimized_for,
            chunk_size=chunk_size,
            data_tuning_params=data_tuning_params,
            coreset_params=coreset_params,
            working_directory=working_directory,
            cache_dir=cache_dir,
            node_train_function=node_train_function,
            node_train_function_params=node_train_function_params,
            node_metadata_func=node_metadata_func,
            chunk_sample_ratio=chunk_sample_ratio,
            model_cls=None,
            chunk_by=chunk_by,
        )

        # We should force save_all to False, we only want to save the aggregations
        self.chunk_sample_ratio = 0.0
        self.save_all = False

    def _get_tree_coreset(
        self,
        tree_idx: int,
        level: int,
        seq_from,
        seq_to,
        purpose: str = None,
        **kwargs,
    ) -> dict:
        result = self._get_coreset_internal(
            tree_idx=tree_idx, level=level, seq_from=seq_from, seq_to=seq_to, inverse_class_weight=True, purpose=purpose
        )

        # Create missing mask for later
        missing_mask = np.isnan(result['X'])

        # Handle missing values in the same way they were handled during the build
        data_processed, _, _ = self._apply_auto_processing(
            ind=result["ind"],
            X=result["X"],
            w=result["w"],
            sparse_threshold=0,
            calc_replacements=False,
            allow_drop_rows=False,
        )
        X_processed = data_processed["X_processed"]
        ind_processed = data_processed["ind_processed"]
        props_processed = result.get("props", None)
        w_processed = np.array(result["w"])

        # Aggregate the data
        ind, w_processed = aggregate_children(X_processed, w_processed)

        # Create the final result
        X_processed = X_processed[ind]
        ind_processed = ind_processed[ind]
        props_processed = props_processed[ind] if props_processed is not None else None
        missing_mask = missing_mask[ind]

        # Replace back the missing values
        X_processed[missing_mask] = np.nan

        # Transform the data to USER format
        X_processed = self.data_manager.convert_encoded_data_to_user(X_processed)

        result = {
            "ind": ind_processed,
            "X": X_processed,
            "w": w_processed,
            "n_represents": result["n_represents"],
            "props": props_processed}
        return result

    @telemetry
    def get_coreset(
        self,
        tree_idx: int = 0,
        level: int = 0,
        seq_from: Any = None,
        seq_to: Any = None,
    ) -> dict:
        """
        Get tree's coreset data in one of the preprocessing_stage(s) in the data preprocessing workflow.
        Use the level parameter to control the level of the tree from which samples will be returned.
        This function is only applicable in case the coreset tree was optimized_for 'training'.

        Parameters:
            tree_idx: int, default = 0
                Defines the index of the tree from which the coreset is extracted.
                The default is index 0, which is the index of the tree built according to the first DataTuningParams combination that was passed
            level: int, optional, default 0.
                Defines the depth level of the tree from which the coreset is extracted.
                Level 0 returns the coreset from the head of the tree with around coreset_size samples.
                Level 1 returns the coreset from the level below the head of the tree with around twice of the samples compared to level 0, etc.
                If the passed level is greater than the maximal level of the tree, the maximal available level is used.
            seq_from: string or datetime, optional, default None.
                The start sequence to filter samples by.
            seq_to: string or datetime, optional, default None.
                The end sequence to filter samples by.
        Returns:
            A dictionary representing the Coreset:
                ind: A numpy array of indices.
                X: A numpy array of the feature matrix.
                y: A numpy array of the target values.
                w: A numpy array of sample weights.
                n_represents: The number of instances represented by the coreset.
                features_out: A list of the output features, if preprocessing_stage=auto, otherwise None.
                props: A numpy array of properties, or None if not available.
        """
        check_feature_for_license("analytics")
        self._requires_tree()
        result = self._get_tree_coreset(
            tree_idx=tree_idx, level=level, seq_from=seq_from, seq_to=seq_to, purpose="analytics"
        )

        return result

    @telemetry
    def get_estimator(
            self,
            level: int = 0,
            seq_from: Any = None,
            seq_to: Any = None,
            method: int = 1,
            missing_replacement: Any = -1,
            num_seq: int = 1,
    ):
        """
        Fetches and processes an estimator dataset based on input parameters and specified sampling methods.

        This method retrieves coreset data, processes it based on the specified probability sampling method,
        filters samples by frequency thresholds, and adjusts weights for time ranges or number of sequences.
        It also handles missing data and prepares the final dataset for downstream analysis.

        Parameters:
            level (int, optional): The hierarchy level of data to fetch. Defaults to 0.
            seq_from (Any, optional): Start of the sequence range. If None, no range is applied.
            seq_to (Any, optional): End of the sequence range. If None, no range is applied.
            method (int, optional): The sampling method to use, corresponding to keys in `SAMPLING_METHODS`. Defaults to 1.
            missing_replacement (Any, optional): Value to replace missing data in the dataset. Defaults to -1.
            num_seq (int, optional): Number of sequences for frequency adjustment if no date range is provided. Defaults to 1.

        Returns:
            np.ndarray: A combined dataset containing prepared features and corresponding sampling probabilities.
        """

        check_feature_for_license("analytics")
        # Fetch the appropriate probability data based on the chosen method
        prob_data = SAMPLING_METHODS.get(method, SAMPLING_METHODS[1])

        # Set the frequency threshold based on the first group in the chosen probability data
        frequency_threshold = sorted(prob_data.keys())[1]  # Corresponds to the lower bound for Group 1

        # Fetch coreset data
        result = self.get_coreset(level=level, seq_from=seq_from, seq_to=seq_to)
        if seq_from or seq_to:
            # transform from string to datetime
            seq_from, seq_to = self.tree._transform_seq_params(seq_from, seq_to)
            units = pd.date_range(start=seq_from, end=seq_to, freq=self.data_manager.data_params_internal.seq_granularity_)
            freq_adjustment = len(units)
        else:
            freq_adjustment = num_seq
        X, weights = result["X"], result["w"]

        # Replace all missing values with the provided missing_replacement
        X = np.where(pd.isna(X), missing_replacement, X)

        # Cast to int if possible
        for i in range(X.shape[1]):
            try:
                # Attempt to convert the column to int
                X[:, i] = X[:, i].astype(int)
            except ValueError:
                # If conversion fails, skip the column
                pass

        # Adjust frequencies based on the number of days in the range
        adjusted_weights = weights / freq_adjustment

        filtered_indices = adjusted_weights > frequency_threshold
        filtered_weights = adjusted_weights[filtered_indices]
        filtered_X = X[filtered_indices]

        if len(filtered_weights) > MAX_SAMPLES:
            top_indices = np.argsort(-filtered_weights)[:MAX_SAMPLES]
            filtered_weights = filtered_weights[top_indices]
            filtered_X = filtered_X[top_indices]

        sampling_probs = np.array([get_sampling_prob(f, method=method) for f in filtered_weights])

        prepared_features = arrange_probs(filtered_X)

        prepared_sampling_probs = prepare_sampling_probs(sampling_probs)

        # Combine
        combined_data = np.hstack([prepared_features, prepared_sampling_probs])

        return combined_data

    @telemetry
    def save_estimator(
            self,
            level: int = 0,
            seq_from: Any = None,
            seq_to: Any = None,
            num_seq: int = 1,
            method: int = 1,
            estimator_path: Union[str, os.PathLike] = None,
            preprocessing_data_path: Union[str, os.PathLike] = None,
            gzip: bool = True,
    ):
        """
        Calls get_estimator to get the data and saves it to files (optionally gzipped).
        If the paths are not provided, the files are saved in the current working directory.

        Args:
            level (int): Level parameter for get_estimator.
            seq_from (Any): Start of the time range for get_estimator.
            seq_to (Any): End of the time range for get_estimator.
            num_seq (int): Number of sequences for frequency adjustment.
            method (int): Method to select the probability data.
            estimator_path (Union[str, os.PathLike]): Path to save the estimator data.
            preprocessing_data_path (Union[str, os.PathLike]): Path to save the preprocessing data.
            gzip (bool): Flag to gzip the files. Defaults to False.
        """

        check_feature_for_license("analytics")

        # Call get_estimator to obtain the data
        prepared_data = self.get_estimator(
            level=level,
            seq_from=seq_from,
            seq_to=seq_to,
            method=method,
            num_seq=num_seq,
        )
        prepared_probability_data = prepare_probability_data(method)

        estimator_path = Path(estimator_path)
        estimator_path.parent.mkdir(parents=True, exist_ok=True)
        preprocessing_path = Path(preprocessing_data_path)
        preprocessing_path.parent.mkdir(parents=True, exist_ok=True)

        # Set file paths with .csv extension
        estimator_path = Path(estimator_path).with_suffix(".csv") or \
                         Path(os.getcwd()) / f"estimator_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv"
        preprocessing_path = (
            Path(preprocessing_data_path).with_suffix(".csv")
            or Path(os.getcwd()) / f"preprocessing_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.csv"
        )

        # Convert prepared data to DataFrame
        df = pd.DataFrame(prepared_data)

        # Save data to CSV
        df.to_csv(estimator_path, index=False, header=False)
        prepared_probability_data.to_csv(preprocessing_path, index=False, header=False)

        if gzip:
            if not shutil.which("gzip"):
                print("gzip is not installed. Please install gzip to compress the files.")
            else:
                # Compress files using gzip via os.system
                os.system(f"gzip -f {estimator_path}")
                os.system(f"gzip -f {preprocessing_path}")

                # Update paths to reflect the .gz extension
                estimator_path = estimator_path.with_suffix("").with_suffix(".gz")
                preprocessing_path = preprocessing_path.with_suffix("").with_suffix(".gz")

        print(f"Estimator saved to: {estimator_path}")
        print(f"Preprocessing data saved to: {preprocessing_path}")

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def fit(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def predict(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def predict_proba(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def get_cleaning_samples(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def auto_preprocessing(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def get_important_samples(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def update_targets(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def update_features(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def set_seen_indication(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def explain(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def grid_search(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def get_hyperparameter_tuning_data(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def holdout_validate(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def seq_dependent_validate(self, *args, **kwargs): ...

    @unsupported_method_in("CoresetTreeServiceAnalytics")
    def cross_validate(self, *args, **kwargs): ...
