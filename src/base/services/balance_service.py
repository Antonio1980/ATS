import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.balance_requests import BalanceServiceRequest


class BalanceService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(BalanceService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def get_balance(self, *args) -> json:
        """
        Authorized method- needs auth_token in request header. (goes to API URL)
        Sends HTTP POST request to IBalanceServiceRequest to get balance for provided currency.
        :param args: currencies (if not specified it return all available).
        :return: Response body as a json.
        """
        payload = BalanceServiceRequest().get_balance(args)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_balance failed with error: {e}")
            raise e
