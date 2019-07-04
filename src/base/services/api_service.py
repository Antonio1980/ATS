import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.api_requests import ApiServiceRequest


class ApiService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(ApiService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def create_api_token(self, token_name: str) -> json:
        """
        Sends HTTP POST request to ApiService to generate api_token and secret.
        :param token_name: Any string.
        :return: Response body as json.
        """
        payload = ApiServiceRequest().create_api_token(token_name)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} create_api_token failed with error: {e}")
            raise e

    @automation_logger(logger)
    def activate_api_token(self, token_id: int, token_state: bool) -> json:
        """
        Sends HTTP POST request to ApiService to make the api_token Active/Not Active.
        :param token_id: Api token ID- int.
        :param token_state: True/False
        :return: Response body as json.
        """
        payload = ApiServiceRequest().change_api_token_activation(token_id, token_state)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} activate_api_token failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_api_token(self, token_id: int) -> json:
        """
        Sends HTTP POST request to ApiService to invalidate api_token.
        :param token_id: Api token ID- int.
        :return: Response body as json.
        """
        payload = ApiServiceRequest().delete_api_token(token_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_api_token failed with error: {e}")
            raise e

    @automation_logger(logger)
    def update_api_token(self, token_id, token_name, ip_1="93.178.204.228", ip_2="90.178.204.228") -> json:
        """
        # 1- token_id, 2- token_name, 3- ip_1, 4- ip_2
        Sends HTTP POST request to ApiService to activate/deactivate api_token.
        :param token_id:
        :param token_name:
        :param ip_1:
        :param ip_2: 
        :return: Response body as json.
        """
        payload = ApiServiceRequest().update_api_token(token_id, token_name, ip_1, ip_2)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} update_api_token failed with error: {e}")
            raise e

    @automation_logger(logger)
    def renew_api_token(self, token_name: str, token_id: int) -> json:
        """
        Sends HTTP POST request to ApiService to update expiration of the given api_token.
        :param token_name: Api token name - str.
        :param token_id: Api token ID- int.
        :return: Response body as json.
        """
        payload = ApiServiceRequest().renew_api_token(token_name, token_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} renew_api_token failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_api_tokens(self) -> json:
        """
        Sends HTTP POST request to ApiService to receive all customer api_tokens.
        :return: Response body as json.
        """
        payload = ApiServiceRequest().get_api_tokens()
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_api_tokens failed with error: {e}")
            raise e
