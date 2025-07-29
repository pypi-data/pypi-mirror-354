from dataclasses import asdict, dataclass, field, fields
from typing import Any, Dict, Optional, Union, List
import copy
import numpy as np
from sklearn.model_selection import ParameterGrid
from dataheroes.core.types import CoresetSampleParams, CoresetSampleParamsClassification
from dataheroes.utils import user_warning

class PreprocessingStage:
    ORIGINAL = 'original'
    USER = 'user'
    AUTO = 'auto'

    valid_values = ORIGINAL, USER, AUTO


class CategoricalEncoding:
    TE_DEFAULT_CV = 5  # Sync with default value in the TargetEncoder constructor.
    ENCODING_METHOD_KEY = 'cat_encoding_method'  # Must be in sync with DataParams class.
    OHE = 'OHE'
    TE = 'TE'
    MIXED = 'MIXED'
    NOTHING = 'NOTHING'


CATEGORICAL_INFREQUENT = 'infrequent'


@dataclass
class CoresetParams:
    random_state: Optional[int] = None
    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return self.to_dict()


@dataclass
class CoresetParamsSVD(CoresetParams):
    algorithm: str = 'svd'
    n_components: int = 2
    dtype: str = 'float32'


@dataclass
class CoresetParamsPCA(CoresetParams):
    algorithm: str = "svd"
    n_components: Optional[int] = None
    dtype: str = 'float32'


@dataclass
class CoresetParamsKMeans(CoresetParams):
    algorithm: str = 'lightweight'
    k: Optional[int] = 8


@dataclass
class CoresetParamsLR(CoresetParams):
    algorithm: str = 'svd'
    dtype: str = 'float32'


@dataclass
class CoresetParamsDTR(CoresetParams):
    algorithm: str = "dtr_method_1"
    dtype: str = 'float32'


@dataclass
class CoresetParamsClassification(CoresetParams):
    class_weight: Optional[Dict[Any, float]] = None
    # fair: bool = None
    dtype: str = 'float32'

    def to_json(self):
        result = super(CoresetParamsClassification, self).to_json()
        if result['class_weight']:
            result['class_weight'] = list(zip(
                np.array(list(result['class_weight'].keys())).tolist(),
                np.array(list(result['class_weight'].values())).tolist()
            )
            )
        return result

    def __post_init__(self):
        if self.class_weight is not None:
            self.class_weight = dict(self.class_weight)


@dataclass
class CoresetParamsLG(CoresetParamsClassification):
    algorithm: str = 'unified'
    enable_estimation: bool = False


@dataclass
class CoresetParamsDTC(CoresetParamsClassification):
    algorithm: str = 'unified'
    enable_estimation: bool = False


class FoldIterator:
    def __init__(self, training_fold_sizes, validation_fold_sizes):
        """
        Initialize the iterator with training fold sizes and validation fold sizes.
        :param training_fold_sizes: A list with the size of each training fold.
        :param validation_fold_sizes: A list with the size of each validation fold.
        """
        self.training_fold_sizes = training_fold_sizes
        self.validation_fold_sizes = validation_fold_sizes
        self.current_fold = 0
        self.total_training_size = sum(training_fold_sizes)

    def __iter__(self):
        """
        Make the object an iterator.
        """
        return self

    def __next__(self):
        """
        Return the next set of fold indexes.
        """
        if self.current_fold >= len(self.training_fold_sizes):
            raise StopIteration

        # Calculate the start and end index of the current training fold
        start_index = sum(self.training_fold_sizes[:self.current_fold])
        end_index = start_index + self.training_fold_sizes[self.current_fold]

        # Get training indexes for the current fold
        training_indexes = list(range(start_index, end_index))

        # Calculate the start index for the current validation fold
        validation_start_index = self.total_training_size + sum(self.validation_fold_sizes[:self.current_fold])

        # Get validation indexes for the current fold
        validation_indexes = list(
            range(validation_start_index, validation_start_index + self.validation_fold_sizes[self.current_fold]))

        # Move to the next fold
        self.current_fold += 1

        # Return the combined indexes
        return training_indexes, validation_indexes
    
    def copy(self, deep=False):
        """
        Return a copy of the object.
        :param deep: If True, return a deep copy. Otherwise, return a shallow copy
        """
        return copy.deepcopy(self) if deep else copy.copy(self)


@dataclass
class PreprocessingParams:
    """
    Convenience class that encapsulates the preprocessing information generated when the data was auto-processed,
    saved, retrieved, or passed through the different stages of the library flow.
    The attributes (except the 'missing_values_params') are a result of either the OHE or the TE encodings, and taken
    directly from their respective encoders.

    Attributes
    ----------
    missing_values_params: dict
        (Applies to all encoding strategies.)
        Replacement values for the features with missing values (under 'features' key), and removed features
        (under 'removed_features' key), in case features have been removed.

    ohe_cat_features_idxs: list of shape (n_features,) of int or None
        (Applies only to the OHE encoding or to the MIXED strategy involving OHE.)
        The indices of categorical features encoded by the OHE encoding strategy, referring to the original indices
        from the dataset on which fit_transform was applied.

    ohe_used_categories: list of shape (n_features,) of ndarray or None
        (Applies only to the OHE encoding or to the MIXED strategy involving OHE.)
        The categories of each input feature determined during fitting or specified in 'categories' in the
        constructor of the OHE encoder (in order of the features in 'X' and corresponding with the output of 'transform').

    te_cat_features_idxs: list of shape (n_features,) of int or None
        (Applies only to the TE encoding or to the MIXED strategy involving TE.)
        The indices of categorical features encoded by the TE encoding strategy, referring to the original indices
        from the dataset on which fit_transform was applied.

    te_used_categories: list of shape (n_features,) of ndarray or None
        (Applies only to the TE encoding or to the MIXED strategy involving TE.)
        The categories of each input feature determined during fitting or specified in 'categories' in the
        constructor of the TE encoder (in order of the features in 'X' and corresponding with the output of 'transform').

    te_target_type: str or None
        (Applies only to the TE encoding or to the MIXED strategy involving TE.)
        Type of target, can be either "binary", "multiclass", or "continuous".

    te_classes: ndarray or None
        (Applies only to the TE encoding or to the MIXED strategy involving TE.)
        If 'te_target_type' is "binary" or "multiclass", holds the label for each class, otherwise 'None'.

    te_target_mean: float or None
        (Applies only to the TE encoding or to the MIXED strategy involving TE.)
        The overall mean of the target. This value is only used in 'transform' to encode categories.

    te_encodings: list of shape (n_features,) or (n_features * n_classes) of ndarray, or None
        (Applies only to the TE encoding or to the MIXED strategy involving TE.)
        Encodings learnt on all of 'X'.
        For feature 'i', 'encodings_[i]' are the encodings matching the categories listed in 'used_categories_[i]'.
        When 'te_target_type' is "multiclass", the encoding for feature 'i' and class 'j' is stored in
        'encodings_[j + (i * len(classes_))]'. E.g., for 2 features (f) and 3 classes (c), encodings are ordered:
        f0_c0, f0_c1, f0_c2, f1_c0, f1_c1, f1_c2,
        NOTE: at this point in time, we do not employ TE for "multiclass" or "continuous" targets, only for "binary".

    ae_feature_classes: dict of used labels per array encoded feature column, used in predict when encoding the data
        For example {0: [1,2,3]} this means that the array [1,2,3,4] will be encoded to [1,1,1]
        with 4 omitted as it is not used.
    """

    missing_values_params: Optional[dict] = None
    ohe_cat_features_idxs: list = field(default_factory=lambda: [])
    ohe_used_categories: list = field(default_factory=lambda: [])
    te_cat_features_idxs: list = field(default_factory=lambda: [])
    te_used_categories: list = field(default_factory=lambda: [])
    te_target_type: Optional[str] = None
    te_classes: list = field(default_factory=lambda: [])
    te_target_mean: Optional[float] = None
    te_encodings: list = field(default_factory=lambda: [])
    ae_feature_classes: dict = field(default_factory=lambda: {})

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict):
        if d is None:
            return cls()
        else:
            # The reason we return named params and not "cls(**d)" is because the provided dictionary may contain
            # additional keys which are not a part of this class.
            # Some of the fields may have originally contained ndarrays, but may later become lists and be maintained
            # as lists. This happens because a call to this method may have passed a dictionary retrieved from a
            # pre-saved JSON, in which case, some ndarrays may have been converted to lists. Their later conversion
            # back to ndarrays, if necessary, will be on the responsibility of the code that uses their values.
            return cls(
                missing_values_params=d.get("missing_values_params"),
                ohe_cat_features_idxs=d.get("ohe_cat_features_idxs", []),
                ohe_used_categories=d.get("ohe_used_categories", []),
                te_cat_features_idxs=d.get("te_cat_features_idxs", []),
                te_used_categories=d.get("te_used_categories", []),
                te_target_type=d.get("te_target_type"),
                te_classes=d.get("te_classes", []),
                te_target_mean=d.get("te_target_mean"),
                te_encodings=d.get("te_encodings", []),
                ae_feature_classes=d.get("ae_feature_classes", {})
            )


@dataclass
class DataTuningParams:
    """
    A class including all required information to tune the data parameters for unsupervised and regression Coreset trees: <a href="https://data-heroes.github.io/dh-library/latest/reference/services/coreset_tree/dtr/">`CoresetTreeServiceDTR`</a>,
    <a href="https://data-heroes.github.io/dh-library/latest/reference/services/coreset_tree/kmeans/">`CoresetTreeServiceKMeans`</a>,
    <a href="https://data-heroes.github.io/dh-library/latest/reference/services/coreset_tree/lr/">`CoresetTreeServiceLR`</a>,
    <a href="https://data-heroes.github.io/dh-library/latest/reference/services/coreset_tree/pca/">`CoresetTreeServicePCA`</a>,
    <a href="https://data-heroes.github.io/dh-library/latest/reference/services/coreset_tree/svd/">`CoresetTreeServiceSVD`</a>.
    The parameters of the class are treated as a <code>param_grid</code> and a Coreset tree will be built for each combination of parameters.

    <table>
        <tr><th> Parameter name</th><th>Type</th><th>Description</th></tr>
        <tr><td colspan='3'><b><a id="General Parameters">General Parameters</a></b></td></tr>
        <tr><td>coreset_size</td><td> List[Optional[Union[int, float]]]</td><td>
        Represents the coreset size of each node in the coreset tree. If None, the coreset size is not specified.
        If provided as a float, it represents the ratio between each chunk and the resulting coreset.
        In any case the coreset_size is limited to 60% of the chunk_size.
        If provided as int, it is the number of samples. The coreset is constructed by sampling data instances
        from the dataset based on their calculated importance. Since each instance may be sampled more than once,
        in practice, the actual size of the coreset is mostly smaller than coreset_size.
        <br>Example: <code>'coreset_size': [1000, 5000, 10000]</code></td></tr>
        <tr><td>deterministic_size</td><td> List[Optional[Union[int, float]]]</td><td>
        The ratio of the coreset_size, which is selected deterministically, based on the calculated importance.
        If None, the deterministic size is not specified and the Coreset would sample all its samples probabilistically.
        <br>Example: <code>'deterministic_size': [0.1, 0.2, None]</code></td></tr>
        <tr><td>det_weights_behaviour</td><td> List[Optional[str]]</td><td>
        Determines how the weights of the Coreset samples will be calculated. The default is <code>auto</code>, which defaults to <code>keep</code>
        <ul>
            <li><code>'keep'</code>: The weights of all samples that were selected deterministically
            are kept as given in the input and the probabilistic samples’ weights sum up proportionally to the <code>dataset_sum_of_weights - sum_of_deterministic_samples</code>.</li>
            <li><code>'inv'</code>:  The weights of all samples that were selected (deterministically or probabilistically) are the inverse of their sampling probabilities.
            This means that there is no difference in weight calculation between the deterministic and probabilistic samples. </li>
            <li><code>'prop'</code>: The weights of all samples that were selected deterministically sums up
            proportionally to the <code>deterministic_size * dataset_sum_of_weights</code> and the probabilistic
            samples sum up to <code>(1 - deterministic_size) * dataset_sum_of_weights</code>.</li>
        </ul>
        <br>Example: <code>'det_weights_behaviour': ['keep', 'inv']</code></td></tr>
        </table>

    Code example:

    ```py
    data_tuning_params = {
        'coreset_size': [500, 2000, 5000],
        'deterministic_size': [0.1, 0.3, None],
        'det_weights_behaviour': ['keep', 'inv']
    }

    service = CoresetTreeServiceDTR(data_tuning_params=data_tuning_params, ...)
    ```
    """
    coreset_size: List[Optional[Union[int, float]]] = field(default_factory=lambda: [None])
    deterministic_size: List[Optional[Union[int, float]]] = field(default_factory=lambda: [None])
    det_weights_behaviour: List[Optional[str]] = field(default_factory=lambda: [None])
    # Class proprieties. No typing
    _sample_params_cls = CoresetSampleParams

    def __post_init__(self):
        # value -> [value] => we allow the user to pass (field = value)
        # [] -> [None]     => we allow the user to pass (fields = [])
        for f in fields(self):
            v = getattr(self, f.name)
            if isinstance(v, list) and len(v) == 0:
                setattr(self, f.name, [None])
            if not isinstance(v, list):
                setattr(self, f.name, [v])

        for size in self.coreset_size:
            if isinstance(size, (int, float)) and size <= 0:
                raise ValueError(
                    f"Invalid `coreset_size` {size}. `coreset_size` must be an integer greater than 0 or None"
                )

    def to_dict(self):
        return asdict(self)

    def create_sample_params(self) -> List[CoresetSampleParams]:
        return [self._sample_params_cls(**params) for params in ParameterGrid(asdict(self))]

    @classmethod
    def _filter(cls, sample_params: CoresetSampleParams) -> dict:
        f_names = [f.name for f in fields(cls)]
        return {f.name: getattr(sample_params, f.name) for f in fields(sample_params) if f.name in f_names}

    def check_for_cleaning(self):
        # We allow a single cleaning tree, so we check for all fields to have a single parameter inside.
        for f in fields(self):
            if len(getattr(self, f.name)) != 1:
                raise ValueError(
                    f"Invalid {f.name} value. A single value is allowed for each parameter of the cleaning tree."
                )
        # Deterministic size will be forced to be 1
        if self.deterministic_size[0] is not None and self.deterministic_size[0] != 1.0:
            user_warning("The deterministic_size provided is not 1.0. Setting it to 1.0 for the cleaning tree.")
            self.deterministic_size[0] = 1.0


@dataclass
class DataTuningParamsClassification(DataTuningParams):
    """
    A class including all required information to tune the data parameters for classification Coreset trees: <a href="https://data-heroes.github.io/dh-library/latest/reference/services/coreset_tree/dtc/">`CoresetTreeServiceDTC`</a>
    and <a href="https://data-heroes.github.io/dh-library/latest/reference/services/coreset_tree/lg/">`CoresetTreeServiceLG`</a>.
    The parameters of the class are treated as a param_grid and a Coreset tree will be built for each combination of parameters.

    <table>
        <tr><th> Parameter name</th><th>Type</th><th>Description</th></tr>
        <tr><td colspan='3'><b><a id="General Parameters">General Parameters</a></b></td></tr>
        <tr><td>coreset_size</td><td> List[Optional[Union[int, float]]]</td><td>
        Represents the coreset size of each node in the coreset tree. If None, the coreset size is not specified.
        If provided as a float, it represents the ratio between each chunk and the resulting coreset.
        In any case the coreset_size is limited to 60% of the chunk_size.
        If provided as int, it is the number of samples. The coreset is constructed by sampling data instances
        from the dataset based on their calculated importance. Since each instance may be sampled more than once,
        in practice, the actual size of the coreset is mostly smaller than coreset_size.
        <br>Example: <code>'coreset_size': [1000, 5000, 10000]</code></td></tr>
        <tr><td>fair</td><td> List[Optional[Union[str, bool]]]</td><td>
        Automatically determines the number of samples to sample from each class. If set to <code>True</code>, small classes will be sampled in a
        higher proportion than their proportion in the full dataset. If set to <code>False</code>, the classes would be
        sampled according to their proportion in the full dataset, unless the <code>class_size</code> parameter is defined.
        <br>Example: <code>'fair': [True, False]</code></td></tr>
        <tr><td>class_size</td><td> List[Optional[Dict[Any, Union[int, float]]]]</td><td>
        Determines the number of samples to sample from each class. If provided as float, it represents the ratio from the <code>coreset_size</code>.
        If provided as int, it is the number of samples. If None, the number of samples per class will be
        automatically determined based on the <code>fair</code> parameter. Entries in the <code>class_size</code> should not sum higher than the provided <code>coreset_size</code>.
        <br>Example: <code>'class_size': [{0: 5000, 1: 1000}, None]</code></td></tr>
        <tr><td>deterministic_size</td><td> List[Optional[Union[int, float]]]</td><td>
        The ratio of the coreset_size, which is selected deterministically, based on the calculated importance.
        If None, the deterministic size is not specified and the Coreset would sample all its samples probabilistically.
        <br>Example: <code>'deterministic_size': [0.1, 0.2, None]</code></td></tr>
        <tr><td>det_weights_behaviour</td><td> List[Optional[str]]</td><td>
        Determines how the weights of the Coreset samples will be calculated. The default is <code>auto</code>, which defaults to <code>keep</code>
        <ul>
            <li><code>'keep'</code>: The weights of all samples that were selected deterministically
            are kept as given in the input and the probabilistic samples’ weights sum up proportionally to the <code>dataset_sum_of_weights - sum_of_deterministic_samples</code>.</li>
            <li><code>'inv'</code>:  The weights of all samples that were selected (deterministically or probabilistically) are the inverse of their sampling probabilities.
            This means that there is no difference in weight calculation between the deterministic and probabilistic samples. </li>
            <li><code>'prop'</code>: The weights of all samples that were selected deterministically sums up
            proportionally to the <code>deterministic_size * dataset_sum_of_weights</code> and the probabilistic
            samples sum up to <code>(1 - deterministic_size) * dataset_sum_of_weights</code>.</li>
        </ul>
        <br>Example: <code>'det_weights_behaviour': ['keep', 'inv']</code></td></tr>
        <tr><td>sample_all</td><td> List[Optional[List[Any]]]</td><td>
        A list of classes for which all data instances should be selected into the Coreset, instead of applying sampling.
        If None, <code>sample_all</code> will apply to no class. Entries in the <code>sample_all</code> should not sum higher than the provided <code>coreset_size</code>.
        <code>sample_all</code> should only be used in highly imbalanced datasets to ensure the rare classes are sampled. A similar effect can be achieved when providing a proper <code>class_size</code>.
        <br>Example: <code>'sample_all': [None, [1]]</code></td></tr>
    </table>

    Code example:
    ```py

    data_tuning_params = {
        'coreset_size': [500, 2000, 5000],
        'deterministic_size': [0.1, 0.3, None],
        'det_weights_behaviour': ['keep', 'inv'],
        'sample_all': 'sample_all': [None, [1]],
        'class_size': [{0: 5000, 1: 1000}, None],
        'fair': [True, False]
    }

    service = CoresetTreeServiceDTC(data_tuning_params=data_tuning_params, ...)
    ```
    """
    deterministic_size: List[Optional[Union[int, float, Dict[Any, Union[int, float]]]]] = field(default_factory=lambda: [None])
    sample_all: List[Optional[List[Any]]] = field(default_factory=lambda: [None])
    class_size: List[Optional[Dict[Any, Union[int, float]]]] = field(default_factory=lambda: [None])
    fair: List[Optional[Union[str, bool]]] = field(default_factory=lambda: [None])
    # Class properties. No typing
    _sample_params_cls = CoresetSampleParamsClassification

    def __post_init__(self):
        super().__post_init__()
        # Double check sample_all because we check against list in super().__post_init__() and sample_all is list[list]
        if any(e is not None and not isinstance(e, list) for e in self.sample_all):
            self.sample_all = [self.sample_all]
