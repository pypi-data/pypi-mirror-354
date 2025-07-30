from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)

class WorkspaceSecret:
    def create_workspace_secret(workspace_id=None, workspace_name=None, json_data=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/secret"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name
                },
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to create workspace secret due to {e}")
            sys.exit(-1)

    def update_workspace_secret(workspace_id=None, workspace_name=None, workspace_secret_id=None, json_data=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/secret"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                    "workspace_secret_id": workspace_secret_id
                },
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to update workspace secret due to {e}")
            sys.exit(-1)

    def list_workspace_secrets(limit, pageNumber, workspace_id=None, workspace_name=None, secret_type=None, workspace_secret_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/secrets"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "limit": limit,
                    "pageNumber": pageNumber,
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                    "secret_type": secret_type,
                    "workspace_secret_id": workspace_secret_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to get workspace secrets due to {e}")
            sys.exit(-1)


    def search_workspace_secrets(workspace_id=None, workspace_name=None, secret_name=None, secret_type=None, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/secrets/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                    "secret_name": secret_name,
                    "secret_type": secret_type,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to search workspace secrets due to {e}")
            sys.exit(-1)


    def delete_workspace_secret(workspace_id=None, workspace_name=None, workspace_secret_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/workspace/secret"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                    "workspace_secret_id": workspace_secret_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to delete workspace secret due to {e}")
            sys.exit(-1)
