import pandas as pd
from typing import Iterator
import pathlib

PREFIX = "main"
TARGET_PREFIX = "target"


def save_databricks_chunks(
    datasets: Iterator[pd.DataFrame] = None,
    target_datasets: Iterator[pd.DataFrame] = None,
    local_copy_dir: pathlib.Path = None,
):
    local_copy_dir.mkdir(parents=True, exist_ok=True)

    def append_save(iterator, prefix):
        for i, chunk in enumerate(iterator):
            chunk_path = local_copy_dir / f"{prefix}_chunk_{i:06d}.parquet"
            chunk.to_parquet(chunk_path, index=False)
            yield chunk

    datasets = append_save(datasets, PREFIX)
    if target_datasets is not None:
        target_datasets = append_save(target_datasets, TARGET_PREFIX)

    return datasets, target_datasets
