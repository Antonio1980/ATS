import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Asset Management")
@allure.story("Client able to get and see common info about ticker.")
@allure.title("GET TICKER.")
@allure.description("""
    Functional tests.
    1. test_get_ticker_default
    2. test_get_ticker_per_instrument and currency
    3. test_get_ticker_with not valid currency id (negative)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='GetTicker')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/asset_service_tests/get_ticker_test.py", "TestGetTicker")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.public_api
@pytest.mark.asset_management
@pytest.mark.asset_service
@pytest.mark.regression
class TestGetTicker(object):
    instrument_id = 1007
    currency_id = 1

    @allure.step("Starting with: Getting ticker details by instrument and currency id")
    @automation_logger(logger)
    def test_get_ticker_object(self, r_customer):
        response = r_customer.postman.asset_service.get_ticker(self.instrument_id, self.currency_id)
        assert response["error"] is None
        assert response["result"]['tickers'] != []
        assert isinstance(response["result"]['tickers'], dict)
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: Verifying response via sending not valid Instrument id ")
    @automation_logger(logger)
    def test_get_ticker_object_with_invalid_data(self, r_customer):
        response = r_customer.postman.asset_service.get_ticker(self.instrument_id, "A1q")
        assert 'cannot unmarshal string into Go' in response["error"]
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
