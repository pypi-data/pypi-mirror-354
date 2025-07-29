from pyspark.sql import SparkSession
from pyspark.ml.linalg import SparseVector, DenseVector, VectorUDT
import pyspark.sql.functions as f

def log_spark_job(spark: SparkSession, description: str):
    """
    Helper function to log and set Spark job descriptions with detailed information.
    """

    # Set the job description for the Spark UI
    spark.sparkContext.setJobDescription(description)

    # Log the message to the console
    print(f"--------------------------------------------------"
          f"\n{description}"
          f"\n--------------------------------------------------")


# Moved this udf to utils.py due to cython serialization issues
def process_combine_features(numeric_columns_len, category_lengths, sparse=True):
    def combine_features(numeric_values, categorical_values, category_lengths):
        num_len = len(numeric_values)
        indices = list(range(num_len))
        values = [float(x) for x in numeric_values]
        offset = num_len
        for cat_value, cat_length in zip(categorical_values, category_lengths):
            if 0 <= cat_value < cat_length:
                indices.append(offset + cat_value)
                values.append(1.0)
            offset += cat_length
        size = num_len + sum(category_lengths)
        vec = SparseVector(size, indices, values)
        if sparse:
            return vec
        else:
            return DenseVector(vec)

    return f.udf(
        lambda *cols: combine_features(
            numeric_values=cols[:numeric_columns_len],
            categorical_values=cols[numeric_columns_len:],
            category_lengths=category_lengths,
        ),
        VectorUDT(),
    )
