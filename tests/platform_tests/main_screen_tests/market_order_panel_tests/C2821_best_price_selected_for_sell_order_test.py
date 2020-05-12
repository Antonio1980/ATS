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

test_case = '2821'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    Functional test. API 
    Verified that "Sell" order matched with the best price. 
    1. Select an instrument(1046).
    2. Place a new "Sell" order with amount smaller than the quantity of the first order from order book.
    3. Get Info about trade from DB
    4. Compare price from trade to the best price from Order Book.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Sell" order - best price is selected.')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2821_best_price_selected_for_sell_order_test.py",
                 "TestBestPriceSelectedForSellOrder")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.functional
@pytest.mark.market_order
@pytest.mark.order_management
class TestBestPriceSelectedForSellOrder(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance."
                 "Define ID of instrument for 'Sell' order ")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 13, 500)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.id_instrument = 1046

    @allure.step("Starting with: test_best_price_selected_for_sell_order")
    @automation_logger(logger)
    def test_best_price_selected_for_sell_order(self):
        result = 0
        try:
            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.id_instrument, "sell", 1)
            quantity = best_price_and_quantity[1]
            price = best_price_and_quantity[0]
            tail_digits = Instruments.get_quantity_tail_digits(self.id_instrument)
            if tail_digits == 0:
                order_quantity = round(quantity - (quantity / 100 * 20))
            else:
                order_quantity = round(quantity - (quantity / 100 * 20), tail_digits)
            order_market_buy = Order().set_order(2, self.id_instrument, order_quantity)
            order_response = self.customer.postman.order_service.create_order(order_market_buy)
            self.assertTrue(order_response['result']['status'])
            time.sleep(3)
            id_trade_crypto = str(Instruments.run_mysql_query(
                "SELECT id FROM trades_crypto WHERE customerId = " + str(self.customer.customer_id) +
                " and direction = 'sell' ORDER BY trades_crypto.executionDate DESC limit 1;")[0][0])
            query_price_from_trade = "SELECT price  FROM trades_crypto WHERE id = " + id_trade_crypto + ";"
            price_from_trade = float((Instruments.run_mysql_query(query_price_from_trade)[0][0]))
            self.assertTrue(price_from_trade == price)
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
