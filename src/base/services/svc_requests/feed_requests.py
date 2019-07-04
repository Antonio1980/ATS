from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class FeedServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(FeedServiceRequest, self).__init__()
        self.method = "Feed."

    @automation_logger(logger)
    def crypto_panic(self):
        """
        Build request body for FeedService.crypto_panic()
        :return: Request body as json dump string.
        """
        self.method += "CryptoPanic"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
