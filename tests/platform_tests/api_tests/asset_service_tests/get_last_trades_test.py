import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Asset Management")
@allure.story("Client able to get records info about last trade.")
@allure.title("GET LAST TRADE")
@allure.description("""
    Functional tests.

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Get Last Trade')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/asset_service_tests/get_last_trade_test.py", "TestGetLastTrades")
@pytest.mark.usefixtures("r_time_count", 'r_customer')
@pytest.mark.asset_management
@pytest.mark.asset_service
@pytest.mark.regression
class TestGetLastTrades(object):
    instrument_id = 1008

    @allure.step("")
    @automation_logger(logger)
    def test_get_last_trades_method_works(self, r_customer):
        response = r_customer.postman.asset_service.get_last_trades(self.instrument_id)
        assert response["error"] is None
        
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("")
    @automation_logger(logger)
    def test_get_last_trades_method(self, r_customer):
        response = r_customer.postman.asset_service.get_last_trades(self.instrument_id)
        assert response["error"] is None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
