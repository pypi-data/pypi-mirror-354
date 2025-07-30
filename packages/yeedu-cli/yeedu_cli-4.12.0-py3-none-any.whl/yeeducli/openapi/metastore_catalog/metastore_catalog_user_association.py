import json
import sys
import requests
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.json_utils import response_validator
from yeeducli import config

logger = Logger.get_logger(__name__, True)

class MetastoreCatalogUserAssociation:
    def link_user_secret(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/user"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to link Unity Catalog User Secret due to {e}")
            sys.exit(-1)

    def update_user_secret(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/user"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to update Unity Catalog User Secret due to {e}")
            sys.exit(-1)

    def list_linked_user_secrets(user_id=None, metastore_catalog_secret_user_id=None, catalog_type=None, metastore_catalog_id=None, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/user"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "user_id": user_id,
                    "metastore_catalog_secret_user_id": metastore_catalog_secret_user_id,
                    "catalog_type": catalog_type,
                    "metastore_catalog_id": metastore_catalog_id,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to list linked Unity Catalog User Secrets due to {e}")
            sys.exit(-1)

    def search_linked_user_secrets(user_id=None, metastore_catalog_secret_user_id=None, metastore_catalog_name=None, catalog_type=None, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/user"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "user_id": user_id,
                    "metastore_catalog_secret_user_id": metastore_catalog_secret_user_id,
                    "metastore_catalog_name": metastore_catalog_name,
                    "catalog_type": catalog_type,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to search linked Unity Catalog User Secrets due to {e}")
            sys.exit(-1)


    def unlink_user_secret(metastore_catalog_secret_user_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/user"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "metastore_catalog_secret_user_id": metastore_catalog_secret_user_id
                }
            ).send_http_request()
            
            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to unlink Unity Catalog User Secret due to {e}")
            sys.exit(-1)

