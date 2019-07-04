import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Feed")
@allure.title("Crypto")
@allure.description("""
    Sanity API test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Crypto Panic')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/feed_service_tests/crypto_panic_test.py", "TestCryptoPanic")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.file_service
class TestCryptoPanic(object):

    @allure.step("Starting: test_crypto_panic_method_works")
    @automation_logger(logger)
    def test_crypto_panic_method_works(self, customer):
        response = customer.postman.feed_service.crypto_panic()
        assert response['error'] is None
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Starting: test_crypto_panic_method")
    @automation_logger(logger)
    def test_crypto_panic_method(self, customer):
        response = customer.postman.feed_service.crypto_panic()
        assert response['error'] is None
        assert response['result']['messages']
        assert isinstance(response['result']['messages'], list)
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

