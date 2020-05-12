import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.tracking_requests import TrackingServiceRequest


class TrackingService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(TrackingService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def add_visit(self) -> json:
        """
        Sends HTTP POST request to TrackingServiceRequest to add record for visit.
        :return: Response body as a json.
        """
        payload = TrackingServiceRequest().add_visit()
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} add_visit failed with error: {e}")
            raise e
