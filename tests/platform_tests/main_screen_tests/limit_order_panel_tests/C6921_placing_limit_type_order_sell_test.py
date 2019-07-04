import time
import unittest

import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage

test_case = '6921'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    api test.
    Verify that the values in the DB are identical to those set after placing Sell order , API
    1. Place Sell order
    2. Verify that the values in the DB are identical to those set:
       Amount, Price, Direction, Instrument ID, Customer ID, Order Type (Limit) 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Placing "Limit" type order - "Sell"')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6921_placing_limit_type_order_sell_test.py",
    "TestPlacingLimitTypeOrderSell")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.limit_order
@pytest.mark.order_management
class PlacingLimitTypeOrderSellTest(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 5)  # BTC crypto
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()
        self.instrument_id = 1007

    @allure.step("Starting with: test_placing_limit_type_order_sell")
    @automation_logger(logger)
    def test_placing_limit_type_order_sell(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_placing_limit_type_order_sell ")

        result = 0
        try:
            enter_amount = Instruments.get_min_order_amount(self.instrument_id)
            estimated_price = Instruments.get_price_last_trade(self.instrument_id)
            order_limit_sell = Order().set_order(2, self.instrument_id, enter_amount, estimated_price)
            order_response = self.customer.postman.order_service.create_order_sync(order_limit_sell)
            time.sleep(5.0)
            assert order_response['error'] is None

            order_id = order_response['result']['orderId']

            data_of_order_query = ("""
                SELECT orders.id,  orders.customerId, orders.instrumentId, orders.direction, orders.price, 
                orders.quantity, order_types.name, orders.dateInserted FROM orders JOIN order_types ON 
                order_types.id = orders.typeId WHERE orders.id = """ + order_id + """;""")

            data_of_order = Instruments.run_mysql_query(data_of_order_query)
            assert float(data_of_order[0][5]) == enter_amount
            assert float(data_of_order[0][4]) == float(estimated_price)
            assert data_of_order[0][3] == 'sell'
            assert data_of_order[0][2] == self.instrument_id
            assert data_of_order[0][1] == self.customer.customer_id
            assert data_of_order[0][6] == 'limit'
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1

        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
