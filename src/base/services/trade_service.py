import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.trade_requests import TradeServiceRequest


class TradeService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(TradeService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def platform_data(self) -> json:
        """
        Sends HTTP POST request to TradeManagementRequests to get platform data.
        :return: Response body as a json.
        """
        payload = TradeServiceRequest().platform_data()
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} platform_data failed with error: {e}")
            raise e

    @automation_logger(logger)
    def country_data(self) -> json:
        """
        Sends HTTP POST request to TradeManagementRequests to get country data.
        :return: Response body as a json.
        """
        payload = TradeServiceRequest().country_data()
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} country_data failed with error: {e}")
            raise e

    @automation_logger(logger)
    def customer_data(self) -> json:
        """
        Sends HTTP POST request to TradeManagementRequests to get customer data.
        :return: Response body as a json.
        """
        payload = TradeServiceRequest().customer_data()
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} customer_data failed with error: {e}")
            raise e

    @automation_logger(logger)
    def crypto_currency_data(self, currency_id: int) -> json:
        """
        Sends HTTP POST request to TradeManagementRequests to get crypto data for provided currency ID.
        :param currency_id: Currency ID- int.
        :return: Response body as a json.
        """
        payload = TradeServiceRequest().crypto_currency_data(currency_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} crypto_currency_data failed with error: {e}")
            raise e
