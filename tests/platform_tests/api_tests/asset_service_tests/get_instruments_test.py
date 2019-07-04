import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "7781"


@allure.feature("Asset Management")
@allure.story("Client able to get and see common info about instrument.")
@allure.title("GET INSTRUMENTS.")
@allure.description("""
    Functional tests.
    1. test_get_instruments_default (without)
    2. test_get_instruments_per_symbol (without symbol)
    3. test_get_instruments_per_symbol_and_product (with symbol and instrument)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Get Instruments')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/asset_service_tests/get_instruments_test.py", "TestGetInstruments")
@pytest.mark.usefixtures("r_time_count", )
@pytest.mark.asset_management
@pytest.mark.asset_service
@pytest.mark.regression
class TestGetInstruments(object):
    ver_token = None

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        return Customer()

    @allure.step("Starting with: test_get_instruments_default")
    @automation_logger(logger)
    def test_get_instruments_default(self, another_customer):
        response = another_customer.postman.asset_service.get_instruments()
        assert response["error"] is None
        assert isinstance(response["result"]['instruments'], list)
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_get_instruments_per_symbol")
    @automation_logger(logger)
    def test_get_instruments_per_symbol(self, another_customer):
        symbol = 'BTC/USD'
        response = another_customer.postman.asset_service.get_instruments(symbol)
        assert response["error"] is None
        assert isinstance(response["result"]['instruments'], list)
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_get_instruments_per_symbol_and_product")
    @automation_logger(logger)
    def test_get_instruments_per_symbol_and_product(self, another_customer):
        symbol = 'BTC/USD'
        product_id = 1013
        response = another_customer.postman.asset_service.get_instruments(symbol, product_id)
        assert response["error"] is None
        assert isinstance(response["result"]['instruments'], list)
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
