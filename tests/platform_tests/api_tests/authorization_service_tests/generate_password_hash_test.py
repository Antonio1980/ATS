import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "6031"


@allure.feature("Authorization")
@allure.story("Client able to generate password hash via API.")
@allure.title("GENERATE PASSWORD HASH.")
@allure.description("""
    Functional tests.
    1. test_generate_password_hash - positive test.
    2. test_generate_password_hash_negative- negative test.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='GeneratePasswordHash')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/change_phone_test.py",
                 "TestGeneratePasswordHash")
@pytest.mark.usefixtures("r_customer", "r_time_count", )
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestGeneratePasswordHash(object):

    @pytest.fixture
    @automation_logger(logger)
    def customer(self):
        customer = Customer()
        return customer

    @allure.step("Starting with: test_generate_password_hash")
    @automation_logger(logger)
    def test_generate_password_hash(self, r_customer):
        _response = r_customer.postman.authorization_service.generate_password_hash(r_customer.email,
                                                                                    r_customer.password)
        assert _response['error'] is None and _response['result']['hashedPassword']
        r_customer.hashed_password = _response['result']['hashedPassword']
        assert isinstance(r_customer.hashed_password, str) and len(r_customer.hashed_password) > 0
        logger.logger.info("Customer Hashed Password -- {0}".format(r_customer.hashed_password))
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_generate_password_hash_negative")
    @automation_logger(logger)
    def test_generate_password_hash_negative(self, customer):
        _response = customer.postman.authorization_service.generate_password_hash(None, None)
        assert _response['error'] is not None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))
