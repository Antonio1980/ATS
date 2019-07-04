import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "Resend SMS"


@allure.feature("Authorization")
@allure.title("RESEND SMS")
@allure.description("""
    Sanity api test.
    Coverage:
    authorization_service, resend SMS  
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Resend Sms')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/resend_sms_test.py",
                 "TestAuthorizationResendSMS")
@pytest.mark.usefixtures("r_customer", "r_time_count")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestResendSms(object):

    @allure.step("Sending SMS to a valid number")
    @automation_logger(logger)
    def test_resend_sms(self, r_customer):
        response = r_customer.postman.authorization_service.resend_sms()
        assert response['error'] is None
        logger.logger.info(F" Sending SMS to a valid number - server response verified")
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Sending SMS to a invalid number")
    @automation_logger(logger)
    def test_resend_to_invalid_number(self, r_customer):
        original_phone_number = r_customer.phone
        r_customer.phone = 999
        response = r_customer.postman.authorization_service.resend_sms()
        assert response['error'] == 'error sending SMS code'
        r_customer.phone = original_phone_number
        logger.logger.info(F"Sending SMS to a invalid number - server response verified")

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!-------------")
