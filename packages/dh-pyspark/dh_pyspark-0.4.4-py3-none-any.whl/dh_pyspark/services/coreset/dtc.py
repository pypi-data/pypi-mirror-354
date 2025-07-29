from typing import Union

from dataheroes.core.coreset.coreset_dtc import CoresetDTC
from dataheroes.data.common import DataParams
from dataheroes.services.common import CoresetParamsDTC, CoresetParams, DataTuningParamsClassification
from pyspark.sql import SparkSession

from dh_pyspark.model.tree_model import SaveOrig
from dh_pyspark.services._coreset_service_base import CoresetTreeServiceBase


class CoresetTreeServiceDTC(CoresetTreeServiceBase):
    coreset_cls = CoresetDTC
    coreset_params_cls = CoresetParamsDTC
    data_tuning_params_cls = DataTuningParamsClassification

    def __init__(
            self,
            *,
            dhspark_path,
            data_params: Union[DataParams, dict] = None,
            data_tuning_params: Union[DataTuningParamsClassification, dict] = None,
            chunk_size: int = None,
            chunk_by=None,
            coreset_params: Union[CoresetParams, dict] = CoresetParamsDTC(),
            n_instances: int = None,
            n_instances_exact: bool = None,
            chunk_sample_ratio=None,
            save_orig: SaveOrig = SaveOrig.NONE,
            spark_session: SparkSession = None,
                 ):
        super().__init__(dhspark_path=dhspark_path, data_params=data_params, data_tuning_params=data_tuning_params,
                         chunk_size=chunk_size, chunk_by=chunk_by, spark_session=spark_session,
                         coreset_params=coreset_params, chunk_sample_ratio=chunk_sample_ratio,
                         n_instances=n_instances, n_instances_exact=n_instances_exact,
                         save_orig=save_orig)

    def _run_group_pandas_udf(self, df, sample_params, chunk_by_coreset_size_list, max_chunk, scm):
        def _create_coreset_udf(key, pdf):
            return self._udf_create_coreset(key=key, pdf=pdf,
                                            sample_params=sample_params,
                                            chunk_by_coreset_size_list=chunk_by_coreset_size_list,
                                            target_column=self.service_params.target_column,
                                            trace_mode=self.service_params.trace_mode,
                                            test_udf_log_path=self.service_params.dhspark_path,
            )
        return df.coalesce(max_chunk).groupby(f"chunk_index").applyInPandas(_create_coreset_udf, schema=scm)

