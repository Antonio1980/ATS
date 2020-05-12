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

test_case = '2828'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    Functional test. API
    Amount verification against Available Funds
    1. Select an instrument(1007).
    2. Enter an amount of base currency ("Buy" section)- "Estimate Price" * "Amount" * buffer ( 1% - hardcoded)
       mustn't exceed the available funds and click on the "Buy" button  / Check - Order was placed successfully
    3. Enter an amount of quoted currency ("Sell" section) - it mustn't exceed the available funds ("Available for 
       trading") and click on the "Sell" button / Check - Order was placed successfully    
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Amount verification against Available Funds')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2828_amount_verification_against_funds_test.py",
                 "TestAmountVerificationAgainstFunds")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.functional
@pytest.mark.market_order
@pytest.mark.order_management
class TestAmountVerificationAgainstFunds(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance."
                 "Define ID of instrument")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 1, 50000)  # USD currency
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 3, 20)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.id_instrument = 1007

    @allure.step("Starting with:test_amount_verification_against_funds")
    @automation_logger(logger)
    def test_amount_verification_against_funds(self):
        result = 0
        try:
            price_and_quantity_sell = Instruments.get_orders_best_price_and_quantity(self.id_instrument, "sell", 1)
            quantity_sell = price_and_quantity_sell[1]
            price_sell = price_and_quantity_sell[0]
            tail_digits = SqlDb.get_quantity_tail_digits(self.id_instrument)
            if tail_digits == 0:
                order_quantity_sell = round(quantity_sell - (quantity_sell / 100 * 20))
            else:
                order_quantity_sell = round(quantity_sell - (quantity_sell / 100 * 20), tail_digits)
            order_market_sell = Order().set_order(2, self.id_instrument, order_quantity_sell)
            order_response_sell = self.customer.postman.order_service.create_order(order_market_sell)
            assert (order_response_sell['result']['status'])
            time.sleep(2)
            id_trade_crypto_sell = str(Instruments.run_mysql_query(
                "SELECT id FROM trades_crypto WHERE customerId = " + str(self.customer.customer_id) +
                " and direction = 'sell' ORDER BY trades_crypto.executionDate DESC limit 1;")[0][0])
            price_from_trade_buy = float((Instruments.run_mysql_query(
                "SELECT price  FROM trades_crypto WHERE id = " + id_trade_crypto_sell + ";")[0][0]))
            assert price_from_trade_buy == price_sell
            price_and_quantity_buy = Instruments.get_orders_best_price_and_quantity(self.id_instrument, "buy", 1)
            quantity_buy = price_and_quantity_buy[1]
            price_buy = price_and_quantity_buy[0]
            if tail_digits == 0:
                order_quantity_buy = round(quantity_buy - (quantity_buy / 100 * 20))
            else:
                order_quantity_buy = round(quantity_buy - (quantity_buy / 100 * 20), tail_digits)
            order_market_buy = Order().set_order(1, self.id_instrument, order_quantity_buy)
            order_response_buy = self.customer.postman.order_service.create_order(order_market_buy)
            assert (order_response_buy['result']['status'])
            time.sleep(2)
            id_trade_crypto_buy = str(Instruments.run_mysql_query(
                "SELECT id FROM trades_crypto WHERE customerId = " + str(self.customer.customer_id) +
                " and direction = 'buy' ORDER BY trades_crypto.executionDate DESC limit 1;")[0][0])
            price_from_trade_sell = float((Instruments.run_mysql_query(
                "SELECT price  FROM trades_crypto WHERE id = " + id_trade_crypto_buy + ";")[0][0]))
            assert price_from_trade_sell == price_buy
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
