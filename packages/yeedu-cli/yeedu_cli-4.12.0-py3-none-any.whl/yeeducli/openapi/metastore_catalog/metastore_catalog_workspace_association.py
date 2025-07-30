import json
import sys
import requests
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.json_utils import response_validator
from yeeducli import config

logger = Logger.get_logger(__name__, True)

class MetastoreCatalogWorkspaceAssociation:

    def link_workspace_secret(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/workspace"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to link Unity Catalog Workspace Secret due to {e}")
            sys.exit(-1)

    def update_workspace_secret(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/workspace"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to update Unity Catalog Workspace Secret due to {e}")
            sys.exit(-1)

    def list_linked_workspace_secrets(workspace_id=None, metastore_catalog_secret_workspace_id=None, catalog_type=None, metastore_catalog_id=None, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/workspace"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "metastore_catalog_secret_workspace_id": metastore_catalog_secret_workspace_id,
                    "catalog_type": catalog_type,
                    "metastore_catalog_id": metastore_catalog_id,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to list linked Unity Catalog Workspace Secrets due to {e}")
            sys.exit(-1)

    def search_linked_workspace_secrets(workspace_id=None, metastore_catalog_secret_workspace_id=None, metastore_catalog_name=None, catalog_type=None, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/workspace"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "workspace_id": workspace_id,
                    "metastore_catalog_secret_workspace_id": metastore_catalog_secret_workspace_id,
                    "metastore_catalog_name": metastore_catalog_name,
                    "catalog_type": catalog_type,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to search linked Unity Catalog Workspace Secrets due to {e}")
            sys.exit(-1)


    def unlink_workspace_secret(metastore_catalog_secret_workspace_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/workspace"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "metastore_catalog_secret_workspace_id": metastore_catalog_secret_workspace_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to unlink Unity Catalog Workspace Secret due to {e}")
            sys.exit(-1)