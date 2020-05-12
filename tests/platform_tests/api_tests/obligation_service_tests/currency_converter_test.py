import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Balance")
@allure.title("Obligation")
@allure.description("""
    Sanity API test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Corrency Converter')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/obligation_service_tests/currency_converter_test.py",
                 "TestCurrencyConverter")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.obligation_service
class TestCurrencyConverter(object):

    @allure.step("Starting: test_corrency_converter_method_works")
    @automation_logger(logger)
    def test_currency_converter_method_works(self, customer):
        response = customer.postman.obligation_service.convert_rate(1, 3)
        assert response['error'] is None
        assert response['result']
        assert response['result']['rates']
        assert isinstance(response['result']['rates'], dict)
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

