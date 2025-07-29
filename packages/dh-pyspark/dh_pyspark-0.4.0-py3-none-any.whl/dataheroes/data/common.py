import os
import pathlib
import uuid
import inspect
import textwrap
import numpy as np
from uuid import uuid4
import dataclasses
from dataclasses import dataclass
from typing import Iterable, Union, Callable, Any, Tuple, Optional
from collections import namedtuple

from numpy.random import RandomState

from . import helpers
from . import utils
from ..configuration import DataHeroesConfiguration

# TODO Dacian: This namedtuple has 6 defaults, leaving ind empty. Is this intended to no tbe able to create datasets without ind?
Dataset = namedtuple("Dataset", "ind X y sample_weight props orig orig_target", defaults=[None]*6)


def to_list(a, allow_None: bool = True) -> Union[list, None]:
    if a is None and not allow_None:
        raise TypeError("None is not allowed when converting to list")
    return list(a) if a is not None else None


def concat_arrays(arrs):
    if not arrs:
        return arrs
    if len(arrs) == 1:
        return arrs[0]

    def _concat(a_list):
        a_list = [a for a in a_list if a is not None]
        return np.concatenate(a_list, axis=0) if a_list else None

    return tuple(map(_concat, zip(*arrs)))


def dtype_str(v):
    return helpers.to_dtype(v).str


def get_working_directory():
    working_directory_from_config = DataHeroesConfiguration().get_param_str("working_directory")
    wd = pathlib.Path(working_directory_from_config) if working_directory_from_config else pathlib.Path(os.getcwd())
    if not wd.exists():
        wd.mkdir(exist_ok=True)
    return str(wd)


def set_working_directory(path: Union[str, os.PathLike]):
    DataHeroesConfiguration().add_params(working_directory=str(pathlib.Path(path)))


def generate_index_uuid(dataset, transform_context, **kwargs):
    return np.array([uuid.uuid4().hex for _ in range(dataset.shape[0])])


def generate_index_uuid_int(dataset, transform_context, **kwargs):
    # return np.random.random_integers(np.iinfo(int).max, size=dataset.shape[0])
    return np.array([uuid.uuid4().int & (1 << 62) - 1 for _ in range(dataset.shape[0])])


def generate_index_seq(dataset, transform_context, **kwargs):
    start_ind = transform_context.setdefault('generate_index_seq', 0)
    last_ind = start_ind + len(dataset)
    transform_context['generate_index_seq'] = last_ind
    return np.arange(start_ind, last_ind)


transform_methods = {
    'generate_index_uuid': generate_index_uuid,
    'generate_index_seq': generate_index_seq
}

DTypeStr = Union[str, np.dtype]
DTypeNumeric = Union[str, np.dtype]
DTypeArray = Union[np.ndarray, list, tuple, Iterable]
DTypeField = Union[DTypeStr, DTypeNumeric]


@dataclass
class BaseDC:
    """base class for all dataclasses """

    def dict_factory(self, result) -> dict:
        return dict(result)

    def __post_init__(self):
        helpers.dicts_to_dataclasses(self)

    def to_dict(self):
        # return asdict(self)
        return helpers.dataclass_to_dict(self)

    @classmethod
    def from_dict(cls, d: dict):
        # noinspection PyArgumentList
        return cls(**d)

    @classmethod
    def from_kw(cls, **kwargs):
        # noinspection PyArgumentList
        return cls(**kwargs)

    @classmethod
    def from_any(cls, o: Any):
        if isinstance(o, dict):
            return cls.from_dict(o)
        elif isinstance(o, cls):
            return o
        else:
            # noinspection PyArgumentList
            return cls(o)


# ==============================================
# Data params structures - for preprocessing
# ==============================================

@dataclass
class Transform(BaseDC):
    """Data class for preprocessing data transformation.

    """

    name: str = None
    func: Callable = None
    func_text: str = None
    func_name: str = None

    __annotations__ = {
        'name': str,
        'func': Callable,
        'func_text': str,
        'func_name': str,
    }

    def restore_function(self):
        if self.func_name is not None:
            exec(self.func_text)
            self.func = globals()[self.func_name]

    def __post_init__(self):
        super(Transform, self).__post_init__()

    def run_transform(self, dataset, transfer_context=None, **kwargs):
        if self.name is not None:
            func = transform_methods.get(self.name)
        else:
            if self.func is None:
                self.restore_function()
            func = self.func
        if func.__code__.co_argcount == 1:
            return func(dataset, **kwargs)
        else:
            return func(dataset, transfer_context, **kwargs)

    def dict_factory(self, result) -> dict:
        result = super(Transform, self).dict_factory(result)
        if result['func'] is not None:
            if not result['func_text']:
                result['func_name'] = self.func.__name__
                func_text = textwrap.dedent(inspect.getsource(result['func']))
                func_text = f'global {self.func.__name__}\n{func_text}'
                result['func_text'] = func_text
            result.pop('func', None)
        else:
            result.pop('func', None)
            result.pop('func_name', None)
            result.pop('func_text', None)

        return result


@dataclass
class DataField(BaseDC):
    """Base class representing dataset field (e.g. feature)"""

    name: str = None
    transform: Transform = None
    dtype: DTypeField = None

    __annotations__ = {
        'name': str,
        'transform': Transform,
        'dtype': DTypeField,
    }

    def __post_init__(self):
        super(DataField, self).__post_init__()
        if self.dtype:
            self.set_dtype(self.dtype)

    def set_dtype(self, v):
        self.dtype = helpers.to_dtype(v)

    def dict_factory(self, result) -> dict:
        result = super(DataField, self).dict_factory(result)
        result['dtype'] = dtype_str(result['dtype'])
        return result


@dataclass
class FeatureField(DataField):
    """
    A representation of a feature. currently only numeric features are supported
    """
    categorical: bool = False
    array: bool = False
    fill_value: Any = None

    __annotations__ = {
        'categorical': bool,
        'array': bool,
        'fill_value': Any,
    }

    def set_dtype(self, v):
        self.dtype = helpers.to_dtype(v)
        if not helpers.is_dtype_numeric(self.dtype):
            raise ValueError(f"All features must be numeric. {self.name} is of type {v}")


@dataclass
class PropertyField(DataField):
    """
    A representation of a property, dataset field that do not impact model, but could be used for samples selection.
    """

@dataclass
class TargetField(DataField):
    """Target field definition (aka y)"""


@dataclass
class IndexField(DataField):
    """Index (id) field definition"""

    transform: Transform = None
    dtype: Union[DTypeStr, DTypeNumeric] = None

    __annotations__ = {
        'transform': Transform,
        'dtype': Union[DTypeStr, DTypeNumeric],
    }


@dataclass
class UUIDIndexField(IndexField):
    """Default index definition when not provided"""

    transform: Transform = dataclasses.field(default_factory=lambda: Transform('generate_index_uuid'))
    name: str = 'index_column'
    dtype: Union[DTypeStr, DTypeNumeric] = str


@dataclass
class SeqIndexField(IndexField):
    """Default index definition when not provided"""

    transform: Transform = dataclasses.field(default_factory=lambda: Transform('generate_index_seq'))
    name: str = 'index_column'
    dtype: Union[DTypeStr, DTypeNumeric] = int


DefaultIndexField = UUIDIndexField


@dataclass
class DataParams(BaseDC):
    """A class including all required information to preprocess the data.
    When not defined all fields/columns in the data are treated as features.

    The example below shows how the class is used by the CoresetTreeService class.
    See a more extensive example at the end of the page.
    ```py
    data_params = {
        'target': {'name': 'Cover_Type'},
        'index': {'name': 'index_column'}
    }

    service_obj = CoresetTreeServiceLG(
        optimized_for='training',
        data_params=data_params
    )
    ```
    <table>
    <tr><th> Parameter name</th><th>Type</th><th>Description</th></tr>
    <tr><td colspan='3'><b><a id="General Parameters">General Parameters</a></b></td></tr>
    <tr><td>features</td><td> List</td><td>The list of the fields/columns used as features to build
    the Coreset and train the model. If not defined, the <code>columns_to_features</code> parameter should be defined.
    Each feature is defined as a dictionary with the following attributes (only name is mandatory):
    <ul>
        <li><code>name</code>: The feature name.</li>
        <li><code>dtype</code>: The feature data type.</li>
        <li><code>categorical</code>: Set to true if the feature is categorical.
        For more information refer to the <a href="#Categorical Features">Categorical Features Parameters</a> section.
        </li>
        <li><code>array</code>: Set to true if the feature is an array.
        For more information refer to the <a href="#Array Features">Array Features Parameters</a> section.
        </li>
        <li><code>fill_value</code>: In case the feature has missing values, how should they be filled.
        For more information refer to the <a href="#Missing Values">Missing Values Parameters</a> section.
        </li>
        <li><code>transform</code>: A function defining the required transformation for the feature.
        For more information refer to the <a href="#Data Transformation">Data Transformation Parameters</a> section.
        </li>
    <ul> See the example at the end of the page.</td></tr>
    <tr><td>target</td><td> dict</td><td>The target column.
    <br>Example: <code>'target': {'name': 'Cover_Type'}</code></td></tr>
    <tr><td>sample_weight</td><td> dict</td><td>The sample weight column.
    <br>Example: <code>'sample_weight': {'name': 'Weights'}</code></td></tr>
    <tr><td>index</td><td> dict</td><td>The index column. <br>Example: <code>'index': {'name': 'index_column'}
    </code></td></tr>
    <tr><td>properties</td><td> List</td><td>A list of fields/columns which won’t be used to build the Coreset or train
    the model, but it is possible to <code>filter_out_samples</code> on them or to pass them in the
    <code>select_from_function</code> of <code>get_cleaning_samples</code>.
    <br><br>Example: <code>'properties': [{'name': 'date'},]</code></td></tr>
    <tr><td>columns_to_features</td><td> Union[bool, dict], default False</td><td>Either <code>bool</code> or
    <code>dict</code> with two possible fields, <code>include</code> or <code>exclude</code>.
    When set to true, all fields/columns in the dataset are treated as features.
    When <code>include</code> is used, only fields/columns defined or those fitting the defined masks are
    treated as features. When <code>exclude</code> is used, only fields/columns defined or those
    fitting the defined masks are not treated as features. <br><br>
    Example: <code>{'exclude': ['internal_.*', 'bad']}</code></td></tr>
    <tr><td>datetime_to_properties </td><td> boolean, default True</td><td>By default, all datetime fields/columns
    are turned into properties. Properties, won’t be used to build the Coreset or train
    the model, but it is possible to <code>filter_out_samples</code> on them or to pass them
    in the <code>select_from_function</code> of <code>get_cleaning_samples</code>. To disable this functionality
    set <code>'datetime_to_properties': False</code>.</td></tr>
    <tr><td>save_orig</td><td>bool, default False</td><td>
    When data transformations are defined (such as data_transform_before or feature level transform),
    the default behavior is to save the data only after the transformations. To save the data also in
     it original format, as it was handed to the build function and before any user defined data
     transformations, set `'save_orig': True`. To retrieve the Coreset in its original format
     user `preprocessing_stage='original'` when calling the `get_coreset` function.
     <tr><td>seq_column</td><td>dict, default None</td><td>
    Defining a sequence column (such as a date), allows to specify <code>seq_from</code> and <code>seq_to</code>
    parameters to <code>get_coreset</code>, <code>fit</code>,
    <code>grid_search</code> and the validation functions, so these functions would be executed on a subset of the
    data (such as certain date ranges). The <code>seq_column</code> is a dictionary containing the following parameters:
    <ul>
        <li><code>name/id/prop_id</code>: Required. The name, id or prop_id of the sequence column. name:
        The name of the column. id: The index of the feature starting from 0. prop_id:
        The index of the property starting from 0.</li>
        <li><code>granularity</code>: Required. The granularity in which the sequence column would be queried.
        Can be either a <a href="https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects">pandas offset</a>
        or a callable function.
        </li>
        <li><code>datetime_format</code>: Required in case the sequence column is a datetime formatted as string.
        The datetime format of the sequence column.</li>
        <li><code>chunk_by</code>: Optional. Optional. When set to <code>True</code>, the Coreset tree will be built using the <code>chunk_by</code> functionality according to the sequence column instead of using a fixed <code>chunk_size</code>.
        When set to <code>every_build</code>, every call to <code>build</code> or <code>partial_build</code> will receive its own sequence, which can be assigned by the user or will be automatically assigned by the library.
        </li>
        <li><code>sliding_window</code>: Optional. Can be set to an integer value. If both sliding_window and chunk_by are set, the tree will only keep samples that are in the last n seq_column granularity units where n is the value of the sliding_window.
        All samples that are outside the sliding window are completely removed from the tree and can not be retrieved unless the tree is rebuilt without the sliding_window parameter.
        </li>
    </ul>
    <br>Example:
    ```py
        'seq_column':
            {
                'name': 'Transaction Date',
                'granularity': 'D',
                'datetime_format': '%yyyy-%mm-%dd',
                'chunk_by': True,
                'sliding_window': 10,
            }
    ```
        </td></tr>
    </td></tr>
    <tr><td colspan='3'><b><a id="Categorical Features">Categorical Features Parameters</a></b></tr>
    <tr><td>detect_categorical </td><td> boolean, default True</td>
    <td>By default, all non-numeric and non-boolean fields/columns are automatically regarded
    as categorical features and one-hot- and/or target-encoded by the library. To disable this
    functionality set <code>'detect_categorical': False</code>.
    <br><br>Note - coresets can only be built with numeric features.</td></tr>
    <tr><td>cat_encoding_method</td><td> str, default None </td>
    <td>Use this parameter to override the default categorical encoding strategy (valid non-default values are
    <code>‘OHE’</code>, <code>‘TE’</code>, <code>‘MIXED’</code>). If this parameter is left on default, the strategy
    for encoding categorical features is determined as follows: a mixed categorical encoding strategy, combining both
    Target Encoding (TE) and One Hot Encoding (OHE), will be used in binary classification tasks; One Hot Encoding (OHE)
    will be used in all other types of learning tasks (multiclass classification, regression, and unsupervised
    learning). Valid overriding is effective only for binary classification tasks (e.g., change of the default
    <code>‘MIXED’</code> to <code>‘OHE’</code> or to <code>‘TE’</code>).<br>
    For more details on the mixed categorical encoding strategy, please see the <code>favor_ohe_num_cats_thresh</code>
    documentation below.</td></tr>
    <tr><td>categorical_features </td><td> List </td><td>Forcing specific features,
    which include only numeric values, to be categorical, can be done in two possible ways.
    On a feature-by-feature base (setting the <code>categorical</code> attribute to True in the <code>features</code>
    list) or using the <code>categorical_features</code> list, passing the feature names or the feature index in
    the dataset starting from 0. <br><br>
    See the example at the end of the page.</td></tr>
    <tr><td>ohe_min_frequency</td><td> float between 0 and 1, default 0.01    </td>
    <td>Similarly to Skicit-learn's OneHotEncoder <code>min_frequency</code> parameter, specifies the minimum frequency
    below which a category will be considered infrequent. <br><br>Example: <code>'ohe_min_frequency': 0</code></td></tr>
    <tr><td>ohe_max_categories</td><td> int, default 100 </td>
    <td>Similarly to Skicit-learn's OneHotEncoder <code>max_categories</code> parameter, specifies an upper limit to the number
    of output features for each input feature when considering infrequent categories.
    <br><br>Example: <code>'ohe_max_categories': 500</code></td></tr>
    <tr><td>te_cv</td><td> int, default 5 </td>
    <td>If Target Encoding is employed, this parameter determines the number of folds in the 'cross fitting' strategy
    used in TargetEncoder’s <code>fit_transform</code>. In practice, a lower number may be applied, based on the
    distribution of classes in the data.</td></tr>
    <tr><td>te_random_state </td><td> int, default None </td>
    <td>If Target Encoding is employed, this parameter affects the ordering of the indices which controls the
    randomness of each fold in its 'cross fitting' strategy. Pass an int for reproducible output across multiple
    function calls.</td></tr>
    <tr><td>favor_ohe_num_cats_thresh</td><td> int, default 50 </td>
    <td>Works in conjunction with <code>favor_ohe_vol_pct_thresh</code>.<br>
    In a mixed categorical encoding strategy, we employ both One Hot Encoding (OHE) and Target Encoding (TE) strategies
    at the same time, and divide the categorical attributes into two distinct groups for each encoding type.<br>
    For the division purposes, if the number of categories for a categorical feature is either lower than
    <code>favor_ohe_num_cats_thresh</code>, or higher than <code>favor_ohe_num_cats_thresh</code> but its
    <code>favor_ohe_num_cats_thresh</code> categories or less cover at least <code>favor_ohe_vol_pct_thresh</code>
    percent of the data instances, the OHE strategy will be favored over the TE.<br><br>
    Using the default values as an example, values of <code>favor_ohe_num_cats_thresh=50</code> and
    <code>favor_ohe_vol_pct_thresh=0.8</code> mean that if a categorical feature's top <code>50</code> (or less)
    categories capture <code>80%</code> (or more) of the volume, the feature will we be encoded using the OHE;
    otherwise, it will be encoded using the TE.</td></tr>
    <tr><td>favor_ohe_vol_pct_thresh </td><td> float between 0 and 1, default 0.8 </td>
    <td>Works in conjunction with <code>favor_ohe_num_cats_thresh</code>, please see its description.</td></tr>
    <tr><td colspan='3'><b><a id="Missing Values">Missing Values Parameters</a></b></tr>
    <tr><td>detect_missing</td><td> bool, default True</td>
    <td>By default, missing values are automatically detected and handled by the library.
    To disable this functionality set <code>'detect_missing': False</code>.
    <br><br>Note - coresets can only be built when there are no missing values.</td></tr>
    <tr><td>drop_rows_below</td><td>float between 0 and 1, default 0 (nothing is dropped)</td>
    <td> If the ratio of instances with missing values on any feature is lower than this ratio,
    those instances would be ignored during the coreset build.<br><br>Example: <code>'drop_rows_below': 0.05</code>
    </td></tr>
    <tr><td>drop_cols_above </td><td> float between 0 and 1, default 1 (nothing is dropped).</td>
    <td>If the ratio of instances with missing values for a certain feature is higher than this ratio,
    this feature would be ignored during the coreset build.<br><br>Example: <code>'drop_cols_above': 0.3</code>
    </td></tr>
    <tr><td>fill_value_num </td><td> float </td><td>By default, missing values for numeric features would be
    replaced with the calculated mean.
    It is possible to change the default behavior for numeric features by defining a specific replacement
    number for all features using the <code>fill_value_num</code> or to use the <code>fill_value</code>
    attribute in the <code>features</code> list, to define a replacement on a
    feature-by-feature base.<br><br>Example: <code>'fill_value_num':-1</code></td></tr>
    <tr><td>fill_value_cat </td><td> Any </td>
    <td>By default, missing values for categorical features would be treated just as another category/value when the
    feature is one-hot encoded by the library. <br><br>It is possible to change the default
    behavior for categorical features by defining a specific replacement value or by
    specifying <code>take_most_common</code>, (which will fill the missing values with the most commonly
     used value of the feature) for all categorical features using the
     <code>fill_value_cat</code> or to use the <code>fill_value</code> attribute in the <code>features</code> list,
     to define a replacement on a feature-by-feature base.
     <br><br>Example: <code>'fill_value_cat': 'take_most_common'</code></td></tr>
    <tr><td colspan='3'><b><a id="Data Transformation">Data Transformation Parameters</a></b></tr>
    <tr><td>data_transform_before</td><td> Transform</td>
    <td>A preprocessing function applied to the entire dataset. The function's signature is
    <code>func(dataset) -> dataset</code>.
    <br><br>See the example at the end of the page.</td></tr>
    <tr><td>feature_transform_default</td><td> Transform</td>
    <td>A default feature transformation function applied on feature-by-feature base.
    Executed after the <code>data_transform_before</code>. The function can be overridden at the feature level
    with by defining the <code>transform</code> attribute in the <code>features</code> list.
    The function's signature is <code>func(dataset, transform_context:dict) -> data</code>.
    The function returns the data of a single feature.
    <br><br>Example: <code>'transform_context': {'feature_name': 'salary'}</code></td></tr>
    <tr><td>data_transform_after</td><td> Transform</td>
    <td>A preprocessing function similar to <br>data_transform_before<br>, executed after the feature-by-feature
    transformation.<br><br>See the example at the end of the page.</td></tr>

    <tr><td colspan='3'><b><a id="Array Features">Array Features Parameters</a></b></tr>
        <tr><td>array_features </td><td> List </td><td>Specify features to be of an array type, can be done in two possible ways.
    On a feature-by-feature base (setting the <code>array</code> attribute to True in the <code>features</code>
    list) or using the <code>array_features</code> list, passing the feature names or the feature index in
    the dataset starting from 0. <br><br>
    See the example at the end of the page.</td></tr>
    <tr><td>array_min_frequency</td><td> float between 0 and 1, default 0.01    </td>
    <td>Similarly to Skicit-learn's OneHotEncoder <code>min_frequency</code> parameter, specifies the minimum frequency
    below which a label in the array will be considered infrequent. <br><br>Example: <code>'array_min_frequency': 0</code></td></tr>
    <tr><td>array_max_categories</td><td> int, default 200 </td>
    <td>Similarly to Skicit-learn's OneHotEncoder <code>max_categories</code> parameter, specifies an upper limit to the number
    of output features for each input array feature when considering infrequent categories.
    <br><br>Example: <code>'array_max_categories': 200</code></td></tr>

    </table>

    Code example:
    ```py
    def data_before_processing(dataset):
        df = pd.DataFrame(dataset)
        # remove dataset rows by condition
        df = df[df['department'] != 'Head Office']
        return df

    def education_level_transform(dataset):
        # replace categorical values with numeric
        df = pd.DataFrame(dataset)
        conditions = [
            df['education_level'] = 'elementary_school',
            df['education_level'] = 'high_school',
            df['education_level'] = 'diploma',
            df['education_level'] = 'associates',
            df['education_level'] = 'bachelors',
            df['education_level'] = 'masters',
            df['education_level'] = 'doctorate',
            ]
        choices = [1, 2, 3, 4, 5, 6, 7]
        df['education_level'] = np.select(conditions, choices)
        return df['education_level']

    def yearly_bonus_transform(dataset):
        df = pd.DataFrame(dataset)
        # for creating new feature
        return df['h1_bonus'] + df['h2_bonus']

    def transform_scaling(dataset):
        from sklearn.preprocessing import MinMaxScaler
        df = pd.DataFrame(dataset)
        scaler = MinMaxScaler()
        columns_to_scale = ['age', 'work_experience_in_months']
        df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
        return df

    data_params = {
        'features': [
            {
                'name': 'family_status',
                'categorical': True, 'fill_value': 'single'
            },
            {'name': 'department', 'categorical': True},
            {'name': 'tags', 'array': True},
            {'name': 'gender'},
            {'name': 'job_title'},
            {'name': 'age', 'fill_value': 18},
            {'name': 'work_experience_in_months'},
            {
                'name': 'education_level',
                'transform': {'func': education_level_transform}
            },
            {
                'name': 'yearly_bonus',
                'transform': {'func': yearly_bonus_transform}
            },
        ],
        'properties': [{'name': 'full_name'}, {'name': 'Hire Date'}],
        'target': {'name': 'salary'},
        'categorical_features': ['gender'],
        'fill_value_cat': 'take_most_common',
        'fill_value_num': 0,
        'data_transform_before': {'func': data_before_processing},
        'data_transform_after': {'func': transform_scaling},
        'seq_column': {
            'name': 'Hire Date',
            'granularity': 'Y',
            'datetime_format': '%d/%m/%Y',
            'chunk_by': True,
        },
    }
    ```

    """

    features: Iterable[FeatureField] = None
    properties: Iterable[PropertyField] = None
    target: TargetField = None
    sample_weight: TargetField = None
    index: IndexField = None
    feature_transform_default: Transform = None
    transform_context: dict = None
    data_transform_before: Transform = None
    data_transform_after: Transform = None
    columns_to_features: Union[bool, dict] = False
    n_instances: int = None
    n_classes: int = None
    is_classification: bool = False
    cat_encoding_method: str = None
    ohe_max_categories: int = 100
    ohe_min_frequency: float = 0.01
    te_cv: int = 5
    te_random_state: Union[int, RandomState] = None
    favor_ohe_num_cats_thresh: int = 50
    favor_ohe_vol_pct_thresh: float = 0.8
    detect_categorical: bool = True
    detect_missing: bool = True
    categorical_features: Iterable[Union[str, int]] = None
    array_features: Iterable[Union[str, int]] = None
    array_max_categories: int = 200
    array_min_frequency: float = 0.01
    drop_rows_below: float = 0
    drop_cols_above: float = 1

    seq_column: dict = None

    fill_value_cat: Any = None
    fill_value_num: float = None
    datetime_to_properties: bool = True
    save_orig: bool = False

    __annotations__ = {
        'features': Iterable[FeatureField],
        'properties': Iterable[PropertyField],
        'target': TargetField,
        'sample_weight': TargetField,
        'index': IndexField,
        'feature_transform_default': Transform,
        'transform_context': dict,
        'data_transform_before': Transform,
        'data_transform_after': Transform,
        'columns_to_features': Union[bool, dict],
        'n_instances': int,
        'n_classes': int,
        'is_classification': bool,
        'cat_encoding_method': str,
        'ohe_max_categories': int,
        'ohe_min_frequency': float,
        'array_max_categories': int,
        'array_min_frequency': float,
        'te_cv': int,
        'te_random_state': Union[int, RandomState],
        'favor_ohe_num_cats_thresh': int,
        'favor_ohe_vol_pct_thresh': float,
        'detect_categorical': bool,
        'detect_missing': bool,
        'categorical_features': Iterable[Union[str, int]],
        'array_features': Iterable[Union[str, int]],
        'datetime_to_properties': bool,
        'drop_rows_below': float,
        'drop_cols_above': float,
        'seq_column': dict,
        'fill_value_cat': Any,
        'fill_value_num': float,
        'save_orig': bool,
    }

    def __post_init__(self):

        # Ensure attributes are lists
        self.features = to_list(self.features)
        self.properties = to_list(self.properties)
        self.categorical_features = to_list(self.categorical_features)

        if self.seq_column is not None:
            chunk_by = self.seq_column.get('chunk_by')
            granularity = self.seq_column.get('granularity')
            datetime_format = self.seq_column.get('datetime_format')
            sliding_window = self.seq_column.get('sliding_window')

            if chunk_by != 'every_build':
                if not any(self.seq_column.get(k) is not None for k in ['id', 'name', 'prop_id']):
                    raise ValueError("`seq_column` must have either `id`, `name`, or `prop_id` defined")

                if granularity is None:
                    raise ValueError("`granularity` must be defined when `seq_column` is provided")

                valid_granularities = [
                    'B', 'C', 'D', 'W', 'M', 'SM', 'BM', 'CBM', 'MS', 'SMS', 'BMS', 'CBMS',
                    'Q', 'BQ', 'QS', 'BQS', 'A', 'Y', 'BA', 'BY', 'AS', 'YS', 'BAS', 'BYS',
                    'BH', 'H', 'T', 'min', 'S', 'L', 'ms', 'U', 'us', 'N'
                ]
                if granularity not in valid_granularities and not callable(granularity):
                    raise ValueError("`granularity` must be a valid pandas offset or a callable")

                if not datetime_format and not callable(granularity):
                    raise ValueError("`datetime_format` must be defined when `seq_column` is datetime")

                self.validate_sliding_window(sliding_window)

        super(DataParams, self).__post_init__()

    def validate_sliding_window(self, sliding_window):
        if sliding_window is None:
            return

        if not isinstance(sliding_window, int):
            raise ValueError(f"`sliding_window` must be of type int but received type {type(sliding_window)}")
        
        if sliding_window <= 0:
            raise ValueError(f"`sliding_window` must be a positive integer but received {sliding_window}")


@dataclass
class DataParamsInternal(BaseDC):
    """
    A class including all **internal** information to preprocess the data.
    """

    used_categories_: dict = None
    # calculated indexes of categorical features based
    # on user-defined categories and auto-detection
    calculated_props_: Iterable[Union[int]] = None
    categorical_features_: Iterable[Union[int]] = None
    array_features_: Iterable[Union[int]] = None
    aggregated_missing_replacements: Iterable[Union[int]] = None
    y_mixed_types: bool = False
    bool_features_: Iterable[int] = None
    last_fit_preprocessing_stage: str = None
    seq_column_: Union[str, int] = None
    seq_column_location_: str = None
    seq_granularity_: Any = None
    seq_granularity_serialized_: Any = None
    seq_datetime_format: str = None
    seq_chunk_by: bool = None
    seq_every_build: Any = None

    __annotations__ = {
        'used_categories_': dict,
        'calculated_props_': Iterable[Union[int]],
        'categorical_features_': Iterable[Union[int]],
        'array_features_': Iterable[Union[int]],
        'aggregated_missing_replacements': Iterable[Union[int]],
        'y_mixed_types': bool,
        'bool_features_': Iterable[int],
        'last_fit_preprocessing_stage': str,
        'seq_column_': Union[str, int],
        'seq_column_location_': str,
        'seq_granularity_': Any,
        'seq_granularity_serialized_': Any,
        'seq_datetime_format': str,
        'seq_chunk_by': bool,
        'seq_every_build': Any,

    }

    def __post_init__(self):
        if self.categorical_features_ is not None:
            self.categorical_features_ = list(self.categorical_features_)
        super(DataParamsInternal, self).__post_init__()


# ==============================================
# Dataset schema structures - data persistence
# ==============================================


@dataclass
class Column(BaseDC):
    """representation of a database column"""

    name: str = None
    dtype: np.dtype = None

    def __post_init__(self):
        super(Column, self).__post_init__()
        self.set_dtype(self.dtype)

    def set_dtype(self, v):
        self.dtype = helpers.to_dtype(v)

    def dict_factory(self, result) -> dict:
        result = super(Column, self).dict_factory(result)
        result['dtype'] = dtype_str(result['dtype'])
        return result


@dataclass
class DataSchema(BaseDC):
    """A representation of a database schema (e.g a table)"""

    columns: Iterable[Column] = None
    features_cols: Iterable[Column] = None
    properties_cols: Iterable[Column] = None
    index_col: Column = None
    target_col: Column = None

    __annotations__ = {
        'columns': Iterable[Column],
        'features_cols': Iterable[Column],
        'properties_cols': Iterable[Column],
        'index_col': Column,
        'target_col': Column,
    }


@dataclass
class DataSchemaSql(DataSchema):
    """An sql representation of a database schema"""

    table_name: str = None
    conn_params: dict = None


# ==============================================
# Data manager main schemas
# ==============================================


@dataclass
class DMSchema(BaseDC):
    """Data manager base configuration """

    data_schema: DataSchema = None
    dataset_schema: DataSchema = None
    data_params: DataParams = None
    data_params_internal: DataParamsInternal = None
    save_orig: bool = False
    save_dataset: bool = True
    node_metadata_func: Union[dict, Callable[[Tuple[np.ndarray], np.ndarray, Union[list, None]], Union[list, dict, None]]] = None
    working_directory: Union[str, os.PathLike] = None

    __annotations__ = {
        'data_schema': DataSchema,
        'dataset_schema': DataSchema,
        'data_params': DataParams,
        'data_params_internal': DataParamsInternal,
        'save_orig': bool,
        'save_dataset': bool,
        'node_metadata_func': Callable,
        'working_directory': Union[str, os.PathLike],
    }

    def __post_init__(self):
        super(DMSchema, self).__post_init__()
        self.data_schema = self.data_schema or dataclasses.fields(type(self))[0].type()
        self.dataset_schema = self.dataset_schema or dataclasses.fields(type(self))[1].type()
        self.working_directory = str(self.working_directory) if self.working_directory else self.working_directory
        self.data_params = self.data_params or DataParams()
        self.data_params_internal = self.data_params_internal or DataParamsInternal()
        if self.node_metadata_func and isinstance(self.node_metadata_func, dict):
            self._node_metadata_func_dict = self.node_metadata_func
            self.node_metadata_func = utils.deserialize_function(self.node_metadata_func)
        else:
            self._node_metadata_func_dict = None

    def dict_factory(self, result) -> dict:
        result = super(DMSchema, self).dict_factory(result)
        node_metadata_func = result.pop('node_metadata_func', None)
        if self._node_metadata_func_dict:
            result['node_metadata_func'] = self._node_metadata_func_dict.copy()
        elif node_metadata_func:
            result['node_metadata_func'] = utils.serialize_function(node_metadata_func)
        if result.get('working_directory') and not isinstance(result['working_directory'], str):
            result['working_directory'] = str(result['working_directory'])
        return result


@dataclass
class DMSchemaSql(DMSchema):
    """Data manager base configuration for an SQL manager"""

    conn_params: dict = None
    data_schema: DataSchemaSql = None
    dataset_schema: DataSchemaSql = None

    __annotations__ = {
        'conn_params': dict,
        'data_schema': DataSchemaSql,
        'dataset_schema': DataSchemaSql,
    }


@dataclass
class DMSchemaSqlite(DMSchemaSql):
    """Data manager base configuration for sqlite3 manager"""

    db_file: Optional[str] = None
    in_memory: bool = False

    def __post_init__(self):
        super(DMSchemaSqlite, self).__post_init__()
        working_directory = self.working_directory or get_working_directory()
        self.dataset_schema.table_name = self.dataset_schema.table_name or f"table_{uuid4().hex}"
        self.dataset_schema.target_col = self.dataset_schema.target_col
        self.dataset_schema.index_col = self.dataset_schema.index_col or 'index_col'
        self.data_schema.table_name = self.data_schema.table_name or f"table_{uuid4().hex}"
        self.data_schema.index_col = self.data_schema.index_col or 'index_column'
        self.db_file = self.db_file or os.path.join(working_directory, f'sqlite_{uuid4().hex}.db')


@dataclass
class DMSchemaHDF5(DMSchema):
    """Data manager base configuration for hdf5 manager"""

    db_file: Optional[str] = None
    data_schema: DataSchemaSql = None
    dataset_schema: DataSchemaSql = None

    __annotations__ = {
        'db_file': Optional[str],
        'data_schema': DataSchemaSql,
        'dataset_schema': DataSchemaSql,
    }

    def __post_init__(self):
        super(DMSchemaHDF5, self).__post_init__()
        working_directory = self.working_directory or get_working_directory()
        self.dataset_schema.table_name = self.dataset_schema.table_name or f"table_{uuid4().hex}"
        self.dataset_schema.target_col = self.dataset_schema.target_col
        self.dataset_schema.index_col = self.dataset_schema.index_col or 'index_col'
        self.data_schema.table_name = self.data_schema.table_name or f"table_{uuid4().hex}"
        self.data_schema.index_col = self.data_schema.index_col or 'index_column'
        self.db_file = self.db_file or os.path.join(working_directory, f'dfh5_{uuid4().hex}.hd5')
