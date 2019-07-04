import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "6034"


@allure.feature("Authorization")
@allure.story("Client able to check his auth token.")
@allure.title("VALIDATE TOKEN.")
@allure.description("""
    Functional tests.
    1. test_validate_token - positive test.
    2. test_validate_token_negative- negative test.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='ValidateToken')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/validate_token_test.py",
                 "TestValidateToken")
@pytest.mark.usefixtures("r_customer", "r_time_count")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestValidateToken(object):

    @pytest.fixture
    @automation_logger(logger)
    def customer(self):
        return Customer()

    @allure.step("Starting with: test_validate_token")
    @automation_logger(logger)
    def test_validate_token(self, r_customer):
        response = r_customer.postman.authorization_service.validate_token(r_customer.auth_token)
        assert response['error'] is None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_validate_token_negative")
    @automation_logger(logger)
    def test_validate_token_negative(self, customer):
        response = customer.postman.authorization_service.validate_token("euforiwuro.32ieruywi392875893462398.sakjdhas")
        assert response['result']['isActiveToken'] is False
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))
