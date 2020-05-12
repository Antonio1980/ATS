import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.customer_requests import CustomerServiceRequest


class CustomerService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(CustomerService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def update_customer(self, dxex_mode=None, api_mode=None) -> json:
        """
        Sends HTTP POST request to CustomerService to update customer modes (turn- on/off).
        :param dxex_mode: True if active and False otherwise.
        :param api_mode: True if active and False otherwise.
        :return: Response body as a json.
        """
        payload = CustomerServiceRequest().update_customer(dxex_mode, api_mode)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} update_customer failed with error: {e}")
            raise e
