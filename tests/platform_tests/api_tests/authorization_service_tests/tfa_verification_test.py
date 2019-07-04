import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "SMS TFA Verification"


@pytest.mark.incremental
@allure.feature("Authorization")
@allure.story("Client can use the TFA feature, turn it on and off.")
@allure.title("TFA Verification")
@allure.description("""
    Functional tests.
    1. Log in 
    2. Turn on TFA
    3. Log out
    4. Log in using TFA
    5. Turn off TFA
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/tfa_verification_test.py",
                 "TestUseTFA")
@pytest.mark.usefixtures("r_time_count", "customer_new")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestTfaValidation(object):
    tfa_token = ""
    jwt_token = ""

    @allure.step("Log in is required to turn on the TFA (SMS)")
    @automation_logger(logger)
    def test_step_one_log_in(self, customer_new):
        log_in_response = customer_new.postman.authorization_service.login_by_credentials(customer_new.email,
                                                                                          customer_new.password)
        assert log_in_response['error'] is None
        assert isinstance(log_in_response['result']['token'], str) and len(log_in_response['result']['token']) > 0
        customer_new.auth_token = log_in_response['result']['token']
        customer_new.get_postman_access(customer_new.auth_token)

    # SMS is activated in 2 steps
    @allure.step("SMS TFA activation - step one")
    @automation_logger(logger)
    def test_step_one_enable_tfa(self, customer_new):
        enable_tfa_response = customer_new.postman.authorization_service.enable_tfa_step_1(customer_new.password)
        assert enable_tfa_response['error'] is None

    @allure.step("SMS TFA activation - step two")
    def test_step_two_enable_tfa(self, customer_new):
        enable_tfa_response = customer_new.postman.authorization_service.enable_tfa_step_2(True)
        assert enable_tfa_response['error'] is None

    @allure.step("Logging out. After the customer_pending is logged out we can verify log in with TFA step")
    def customer_logout(self, customer_pending):
        response = customer_pending.postman.authorization_service.log_out()
        assert response['error'] is None

    @allure.step("Sending a log in request to receive the TFA token. It's used to get the regular JWT token.")
    @automation_logger(logger)
    def test_get_tfa_token(self, customer_new):
        customer_new.get_postman_access()
        response = customer_new.postman.authorization_service.login_by_credentials(customer_new.email, customer_new.password)
        TestTfaValidation.tfa_token = response['result']['twoFactor']['token']
        assert len(TestTfaValidation.tfa_token) > 0

        logger.logger.info(
            F"Customer ID: {customer_new.customer_id}, Customer EMAIL: {customer_new.email}, Customer Token: {TestTfaValidation.tfa_token}")

    # Using TFA token to receive the authorization token (JWT token)
    @automation_logger(logger)
    def test_log_in_with_tfa(self, customer_new):
        # Sending the TFA received to get the JWT token
        response_get_jwt = customer_new.postman.authorization_service.log_in_by_tfa_token(TestTfaValidation.tfa_token)
        TestTfaValidation.jwt_token = response_get_jwt['result']['token']
        assert len(TestTfaValidation.jwt_token) > 0

    @allure.step("Verifying that customer_pending is logged in. Verifying that TFA (SMS) is activated.")
    @automation_logger(logger)
    def test_use_jwt_token_received(self, customer_new):
        customer_new.auth_token = TestTfaValidation.jwt_token
        customer_new.get_postman_access(customer_new.auth_token)
        customer_data_response = customer_new.postman.trade_service.customer_data()
        assert customer_data_response['result']['customer']['sms2FAEnabled'] is True

    @allure.step("Disabling tfa verification")
    @automation_logger(logger)
    def test_disable_tfa(self, customer_new):
        disable_tfa_response = customer_new.postman.authorization_service.enable_tfa_step_2(False)
        assert disable_tfa_response['error'] is None

        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))
