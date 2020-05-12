import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "6029"


@allure.feature("Authorization")
@allure.story("Client able to log in using his Platform credentials.")
@allure.title("LOG IN BY CREDENTIALS.")
@allure.description("""
    Functional tests.
    1. test_log_in_by_credentials - positive test (get existing customer and log in).
    2. test_log_in_by_credentials_negative- negative test.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='LoginByCredentials')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/log_in_by_credentials_test.py",
                 "TestLogInByCredentials")
@pytest.mark.usefixtures("r_customer", "r_time_count", )
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestLogInByCredentials(object):

    @pytest.fixture
    @automation_logger(logger)
    def customer(self):
        customer = Customer()
        return customer

    @allure.step("Starting with: test_log_in_by_credentials")
    @automation_logger(logger)
    def test_log_in_by_credentials(self, r_customer):
        r_customer.set_customer_details()
        _response = r_customer.postman.authorization_service.login_by_credentials(r_customer.email, r_customer.password)
        assert _response['error'] is None and _response['result']['token']
        assert len(_response['result']['token']) > 0
        assert _response['result']['expiry'] > 0
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_log_in_by_credentials_negative")
    @automation_logger(logger)
    def test_log_in_by_credentials_negative(self, customer):
        _response = customer.postman.authorization_service.login_by_credentials(None, None)
        assert _response['error'] is not None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))
