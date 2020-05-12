import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "6030"


@allure.feature("Authorization")
@allure.story("Client able to log out from Trading Platform.")
@allure.title("LOG OUT")
@allure.description("""
    Functional tests.
    1. test_log_out - positive test.
    2. test_log_out_invalidate_auth_token- advanced positive test (check if auth_token invalidated).
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='LogOut')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/log_out_test.py", "TestLogOut")
@pytest.mark.usefixtures("r_time_count", "customer_app", "conf_customer_app")
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestLogOut(object):

    @allure.step("Starting with: test_log_out")
    @automation_logger(logger)
    def test_log_out(self, customer_app):
        _response = customer_app.postman.authorization_service.log_out()
        assert _response['error'] is None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_log_out_invalidate_auth_token")
    @automation_logger(logger)
    def test_log_out_invalidate_auth_token(self, conf_customer_app):
        _response = conf_customer_app.postman.authorization_service.log_out()
        assert _response['error'] is None
        o_response = conf_customer_app.postman.authorization_service.validate_token(conf_customer_app.auth_token)
        assert o_response['error']
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))
