from yeeducli.openapi.job.spark_job_config import SparkJobConfig
from yeeducli.openapi.job.spark_job_instance import SparkJobInstance
from yeeducli.openapi.job.download_job_instance_logs import DownloadJobInstanceLogs
from yeeducli.utility.file_utils import FileUtils
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.json_utils import *
from yeeducli import config
import sys
import json
import time

logger = Logger.get_logger(__name__, True)


# Spark Job Configuration
def create_spark_job_config(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(
            remove_output(args, subcommand='create-conf'))

        del json_data["workspace_id"]
        if hasattr(args, 'job_raw_scala_code') and trim_json_data.get('job_raw_scala_code')[0] != None:
            rawScalaCodeFilePath = FileUtils.checkFilePathExists(file_path=trim_json_data.get(
                'job_raw_scala_code')[0], argument='job_raw_scala_code')

            json_data['job_rawScalaCode'] = FileUtils.readFileContent(
                rawScalaCodeFilePath)

            del json_data["job_raw_scala_code"]

            response_json = SparkJobConfig.add_spark_job_config(
                trim_json_data.get('workspace_id')[0],
                json_data
            )
            confirm_output(response_json, trim_json_data)

        else:
            response_json = SparkJobConfig.add_spark_job_config(
                trim_json_data.get('workspace_id')[0],
                json_data
            )
            confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_spark_job_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobConfig.get_spark_job_config_by_id_or_name(
            json_data.get('workspace_id'),
            json_data.get('job_conf_id'),
            json_data.get('job_conf_name')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_spark_job_configs(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobConfig.search_spark_job_config_by_workspaceId_and_name(
            json_data.get('workspace_id'),
            json_data.get('job_conf_name'),
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_ids'),
            json_data.get('job_type'),
            json_data.get('job_type_langs'),
            json_data.get('last_run_status'),
            json_data.get('created_by_ids'),
            json_data.get('modified_by_ids')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_spark_job_config(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobConfig.list_spark_job_config(
            json_data.get('workspace_id'),
            json_data.get('enable'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_ids'),
            json_data.get('job_type'),
            json_data.get('job_type_langs'),
            json_data.get('last_run_status'),
            json_data.get('created_by_ids'),
            json_data.get('modified_by_ids')
        )
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_spark_job_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = remove_output(args, subcommand='edit-conf')
        if json_data.get('job_conf_id') is not None:
            del json_data["job_conf_id"]
        if json_data.get('job_conf_name') is not None:
            del json_data["job_conf_name"]

        del json_data["workspace_id"]

        if hasattr(args, 'job_raw_scala_code') and trim_json_data.get('job_raw_scala_code') != None:
            if trim_json_data.get('job_raw_scala_code') != "null":
                rawScalaCodeFilePath = FileUtils.checkFilePathExists(
                    file_path=trim_json_data.get('job_raw_scala_code'), argument='job_raw_scala_code')

                json_data['job_rawScalaCode'] = FileUtils.readFileContent(
                    rawScalaCodeFilePath)
            else:
                json_data['job_rawScalaCode'] = trim_json_data.get(
                    'job_raw_scala_code')

            del json_data["job_raw_scala_code"]
            response_json = SparkJobConfig.edit_spark_job_config(
                trim_json_data.get('workspace_id'),
                json.dumps(process_null_values(json_data)),
                trim_json_data.get('job_conf_id'),
                trim_json_data.get('job_conf_name')
            )
            confirm_output(response_json, trim_json_data)

        else:
            response_json = SparkJobConfig.edit_spark_job_config(
                trim_json_data.get('workspace_id'),
                json.dumps(process_null_values(json_data)),
                trim_json_data.get('job_conf_id'),
                trim_json_data.get('job_conf_name')
            )
            confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def enable_spark_job_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobConfig.enable_spark_job_config_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('job_conf_id'),
            trim_json_data.get('job_conf_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def disable_spark_job_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobConfig.disable_spark_job_config_by_id_or_name(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('job_conf_id'),
            trim_json_data.get('job_conf_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def export_spark_job_config(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobConfig.export_spark_job_config(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('job_conf_id'),
            trim_json_data.get('job_conf_name')
        )
        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Spark Job Instance
def start_spark_job_run(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args, subcommand='start'))
        del json_data['workspace_id']
        del json_data['follow']

        workspace_id = trim_json_data.get('workspace_id')[0]
        job_states = ['ERROR', 'STOPPED', 'DONE', 'TERMINATED']

        if args.follow:
        # Submit Spark job
            submit_url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job"
            response = send_api_request("POST", submit_url, headers=config.headers, json=json_data)
            response_json = response.json()
            job_id = response_json.get('job_id')

            # Poll for job status
            while True:
                time.sleep(5)
                try:
                    status_url = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/{job_id}"
                    response = send_api_request("GET", status_url, headers=config.headers)
                    api_status_code = response.status_code

                    if api_status_code == 200:
                        current_status = response.json().get('job_status')
                        logger.info("Current Job Status: %s", current_status)

                        if current_status in job_states:
                            logger.info(f"Final Job Status {current_status}")
                            time.sleep(10)

                            # Fetch logs with retry
                            log_url_stdout = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/{job_id}/log/stdout"
                            log_url_stderr = f"{config.YEEDU_RESTAPI_URL}/workspace/{workspace_id}/spark/job/{job_id}/log/stderr"

                            stdout_response = send_api_request("GET", log_url_stdout, headers=config.headers)
                            stderr_response = send_api_request("GET", log_url_stderr, headers=config.headers)
                            
                            logger.info(f"=====STDOUT for Job ID {job_id} ====\n")
                            FileUtils.process_file_response(stdout_response, save_to_disk=False)

                            logger.info(f"=====STDERR for Job ID {job_id} ====\n")
                            FileUtils.process_file_response(stderr_response, save_to_disk=False)

                            break
                    else:
                        raise Exception(f"Failed to get job status, API returned status code: {api_status_code}")

                except Exception as e:
                    raise Exception(f"API failure while waiting for job completion: {e}")

            confirm_output(response_json, trim_json_data)
        else:
        # Submit Spark job without follow option
            response_json = SparkJobInstance.add_spark_job_instance(
                trim_json_data.get('workspace_id')[0],
                json_data)
            confirm_output(response_json, trim_json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def describe_spark_job_inst(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobInstance.get_spark_job_inst_by_id(
            json_data.get('workspace_id'),
            json_data.get('job_id'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_spark_job_inst(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobInstance.search_spark_job_instance_by_workspaceId_and_name(
            json_data.get('workspace_id'),
            json_data.get('job_conf_name'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_ids'),
            json_data.get('job_status'),
            json_data.get('job_type'),
            json_data.get('job_type_langs'),
            json_data.get('created_by_ids'),
            json_data.get('modified_by_ids')
        )

        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_spark_job_inst(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobInstance.list_spark_job_instances(
            json_data.get('workspace_id'),
            json_data.get('page_number'),
            json_data.get('limit'),
            json_data.get('cluster_ids'),
            json_data.get('job_conf_ids'),
            json_data.get('job_status'),
            json_data.get('job_type'),
            json_data.get('job_type_langs'),
            json_data.get('created_by_ids'),
            json_data.get('modified_by_ids')
        )

        confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def stop_spark_job_inst(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobInstance.stop_spark_job_instance_by_id(
            trim_json_data.get('workspace_id'),
            trim_json_data.get('job_id')
        )

        confirm_output(response_json, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_workflow_job_instance_details(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobInstance.get_workflow_job_instance_details_by_appId(
            json_data.get('workspace_id'),
            json_data.get('job_application_id'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_spark_job_inst_status(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = SparkJobInstance.get_spark_job_status_by_id(
            json_data.get('workspace_id'),
            json_data.get('job_id'))
        confirm_output(response_json, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# Download Job Instance Log Files
def download_job_instance_log_records(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json = DownloadJobInstanceLogs.get_job_instance_log_records(
            json_data.get('workspace_id'),
            json_data.get('log_type'),
            json_data.get('job_id')
        )
        if (response_json is not True):
            confirm_output(response_json, json_data)

    except Exception as e:
        logger.exception(e)
        sys.exit(-1)