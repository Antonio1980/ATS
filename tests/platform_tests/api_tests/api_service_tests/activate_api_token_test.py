import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, "Activation Api Token")
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/api_service_tests/renew_api_token_test.py",
                 "TestActivationTokenAPI")
@pytest.mark.usefixtures("r_time_count", "customer_app")
@pytest.mark.regression
@pytest.mark.api_service
class TestActivationTokenAPI(object):

    @automation_logger(logger)
    def test_activation_api_token_method_works(self, customer_app):
        tokens = customer_app.postman.api_service.get_api_tokens()
        activate_response = customer_app.postman.api_service.activate_api_token(customer_app.api_token_id, True)
        assert activate_response['error'] is None

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))

    @automation_logger(logger)
    def test_deactivate_api_token(self, customer_app):
        deactivate_response = customer_app.postman.api_service.activate_api_token(customer_app.api_token_id, False)
        assert deactivate_response['error'] is None

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))

    @automation_logger(logger)
    def test_activate_api_token(self, customer_app):
        activate_response = customer_app.postman.api_service.activate_api_token(customer_app.api_token_id, True)
        assert activate_response['error'] is None

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))
