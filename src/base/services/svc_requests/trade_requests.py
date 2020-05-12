from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class TradeServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(TradeServiceRequest, self).__init__()
        self.method = "TradeManagement."

    @automation_logger(logger)
    def platform_data(self):
        """

        @return:
        """
        self.method += "PlatformData"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def country_data(self):
        """

        @return:
        """
        self.method += "CountryData"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def customer_data(self):
        """

        @return:
        """
        self.method += "CustomerData"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def crypto_currency_data(self, currency_id: int):
        """

        @param currency_id:
        @return:
        """
        self.method += "CryptoCurrencyData"
        self.params.extend([
            {
                CURRENCY_ID: currency_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
