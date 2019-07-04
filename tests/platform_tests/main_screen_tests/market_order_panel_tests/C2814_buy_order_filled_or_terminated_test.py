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

test_case = '2814'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    Functional test. API 
    "Buy" order is filled or terminated. 
    1. Select an instrument(1022).
    2. Place a new "Buy" order with amount greater than the sum of amounts of all orders from order book.
    3. Get Info about trade from DB
    4. Compare status_id to "2", quantity to amount for trade, filled_quantity to total_amount_order_book 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Buy" order is filled or terminated')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2814_buy_order_filled_or_terminated_test.py",
                 "TestBuyOrderFilledOrTerminated")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.functional
@pytest.mark.market_order
@pytest.mark.order_management
class TestBuyOrderFilledOrTerminated(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance."
                 "Define ID of instrument for 'Buy' order ")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 800000)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.id_instrument = 1022

    @allure.step("Starting with: test_buy_order_filled_or_terminated")
    @automation_logger(logger)
    def test_buy_order_filled_or_terminated(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        result = 0
        try:
            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.id_instrument, "buy", 2)
            total_amount_order_book = sum([y for z, y in best_price_and_quantity if y is not None])
            amount_for_trade = round(total_amount_order_book + (total_amount_order_book / 100 * 2))
            order_market_buy = Order().set_order(1, self.id_instrument, amount_for_trade)
            order_response = self.customer.postman.order_service.create_order(order_market_buy)
            self.assertTrue(order_response['result']['status'])
            time.sleep(10)
            inf_about_trade = Instruments.run_mysql_query(
                "SELECT statusId, quantity, filledQuantity FROM orders WHERE customerId = "
                + str(self.customer.customer_id) +
                " and direction = 'buy' ORDER BY orders.dateInserted DESC limit 1;")
            status_id = inf_about_trade[0][0]
            quantity = float(inf_about_trade[0][1])
            filled_quantity = float(inf_about_trade[0][2])
            self.assertTrue(
                status_id == 2 and quantity == amount_for_trade and filled_quantity == total_amount_order_book)
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
