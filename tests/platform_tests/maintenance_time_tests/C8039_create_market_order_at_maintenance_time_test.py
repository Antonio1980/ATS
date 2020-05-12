import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '8039'


@allure.title("Maintenance Time")
@allure.description("""
    Verification  that there is no ability to generate order. API test
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Generate Market Buy order
    4. Verify that there is  no ability to generate order.
    3. Generate Market Sell order
    4. Verify that there is  no ability to generate order.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Generate the Order Market during Maintenance time via API')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/maintenance_time_tests/C8039_create_market_order_at_maintenance_time_test.py",
    "TestCreateMarketOrderDuringMaintenanceTime")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.maintenance_time
class TestCreateMarketOrderDuringMaintenanceTime(unittest.TestCase):
    @automation_logger(logger)
    @allure.step("SetUp: calling registered customer, get me-state, increase customer's balance")
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.state_me = Instruments.get_me_state()
        self.instrument_id = 1007
        self.last_trade = Instruments.get_price_last_trade(self.instrument_id)
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 1, 5000)
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 3, 2)

    @automation_logger(logger)
    @allure.step("Starting with: test_create_market_order_during_maintenance_time")
    def test_create_market_order_during_maintenance_time(self):
        assert self.state_me == 2
        order_market_buy = Order().set_order(1, self.instrument_id, 0.5)
        order_market_sell = Order().set_order(2, self.instrument_id, 1)
        order_response_buy_market = self.postman.create_order(order_market_buy)
        order_error_buy_market = order_response_buy_market['error']
        assert 'order_creation.matching_engine.trading_disabled' in order_error_buy_market
        order_response_sell_market = self.postman.create_order(order_market_sell)
        order_error_sell_market = order_response_sell_market['error']
        assert 'order_creation.matching_engine.trading_disabled' in order_error_sell_market
        logger.logger.info("Test {0} PASSED, with CustomerID {1}".format(test_case, self.customer.customer_id))
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
