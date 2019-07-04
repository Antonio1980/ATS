from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class BalanceServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(BalanceServiceRequest, self).__init__()
        self.method = "Balance."

    @automation_logger(logger)
    def get_balance(self, *args):
        """
        Method is part of public API
        Build request body for IBalanceService.get_currency_balance()
        :param args: currencies (if not specified it return all available).
        :return: Request body as json dump string.
        """
        self.method += "Get"
        self.params.append({})
        self.params[0].update({CURRENCIES: []})
        if args:
            for currency in args[0]:
                self.params[0][CURRENCIES].append(currency)
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
