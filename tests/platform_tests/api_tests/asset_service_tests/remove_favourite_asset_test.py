import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = ""
instrument_id = 1012


@allure.feature("Asset Management")
@allure.story("Client able to remove favourite asset from Asset Panel (unset favourite one).")
@allure.title("REMOVE FAVOURITE ASSET.")
@allure.description("""
    Functional tests.
    1. test_remove_favourite_asset
    2. test_set_favourite_asset_without_authorization_negative
   """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='RemoveFavouriteAsset')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/asset_service_tests/remove_favourite_asset_test.py",
                 "TestRemoveFavouriteAsset")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.asset_management
@pytest.mark.asset_service
@pytest.mark.regression
class TestRemoveFavouriteAsset(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        return Customer()

    @allure.step("Starting with: Removing the favourite asset by instrument id for logged in customer")
    @automation_logger(logger)
    def test_remove_favourite_asset(self, r_customer):
        response = r_customer.postman.asset_service.set_favorite_instrument(instrument_id)
        assert response["error"] is None

        response = r_customer.postman.asset_service.remove_favorite_instrument(instrument_id)
        assert response["error"] is None
        assert isinstance(response, dict)
        assert response != {}

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: Try to remove favourite asset without authorization - negative")
    @automation_logger(logger)
    def test_remove_favourite_asset_without_authorization_negative(self, another_customer):
        response = another_customer.postman.asset_service.remove_favorite_instrument(instrument_id)
        assert response["error"] == 'forbidden'

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
