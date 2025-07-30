import os
import time

from google.cloud.dataproc_v1.types import Component
from google.cloud import dataproc_v1, storage
from google.oauth2 import service_account

from dh_pyspark.services.remote.base import RemoteCoresetTreeService


class RemoteGCPCoresetTreeService(RemoteCoresetTreeService):
    """
    GCP-specific implementation of the remote coreset tree service using Google Dataproc.
    """

    def __init__(self, *, dhspark_path, data_params=None, chunk_size=None, chunk_by=None, 
                 data_tuning_params=None, coreset_params=None, n_instances=None, n_instances_exact=None,
                 sample_all=None, chunk_sample_ratio=None, class_size=None, save_orig=None,
                 remote_service_config):
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
        # Create credentials from service account info
        credentials = self.get_config_value("credentials")
        if credentials is not None:
            self.credentials = service_account.Credentials.from_service_account_info(
                credentials,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        else:
            self.credentials = None

    def upload_text_to_cloud(self, destination_file_name, text):
        """
        Upload a script or text to Google Cloud Storage.

        Args:
            destination_file_name (str): Name of the file to upload.
            text (str): Content of the file.

        Returns:
            str: GCS path to the uploaded file.
        """
        client = storage.Client(
            project=self.get_config_value("project_id"),
            credentials=self.credentials
        )
        full_destination_path = "/".join([
            self.remote_service_config["main"]["destination_path"],
            self.workflow_id,
            destination_file_name
        ])
        bucket = client.bucket(full_destination_path.split('/')[0])
        path_without_bucket = "/".join(full_destination_path.split('/')[1:])
        blob = bucket.blob(path_without_bucket)
        blob.upload_from_string(text, content_type="text/plain")
        gcp_path = f"gs://{full_destination_path}"
        print(f"✅ Text uploaded to: {gcp_path}")
        return gcp_path

    def download_from_cloud(self, source_folder, local_dir):
        """
        Download all files from a GCS folder into a local directory.

        Args:
            source_folder (str): GCS path, like gs://bucket/path
            local_dir (str): Local path to download into.
        """
        storage_client = storage.Client(credentials=self.credentials)
        source_folder_clean = source_folder.replace('gs://', '')
        bucket_name = source_folder_clean.split('/')[0]
        prefix = "/".join(source_folder_clean.split('/')[1:])

        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
        for blob in blobs:
            if blob.name.endswith("/"):
                continue
            relative_path = blob.name[len(prefix):].lstrip("/")
            local_path = os.path.join(local_dir, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            blob.download_to_filename(local_path)
            print(f"✅ Downloaded: gs://{bucket_name}/{blob.name} → {local_path}")

    def get_gcp_workflow_template(self):
        """
        Generate a Dataproc workflow template from uploaded scripts.

        Returns:
            dict: Workflow template to submit.
        """
        scripts = self.upload_scripts()
        initial_script_path = scripts[0]["path"]
        previous_step = None
        jobs = []

        for workflow_step in scripts[1:]:
            step_name = workflow_step["name"]
            exec_name = workflow_step["path"]
            step_config = {
                "step_id": step_name,
                "pyspark_job": {
                    "main_python_file_uri": exec_name,
                    "file_uris": [initial_script_path],
                    "properties": workflow_step['spark_config']
                }
            }
            if previous_step:
                step_config["prerequisite_step_ids"] = [previous_step]
            jobs.append(step_config)
            previous_step = step_name

        # Cluster configuration
        cluster_config = self.remote_service_config['cluster_config']
        cluster_config['initialization_actions'] = [{
            "executable_file": initial_script_path
        }]
        cluster_config['gce_cluster_config'] = {
            "metadata": {"PIP_PACKAGES": self.get_config_value("python_libraries")},
            "internal_ip_only": False
        }
        cluster_config['software_config'] = {
            "optional_components": [Component.JUPYTER]
        }
        cluster_config['endpoint_config'] = {
            "enable_http_port_access": True
        }

        workflow_template = {
            "id": self.workflow_id,
            "placement": {
                "managed_cluster": {
                    "cluster_name": self.cluster_name,
                    "config": {**cluster_config}
                }
            },
            "jobs": jobs,
        }

        return workflow_template

    def get_cluster_web_interfaces(self):
        """
        Wait until the cluster is created and return available web UIs.

        Returns:
            list[dict]: UI names and URLs.
        """
        cluster_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{self.get_config_value('region')}-dataproc.googleapis.com:443"},
            credentials=self.credentials
        )
        start_time = time.time()
        timeout_sec = 900

        while time.time() - start_time < timeout_sec:
            if self.get_cluster_status() == 'RUNNING':
                clusters = cluster_client.list_clusters(
                    project_id=self.get_config_value('project_id'),
                    region=self.get_config_value('region'))

                for cluster in clusters.clusters:
                    if cluster.cluster_name.startswith(self.cluster_name):
                        print(f"Updating cluster name {cluster.cluster_name}")
                        self.cluster_name = cluster.cluster_name
                        cluster = cluster_client.get_cluster(
                            project_id=self.get_config_value('project_id'),
                            region=self.get_config_value('region'),
                            cluster_name=self.cluster_name
                        )

                        if cluster.config.endpoint_config.enable_http_port_access:
                            endpoints = cluster.config.endpoint_config.http_ports
                            return [{"name": name, "url": url} for name, url in endpoints.items()]
                        else:
                            return None

            print(f"🛰 Waiting for cluster: {self.cluster_name} {time.strftime('%H:%M:%S')}")
            time.sleep(10)

        raise RuntimeError("Failed to get a cluster")
    
    def upload_from_path(self, local_path: str):
        client = storage.Client(project=self.get_config_value("project_id"), credentials=self.credentials)
        base_file_name = os.path.basename(local_path)

        path_parts = [
            self.remote_service_config["main"]["destination_path"],
            self.workflow_id
        ]
        if os.path.isdir(local_path):
            path_parts += [base_file_name]

        full_destination_path = "/".join(path_parts)
        bucket_name = full_destination_path.split('/')[0]
        bucket = client.bucket(bucket_name)

        def upload_file(file_path, blob_path):
            blob_path = blob_path.replace(bucket_name+"/", "")
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(file_path)
            print(f"✅ Uploaded: {file_path} → gs://{bucket_name}/{blob_path}")

        if os.path.isfile(local_path):
            filename = os.path.basename(local_path)
            target_blob = os.path.join(full_destination_path, filename)
            upload_file(local_path, target_blob)
        elif os.path.isdir(local_path):
            for root, _, files in os.walk(local_path):
                for name in files:
                    file_path = os.path.join(root, name)
                    rel_path = os.path.relpath(file_path, local_path)
                    blob_path = os.path.join(full_destination_path, rel_path)
                    upload_file(file_path, blob_path)
        else:
            raise FileNotFoundError(f"Path does not exist: {local_path}")


    def execute(self, wait_for_cluster: bool = True):
        """
        Launch the remote job workflow. Must be implemented in subclasses.
        Parameters:
            wait_for_cluster: define if return control immediately, or wait for the start iof the cluster.
            If passed True, the method return a list of web-services for cluster control and print these web-links
            in the output
        """
        workflow_template = self.get_gcp_workflow_template()
        request = dataproc_v1.CreateWorkflowTemplateRequest(
            parent=f"projects/{self.get_config_value('project_id')}/regions/{self.get_config_value('region')}",
            template=workflow_template,
        )

        client_options = {"api_endpoint": f"{self.get_config_value('region')}-dataproc.googleapis.com:443"}
        workflow_template_client = dataproc_v1.WorkflowTemplateServiceClient(
            client_options=client_options,
            credentials=self.credentials
        )
        workflow_template_client.create_workflow_template(request=request)

        print(f"Workflow template created: {self.workflow_id}")

        request = dataproc_v1.InstantiateWorkflowTemplateRequest(
            name=f"projects/{self.get_config_value('project_id')}/regions/"
                 f"{self.get_config_value('region')}/workflowTemplates/{self.workflow_id}"
        )
        workflow_template_client.instantiate_workflow_template(request=request)
        if wait_for_cluster:
            return self.print_cluster_web_interfaces()
        return []

    def get_cluster_status(self):
        """
        Return the current status of the cluster.

        Returns:
            str or None: Status name or None if cluster not found.
        """
        cluster_client = dataproc_v1.ClusterControllerClient(
            client_options={"api_endpoint": f"{self.get_config_value('region')}-dataproc.googleapis.com:443"},
            credentials=self.credentials
        )
        clusters = cluster_client.list_clusters(
            project_id=self.get_config_value('project_id'),
            region=self.get_config_value('region'))

        for cluster in clusters.clusters:
            if cluster.cluster_name.startswith(self.cluster_name):
                return cluster.status.state.name

        return None

    def get_cluster_finished(self):
        """
        Check if the cluster is in a terminal state.

        Returns:
            bool: True if cluster finished, False otherwise.
        """
        status = self.get_cluster_status()
        return status in ['DELETING', 'ERROR', 'STOPPED']