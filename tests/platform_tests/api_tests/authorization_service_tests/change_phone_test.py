import random
import string
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "6048"


@pytest.mark.incremental
@allure.feature("Authorization")
@allure.story("Client able to change his phone via API (4 steps).")
@allure.title("CHANGE PHONE.")
@allure.description("""
    Functional tests.
    1. test_change_phone_1 
    2. test_change_phone_2
    3. test_change_phone_3
    4. test_change_phone_4
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='ChangePhone')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/change_phone_test.py", "TestChangePhone")
@pytest.mark.usefixtures("r_customer", "r_time_count")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestChangePhone(object):
    phone_token = None
    full_phone = '+97252' + ''.join(random.choice(string.digits) for _ in range(7))

    @allure.step("Starting with: test_change_phone_1")
    @automation_logger(logger)
    def test_change_phone_1(self, r_customer):
        response = r_customer.postman.authorization_service.change_phone_step1()
        assert response['error'] is None
        logger.logger.info("test_change_phone_1 --- PASSED")

    @allure.step("Starting with: test_change_phone_2")
    @automation_logger(logger)
    def test_change_phone_2(self, r_customer):
        r_customer.get_postman_access(r_customer.auth_token)
        response = r_customer.postman.authorization_service.change_phone_step2()
        assert response['error'] is None
        assert response['result']['token']
        TestChangePhone.phone_token = response['result']['token']
        logger.logger.info("test_change_phone_2 --- PASSED")

    @allure.step("Starting with: test_change_phone_3")
    @automation_logger(logger)
    def test_change_phone_3(self, r_customer):
        r_customer.get_postman_access(r_customer.auth_token)
        response = r_customer.postman.authorization_service.change_phone_step3(TestChangePhone.phone_token,
                                                                               self.full_phone)
        assert response['error'] is None
        logger.logger.info("test_change_phone_3 --- PASSED")

    @allure.step("Starting with: test_change_phone_4")
    @automation_logger(logger)
    def test_change_phone_4(self, r_customer):
        r_customer.get_postman_access(r_customer.auth_token)
        response = r_customer.postman.authorization_service.change_phone_step4()
        assert response['error'] is None
        logger.logger.info("test_change_phone_4 --- PASSED")
        logger.logger.info("Customer Phone- {0}".format(TestChangePhone.full_phone))
        logger.logger.info("{0}, {1}, {2}".format(r_customer.email, r_customer.password, r_customer.customer_id))
