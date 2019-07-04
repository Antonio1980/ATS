import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "7780"


@allure.feature("Authorization")
@allure.story("Client able to log in using his API token and secret.")
@allure.title("LOG IN BY TOKEN.")
@allure.description("""
    Functional tests.
    1. test_log_in_by_token - positive test (get existing customer and check if it has api token and secret).
    2. test_log_in_by_token_local- negative test.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='LoginByToken')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/log_in_by_token_test.py",
                 "TestLogInByToken")
@pytest.mark.usefixtures("r_time_count", "customer_app", "conf_customer_app")
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestLogInByToken(object):
    
    @allure.step("Starting with: test_generate_password_hash")
    @automation_logger(logger)
    def test_log_in_by_token(self, customer_app):
        _response = customer_app.postman.authorization_service.login_by_token(customer_app.api_token,
                                                                                  customer_app.api_secret)
        assert _response['error'] is None and _response['result']['token']
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_generate_password_hash")
    @automation_logger(logger)
    def test_log_in_by_token_local(self, conf_customer_app):
        _response = conf_customer_app.postman.authorization_service.login_by_token(conf_customer_app.api_token,
                                                                                   conf_customer_app.api_secret)
        assert _response['error'] is None and _response['result']['token']
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))
