from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class NotificationServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(NotificationServiceRequest, self).__init__()
        self.method = "Notification."

    @automation_logger(logger)
    def resend_sms(self, token_name: str, sms_type: int, action: str):
        """
        Builds request body for ApiService.create_api_token()
        :param token_name: Any string.
        :param sms_type:
        :param action:
        :return: Request body as json dump string.
        """
        self.method += "ResendSms"
        self.params.extend([
            {
                NAME: token_name,
                SMS_TYPE: sms_type,
                ACTION: action
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
