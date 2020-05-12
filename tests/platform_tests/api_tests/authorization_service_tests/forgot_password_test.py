import json
import allure
import pytest
from src.base import logger
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "Forgot Password"

@pytest.mark.incremental
@allure.title("FORGOT PASSWORD")
@allure.description("""
    Sanity tests.
    1. Send "Forgot Password" email.
    2. Use the validation token to change the password to "Password1" 
    3. Log out.
    4. Log in with "Password1".  
    5. Verify old password can't be used to log in.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/forgot_password_test.py",
                 "TestForgotPasswordFullFlow")
@pytest.mark.usefixtures("r_time_count", "customer_new")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestForgotPassword(object):
    old_password = ""

    @allure.step("Send 'Forgot Password' email")
    @automation_logger(logger)
    def test_extract_token_from_email(self, customer_new):
        TestForgotPassword.old_password = customer_new.password
        customer_new.get_postman_access()
        response = customer_new.postman.authorization_service.forgot_password_step1(customer_new.email)
        assert response['error'] is None
        Utils.get_mail_gun_item(customer_new, forgot=True)
        assert len(customer_new.ver_token) > 0

    @allure.step("Use the validation token to change the password to 'Password1'")
    @automation_logger(logger)
    def test_change_password(self, customer_new):
        response = customer_new.postman.authorization_service.forgot_password_step2(customer_new.email, customer_new.ver_token,
                                                                                "Password1")
        assert response['error'] is None

    @allure.step("Log out")
    @automation_logger(logger)
    def test_log_out(self, customer_new):
        response = customer_new.postman.authorization_service.log_out()
        assert response['error'] is None

    @allure.step("Log in with 'Password1'")
    @automation_logger(logger)
    def test_sign_in_new_password(self, customer_new):
        response = customer_new.postman.authorization_service.login_by_credentials(customer_new.email, "Password1")
        jwt_token = response['result']['token']
        assert response['error'] is None
        response_token_validation = customer_new.postman.authorization_service.validate_token(jwt_token)
        assert response_token_validation['error'] is None
        assert response_token_validation['result']['isActiveToken'] is True

    @allure.step("Verify old password can't be used to log in")
    @automation_logger(logger)
    def test_sign_in_old_password(self, customer_new):
        response = customer_new.postman.authorization_service.login_by_credentials(customer_new.email,
                                                                                   TestForgotPassword.old_password)
        error = json.loads(response['error'])
        assert error['id'] == "invalidCredentials"

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
