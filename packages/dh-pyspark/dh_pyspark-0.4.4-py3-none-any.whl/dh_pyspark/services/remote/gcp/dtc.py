from dh_pyspark.services.remote.gcp.base import RemoteGCPCoresetTreeService


class RemoteGCPCoresetTreeServiceDTC(RemoteGCPCoresetTreeService):
    """
    GCP-specific remote service for the DTC (Decision Tree Compression) variant.
    This class connects the GCP job runner to the DTC coreset service.
    """
    service_class_name = "CoresetTreeServiceDTC"
    service_class_module_name = "dh_pyspark.services.coreset.dtc"
