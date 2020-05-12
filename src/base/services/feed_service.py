import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.feed_requests import FeedServiceRequest


class FeedService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(FeedService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def crypto_panic(self):
        """
        Sends HTTP POST request to FeedService to receive all crypto data.
        :return: Response body as a json.
        """
        payload = FeedServiceRequest().crypto_panic()
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} crypto_panic failed with error: {e}")
            raise e
