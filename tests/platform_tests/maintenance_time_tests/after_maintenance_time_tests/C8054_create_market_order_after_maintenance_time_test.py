import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '8055'


@allure.title("After Maintenance Time")
@allure.description("""
    Verification  that there is no ability to generate order. API test
    1. Get me-state 
    2. Verify that me-state equal 1 (Trading time)
    3. Generate Market Buy order
    4. Verify that there is  ability to generate order.
    3. Generate Market Sell order
    4. Verify that there is  ability to generate order.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Generate the Order Market after Maintenance time via API')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/maintenance_time_tests/after_maintenance_time_tests/C8054_create_market_order_after_maintenance_time.py",
    "TestCreateMarketOrderAfterMaintenanceTime")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.after_maintenance_time
class TestCreateMarketOrderAfterMaintenanceTime(unittest.TestCase):
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
    @allure.step("Starting with: test_create_market_order_after_maintenance_time")
    def test_create_market_order_after_maintenance_time(self):
        assert self.state_me == 1
        order_market_buy = Order().set_order(1, self.instrument_id, 0.5)
        order_market_sell = Order().set_order(2, self.instrument_id, 1)
        order_response_buy_market = self.postman.create_order(order_market_buy)
        order_status = order_response_buy_market['result']['status']
        assert order_status is True
        order_response_sell_market = self.postman.create_order(order_market_sell)
        order_status = order_response_sell_market['result']['status']
        assert order_status is True
        logger.logger.info("Test {0} PASSED, with CustomerID {1}".format(test_case, self.customer.customer_id))
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
