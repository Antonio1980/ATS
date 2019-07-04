import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = ""
instrument_id = 1012


@allure.feature("Asset Management")
@allure.story("Client able to set favourite asset at the Asset Panel.")
@allure.title("SET FAVOURITE ASSET.")
@allure.description("""
    Functional tests.
    1. test_set_favourite_asset
    2. test_set_favourite_asset_without_login
   """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='SetFavouriteAsset')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/asset_service_tests/set_favourite_asset_test.py",
                 "SetFavouriteAsset")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.public_api
@pytest.mark.asset_management
@pytest.mark.asset_service
@pytest.mark.regression
class TestSetFavouriteAsset(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        return Customer()

    @allure.step("Starting with: Setting the favourite asset by instrument id for logged in customer")
    @automation_logger(logger)
    def test_set_favourite_asset(self, r_customer):
        response = r_customer.postman.asset_service.set_favorite_instrument(instrument_id)
        assert response["error"] is None
        assert isinstance(response, dict)
        assert response != {}
        assert str(r_customer.customer_id) == response['result']['customerId']
        assert instrument_id == response['result']['instrumentId']
        assert response['result']['status']
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: Setting the favourite asset by instrument id for not logged in customer (negative)")
    @automation_logger(logger)
    def test_set_favourite_asset_without_login(self, another_customer):
        response = another_customer.postman.asset_service.set_favorite_instrument(instrument_id)
        assert response["error"] == 'forbidden'
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
