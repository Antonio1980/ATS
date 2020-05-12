import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.notification_requests import NotificationServiceRequest


class NotificationService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(NotificationService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def resend_sms(self, token_name: str, sms_type, action) -> json:
        """
        Sends HTTP POST request to ApiService to generate api_token and secret.
        :param token_name: Any string.
        :param sms_type:
        :param action:
        :return: Response body as json.
        """
        payload = NotificationServiceRequest().resend_sms(token_name, sms_type, action)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} resend_sms failed with error: {e}")
            raise e
