import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, "Renew Api Token")
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/api_service_tests/renew_api_token_test.py",
                 "TestRenewTokenAPI")
@pytest.mark.usefixtures("r_time_count", "customer_app")
@pytest.mark.regression
@pytest.mark.api_service
class TestRenewTokenAPI(object):

    @automation_logger(logger)
    def test_renew_existing_api_token(self, customer_app):
        # notification_response = customer_app.postman.notification_service.resend_sms(customer_app.api_key, 7, "renew")
        # assert notification_response['error'] is None
        renew_response = customer_app.postman.api_service.renew_api_token(customer_app.api_key, customer_app.api_token_id)
        logger.logger.info("renew_api_token", renew_response)
        assert renew_response['error'] is None
        assert renew_response['result']['secret']
        assert renew_response['result']['token']
        assert renew_response['result']['id']

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))
