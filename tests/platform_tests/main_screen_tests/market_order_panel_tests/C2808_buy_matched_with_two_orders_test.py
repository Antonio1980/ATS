import time
import unittest
import allure
import pytest
from src.base import logger
from src.base.data_bases.sql_db import SqlDb
from src.base.equipment.order import Order
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '2808'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    Functional test. API
    "Buy" order is matched with two and more orders. 
    1. Select an instrument(1022).
    2. Place a new "Buy" order with amount greater than the sum of the first orders from order book.
    3. Get the sum of amount first price from Order Book / Compare amount from DB by Order Id to Amount from Order Book 
    4. Get the sum of amount second price from Order Book / Compare amount from DB by Order Id to Amount from Order Book
    5. Get the sum of amount third price from Order Book / Compare amount from DB by Order Id to Amount from Order Book
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Buy" order is matched with 2 and more orders')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2808_buy_matched_with_two_orders_test.py",
                 "TestBuyMatchedWithTwoOrders")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.functional
@pytest.mark.market_order
@pytest.mark.order_management
class TestBuyMatchedWithTwoOrders(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance."
                 "Define ID of instrument for 'Buy' order ")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 48, 15000000)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.instrument = 1022

    @allure.step("Starting with:test_buy_matched_with_two_orders")
    @automation_logger(logger)
    def test_buy_matched_with_two_orders(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        result = 0
        try:
            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument, "buy", 2)[:50]
            quantity_of_two_best_price = best_price_and_quantity[0][1] + best_price_and_quantity[1][1]
            tail_digits = SqlDb.get_quantity_tail_digits(self.instrument)
            if tail_digits == 0:
                order_quantity = round(quantity_of_two_best_price + (quantity_of_two_best_price / 100 * 0.01),
                                       tail_digits)
            else:
                order_quantity = round(quantity_of_two_best_price + (quantity_of_two_best_price / 100 * 0.01),
                                       tail_digits)

            order_market_buy = Order().set_order(1, self.instrument, order_quantity)
            order_response = self.customer.postman.order_service.create_order(order_market_buy)
            order_status = order_response['result']['status']
            self.assertTrue(order_status)
            time.sleep(3)

            order_id = str(Instruments.run_mysql_query(
                "SELECT id FROM orders WHERE customerId = " + str(self.customer.customer_id) +
                " and direction = 'buy' ORDER BY orders.dateInserted DESC limit 1;")[0][0])

            best_price_and_quantity_first = str(best_price_and_quantity[0][0])
            sum_quantity_for_first_best_price = float(
                Instruments.run_mysql_query("SELECT SUM(quantity) FROM trades_crypto WHERE price = "
                                            + best_price_and_quantity_first + " and orderId = " + order_id +
                                            " and direction = 'buy';")[0][0])
            self.assertTrue(sum_quantity_for_first_best_price == best_price_and_quantity[0][1])

            best_price_and_quantity_second = str(best_price_and_quantity[1][0])
            sum_quantity_for_second_best_price = float(
                Instruments.run_mysql_query("SELECT SUM(quantity) FROM trades_crypto WHERE price = " +
                                            best_price_and_quantity_second + " and orderId = " + order_id +
                                            " and direction = 'buy';")[0][0])
            self.assertTrue(sum_quantity_for_second_best_price == best_price_and_quantity[1][1])

            best_price_and_quantity_third = str(best_price_and_quantity[2][0])
            sum_quantity_for_third_best_price = float(
                Instruments.run_mysql_query("SELECT SUM(quantity) FROM trades_crypto WHERE price = " +
                                            best_price_and_quantity_third + " and orderId = " + order_id +
                                            " and direction = 'buy';")[0][0])
            if tail_digits == 0:
                quantity_for_third_best_price = round((order_quantity - quantity_of_two_best_price))
            else:
                quantity_for_third_best_price = round((order_quantity - quantity_of_two_best_price), tail_digits)
            self.assertTrue(sum_quantity_for_third_best_price == quantity_for_third_best_price)
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
