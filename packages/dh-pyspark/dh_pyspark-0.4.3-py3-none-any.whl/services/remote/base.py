import inspect
from pprint import pformat
import textwrap
import warnings
import time
from typing import Union

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from dataheroes.services.common import CoresetParamsDTC, CoresetParams, PreprocessingStage
from dh_pyspark.model.tree_model import SaveOrig
from dh_pyspark.services._coreset_service_base import CoresetTreeServiceBase, OutputFormat


def get_id():
    """
    Generate a simple timestamp-based ID.
    """
    return round(time.time())


class RemoteCoresetTreeService(CoresetTreeServiceBase):
    """
    Base class for running CoresetTreeService jobs on remote Spark clusters.
    Must be subclassed for specific cloud providers (e.g. AWS, Azure, GCP).

    We support two options for build spark configurations -
    1) List for different level range, when we run few builds with different stop_level and configurations
    "build": [
            {"stop_level": 4,
             "config": {'spark.executor.memory': '15g', ...}
            },
            {"stop_level": 6,
             "config": {'spark.executor.memory': '10g', ...}
            },
            {"stop_level": None,
             "config": {'spark.executor.memory': '5g', ...}
            },
        ]
    2)  Plain build configurations - single configuration and only one build step
    "build": {
            'spark.executor.memory': '5g',
        }
    """
    service_class_name = "Show be defined in terminal class"
    service_class_module_name = "Show be defined in terminal class"

    def get_wrapped_code(self, text):
        """
        Wrap job code into a standalone executable Python script
        with SparkSession setup and service initialization.
        """
        text = textwrap.indent(textwrap.dedent(text), "    ")
        if self.get_config_value('license_account') is not None:
            activate_account_str = f"""activate_account("{self.get_config_value('license_account')}")"""
        else:
            activate_account_str = ""

        job_text = textwrap.dedent(f"""
import sys
import os

os.environ["OTEL_PYTHON_DISABLED"] = "true"

# Defensive patch: filter out broken entries in sys.path
sys.path = [p for p in sys.path if p and os.path.exists(p)]
sys.path.append(os.getenv("HOME"))      
sys.path.append(os.getcwd())  
from pyspark.sql import SparkSession
import dataheroes.utils
import dataheroes.core.tree.tree
import dataheroes.services.coreset_tree._base
import dataheroes.services.coreset_tree._mixin
import dataheroes.services.coreset._base
import dataheroes.data.manager
                                   
def dummy_function(feature_name, key=None):
    pass
dataheroes.utils.check_feature_for_license = dummy_function
dataheroes.core.tree.tree.check_feature_for_license = dummy_function
dataheroes.services.coreset_tree._base.check_feature_for_license = dummy_function
dataheroes.services.coreset._base.check_feature_for_license = dummy_function
dataheroes.services.coreset_tree._mixin.check_feature_for_license = dummy_function
dataheroes.services.coreset_tree.analytics.check_feature_for_license = dummy_function
dataheroes.data.manager.check_feature_for_license = dummy_function

print("================" + "Current working directory:")
for item in os.listdir('.'):
    print(item)

from {self.service_class_module_name} import {self.service_class_name}
from dh_pyspark.services._coreset_service_base import DataParams
spark = SparkSession.builder.appName("build_from_file").getOrCreate()


if __name__ == "__main__":
{text}""")
        return job_text

    def __init__(self, *, dhspark_path, data_params = None,
                 chunk_size: int = None, chunk_by=None,
                 coreset_params: Union[CoresetParams, dict] = CoresetParamsDTC(),
                 data_tuning_params = None,
                 n_instances: int = None, n_instances_exact: bool = None,
                 sample_all=None, chunk_sample_ratio=None, class_size=None,
                 save_orig: SaveOrig = SaveOrig.NONE,
                 remote_service_config):
        """
        Initialize the remote service with configuration and training parameters.
        Saves passed arguments in `init_params` for job construction.
        """
        self.remote_service_config = remote_service_config
        self.remote_jobs = []
        self.workflow_id = f"wf-{get_id()}"

        # Save only explicitly passed parameters
        all_params = locals()
        signature = inspect.signature(self.__init__)
        default_values = {k: v.default for k, v in signature.parameters.items() if v.default is not inspect.Parameter.empty}

        explicitly_passed = {
            k: v for k, v in all_params.items()
            if k not in default_values or (v != default_values[k] and not (v is None and default_values[k] is None))
        }
        del explicitly_passed["self"]
        del explicitly_passed["remote_service_config"]

        self.init_params = explicitly_passed
        self.cluster_name = f"cluster-id-{get_id()}"
        self.cluster_params = {}

    def get_job_spark_config(self, job_name):
        """
        Return Spark config dict for a specific job name, combining default and job-specific values.
        """
        spark_config = self.remote_service_config.get('spark_config') or {}
        default_config = spark_config.get('default') or {}
        job_config = spark_config.get(job_name) or {}
        if isinstance(job_config, list):
            return job_config
        else:
            default_config.update(job_config)
            return default_config

    def upload_from_path(self, local_path: str):
        """
        Upload folder or file to cloud storage. Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def upload_text_to_cloud(self, destination_file_name, text):
        """
        Upload script text to cloud storage. Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_pip_install_text(self):
        """
        Return Bash script to install Python dependencies on the cluster.
        """
        full_destination_path = "/".join([
            self.remote_service_config["main"]["destination_path"],
            self.workflow_id,
        ])
        if self.get_config_value("bootstrap_text") is not None:
            text  = f"""#!/bin/bash
DESTINATION_PATH="{full_destination_path}"           
{self.get_config_value("bootstrap_text")}"""
        else:
            pip_packages = f" dataheroes dh_pyspark {self.get_config_value('python_libraries')}"
            text =  f"""#!/bin/bash\nsudo python3 -m pip install {pip_packages}"""
            text +=  f"\nsudo python3 -m pip install --force-reinstall --no-cache-dir numpy==1.24.4"
            text +=  f"\nsudo python3 -m pip install --only-binary=:all: tables==3.8.0"""
        return text

    def upload_scripts(self):
        """
        Upload all job scripts and bootstrap script to cloud storage.
        Returns list of remote job definitions.
        """
        if self.get_config_value("upload") is not None:
            for upload_item in self.get_config_value("upload"):
                self.upload_from_path(upload_item)
        scripts = []

        # Upload bootstrap script
        initial_script_path = self.upload_text_to_cloud(
            destination_file_name="bootstrap.sh",
            text=self.get_pip_install_text()
        )
        scripts.append({"step": "bootstrap", "path": initial_script_path})

        # Upload each Spark job
        for index, workflow_step in enumerate(self.remote_jobs):
            step_name = f"step_{index}_{workflow_step.get('job_name')}"
            exec_name = self.upload_text_to_cloud(
                destination_file_name=f"{step_name}.py",
                text=workflow_step.get('job_text')
            )
            scripts.append({
                "name": step_name,
                "path": exec_name,
                "spark_config": workflow_step['spark_config']
            })

        return scripts

    def build_from_file(self, input_path: str, input_format: str = "parquet", partial=False):
        """
        Add two remote jobs to the workflow:
        1. Preprocess input file
        2. Build coreset from preprocessed data
        """
        # Preprocessing job
        job_text = self.get_wrapped_code(f"""\
            print("Starting build_preprocess_from_file")
            init_params = {pformat(self.init_params, indent=4)}
            service = {self.service_class_name}(**init_params, spark_session=spark)
            service.{ 'partial_' if partial else '' }build_preprocess_from_file(
                spark, input_path="{input_path}", input_format="{input_format}"
            )
            print("build_preprocess_from_file finished, the data is saved to {self.init_params.get('dhspark_path')}")
        """)
        self.remote_jobs.append({
            "job_name": f"{ 'partial_' if partial else '' }preprocess",
            "job_text": job_text,
            "spark_config": self.get_job_spark_config("preprocess")
        })
        build_spark_config = self.get_job_spark_config("build")
        if isinstance(build_spark_config, list):
            for stop_level_build_spark_config in build_spark_config:
                stop_level = stop_level_build_spark_config.get('stop_level')
                build_call = "partial_build(spark_session=spark" if partial else "build(spark_session=spark"
                if stop_level is not None:
                    build_call += f", stop_level={stop_level}"
                build_call += ")"

                # Build coreset job
                job_text = self.get_wrapped_code(f"""\
                    print(f"Starting build")
                    init_params = {self.init_params}
                    service = {self.service_class_name}(**init_params, spark_session=spark)
                    service.{build_call}
                    print(f"build finished, the data is saved to {self.init_params.get('dhspark_path')}")
                """)
                self.remote_jobs.append({
                    "job_name": f"{ 'partial_' if partial else '' }build",
                    "job_text": job_text,
                    "spark_config": stop_level_build_spark_config.get("config")
                })
        else:
            build_call = "partial_build(spark_session=spark)" if partial else "build(spark_session=spark)"
            # Build coreset job
            job_text = self.get_wrapped_code(f"""\
                                print(f"Starting build")
                                init_params = {self.init_params}
                                service = {self.service_class_name}(**init_params, spark_session=spark)
                                service.{build_call}
                                print(f"build finished, the data is saved to {self.init_params.get('dhspark_path')}")
                            """)
            self.remote_jobs.append({
                "job_name": f"{'partial_' if partial else ''}build",
                "job_text": job_text,
                "spark_config": build_spark_config
            })

    def partial_build_from_file(self, input_path: str, input_format: str = "parquet"):
        """
        Shortcut for partial preprocessing and coreset building.
        """
        self.build_from_file(input_path=input_path, input_format=input_format, partial=True)

    def get_coreset(self, level: int = 0, seq_from=None, seq_to=None, save_path=None,
                    preprocessing_stage: str = PreprocessingStage.AUTO,
                    output_format: str = OutputFormat.SPARK_DF,
                    sparse_threshold: float = 0.01):
        """
        Add a coreset extraction job to the workflow.
        """
        get_coreset_params = locals()
        del get_coreset_params['self']
        job_text = self.get_wrapped_code(text=f"""\
            print(f"Starting get_coreset")
            init_params = {self.init_params}
            get_coreset_params = {get_coreset_params}
            service = {self.service_class_name}(**init_params, spark_session=spark)
            service.get_coreset(spark_session=spark, **get_coreset_params)
            print(f"get_coreset finished, the data is saved to {save_path}")
        """)
        self.remote_jobs.append({
            "job_name": f"get_coreset_level_{level}",
            "job_text": job_text,
            "spark_config": self.get_job_spark_config("get_coreset")
        })

    def callable_remote_run(self, job_name, func):
        """
        Wrap and submit an arbitrary Python function as a Spark job.
        """
        source = inspect.getsource(func)
        source_lines = source.split("\n")
        body_lines = source_lines[1:]  # Skip function definition line
        self.remote_jobs.append({
            "job_name": job_name,
            "job_text": self.get_wrapped_code("\n".join(body_lines)),
            "spark_config": self.get_job_spark_config("default")
        })

    
    def get_config_value(self, name):
        """
        Read a value from the remote service configuration (main section).
        """
        return self.remote_service_config['main'].get(name)

    def get_cluster_web_interfaces(self):
        """
        Return list of cluster web UIs. Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def print_cluster_web_interfaces(self):
        """
        Print available web interfaces (e.g. Spark UI).
        """
        ui_list = self.get_cluster_web_interfaces()
        if ui_list and len(ui_list) > 0:
            print("\nWeb Interfaces available:")
            for ui in ui_list:
                print(f"{ui.get('name')}: {ui.get('url')}")
        else:
            print("Web Interfaces are not available")
        return ui_list

    def execute(self, wait_for_cluster: bool = True):
        """
        Launch the remote job workflow. Must be implemented in subclasses.
        Parameters:
            wait_for_cluster: define if return control immediately, or wait for the start iof the cluster.
            If passed True, the method return a list of web-services for cluster control and print these web-links
            in the output
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_cluster_status(self):
        """
        Check cluster status. Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_cluster_finished(self):
        """
        Check if the cluster has finished processing. Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def download_from_cloud(self, source_folder, local_dir):
        """
        Download results from cloud storage. Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")