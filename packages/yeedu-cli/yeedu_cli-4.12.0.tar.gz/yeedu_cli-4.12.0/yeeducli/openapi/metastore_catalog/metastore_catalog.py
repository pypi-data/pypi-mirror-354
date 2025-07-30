import json
import sys
import requests
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.json_utils import response_validator
from yeeducli import config

logger = Logger.get_logger(__name__, True)

class MetastoreCatalog:
    def create_catalog(json_data, catalog_type=""):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/{catalog_type}"
            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to create Unity Catalog due to {e}")
            sys.exit(-1)


    def edit_catalog(metastore_catalog_id, json_data, catalog_type=""):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/{catalog_type}"
            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                params={
                    "metastore_catalog_id": metastore_catalog_id
                },
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to edit Unity Catalog due to {e}")
            sys.exit(-1)


    def list_catalogs(metastore_catalog_id=None, catalog_type=None, limit=None, pageNumber=None):
        try:            
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalogs"
            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "metastore_catalog_id": metastore_catalog_id,
                    "catalog_type": catalog_type,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to list Unity Catalogs due to {e}")
            sys.exit(-1)

    def search_catalog(metastore_catalog_name, catalog_type, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalogs/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "metastore_catalog_name": metastore_catalog_name,
                    "catalog_type": catalog_type,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to search Unity Catalogs due to {e}")
            sys.exit(-1)

    def delete_catalog(metastore_catalog_id, catalog_type=""):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/{catalog_type}"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "metastore_catalog_id": metastore_catalog_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to delete Unity Catalog due to {e}")
            sys.exit(-1)