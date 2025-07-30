from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)

class TenantSecret:
    def create_tenant_secret(json_data):

        try:
            url = f"{config.YEEDU_RESTAPI_URL}/tenant/secret"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to create tenant secret due to {e}")
            sys.exit(-1)

    def update_tenant_secret(tenant_secret_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/tenant/secret"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                params={
                    "tenant_secret_id": tenant_secret_id
                },
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to update tenant secret due to {e}")
            sys.exit(-1)

    def list_tenant_secrets(limit, pageNumber, secret_type=None, tenant_secret_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/tenant/secrets"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "secret_type": secret_type,
                    "limit": limit,
                    "pageNumber": pageNumber,
                    "tenant_secret_id": tenant_secret_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to get tenant secrets due to {e}")
            sys.exit(-1)

    def search_tenant_secrets(secret_name, secret_type, limit, pageNumber):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/tenant/secrets/search"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "secret_name": secret_name,
                    "secret_type": secret_type,
                    "limit": limit,
                    "pageNumber": pageNumber
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to search tenant secrets due to {e}")
            sys.exit(-1)

    def delete_tenant_secret(tenant_secret_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/tenant/secret"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "tenant_secret_id": tenant_secret_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to delete tenant secret due to {e}")
            sys.exit(-1)