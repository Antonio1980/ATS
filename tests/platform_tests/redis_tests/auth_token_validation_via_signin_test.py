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
@allure.testcase(BaseConfig.GITLAB_URL + "/redis_tests/auth_token_validation_via_signin_test.py",
                 "TestValidationJWTTokenOnSignIn")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.redis
@pytest.mark.smoke
class TestValidationJWTTokenOnSignIn(object):
    @allure.step("Starting with: test_validate_redis_jwt_token_via_signin")
    @automation_logger(logger)
    def test_validate_redis_jwt_token_via_signin(self, r_customer):
        logger.logger.info("method test_validate_redis_auth_token_via_signin_test")
        response = r_customer.postman.authorization_service.login_by_credentials(r_customer.email, r_customer.password)
        assert response['error'] is None
        r_customer.auth_token = response['result']['token']
        token_state = RedisDb.validate_auth_token(r_customer.auth_token)
        assert 86399 <= token_state <= 86400
        logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
        logger.logger.info("Token State: {0}".format(token_state))
