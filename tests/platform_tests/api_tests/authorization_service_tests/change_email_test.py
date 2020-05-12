import time
import allure
import pytest
from src.base import logger
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "6044"


@pytest.mark.incremental
@allure.feature("Authorization")
@allure.story("Client able to chage his email via API (4 steps).")
@allure.title("CHANGE EMAIL.")
@allure.description("""
    Functional tests.
    1. test_change_email_1 
    2. test_change_email_2
    3. test_change_email_3
    3. test_change_email_4
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='ChangeEmail')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/change_email_test.py", "TestChangeEmail")
@pytest.mark.usefixtures("r_time_count", "customer_new")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestChangeEmail(object):
    ver_token = None

    @allure.step("Proceed with registration: verify_email_step_2")
    @automation_logger(logger)
    def test_verify_email(self, customer_new):
        Utils.get_mail_gun_item(customer_new)
        logger.logger.info("TOKEN: " + customer_new.ver_token)
        step2 = customer_new.postman.authorization_service.verify_email_step_2(customer_new.email, customer_new.ver_token)
        assert step2['error'] is None and step2['result']['errors'] is None

    @allure.step("Starting with: test_change_email_1")
    @automation_logger(logger)
    def test_change_email_1(self, customer_new):
        response = customer_new.postman.authorization_service.change_email_step1()
        assert response['error'] is None
        logger.logger.info("test_change_email_1 --- PASSED")

    @allure.step("Starting with: test_change_email_2")
    @automation_logger(logger)
    def test_change_email_2(self, customer_new):
        customer_new.get_postman_access(customer_new.auth_token)
        response = customer_new.postman.authorization_service.change_email_step2()
        assert response['error'] is None
        assert response['result']['token']
        TestChangeEmail.ver_token = response['result']['token']
        logger.logger.info("test_change_email_2 --- PASSED")

    @allure.step("Starting with: test_change_email_3")
    @automation_logger(logger)
    def test_change_email_3(self, customer_new):
        customer_new.email = "QA_" + customer_new.email
        response = customer_new.postman.authorization_service.change_email_step3(TestChangeEmail.ver_token,
                                                                                 customer_new.email)
        assert response['error'] is None
        logger.logger.info("test_change_email_3 --- PASSED")

    @allure.step("Starting with: test_change_email_4")
    @automation_logger(logger)
    def test_change_email_4(self, customer_new):
        time.sleep(5.0)
        Utils.get_mail_gun_item(customer_new)
        logger.logger.info("TOKEN" + customer_new.ver_token)
        response = customer_new.postman.authorization_service.change_email_step4(customer_new.ver_token)
        assert response['error'] is None
        logger.logger.info("test_change_email_4 --- PASSED")
        logger.logger.info("{0}, {1}, {2}".format(customer_new.email, customer_new.password,
                                                  customer_new.customer_id))
