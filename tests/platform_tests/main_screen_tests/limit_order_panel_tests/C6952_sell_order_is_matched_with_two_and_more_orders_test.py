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

test_case = '6952'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    "Sell" Order is matched with two and more Orders, API
    1. Select an instrument(1022).
    2. Place a new "Sell" order with quantity that greater than the sum of the first 2 quantities in Order Book,
     but smaller than the sum of the first 3 orders.
    3. Check sum of quantity for first best price
    4. Check sum of quantity for second best price
    5. Check sum of quantity for third best price
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Sell" Order Is Matched With 2 And More Orders')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/limit_order_panel_tests/C6952_sell_order_is_matched_with_two_and_more_orders_test.py",
                 "TestSellOrderIsMatchedWithTwoAndMoreOrders")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.functional
@pytest.mark.limit_order
@pytest.mark.limit_order_api
@pytest.mark.order_management
class TestSellOrderIsMatchedWithTwoAndMoreOrders(unittest.TestCase):
    @allure.step("SetUp: calling registered customer and updated him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.instrument_id = 1014
        self.customer.clean_instrument(self.instrument_id)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 6, 500000)
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_sell_order_is_matched_with_two_and_more_orders")
    @automation_logger(logger)
    def test_sell_order_is_matched_with_two_and_more_orders(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info(
            "method test_sell_order_is_matched_with_two_and_more_orders")
        result = 0
        try:
            price_tail_digits = Instruments.get_price_tail_digits(self.instrument_id)
            price_1 = Instruments.get_price_last_trade(self.instrument_id)
            quantity_n = Instruments.get_min_order_amount(self.instrument_id)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 100000)
            order_limit_1 = Order().set_order(1, self.instrument_id, quantity_n + 10, price_1)
            order_response_1 = self.customer.postman.order_service.create_order(order_limit_1)
            time.sleep(3.0)
            order_status_1 = order_response_1['result']['status']
            assert order_status_1

            price_2 = round((price_1 + (price_1 * 0.1)), price_tail_digits)
            order_limit_2 = Order().set_order(1, self.instrument_id, quantity_n + 8, price_2)
            order_response_2 = self.customer.postman.order_service.create_order(order_limit_2)
            time.sleep(3.0)
            order_status_2 = order_response_2['result']['status']
            assert order_status_2

            price_3 = round((price_1 + (price_1 * 0.2)), price_tail_digits)
            order_limit_3 = Order().set_order(1, self.instrument_id, quantity_n + 16, price_3)
            order_response_3 = self.customer.postman.order_service.create_order(order_limit_3)
            time.sleep(3.0)
            order_status_3 = order_response_3['result']['status']
            assert order_status_3

            quantity_tail_digits = Instruments.get_quantity_tail_digits(self.instrument_id)
            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument_id, "sell", 2)
            quantity_of_two_best_price = best_price_and_quantity[0][1] + best_price_and_quantity[1][1]
            quantity = round(quantity_of_two_best_price + (quantity_of_two_best_price / 100 * 0.10),
                             quantity_tail_digits)
            price = best_price_and_quantity[2][0]
            order_limit_sell = Order().set_order(2, self.instrument_id, quantity, price)
            order_response = self.customer.postman.order_service.create_order(order_limit_sell)
            time.sleep(7)
            order_status = order_response['result']['status']
            assert order_status
            order_id_query = ("SELECT id FROM orders WHERE customerId = " + str(
                self.customer.customer_id) + " and direction = 'sell' ORDER BY orders.dateInserted DESC limit 1;")
            order_id = str(Instruments.run_mysql_query(order_id_query)[0][0])
            best_price_and_quantity_first = str(best_price_and_quantity[0][0])
            sum_quantity_for_first_best_price_query = ("SELECT SUM(quantity) FROM trades_crypto WHERE price = "
                                                       + best_price_and_quantity_first + " and orderId = " +
                                                       order_id + " and direction = 'sell';")
            sum_quantity_for_first_best_price = float(
                Instruments.run_mysql_query(sum_quantity_for_first_best_price_query)[0][0])
            assert sum_quantity_for_first_best_price == best_price_and_quantity[0][1]
            best_price_and_quantity_second = str(best_price_and_quantity[1][0])
            sum_quantity_for_second_best_price_query = ("SELECT SUM(quantity) FROM trades_crypto WHERE price = " +
                                                        best_price_and_quantity_second + " and orderId = " +
                                                        order_id + " and direction = 'sell';")
            sum_quantity_for_second_best_price = float(
                Instruments.run_mysql_query(sum_quantity_for_second_best_price_query)[0][0])
            assert sum_quantity_for_second_best_price == best_price_and_quantity[1][1]
            best_price_and_quantity_third = str(best_price_and_quantity[2][0])
            sum_quantity_for_third_best_price_query = ("SELECT SUM(quantity) FROM trades_crypto WHERE price = " +
                                                       best_price_and_quantity_third + " and orderId = " +
                                                       order_id + " and direction = 'sell';")
            sum_quantity_for_third_best_price = float(
                Instruments.run_mysql_query(sum_quantity_for_third_best_price_query)[0][0])
            quantity_for_third_best_price = round((quantity - quantity_of_two_best_price), quantity_tail_digits)
            assert sum_quantity_for_third_best_price == quantity_for_third_best_price
            logger.logger.info("sum_quantity_for_first_best_price {0} == {1}".format(sum_quantity_for_first_best_price,
                                                                                     best_price_and_quantity[0][1]))
            logger.logger.info("sum_quantity_for_second_best_price {0} == {1}".format(
                sum_quantity_for_second_best_price, best_price_and_quantity[1][1]))
            logger.logger.info("sum_quantity_for_third_best_price {0} == {1}".format(
                sum_quantity_for_third_best_price, quantity_for_third_best_price))
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1

        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
