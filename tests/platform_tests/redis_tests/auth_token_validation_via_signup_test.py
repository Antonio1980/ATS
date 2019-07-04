import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.data_bases.redis_db import RedisDb
from src.base.log_decorator import automation_logger

test_case = ""


@allure.severity(allure.severity_level.NORMAL)
@allure.title("REDIS JWT TOKEN TEST")
@allure.description("""
    PRECONDITION: TOKEN_JWT_LIFETIME_SECONDS set on 86400 sec (24 hours) in ConfigMap of Kubernetes.
    Verify that customer balance unfrozen when limit buy order created and cancelled.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/redis_tests/auth_token_validation_via_signup_test.py", "TestValidationJWTTokenOnSignIn")
@pytest.mark.usefixtures("r_time_count", "customer")
@pytest.mark.redis
@pytest.mark.smoke
class TestValidationJWTTokenOnSignUp(object):
    @allure.step("Starting with: test_validate_redis_jwt_token_via_signup")
    @automation_logger(logger)
    def test_validate_redis_jwt_token_via_signup(self, customer):
        logger.logger.info("method test_validate_redis_auth_token_via_signup")
        response = customer.postman.authorization_service.sign_up_step_1(customer)
        assert response['error'] is None and response['result']['errors'] is None
        customer.customer_id = response['result']['customerId']
        assert customer.customer_id
        customer.auth_token = response['result']['token']
        token_state = RedisDb.validate_auth_token(customer.auth_token)
        assert 86399 <= token_state <= 86400
        logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
        logger.logger.info("Token State: {0}".format(token_state))
