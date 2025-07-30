import json
import sys
import requests
from yeeducli.utility.logger_utils import Logger
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.json_utils import response_validator
from yeeducli import config

logger = Logger.get_logger(__name__, True)

class MetstoreCatalogTenantAssociation:
    def link_tenant_secret(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/tenant"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to link Unity Catalog Tenant Secret due to {e}")
            sys.exit(-1)

    def update_tenant_secret(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/tenant"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to update Unity Catalog Tenant Secret due to {e}")
            sys.exit(-1)

    def unlink_tenant_secret(metastore_catalog_secret_tenant_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/tenant"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "metastore_catalog_secret_tenant_id": metastore_catalog_secret_tenant_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to unlink Unity Catalog Tenant Secret due to {e}")
            sys.exit(-1)


    def list_linked_tenant_secrets(metastore_catalog_secret_tenant_id=None, catalog_type=None, metastore_catalog_id=None, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/tenant"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "metastore_catalog_secret_tenant_id": metastore_catalog_secret_tenant_id,
                    "catalog_type": catalog_type,
                    "metastore_catalog_id": metastore_catalog_id,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)
        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to get linked Unity Catalog Tenant Secret due to {e}")
            sys.exit(-1)

    def search_linked_tenant_secrets(metastore_catalog_secret_tenant_id=None, catalog_type=None, metastore_catalog_name=None, limit=None, pageNumber=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/metastore/catalog/secret/tenant"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "metastore_catalog_secret_tenant_id": metastore_catalog_secret_tenant_id,
                    "catalog_type": catalog_type,
                    "metastore_catalog_name": metastore_catalog_name,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to search linked Unity Catalog Tenant Secret due to {e}")
            sys.exit(-1)
