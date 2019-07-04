from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class CustomerServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(CustomerServiceRequest, self).__init__()
        self.method = "CustomerManagement."

    @automation_logger(logger)
    def update_customer(self, dxex_mode=None, api_mode=None):
        """
        Builds request body for CustomerService.update_customer()
        :param api_mode:
        :param dxex_mode: True or False.
        :return: Request body as json dump string.
        """
        self.method += "UpdateCustomer"
        if dxex_mode and api_mode is None:
            self.params.extend([
                {
                    DXEX_FEES_ENABLED: dxex_mode,
                    UPDATE_FIELDS: [
                        DXEX_FEES_ENABLED
                    ]
                }
            ])
        elif api_mode and dxex_mode is None:
            self.params.extend([
                {
                    API_ENABLED: api_mode,
                    UPDATE_FIELDS: [
                        API_ENABLED
                    ]
                }
            ])
        else:
            self.params.extend([
                {
                    DXEX_FEES_ENABLED: dxex_mode,
                    API_ENABLED: api_mode,
                    UPDATE_FIELDS: [
                        DXEX_FEES_ENABLED,
                        API_ENABLED
                    ]
                }
            ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
