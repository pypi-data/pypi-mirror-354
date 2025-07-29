import os
import re
import time
from typing import Union

from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from azure.synapse.spark import SparkClient
from azure.synapse.spark.models import SparkBatchJobOptions

from dataheroes import CoresetParams, CoresetParamsDTC, DataParams
from dh_pyspark.model.tree_model import SaveOrig
from dh_pyspark.services.remote.base import RemoteCoresetTreeService


class RemoteAzureCoresetTreeService(RemoteCoresetTreeService):
    """
    Azure Synapse-specific implementation of the remote coreset service.
    Handles Spark job submission and script management using Azure SDKs.
    """

    def __init__(self, *, dhspark_path, data_params: Union[DataParams, dict] = None,
                 chunk_size: int = None, chunk_by=None, data_tuning_params=None,
                 coreset_params: Union[CoresetParams, dict] = CoresetParamsDTC(),
                 n_instances: int = None, n_instances_exact: bool = None,
                 sample_all=None, chunk_sample_ratio=None, class_size=None,
                 save_orig: SaveOrig = SaveOrig.NONE,
                 remote_service_config):
        """
        Initialize the remote Azure service with given Spark job configuration.
        """
        super().__init__(
            dhspark_path=dhspark_path,
            data_params=data_params,
            chunk_size=chunk_size,
            chunk_by=chunk_by,
            data_tuning_params=data_tuning_params,
            coreset_params=coreset_params,
            n_instances=n_instances,
            n_instances_exact=n_instances_exact,
            sample_all=sample_all,
            chunk_sample_ratio=chunk_sample_ratio,
            class_size=class_size,
            save_orig=save_orig,
            remote_service_config=remote_service_config
        )
        self.container_name = self.cluster_name

    def upload_from_path(self, local_path: str):
        # Initialize the BlobServiceClient with DefaultAzureCredential
        account_url = f"https://{self.remote_service_config['main']['storage_account_name']}.blob.core.windows.net"
        blob_service_client = BlobServiceClient(
            account_url=account_url,
            credential=self.get_config_value("storage_account_key"))

        # Construct the full destination path
        base_file_name = os.path.basename(local_path)
        path_parts = [
            self.remote_service_config["main"]["destination_path"],
            self.workflow_id
        ]
        if os.path.isdir(local_path):
            path_parts.append(base_file_name)
        full_destination_path = "/".join(path_parts)

        # self.remote_service_config["main"]["container"]
        container_client = blob_service_client.get_container_client(self.container_name)
        if not container_client.exists():
            container_client.create_container()
            print(f"✅ Container '{self.container_name}' created.")

        def upload_file(file_path, blob_path):
            blob_client = container_client.get_blob_client(blob=blob_path)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"✅ Uploaded: {file_path} → azure://{self.container_name}/{blob_path}")

        if os.path.isfile(local_path):
            filename = os.path.basename(local_path)
            blob_path = f"{full_destination_path}/{filename}"
            upload_file(local_path, blob_path)
        elif os.path.isdir(local_path):
            for root, _, files in os.walk(local_path):
                for name in files:
                    file_path = os.path.join(root, name)
                    rel_path = os.path.relpath(file_path, local_path)
                    blob_path = f"{full_destination_path}/{rel_path.replace(os.sep, '/')}"
                    upload_file(file_path, blob_path)
        else:
            raise FileNotFoundError(f"Path does not exist: {local_path}")


    def upload_text_to_cloud(self, destination_file_name, text):
        """
        Upload text content as a blob to Azure Blob Storage.

        Returns:
            str: Path inside the container.
        """
        blob_service_client = BlobServiceClient(
            account_url=f"https://{self.get_config_value('storage_account_name')}.blob.core.windows.net",
            credential=self.get_config_value("storage_account_key")
        )
        destination_path = self.get_config_value("destination_path")
        container_client = blob_service_client.get_container_client(self.container_name)

        if not container_client.exists():
            container_client.create_container()
            print(f"✅ Container '{self.container_name}' created.")

        path_in_container = "/".join([destination_path, destination_file_name])
        blob_client = blob_service_client.get_blob_client(
            container=self.container_name,
            blob=path_in_container
        )
        blob_client.upload_blob(text, overwrite=True)
        print(f"✅ Uploaded: {path_in_container}")
        return path_in_container

    def download_from_cloud(self, source_folder, local_dir):
        """
        Download blobs from an abfss:// path in Azure Data Lake Storage.

        Args:
            source_folder (str): abfss://... path
            local_dir (str): Path to save locally
        """
        if source_folder.startswith("abfss://"):
            match = re.match(r"abfss://(.+?)@(.+?)\.dfs\.core\.windows\.net/(.*)", source_folder)
            if not match:
                raise ValueError(f"Invalid abfss path: {source_folder}")
            container_name, account_name, prefix = match.groups()
        else:
            raise ValueError("Only abfss:// paths are supported here")

        account_url = f"https://{account_name}.blob.core.windows.net"
        blob_service_client = BlobServiceClient(
            account_url=account_url,
            credential=self.get_config_value("storage_account_key"))
        container_client = blob_service_client.get_container_client(container_name)

        blobs = container_client.list_blobs(name_starts_with=prefix)

        for blob in blobs:
            if blob.name.endswith("/"):
                continue
            if blob.size == 0 and not os.path.splitext(blob.name)[1]:
                continue
            if not prefix.endswith("/"):
                prefix += "/"
            relative_path = blob.name[len(prefix):]
            local_path = os.path.join(local_dir, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as file:
                file.write(container_client.download_blob(blob.name).readall())
            print(f"✅ Downloaded: abfss://{container_name}@{account_name}.dfs.core.windows.net/{blob.name} → {local_path}")

    def upload_main_script(self, job_scripts):
        """
        Generates the main `run.py` script that installs dependencies and runs Spark jobs.
        Uploads it to cloud storage and returns its path.
        """
        pip_packages = f" fsspec adlfs {self.get_config_value('python_libraries')}"
        text = f"""
import subprocess
import sys
import os
from pyspark.sql import SparkSession
from azure.storage.blob import BlobServiceClient

print("🚀 Starting libs_to_workers.py")
spark = SparkSession.builder.getOrCreate()

account_name = "{self.get_config_value('storage_account_name')}"
container = "{self.container_name}"
storage_key = "{self.get_config_value('storage_account_key')}"
workflow_id = "{self.workflow_id}"
remote_wheel_dir = f"run-folder/{{workflow_id}}/wheelhouse-x86-pypi"

# Install base pip packages on driver
subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=False)
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([sys.executable, "-m", "pip", "install"] + "{pip_packages}".split(), check=True)

print('before # Azure setup') 
# Azure setup
blob_service_client = BlobServiceClient(
    account_url=f"https://{{account_name}}.blob.core.windows.net",
    credential=storage_key
)
container_client = blob_service_client.get_container_client(container)
print(f' got container_client {{container}}')
# Get list of wheel files

wheel_files = []
if os.getenv("CIRCLECI"):
    blobs = container_client.list_blobs(name_starts_with=remote_wheel_dir)
    print(f'{{remote_wheel_dir=}}')
    for blob in blobs:
        print(f'{{blob=}}')
        if blob.name.endswith(".whl"):
            wheel_files.append(blob.name)
    print(f'{{wheel_files=}}')
    # Download & install wheels on driver
    for file_path in wheel_files:
        print(f"📥 Downloading wheel: {{file_path}}")
        blob_client = container_client.get_blob_client(blob=file_path)
        local_name = os.path.basename(file_path)
        with open(local_name, "wb") as f:
            f.write(blob_client.download_blob().readall())
        print(f"📦 Installing wheel on driver: {{local_name}}")
        subprocess.run([sys.executable, "-m", "pip", "install", local_name], check=True)

# Broadcast wheel list to workers
# wheel_df = spark.createDataFrame([(w,) for w in wheel_files], ["wheel_path"])
# def install_on_worker(wheel_path):
#     import subprocess, sys, os
#     from azure.storage.blob import BlobServiceClient
#     account_name = "{self.get_config_value('storage_account_name')}"
#     container = "{self.container_name}"
#     storage_key = "{self.get_config_value('storage_account_key')}"
#     filename = os.path.basename(wheel_path)
#     local_path = f"/tmp/{{filename}}"
#     print(f"📥 Worker downloading wheel: {{wheel_path}}")
#     blob_service_client = BlobServiceClient(
#         account_url=f"https://{{account_name}}.blob.core.windows.net",
#         credential=storage_key
#     )
#     container_client = blob_service_client.get_container_client(container)
#     blob_client = container_client.get_blob_client(blob=wheel_path)
#     subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=False)
#     subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
#     subprocess.run([sys.executable, "-m", "pip", "install"] + "{pip_packages}".split(), check=True)
#     with open(local_path, "wb") as f:
#         f.write(blob_client.download_blob().readall())
#     print(f"📦 Worker installing: {{local_path}}")
#     subprocess.run([sys.executable, "-m", "pip", "install", local_path], check=True)
#     return f"✅ Installed on worker: {{filename}}"
# 
# results = wheel_df.rdd.map(lambda row: install_on_worker(row.wheel_path)).collect()
# Create one partition per executor to ensure all run the task
num_executors = spark.sparkContext.defaultParallelism
rdd = spark.sparkContext.parallelize(range(num_executors), num_executors)

def install_all_wheels(_):
    import subprocess, sys, os
    from azure.storage.blob import BlobServiceClient

    account_name = "{self.get_config_value('storage_account_name')}"
    container = "{self.container_name}"
    storage_key = "{self.get_config_value('storage_account_key')}"
    pip_packages = "{pip_packages}"
    wheel_files =wheel_files # send the full list of wheels to each worker
    def safe(cmd):
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed: {{cmd}} — {{e}}")

    # Install base pip packages
    print("📦 Installing base pip packages on worker")
    safe([sys.executable, "-m", "ensurepip", "--upgrade"])
    safe([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    safe([sys.executable, "-m", "pip", "install"] + pip_packages.split())

    # Connect to Azure Blob Storage
    blob_service_client = BlobServiceClient(
        account_url=f"https://{{account_name}}.blob.core.windows.net",
        credential=storage_key
    )
    container_client = blob_service_client.get_container_client(container)

    # Download and install all wheel files
    for wheel_path in wheel_files:
        filename = os.path.basename(wheel_path)
        local_path = f"/tmp/{{filename}}"
        print(f"📥 Worker downloading: {{wheel_path}}")
        blob_client = container_client.get_blob_client(blob=wheel_path)
        with open(local_path, "wb") as f:
            f.write(blob_client.download_blob().readall())

        print(f"📦 Worker installing: {{local_path}}")
        safe([sys.executable, "-m", "pip", "install", local_path])

    return f"✅ Installed {{wheel_files}} wheels and base packages"

# Trigger the install job on all workers
results = rdd.map(install_all_wheels).collect()
for r in results:
    print(r)

# Add barrier to ensure all workers have completed installation
spark.sparkContext.parallelize(range(spark.sparkContext.defaultParallelism), spark.sparkContext.defaultParallelism).barrier().mapPartitions(lambda _: [1]).count()
print("✅ All workers confirmed package installation")

scripts = {str(job_scripts)}
for workflow_step in scripts:
    remote_path = workflow_step['path']
    local_path = workflow_step['name'] + '.py'
    print(f"📥 Downloading {{remote_path}}")
    blob_client = container_client.get_blob_client(blob=remote_path)
    with open(local_path, "wb") as f:
        f.write(blob_client.download_blob().readall())

    print(f"🚀 Running {{local_path}}")
    # Add both blob and ADLS Gen2 configurations
    subprocess.run([
        "spark-submit",
        "--master", "yarn",
        "--deploy-mode", "client",
        # Blob storage config
        "--conf", f"spark.hadoop.fs.azure.account.key.{{account_name}}.blob.core.windows.net={{storage_key}}",
        "--conf", f"spark.hadoop.fs.azure.account.auth.type.{{account_name}}.blob.core.windows.net=SharedKey",
        # ADLS Gen2 config
        "--conf", f"spark.hadoop.fs.azure.account.key.{{account_name}}.dfs.core.windows.net={{storage_key}}",
        "--conf", f"spark.hadoop.fs.azure.account.auth.type.{{account_name}}.dfs.core.windows.net=SharedKey",
        "--conf", "spark.hadoop.fs.azure.createRemoteFileSystemDuringInitialization=true",
        "--conf", "spark.hadoop.fs.AbstractFileSystem.abfss.impl=org.apache.hadoop.fs.azurebfs.Abfs",
        "--conf", "spark.hadoop.fs.abfss.impl=org.apache.hadoop.fs.azurebfs.AzureBlobFileSystem",
        local_path
    ], check=True)
"""
        return self.upload_text_to_cloud("run.py", text)

    def get_spark_client(self):
        """
        Initialize and return the Azure Synapse Spark client.
        """
        credential = ClientSecretCredential(
            tenant_id=self.get_config_value('tenant_id'),
            client_id=self.get_config_value('client_id'),
            client_secret=self.get_config_value('client_secret')
        )
        return SparkClient(
            endpoint=f"https://{self.get_config_value('synapse_workspace')}.dev.azuresynapse.net",
            credential=credential,
            spark_pool_name=self.get_config_value("spark_pool_name")
        )

    def execute(self, wait_for_cluster: bool = True):
        """
        Launch the remote job workflow. Must be implemented in subclasses.
        Parameters:
            wait_for_cluster: define if return control immediately, or wait for the start iof the cluster.
            If passed True, the method return a list of web-services for cluster control and print these web-links
            in the output
        """
        print("🚀 Preparing Spark job for Azure Synapse...")
        scripts = self.upload_scripts()
        main_script_path = self.upload_main_script(scripts[1:])

        storage_account = self.get_config_value('storage_account_name')
        storage_key = self.get_config_value('storage_account_key')

        spark_file_path = (
            f"abfss://{self.container_name}@{storage_account}."
            f"dfs.core.windows.net/{main_script_path}"
        )

        # Configure Spark job with ADLS Gen2 authentication
        spark_config = {
            # For blob storage access
            f"spark.hadoop.fs.azure.account.key.{storage_account}.blob.core.windows.net": storage_key,
            # For ADLS Gen2 access
            f"spark.hadoop.fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net": "SharedKey",
            f"spark.hadoop.fs.azure.account.key.{storage_account}.dfs.core.windows.net": storage_key,
            # Enable ABFS driver
            "spark.hadoop.fs.AbstractFileSystem.abfss.impl": "org.apache.hadoop.fs.azurebfs.Abfs",
            "spark.hadoop.fs.abfss.impl": "org.apache.hadoop.fs.azurebfs.AzureBlobFileSystem",
        }

        job = SparkBatchJobOptions(
            name="dh-spark-job",
            file=spark_file_path,
            class_name="org.apache.spark.deploy.PythonRunner",
            configuration=spark_config,
            driver_memory=self.remote_service_config['cluster_config'].get("driver_memory"),
            driver_cores=self.remote_service_config['cluster_config'].get("driver_cores"),
            executor_memory=self.remote_service_config['cluster_config'].get("executor_memory"),
            executor_cores=self.remote_service_config['cluster_config'].get("executor_cores"),
            executor_count=self.remote_service_config['cluster_config'].get("executor_count"),
        )

        job_response = self.get_spark_client().spark_batch.create_spark_batch_job(spark_batch_job_options=job)
        print("✅ Spark job submitted.")
        self.cluster_params['job_id'] = job_response.id
        print("🧾 Job ID:", self.cluster_params['job_id'])
        if wait_for_cluster:
            return self.print_cluster_web_interfaces()
        return []

    def get_cluster_web_interfaces(self):
        """
        Wait for the job to start and return URLs to Synapse Monitoring and Spark UI.
        """
        timeout_sec = 900
        spark_client = self.get_spark_client()
        start_time = time.time()

        while time.time() - start_time < timeout_sec:
            job = spark_client.spark_batch.get_spark_batch_job(self.cluster_params.get('job_id'))
            state = job.state
            print(f"⏳ Job state: {state}")
            if state == 'running':
                return [
                    {
                        "name": "Synapse Analytics Job page",
                        "url": f"https://web.azuresynapse.net/en/monitoring/sparkapplication/dh-spark-job?"
                               f"workspace=%2Fsubscriptions%2F{self.get_config_value('subscription_id')}"
                               f"%2FresourceGroups%2F{self.get_config_value('resource_group')}"
                               f"%2Fproviders%2FMicrosoft.Synapse%2Fworkspaces%2F{self.get_config_value('synapse_workspace')}"
                               f"&sparkPoolName={self.get_config_value('spark_pool_name')}"
                               f"&livyId={self.cluster_params.get('job_id')}"
                    },
                    {"name": "Spark UI", "url": job.app_info['sparkUiUrl']},
                    {"name": "Driver Log", "url": job.app_info['driverLogUrl']},
                ]
            time.sleep(10)

        raise TimeoutError(f"Job {self.cluster_params.get('job_id')} was not ready in {timeout_sec} seconds")


    def get_cluster_status(self):
        """
        Return the current status of the Azure Synapse job.
        """
        spark_client = self.get_spark_client()
        job = spark_client.spark_batch.get_spark_batch_job(self.cluster_params.get('job_id'))
        return job.state

    def get_cluster_finished(self):
        """
        Check if the job is in a terminal state.

        Returns:
            bool: True if finished, False otherwise.
        """
        status = self.get_cluster_status()
        return status in ['success', 'error', 'dead', 'killed']