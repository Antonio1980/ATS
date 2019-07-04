import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.obligation_requests import ObligationServiceRequest


class ObligationService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(ObligationService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def convert_rate(self, currency_id: int, currency_id_2: int) -> json:
        """
        Sends HTTP POST request to ObligationService to calculate rate..
        :param currency_id: Base currency.
        :param currency_id_2: Quoted currency.
        :return:
        """
        payload = ObligationServiceRequest().convert_currency(currency_id, currency_id_2)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} convert_rate failed with error: {e}")
            raise e
