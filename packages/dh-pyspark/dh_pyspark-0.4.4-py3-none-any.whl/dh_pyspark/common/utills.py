import datetime
import importlib
import logging
import os
import random

import pandas as pd
import pyspark.ml.functions as mf
import pyspark.sql.functions as f
from pyspark.ml.linalg import VectorUDT
from pyspark.sql import DataFrame
from pyspark.sql.types import ArrayType, DoubleType, IntegerType

logger = logging.getLogger(__name__)


def df_vector_to_array(df):
    for field in df.schema.fields:
        if field.dataType == VectorUDT():
            df = df.withColumn(field.name, mf.vector_to_array(field.name))
    return df


def df_array_to_vector(df: DataFrame):
    for field in df.schema.fields:

        if isinstance(field.dataType, ArrayType) and isinstance(field.dataType.elementType, DoubleType):
            df = df.withColumn(field.name, mf.array_to_vector(field.name))
    return df


def set_udf_logging(test: bool, filename: str = None):
    if test:  # this should not be used on EMR
        log_directory = os.path.dirname(filename)
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(filename=filename, encoding='utf-8', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-2s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filemode="a")


def convert_spark_date_format_to_pandas_date_format(spark_date_format: str) -> str:
    """
    Converts a PySpark date format to a pandas-compatible strftime format.

    Args:
        spark_date_format (str): PySpark date format string.

    Returns:
        str: Pandas-compatible date format string.
    """
    replacements = {
        'yyyy': '%Y',
        'yy': '%y',
        'MM': '%m',
        'dd': '%d',
        'HH': '%H',
        'hh': '%I',
        'mm': '%M',
        'ss': '%S'
    }

    pandas_format = spark_date_format
    for spark_token, pandas_token in replacements.items():
        pandas_format = pandas_format.replace(spark_token, pandas_token)

    return pandas_format


def convert_pandas_date_format_to_spark_date_format(pandas_date_format: str) -> str:
    """
    Converts a pandas-compatible strftime date format to a PySpark date format.

    Args:
        pandas_date_format (str): Pandas strftime date format string.

    Returns:
        str: PySpark-compatible date format string.
    """
    replacements = {
        '%Y': 'yyyy',
        '%y': 'yy',
        '%m': 'MM',
        '%d': 'dd',
        '%H': 'HH',
        '%I': 'hh',
        '%M': 'mm',
        '%S': 'ss'
    }

    spark_format = pandas_date_format
    for pandas_token, spark_token in replacements.items():
        spark_format = spark_format.replace(pandas_token, spark_token)

    return spark_format






def get_random_percent_indexes(array, n):
    # Calculate the number of indexes to return (30% of the length of the array)
    num_indexes_to_return = int(len(array) * n)
    # Shuffle the indexes of the array
    shuffled_indexes = list(range(len(array)))
    random.shuffle(shuffled_indexes)
    # Return the first 30% of shuffled indexes
    return shuffled_indexes[:num_indexes_to_return], [0.5] * num_indexes_to_return


# Function to get fully qualified name of a class
def get_fully_qualified_name(cls):
    return f"{cls.__module__}.{cls.__name__}"


# Function to get class object from fully qualified name
def get_class_from_fully_qualified_name(name):
    parts = name.split('.')
    module_name = '.'.join(parts[:-1])
    class_name = parts[-1]
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls
