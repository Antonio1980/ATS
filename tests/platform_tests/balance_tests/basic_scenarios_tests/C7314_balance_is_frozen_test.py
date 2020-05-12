import time
import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '7314'


@allure.title("BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'total', 'frozen' balance after trying "Buy" and "Sell" Limit order if part of balance
     is frozen, via API.
    1. Half of quoted balance is frozen.
    2. Checking of 'available', 'total', 'frozen' base and quoted currency balances before order.
    3. Trying to place 'Buy' Limit order.
    4. Trying to place 'Sell' Limit order.       
    5. Checking of 'available', 'total', 'frozen' base and quoted currency balances after order. 
    Calculation: available_balance_base_currency_after_orders = half of 'total balance base currency' added in SetUp 
                 available_balance_quoted_currency_after_orders = half of 'total balance quoted currency'added in SetUp
                 frozen_balance_base_currency_after_orders = half of 'total balance base currency' added in SetUp
                 frozen_balance_quoted_currency_after_orders = half of 'total balance quoted currency'added in SetUp 
                 total_balance_base_currency_after_orders =  'total balance base currency' added in SetUp 
                 total_balance_quoted_currency_after_orders =  'total balance quoted currency' added in SetUp
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + '/index.php?/cases/view/' + test_case, name='Balance Is Frozen')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7314_balance_is_frozen_test.py",
                 "TestBalanceIsFrozen")
@pytest.mark.usefixtures("r_time_count", )
@pytest.mark.balance
class TestFrozenBalanceIsNotChangedAfterOrderRejected(unittest.TestCase):

    @allure.step("SetUp:  registration new customer, increase him USD and BTC balance."
                 " Define ID of instrument for order")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id = 1012
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.price_origin = Instruments.get_price_last_trade(self.instrument_id)
        Instruments.set_price_last_trade(self.instrument_id, 5000)
        Instruments.set_ticker_last_price(self.instrument_id, 5000)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 10000)  # USD
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 2)  # BTC
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_balance_is_frozen")
    @automation_logger(logger)
    def test_balance_is_frozen(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method test_balance_is_frozen")
        result = 0
        try:
            price = Instruments.get_price_last_trade(self.instrument_id)
            order_limit1 = Order().set_order(1, self.instrument_id, 1, price)
            order_response1 = self.customer.postman.order_service.create_order(order_limit1)
            time.sleep(3.0)
            self.assertTrue(order_response1['result']['status'], "Status Order1: failed with Error")

            best_price_from_order_book = float(
                round(Instruments.get_orders_best_price_and_quantity(self.instrument_id, "sell", 1)[0]))
            price = best_price_from_order_book + best_price_from_order_book * 0.15
            order_limit2 = Order().set_order(2, self.instrument_id, 1, price)
            order_response2 = self.customer.postman.order_service.create_order(order_limit2)
            time.sleep(8.0)
            self.assertTrue(order_response2['result']['status'], "Status Order2: failed with Error")

            base_before = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 3)
            available_base_before = float(base_before['result']['balance']['available'])
            frozen_base_before = float(base_before['result']['balance']['frozen'])
            total_base_before = float(base_before['result']['balance']['total'])

            quoted_before = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            frozen_quoted_before = float(quoted_before['result']['balance']['frozen'])
            available_quoted_before = float(quoted_before['result']['balance']['available'])
            total_quoted_before = float(quoted_before['result']['balance']['total'])

            assert available_base_before == 1.0
            assert available_quoted_before == 5000.0
            assert frozen_base_before == 1.0
            assert frozen_quoted_before == 5000.0
            assert total_base_before == 2.0
            assert total_quoted_before == 10000.0

            order_limit3 = Order().set_order(1, self.instrument_id, 1, 5001)
            order_response3 = self.customer.postman.order_service.create_order(order_limit3)
            order_error3 = order_response3['error']
            self.assertTrue(order_error3.find('error freezing balance') != -1, "Status Order3: error freezing balance")

            order_limit4 = Order().set_order(2, self.instrument_id, 1.1, price)
            order_response4 = self.customer.postman.order_service.create_order(order_limit4)
            order_error4 = order_response4['error']
            self.assertTrue(order_error4.find('error freezing balance') != -1, "Status Order4: error freezing balance")
            time.sleep(8.0)

            base_after = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 3)
            available_base_after = float(base_after['result']['balance']['available'])
            frozen_base_after = float(base_after['result']['balance']['frozen'])
            total_base_after = float(base_after['result']['balance']['total'])

            quoted_after = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            available_quoted_after = float(quoted_after['result']['balance']['available'])
            frozen_quoted_after = float(quoted_after['result']['balance']['frozen'])
            total_quoted_after = float(quoted_after['result']['balance']['total'])

            assert available_base_after == 1.0
            assert available_quoted_after == 5000.0
            assert frozen_base_after == 1.0
            assert frozen_quoted_after == 5000.0
            assert total_base_after == 2.0
            assert total_quoted_after == 10000.0

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
            Instruments.set_price_last_trade(self.instrument_id, self.price_origin)
            Instruments.set_ticker_last_price(self.instrument_id, self.price_origin)
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
