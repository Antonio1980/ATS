import time
import unittest
import allure
import pytest
from src.base import logger
from src.base.equipment.order import Order
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '6938'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    No trade if the price is too high, API
    1. Select an instrument(1007).
    2. Find the best price offered(the lowest) from Order Book
    3. Place a "Buy" order with a price that is much lower then the "Best price" offered 
    4. Verify that the order you placed wasn't matched
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='No trade if the price is too high')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6938_no_trade_if_price_is_too_high_test.py",
                 "TestNoTradeIfPriceIsTooHigh")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.functional
@pytest.mark.limit_order
@pytest.mark.limit_order_api
@pytest.mark.order_management
class TestNoTradeIfPriceIsTooHigh(unittest.TestCase):
    @allure.step("SetUp: calling registered  and updated him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.instrument_id = 1012
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        Instruments.set_price_last_trade(self.instrument_id, 5000)
        Instruments.set_ticker_last_price(self.instrument_id, 5000)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 10000)
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_no_trade_if_price_is_too_high")
    @automation_logger(logger)
    def test_no_trade_if_price_is_too_high(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_no_trade_if_price_is_too_high")
        result = 0
        try:
            price_tail_digits = Instruments.get_price_tail_digits(self.instrument_id, )
            price_1 = Instruments.get_price_last_trade(self.instrument_id)
            quantity = Instruments.get_min_order_amount(self.instrument_id)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 10000)
            order_limit_1 = Order().set_order(2, self.instrument_id, quantity, price_1)
            order_response_1 = self.customer.postman.order_service.create_order_sync(order_limit_1)
            time.sleep(4.0)
            assert order_response_1['error'] is None
            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 1)
            price = round((best_price_and_quantity[0] - (best_price_and_quantity[0] * 0.1)), price_tail_digits)
            order_limit_buy = Order().set_order(1, self.instrument_id, quantity, price)
            order_response = self.customer.postman.order_service.create_order_sync(order_limit_buy)
            time.sleep(7.0)
            assert order_response['error'] is None

            order_id = order_response['result']['orderId']
            data_order = Instruments.run_mysql_query("SELECT filledQuantity, price, quantity FROM orders WHERE id = "
                                                     + order_id + " and direction = 'buy';")
            filled_quantity = data_order[0][0]
            price_db = float(data_order[0][1])
            quantity_db = float(data_order[0][2])

            assert filled_quantity == 0
            assert price == price_db
            assert quantity == quantity_db
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
