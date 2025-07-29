from dh_pyspark.services.remote.aws.base import RemoteAWSCoresetTreeService


class RemoteAWSCoresetTreeServiceDTC(RemoteAWSCoresetTreeService):
    """
    AWS-specific remote service for the DTC (Decision Tree Compression) variant.
    This class links the job runner to the specific service class implementation.
    """
    service_class_name = "CoresetTreeServiceDTC"
    service_class_module_name = "dh_pyspark.services.coreset.dtc"
