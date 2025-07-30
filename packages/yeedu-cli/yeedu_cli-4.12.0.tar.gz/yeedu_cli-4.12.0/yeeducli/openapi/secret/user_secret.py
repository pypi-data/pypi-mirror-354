import json
from yeeducli.utility.json_utils import response_validator
from yeeducli.utility.request_utils import Requests
from yeeducli.utility.logger_utils import Logger
from yeeducli import config
import requests
import sys

logger = Logger.get_logger(__name__, True)

class UserSecret:
    def create_user_secret(json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/secret"

            response = Requests(
                url=url,
                method="POST",
                headers=config.headers,
                json=json_data
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to create user secret due to {e}")
            sys.exit(-1)

    def update_user_secret(user_secret_id, json_data):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/secret"

            response = Requests(
                url=url,
                method="PUT",
                headers=config.headers,
                params={
                    "user_secret_id": user_secret_id
                },
                json=json_data
            ).send_http_request()
            
            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to update user secret due to {e}")
            sys.exit(-1)



    def list_user_secrets(limit, pageNumber, secret_type=None, user_secret_id=None):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/secrets"

            response = Requests(
                url=url,
                method="GET",
                headers=config.headers,
                params={
                    "secret_type": secret_type,
                    "limit": limit,
                    "pageNumber": pageNumber,
                    "user_secret_id": user_secret_id
                }
            ).send_http_request()
            
            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to get user secrets due to {e}")
            sys.exit(-1)


    def search_user_secrets(secret_name, secret_type, limit, pageNumber):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/secrets/search"

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
            logger.exception(f"Failed to search user secrets due to {e}")
            sys.exit(-1)

    def delete_user_secret(user_secret_id):
        try:
            url = f"{config.YEEDU_RESTAPI_URL}/user/secret"

            response = Requests(
                url=url,
                method="DELETE",
                headers=config.headers,
                params={
                    "user_secret_id": user_secret_id
                }
            ).send_http_request()

            return response_validator(response)

        except requests.exceptions.RequestException as e:
            logger.exception(f"Failed to delete user secret due to {e}")
            sys.exit(-1)
