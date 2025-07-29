import os
import time

import boto3

from dh_pyspark.services.remote.base import RemoteCoresetTreeService


class RemoteAWSCoresetTreeService(RemoteCoresetTreeService):
    """
    AWS implementation of the RemoteCoresetTreeService.
    Uses Amazon EMR and S3 for remote Spark job execution and storage.
    """

    def _get_aws_client(self, service_name):
        """
        Create a boto3 client with credentials from config.
        """
        aws_config = {
            "region_name": self.get_config_value("region")
        }
        
        # Add credentials if provided in config
        if self.get_config_value("aws_access_key_id") and self.get_config_value("aws_secret_access_key"):
            aws_config.update({
                "aws_access_key_id": self.get_config_value("aws_access_key_id"),
                "aws_secret_access_key": self.get_config_value("aws_secret_access_key")
            })
        
        return boto3.client(service_name, **aws_config)

    def upload_from_path(self, local_path: str):
        """
        Upload a local file or directory to S3.
        
        Args:
            local_path (str): Path to local file or directory to upload
            
        Returns:
            str: S3 path where the content was uploaded
        """
        s3_client = self._get_aws_client('s3')
        base_file_name = os.path.basename(local_path)
        
        # Construct the destination path
        path_parts = [
            self.remote_service_config["main"]["destination_path"],
            self.workflow_id
        ]
        if os.path.isdir(local_path):
            path_parts.append(base_file_name)
            
        full_destination_path = "/".join(path_parts)
        bucket_name = full_destination_path.split('/')[0]
        
        def upload_file(file_path, s3_path):
            s3_path = s3_path.replace(bucket_name + "/", "")
            s3_client.upload_file(file_path, bucket_name, s3_path)
            print(f"✅ Uploaded: {file_path} → s3://{bucket_name}/{s3_path}")
            
        if os.path.isfile(local_path):
            filename = os.path.basename(local_path)
            target_s3_path = os.path.join(full_destination_path, filename)
            upload_file(local_path, target_s3_path)
        elif os.path.isdir(local_path):
            for root, _, files in os.walk(local_path):
                for name in files:
                    file_path = os.path.join(root, name)
                    rel_path = os.path.relpath(file_path, local_path)
                    s3_path = os.path.join(full_destination_path, rel_path)
                    upload_file(file_path, s3_path)
        else:
            raise FileNotFoundError(f"Path does not exist: {local_path}")
            
        return f"s3://{full_destination_path}"

    def upload_text_to_cloud(self, destination_file_name, text):
        """
        Upload a text file (e.g. Python script) to S3 bucket specified in the config.

        Args:
            destination_file_name (str): Filename to upload.
            text (str): File content.

        Returns:
            str: Full S3 path to the uploaded file.
        """
        s3_client = self._get_aws_client("s3")

        # Construct full path: bucket_name/workflow_id/filename
        full_destination_path = "/".join([
            self.remote_service_config["main"]["destination_path"],
            self.workflow_id,
            destination_file_name
        ])
        bucket_name = full_destination_path.split('/')[0]
        path_without_bucket = "/".join(full_destination_path.split('/')[1:])

        # Upload to S3
        s3_client.put_object(Bucket=bucket_name, Key=path_without_bucket, Body=text)
        s3_path = f"s3://{full_destination_path}"
        print(f"✅ Text uploaded to: {s3_path}")
        return s3_path

    def download_from_cloud(self, source_folder, local_dir):
        """
        Download all files from a given S3 folder to a local directory.

        Args:
            source_folder (str): S3 folder (e.g. "s3://my-bucket/path/")
            local_dir (str): Local destination directory
        """
        from smart_open import open as s3_open
        s3 = self._get_aws_client("s3")

        paginator = s3.get_paginator("list_objects_v2")

        # Clean S3 path into bucket + key prefix
        source_folder_clean = source_folder.replace('s3://', '')
        bucket_name = source_folder_clean.split('/')[0]
        path_without_bucket = "/".join(source_folder_clean.split('/')[1:])

        pages = paginator.paginate(Bucket=bucket_name, Prefix=path_without_bucket)

        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]
                relative_path = key[len(path_without_bucket):].lstrip("/")
                local_path = os.path.join(local_dir, relative_path)

                # Ensure folder exists
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                # Download file
                s3_uri = f"s3://{bucket_name}/{key}"
                with s3_open(s3_uri, "rb") as src, open(local_path, "wb") as dst:
                    dst.write(src.read())

                print(f"✅ Downloaded: {s3_uri} → {local_path}")

    def execute(self, wait_for_cluster: bool = True):
        """
        Launch the remote job workflow. Must be implemented in subclasses.
        Parameters:
            wait_for_cluster: define if return control immediately, or wait for the start iof the cluster.
            If passed True, the method return a list of web-services for cluster control and print these web-links
            in the output
        """
        emr_client = self._get_aws_client("emr")

        # Upload scripts to S3
        scripts = self.upload_scripts()
        bootstrap_path = scripts[0]["path"]
        job_steps = []

        # Convert each job into EMR step
        for workflow_step in scripts[1:]:
            step_name = workflow_step["name"]
            exec_name = workflow_step["path"]
            job_args = ["spark-submit"]

            # Add --conf for each Spark config
            for conf_item in [f"{c}={workflow_step['spark_config'][c]}" for c in workflow_step['spark_config']]:
                job_args.append("--conf")
                job_args.append(conf_item)
            job_args.append(exec_name)

            job_steps.append({
                "Name": step_name,
                "ActionOnFailure": "TERMINATE_CLUSTER",
                "HadoopJarStep": {
                    "Jar": "command-runner.jar",
                    "Args": job_args,
                },
            })

        # Submit EMR cluster + steps
        cluster_response = emr_client.run_job_flow(
            Name=self.cluster_name,
            LogUri=f"s3://{self.get_config_value('destination_path')}/logs/",
            ReleaseLabel=self.get_config_value('emr_release_label'),
            Applications=[{"Name": "Spark"}],
            Instances={
                **self.remote_service_config['cluster_config'],
                "KeepJobFlowAliveWhenNoSteps": False,
                "TerminationProtected": False,
            },
            BootstrapActions=[
                {
                    "Name": "Bootstrap Script",
                    "ScriptBootstrapAction": {
                        "Path": bootstrap_path,
                        "Args": []
                    },
                }
            ],
            Steps=job_steps,
            VisibleToAllUsers=True,
            JobFlowRole="EMR_EC2_DefaultRole",
            ServiceRole="EMR_DefaultRole",
        )

        # Store cluster ID
        self.cluster_params['cluster_id'] = cluster_response["JobFlowId"]
        print(f"✅ EMR Cluster Created: {self.cluster_params['cluster_id']}")
        if wait_for_cluster:
            return self.print_cluster_web_interfaces()
        return []

    def get_cluster_web_interfaces(self):
        """
        Return list of web interfaces (EMR console + Spark History Server).
        """
        timeout_sec = 900
        start_time = time.time()

        while time.time() - start_time < timeout_sec:
            if self.get_cluster_status() in ['RUNNING', 'WAITING']:
                return [
                    {
                        "name": "EMR Console UI",
                        "url": f"https://console.aws.amazon.com/elasticmapreduce"
                               f"/home?region={self.get_config_value('region')}#cluster-details:{self.cluster_params['cluster_id']}"
                    },
                    {
                        "name": "Spark History Server",
                        "url": f"https://{self.cluster_params['cluster_id']}.emrappui-prod.{self.get_config_value('region')}.amazonaws.com/shs/"
                    }
                ]
            time.sleep(10)

        raise TimeoutError(f"Job {self.cluster_params.get('job_id')} was not ready in {timeout_sec} seconds")

    def get_cluster_status(self):
        """
        Return current status of the EMR cluster.
        """
        emr_client = self._get_aws_client("emr")
        response = emr_client.describe_cluster(ClusterId=self.cluster_params['cluster_id'])
        state = response["Cluster"]["Status"]["State"]
        return state

    def get_cluster_finished(self):
        """
        Check if the EMR cluster has reached a finished state.
        """
        status = self.get_cluster_status()
        return status in ['TERMINATED', 'TERMINATED_WITH_ERRORS', 'WAITING']