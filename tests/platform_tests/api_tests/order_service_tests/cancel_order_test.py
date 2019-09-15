import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

instrument_id = 1008
test_case = "6077"


@allure.feature("Order Management")
@allure.story("Client able to cancel his open order.")
@allure.title("CANCEL ORDER")
@allure.description("""
    Functional api test.
    Test coverage:
    'public_api', 'order_management', 'order_service'
    1 test_cancel_order_limit_buy
    2 test_cancel_order_limit_sell
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='CancelOrder')
@allure.testcase(BaseConfig.API_BASE_URL, "TestCancelOrder")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestCancelOrder(object):
    sleep_delay = 5.0

    @allure.step("Starting: test_cancel_order_limit_buy")
    @automation_logger(logger)
    @pytest.mark.parametrize('create_order_limit_buy', [[instrument_id]], indirect=True)
    def test_cancel_order_limit_buy(self, r_customer, create_order_limit_buy):
        time.sleep(self.sleep_delay)
        response = r_customer.postman.order_service.cancel_order(create_order_limit_buy.external_id)
        assert response['error'] is None

    @allure.step("Starting: test_cancel_order_limit_buy")
    @automation_logger(logger)
    @pytest.mark.parametrize('create_order_limit_buy', [[instrument_id]], indirect=True)
    def test_cancel_order_limit_buy_by_internal_id(self, r_customer, create_order_limit_buy):
        time.sleep(self.sleep_delay)
        response = r_customer.postman.order_service.cancel_order(create_order_limit_buy.internal_id)
        assert response['error'] is None

    @allure.step("Starting: test_cancel_order_limit_sell")
    @automation_logger(logger)
    @pytest.mark.parametrize('create_order_limit_sell', [[instrument_id]], indirect=True)
    def test_cancel_order_limit_sell(self, r_customer, create_order_limit_sell):
        time.sleep(self.sleep_delay)
        response = r_customer.postman.order_service.cancel_order(create_order_limit_sell.external_id)
        assert response['error'] is None

    @allure.step("Starting: test_cancel_order_limit_sell")
    @automation_logger(logger)
    @pytest.mark.parametrize('create_order_limit_sell', [[instrument_id]], indirect=True)
    def test_cancel_order_limit_sell_by_internal_id(self, r_customer, create_order_limit_sell):
        time.sleep(self.sleep_delay)
        response = r_customer.postman.order_service.cancel_order(create_order_limit_sell.internal_id)
        assert response['error'] is None
