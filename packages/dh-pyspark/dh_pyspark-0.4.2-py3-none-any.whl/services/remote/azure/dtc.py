from dh_pyspark.services.remote.azure.base import RemoteAzureCoresetTreeService


class RemoteAzureCoresetTreeServiceDTC(RemoteAzureCoresetTreeService):
    """
    Azure-specific remote service for the DTC (Decision Tree Compression) variant.
    This class connects Synapse execution to the DTC service implementation.
    """
    service_class_name = "CoresetTreeServiceDTC"
    service_class_module_name = "dh_pyspark.services.coreset.dtc"
