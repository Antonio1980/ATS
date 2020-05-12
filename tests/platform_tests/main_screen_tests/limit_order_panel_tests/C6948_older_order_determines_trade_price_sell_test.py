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

test_case = '6948'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    API test.
    Older order determines the trade price - "Sell"
    1. Select an instrument(1022).
    2. Place a new "Sell" order with price between the first and the second price from Order Book and quantity
     is equals or smaller than the quantity offered for sale in the first order.
    3. Verify that Order is saved correctly in DB
    4. 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Older order determines the trade price - "Sell"')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/main_screen_tests/limit_order_panel_tests/C6948_older_order_determines_trade_price_sell_test.py",
    "TestOlderOrderDeterminesTradePriceSell")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.functional
@pytest.mark.limit_order
@pytest.mark.limit_order_api
@pytest.mark.order_management
class TestOlderOrderDeterminesTradePriceSell(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.instrument_id = 1014
        self.customer.clean_instrument(self.instrument_id)
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 8, 50000.0)  # EUR
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_older_order_determines_trade_price_sell")
    @automation_logger(logger)
    def test_older_order_determines_trade_price_sell(self):
        result = 0
        try:
            price_1 = Instruments.get_price_last_trade(self.instrument_id)
            quantity = Instruments.get_min_order_amount(self.instrument_id)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 50000.0)
            order_limit_1 = Order().set_order(1, self.instrument_id, quantity + 50, price_1)
            order_response_1 = self.customer.postman.order_service.create_order(order_limit_1)
            time.sleep(3.0)
            order_status_1 = order_response_1['result']['status']
            assert order_status_1

            price_tail_digits = Instruments.get_price_tail_digits(self.instrument_id)
            price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument_id, "sell", 2)
            quantity = price_and_quantity[0][1]
            price = round(price_and_quantity[0][0] - (price_and_quantity[0][0] * 0.001), price_tail_digits)
            order_limit_buy = Order().set_order(2, self.instrument_id, quantity, price)
            order_response = self.customer.postman.order_service.create_order(order_limit_buy)
            time.sleep(7)
            order_status = order_response['result']['status']
            assert order_status

            order_id = str(Instruments.run_mysql_query("SELECT id FROM orders WHERE customerId = " + str(
                self.customer.customer_id) + " and direction = 'sell'ORDER BY orders.dateInserted DESC limit 1;")[0][0])
            best_price_first = float(price_and_quantity[0][0])
            price_from_order = float(Instruments.run_mysql_query(
                "SELECT price FROM trades_crypto WHERE orderId = " + order_id +
                " and direction = 'sell' GROUP BY price; ")[0][0])
            assert best_price_first == price_from_order
            logger.logger.info("best_price_first {0} == price_from_order {1}".format(best_price_first, price_from_order))
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
