import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "6067"


@allure.feature("Asset Management")
@allure.story("Client able to get records info about assets.")
@allure.title("GET ASSET HISTORY.")
@allure.description("""
    Functional tests.
    1. test_get_asset_history (with instrument: 1012)
    2. test_get_asset_history_default (without instrument)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Asset History')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/asset_service_tests/get_asset_history_test.py", "TestAssetHistory")
@pytest.mark.usefixtures("r_time_count", 'r_customer')
@pytest.mark.asset_management
@pytest.mark.asset_service
@pytest.mark.regression
class TestAssetHistory(object):
    instrument_id = 1012
    asset_type = ["1m", "5m", "1h", "1d"]

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        return Customer()

    @allure.step("Starting with: Getting asset history without authorization default")
    @automation_logger(logger)
    def test_get_asset_history_without_authorization_default(self, another_customer):
        for x in self.asset_type:
            response = another_customer.postman.asset_service.get_history(self.instrument_id, x)
            assert response["error"] is None
            assert isinstance(response["result"]['assets'], list)
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @automation_logger(logger)
    def test_get_asset_history_without_authorization(self, another_customer):
        for x in self.asset_type:
            response = another_customer.postman.asset_service.get_history(self.instrument_id, x)
            assert response["error"] is None
            assert response["result"]['assets'] != []
            for index in range(len('assets')):
                assert self.instrument_id == response['result']['assets'][index]['instrumentId']
                assert x == response['result']['assets'][index]['type']
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: Getting asset history with authorization")
    @automation_logger(logger)
    def test_get_asset_history_with_authorization_default(self, r_customer):
        for x in self.asset_type:
            response = r_customer.postman.asset_service.get_history(self.instrument_id, x)
            assert response["error"] is None
            assert isinstance(response["result"]['assets'], list)

    @automation_logger(logger)
    def test_get_asset_history_with_authorization(self, r_customer):
        for x in self.asset_type:
            response = r_customer.postman.asset_service.get_history(self.instrument_id, x)
            assert response["error"] is None
            assert response["result"]['assets'] != []
            for index in range(len('assets')):
                assert self.instrument_id == response['result']['assets'][index]['instrumentId']
                assert x == response['result']['assets'][index]['type']
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
