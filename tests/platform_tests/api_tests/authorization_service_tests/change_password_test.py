import json
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "Change Password"


@pytest.mark.incremental
@allure.title("CHANGE PASSWORD")
@allure.description("""
    Sanity tests.
    1. Log in 
    2. Change password to "Password1"
    3. Log out
    4. Try to log in with the old password (negative)
    5. Try to log in with the new password ("Password1")
    6. Verify the authorization token received is valid and can be used to get customer_pending data 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/change_password_test.py",
                 "TestChangePassword")
@pytest.mark.usefixtures("r_time_count", "customer_new")
class TestChangePassword(object):
    old_password = ""

    @allure.step("Change password to Password1")
    @automation_logger(logger)
    def test_change_password(self, customer_new):
        # Saving the password before changing it for negative testing
        TestChangePassword.old_password = customer_new.password
        response = customer_new.postman.authorization_service.change_password(customer_new.password, "Password1")
        print(F"My email {customer_new.email}")
        assert response['error'] is None
        assert response['result']['errors'] is None

    @allure.step("Log out")
    @automation_logger(logger)
    def test_log_out(self, customer_new):
        response = customer_new.postman.authorization_service.log_out()
        customer_new.get_postman_access()
        assert response['error'] is None

    @allure.step("Try to log in with the old password (negative)")
    @automation_logger(logger)
    def test_log_in_old_password(self, customer_new):
        response = customer_new.postman.authorization_service.login_by_credentials(customer_new.email,
                                                                                   TestChangePassword.old_password)
        error = json.loads(response['error'])
        assert error['id'] == "invalidCredentials"

    @allure.step("Try to log in with the new password Password1")
    @automation_logger(logger)
    def test_login_with_new_password(self, customer_new):
        response = customer_new.postman.authorization_service.login_by_credentials(customer_new.email, "Password1")
        assert response['error'] is None
        customer_new.auth_token = response['result']['token']
        customer_new.get_postman_access(customer_new.auth_token)

    @allure.step("Verify the authorization token received is valid and can be used to get customer_pending data")
    @automation_logger(logger)
    def test_token_is_valid(self, customer_new):
        customer_data_response = customer_new.postman.trade_service.customer_data()
        assert customer_data_response['error'] is None
        assert customer_data_response['result']['customer']['email'] == customer_new.email
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
