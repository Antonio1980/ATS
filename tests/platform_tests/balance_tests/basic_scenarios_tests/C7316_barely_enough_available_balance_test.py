import time
import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = '7316'


@allure.title("API BALANCE")
@allure.description("""
    Functional test
    Validation of 'available', 'total', 'frozen' base and quoted currency balances after "Buy" and "Sell" Limit orders
     using exactly 100% of available balance.
    1. Checking of 'available', 'total', 'frozen' base and quoted currency balances before 'Buy' and 'Sell' order.
    2. Place 'Buy' Limit order using all available balance for that currency.
    3. Place 'Sell' Limit order sing all available balance for that currency.
    4. Checking of 'available', 'total', 'frozen' base and quoted currency balances after 'Buy' and 'Sell' order
    Calculation: frozen_balance_base_currency_after_orders = total_balance_base_currency_after_orders 
                 frozen_balance_quoted_currency_after_orders = total_balance_quoted_currency_after_orders
                 available_balance_base_currency_after_orders = 0.0 
                 available_balance_quoted_currency_after_orders = 0.0 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Barely Enough Available Balance')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7316_barely_enough_available_balance_test.py",
                 "TestBarelyEnoughAvailableBalance")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestBarelyEnoughAvailableBalance(unittest.TestCase):
    @allure.step("SetUp:  registration new customer, increase him USD and BTC balance."
                 " Define ID of instrument for order")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id = 1012
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.price_origin = Instruments.get_price_last_trade(self.instrument_id)
        Instruments.set_price_last_trade(self.instrument_id, 500)
        Instruments.set_ticker_last_price(self.instrument_id, 500)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 1000)  # USD
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 2)  # BTC
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step(
        "Starting with: test_barely_enough_available_balance")
    @automation_logger(logger)
    def test_barely_enough_available_balance(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method test_barely_enough_available_balance =['balance', ]), ")
        result = 0
        try:
            order_limit1 = Order().set_order(1, self.instrument_id, 1, 500)
            order_response1 = self.customer.postman.order_service.create_order(order_limit1)
            order_status1 = order_response1['result']['status']
            self.assertTrue(order_status1, "Status Order1: failed with Error")

            best_price_from_order_book = float(
                round(Instruments.get_orders_best_price_and_quantity(self.instrument_id, "sell", 1)[0]))
            price = best_price_from_order_book + best_price_from_order_book * 0.15
            order_limit2 = Order().set_order(2, self.instrument_id, 1, price)
            order_response2 = self.customer.postman.order_service.create_order(order_limit2)
            order_status2 = order_response2['result']['status']
            self.assertTrue(order_status2, "Status Order2: failed with Error")

            base_before = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 3)
            available_base_before = float(base_before['result']['balance']['available'])
            frozen_base_before = float(base_before['result']['balance']['frozen'])
            total_base_before = float(base_before['result']['balance']['total'])

            quoted_before = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            frozen_quoted_before = float(quoted_before['result']['balance']['frozen'])
            available_quoted_before = float(quoted_before['result']['balance']['available'])
            total_balance_quoted_before_order = float(quoted_before['result']['balance']['total'])

            self.assertTrue(available_base_before == 1.0)
            self.assertTrue(available_quoted_before == 500.0)
            self.assertTrue(frozen_base_before == 1.0)
            self.assertTrue(frozen_quoted_before == 500.0)
            self.assertTrue(total_base_before == 2.0)
            self.assertTrue(total_balance_quoted_before_order == 1000.0)

            order_limit3 = Order().set_order(1, self.instrument_id, 1, 500)
            order_response3 = self.customer.postman.order_service.create_order(order_limit3)
            order_status3 = order_response3['result']['status']
            self.assertTrue(order_status3, "Status Order3: failed with Error")

            order_limit4 = Order().set_order(2, self.instrument_id, 1, price)
            order_response4 = self.customer.postman.order_service.create_order(order_limit4)
            order_status4 = order_response4['result']['status']
            self.assertTrue(order_status4, "Status Order4: failed with Error")
            time.sleep(3)

            base_after = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 3)
            available_base_after = float(base_after['result']['balance']['available'])
            frozen_base_after = float(base_after['result']['balance']['frozen'])
            total_base_after = float(base_after['result']['balance']['total'])

            quoted_after = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            available_quoted_after = float(quoted_after['result']['balance']['available'])
            frozen_quoted_after = float(quoted_after['result']['balance']['frozen'])
            total_quoted_after = float(
                quoted_after['result']['balance']['total'])

            self.assertTrue(available_base_after == 0.0)
            self.assertTrue(available_quoted_after == 0.0)
            self.assertTrue(frozen_base_after == 2.0)
            self.assertTrue(frozen_quoted_after == 1000.0)
            self.assertTrue(total_base_after == 2.0)
            self.assertTrue(total_quoted_after == 1000.0)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            Instruments.set_price_last_trade(self.instrument_id, self.price_origin)
            Instruments.set_ticker_last_price(self.instrument_id, self.price_origin)
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
