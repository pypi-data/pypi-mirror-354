import json
from dataclasses import dataclass, field, asdict
from enum import IntEnum
from io import StringIO
from typing import Union, Dict, Any, Iterable

import pandas as pd

from dataheroes.core.types import CoresetSampleParamsClassification, CoresetSampleParams
from dataheroes.data.common import DataParams
from dataheroes.services.common import CoresetParams, DataTuningParams, DataTuningParamsClassification
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, StringType, ArrayType, MapType, \
    BooleanType, FloatType


@dataclass
class LevelDataFrame:
    """
    Represents a level in a tree structure with associated DataFrame and metadata.
    """

    def __init__(self, level=0, level_df=None, level_metadata=None):
        """
        Initialize LevelDataFrame.

        Parameters:
            level (int): The level in the tree.
            level_df (DataFrame): The DataFrame associated with the level.
            level_metadata (dict): Metadata associated with the level.
        """
        if level_metadata is None:
            level_metadata = {}
        self.level = level
        self.level_df = level_df
        self.level_metadata = level_metadata

    level: int
    level_df: DataFrame
    level_metadata: dict = field(default_factory=dict)

    class MetaDataParams:
        PARTITIONS_TO_SAVE = "partitions_to_save"
        ROOT_CORESET_PARTITION = "root_coreset_partition"


class SaveOrig(IntEnum):
    """
    Enumeration of data column save modes.
    """
    NONE = 1
    PREPROCESSING_ONLY = 2
    PREPROCESSING_AND_BUILD = 3


def _prepare_tree_params(data_tuning_params: Union[DataTuningParams, DataTuningParamsClassification]):
    """
    Prepares the tree parameters by merging static kwargs and dynamic hyperparameters.

    Parameters:
        data_tuning_params (Union[DataTuningParams, DataTuningParamsClassification]): The data tuning parameters.

    Returns:
        list: List of TreeParams objects with combined parameters.
    """
    # Merge static kwargs with each hyperparameter set, with data_tuning_params taking precedence
    return [TreeParams(sample_params=param, tree_index=idx) for idx, param in enumerate(data_tuning_params.create_sample_params())]


@dataclass
class ServiceParams:
    """
    A class to hold parameters for configuring the coreset tree service. This is a private class which holds the state of the service in the Coreset service.
    Please do not add to here spark object like a session or dataframe because of serialization issues this class will only be available on the driver.
    """

    dhspark_path: str = None
    data_params: Union[DataParams, dict] = None
    data_tuning_params: Union[DataTuningParams, DataTuningParamsClassification, list] = None
    coreset_params: Union[CoresetParams, dict] = None
    chunk_size: int = None
    chunk_sample_ratio: float = None
    n_instances: int = None
    n_instances_exact: bool = None
    first_level_max_chunk: int = None
    first_level_last_max_chunk: int = None  # max chunk before partial tree build
    partial_build_starting_index: int = None
    partial_build_ending_chunk_by: str = None
    tree_size: int = None
    categorical_columns: [] = None
    numeric_columns: [] = None
    calc_column_names: [] = None
    ohe_arr_size_diff: {} = None
    target_column: str = None
    index_column: str = None
    model_cls: str = None
    chunk_by: str = None
    stop_level_max_chunk: int = None
    stop_level: int = None
    stop_tree_size: int = None
    leaf_factor: int = 2
    save_orig: SaveOrig = SaveOrig.NONE
    trace_mode: str = None
    tree_params: list = None

    def __post_init__(self):
        if self.data_tuning_params is not None:
            self.tree_params = _prepare_tree_params(self.data_tuning_params)

        self.schema = StructType([
            StructField("dhspark_path", StringType(), True),
            StructField("data_params", StringType(), True),
            StructField("data_tuning_params", StringType(), True),
            StructField("coreset_params", StringType(), True),
            StructField("chunk_size", IntegerType(), True),
            StructField("chunk_sample_ratio", FloatType(), True),
            StructField("n_instances", IntegerType(), True),
            StructField("n_instances_exact", BooleanType(), True),
            StructField("first_level_max_chunk", IntegerType(), True),
            StructField("first_level_last_max_chunk", IntegerType(), True),
            StructField("partial_build_starting_index", IntegerType(), True),
            StructField("partial_build_ending_chunk_by", StringType(), True),
            StructField("tree_size", IntegerType(), True),
            StructField("categorical_columns", ArrayType(StringType()), True),
            StructField("numeric_columns", ArrayType(StringType()), True),
            StructField("calc_column_names", ArrayType(StringType()), True),
            StructField("ohe_arr_size_diff", MapType(StringType(), IntegerType()), True),
            StructField("target_column", StringType(), True),
            StructField("index_column", StringType(), True),
            StructField("model_cls", StringType(), True),
            StructField("chunk_by", StringType(), True),
            StructField("stop_level_max_chunk", IntegerType(), True),
            StructField("stop_level", IntegerType(), True),
            StructField("stop_tree_size", IntegerType(), True),
            StructField("leaf_factor", IntegerType(), True),
            StructField("save_orig", IntegerType(), True),
            StructField("trace_mode", StringType(), True),
            StructField("tree_params", ArrayType(MapType(StringType(), StringType())), True)
        ])

    def as_dict(self, datetime_format:str = None):
        data = asdict(self)
        data['data_params'] = json.dumps(data['data_params']) if self.data_params else None
        data['data_tuning_params'] = json.dumps(data['data_tuning_params'])
        data['coreset_params'] = json.dumps(data['coreset_params']) if data['coreset_params'] else None
        data['tree_params'] = [param.as_dict() for param in self.tree_params]
        data['save_orig'] = self.save_orig.value
        return data


    def to_spark_df(self, spark_session: SparkSession):
        return spark_session.createDataFrame([self.as_dict()], schema=self.schema)

    def from_dict(self, metadata, data_tuning_params_cls, coreset_params_cls):
        self.__dict__.update(metadata)

        if isinstance(metadata['data_tuning_params'], str):
            self.data_tuning_params = data_tuning_params_cls(**json.loads(metadata['data_tuning_params']))
        if isinstance(metadata['data_params'], str):
            self.data_params = DataParams(**json.loads(metadata['data_params']))
        self.save_orig = SaveOrig(metadata['save_orig'])
        if isinstance(metadata['coreset_params'], str):
            self.coreset_params = coreset_params_cls(**json.loads(metadata['coreset_params']))
        self.tree_params = [TreeParams().from_dict(param, data_tuning_params_cls._sample_params_cls) for param in metadata['tree_params']]

        return self


@dataclass
class TreeParams:
    """
       A class to hold parameters for configuring of the coreset tree.
       This is a private class which holds the state of the tree in the Coreset service.
       Please do not add to here spark object like a session or dataframe because of serialization issues.
       This class will only be available on the driver.
    """

    sample_params: Union[CoresetSampleParams, CoresetSampleParamsClassification, dict] = None
    chunk_by_tree: Any = None
    tree_index: int = None

    def as_dict(self):
        return {
            "sample_params": json.dumps(self.sample_params.to_dict()) if self.sample_params else None,
            "chunk_by_tree": self._chunk_tree_to_json() if self.chunk_by_tree is not None else None,
            "tree_index": self.tree_index
        }

    def _chunk_tree_to_json(self):

        df_combined = self.chunk_by_tree.copy()
        # Format the date columns as strings
        df_combined['start_seq'] = df_combined['start_seq'].astype(str)
        df_combined['end_seq'] = df_combined['end_seq'].astype(str)
        # Convert the combined DataFrame to JSON
        json_data = df_combined.to_json(orient='records')
        return json_data

    def from_dict(self, metadata, coreset_params_cls):
        self.__dict__.update(metadata)
        if self.sample_params:
            self.sample_params = coreset_params_cls(**json.loads(metadata['sample_params']))
        # unpack the chunk_by_tree json
        if self.chunk_by_tree:
            self.chunk_by_tree = pd.read_json(StringIO(metadata['chunk_by_tree']), orient='records')
            # Convert the date columns back to datetime objects
            self.chunk_by_tree['start_seq'] = pd.to_datetime(self.chunk_by_tree['start_seq'])
            self.chunk_by_tree['end_seq'] = pd.to_datetime(self.chunk_by_tree['end_seq'])
        self.tree_index = int(self.tree_index)
        return self

    @property
    def coreset_size(self):
        return self.sample_params.coreset_size

    @property
    def class_size(self):
        return self.sample_params.class_size

    @property
    def sample_all(self):
        return self.sample_params.sample_all


@dataclass
class TreeDataFrame:
    """
    Represents a tree structure with associated DataFrames and parameters.   """

    validation_ldf: LevelDataFrame = None
    chunk_data_no_coreset_ldf: LevelDataFrame = None
    tree_ldf: list[LevelDataFrame] = field(default_factory=list)

    def addUpdateLevel(self, level: int, df: DataFrame = None) -> LevelDataFrame:
        """
        Add or update a level in the tree with the specified DataFrame.

        Parameters:
            level (int): The level in the tree.
            df (DataFrame): The DataFrame associated with the level.

        Returns:
            LevelDataFrame: The LevelDataFrame object.
        """
        if self.levelInTree(level):
            self.setLevelDF(level, df)
        else:
            self.tree_ldf.append(LevelDataFrame(level, df))
        return self.getLevel(level)

    def addValidation(self, df: DataFrame):
        """
        Add validation DataFrame.

        Parameters:
            df (DataFrame): The DataFrame for validation.
        """
        self.validation_ldf = LevelDataFrame(0, df)

    def levelInTree(self, level) -> bool:
        """
        Check if a level is present in the tree.

        Parameters:
            level: The level to check.

        Returns:
            bool: True if the level is present, False otherwise.
        """
        ldf_ = level < len(self.tree_ldf)
        return ldf_

    def getLevel(self, level) -> LevelDataFrame:
        return self.tree_ldf[level]

    def getLevelDF(self, level) -> DataFrame:
        return self.getLevel(level).level_df

    def setLevelDF(self, level, df: DataFrame):
        self.tree_ldf[level].level_df = df

    def getValidation(self) -> LevelDataFrame:
        return self.validation_ldf

    def getValidationDF(self) -> Union[DataFrame, None]:
        if self.getValidation() is not None:
            return self.getValidation().level_df
        else:
            return None

    def setValidationDF(self, df: DataFrame, metadata: dict):
        self.validation_ldf = LevelDataFrame(level_df=df, level_metadata=metadata)

    def getChunkDataNoCoreset(self) -> LevelDataFrame:
        return self.chunk_data_no_coreset_ldf

    def getChunkDataNoCoresetDF(self) -> DataFrame:
        return self.getChunkDataNoCoreset().level_df

    def setChunkDataNoCoresetDF(self, df: DataFrame, metadata: dict = None):
        self.chunk_data_no_coreset_ldf = LevelDataFrame(level_df=df, level_metadata=metadata)

    def getTreeSize(self):
        if self.tree_ldf is not None:
            return len(self.tree_ldf)
        else:
            return None
