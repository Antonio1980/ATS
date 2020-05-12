from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class TrackingServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(TrackingServiceRequest, self).__init__()
        self.method = "Tracking."

    @automation_logger(logger)
    def add_visit(self):
        """

        @return:
        """
        self.method += "AddVisit"
        self.params.extend([
            {
                "CampaignId": 1,
                "SubCampaignId": 2,
                "isUnique": False
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
