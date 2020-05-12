import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '7178'


@allure.title("Maintenance Time")
@allure.description("""
    Verification  that there is no ability to generate order. API test
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Generate Limit Buy order
    4. Verify that there is  no ability to generate order.
    3. Generate Limit Sell order
    4. Verify that there is  no ability to generate order.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Generate the Order Limit during Maintenance time via API')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/maintenance_time_tests/C7178_create_limit_order_at_maintenance_time_test.py",
    "TestCreatLimitOrderDuringMaintenanceTime")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.maintenance_time
class TestCreatLimitOrderDuringMaintenanceTime(unittest.TestCase):
    @automation_logger(logger)
    @allure.step("SetUp: calling registered customer, get me-state, increase customer's balance")
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.state_me = Instruments.get_me_state()
        self.instrument_id = 1007
        self.price = Instruments.get_price_last_trade(self.instrument_id)
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 1, 5000)
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 3, 2)

    @automation_logger(logger)
    @allure.step("Starting with: test_create_limit_order_during_maintenance_time")
    def test_create_market_limit_orders_during_maintenance_time(self):
        assert self.state_me == 2
        order_limit_buy = Order().set_order(1, self.instrument_id, 1, self.price)
        order_limit_sell = Order().set_order(2, self.instrument_id, 1, self.price)
        order_response_buy_limit = self.customer.postman.order_service.create_order(order_limit_buy)
        order_error_buy_limit = order_response_buy_limit['error']
        assert 'order_creation.matching_engine.trading_disabled' in order_error_buy_limit
        order_response_sell_limit = self.customer.postman.order_service.create_order(order_limit_sell)
        order_error_sell_limit = order_response_sell_limit['error']
        assert 'order_creation.matching_engine.trading_disabled' in order_error_sell_limit
        logger.logger.info("Test {0} PASSED, with CustomerID {1}".format(test_case, self.customer.customer_id))
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
