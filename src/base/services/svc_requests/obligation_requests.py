from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class ObligationServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(ObligationServiceRequest, self).__init__()
        self.method = "Balance."

    @automation_logger(logger)
    def convert_currency(self, currency_id, currency_id_2):
        """
        Build request body for ObligationService.convert_rate()
        :param currency_id: ID of base currency as an Integer
        :param currency_id_2: ID of quote currency as an Integer.
        :return: Request body.
        """
        self.method += "CurrenciesConverter"
        self.params.extend([
            {
                CURRENCY_ID: [currency_id],
                PRICE_TO: currency_id_2
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
