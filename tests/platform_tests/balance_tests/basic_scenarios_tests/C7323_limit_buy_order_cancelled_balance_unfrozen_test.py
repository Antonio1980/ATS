import time
import unittest
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '7323'


@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'frozen' balance after canceled "Buy" Limit order via API
    1. Checking of 'available', 'frozen' balances before order.
    2. Place 'Buy' Limit order.
    3. Checking of 'available', 'frozen' balances after order.
    4. Cancel 'Buy' Limit order.
    3. Checking of 'available', 'frozen' balances after cancel. 
    Calculation formula: available_balance_base_after_cancel = available_balance_base_before_order
                         available_balance_quoted_after_cancel = available_balance_quoted_before_order
                         frozen_balance_quoted_after_cancel = frozen_balance_quoted_before_order
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Limit Buy Order Cancelled - Unfrozen')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7323_limit_buy_order_cancelled_balance_unfrozen_test.py",
                 "TestUnfrozenBalanceAfterOrderLimitBuyCanceled")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestBuyLimitCanceledOrderUnfrozenBalance(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him USD balance."
                 " Define ID of instrument for 'Buy' order")
    def setUp(self):
        self.instrument_id = 1012
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.price_origin = Instruments.get_price_last_trade(self.instrument_id)
        Instruments.set_price_last_trade(self.instrument_id, 5000)
        Instruments.set_ticker_last_price(self.instrument_id, 5000)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 10000)  # USD
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_buy_limit_canceled_order_unfrozen_balance")
    @automation_logger(logger)
    def test_buy_limit_canceled_order_unfrozen_balance(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method test_buy_limit_canceled_order_unfrozen_balance")
        result = 0
        try:
            available_base_before = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)['result'][
                    'balance']['available'])

            balance_quoted_before = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            available_quoted_before = float(balance_quoted_before['result']['balance']['available'])
            frozen_quoted_before = float(balance_quoted_before['result']['balance']['frozen'])

            price = Instruments.get_price_last_trade(self.instrument_id)
            quantity = 1
            order_limit_buy = Order().set_order(1, self.instrument_id, quantity, price)
            order_response = self.customer.postman.order_service.create_order(order_limit_buy)
            order_status = order_response['result']['status']
            self.assertTrue(order_status, "Status Order failed with Error")
            external_order_id = order_response['result']['externalOrderId']
            time.sleep(5)

            available_base_after = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)['result'][
                    'balance']['available'])

            quoted_after = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            available_quoted_after = float(quoted_after['result']['balance']['available'])
            frozen_quoted_after = float(quoted_after['result']['balance']['frozen'])

            self.assertTrue(available_base_before == available_base_after)
            self.assertTrue(available_quoted_after == available_quoted_before - price)
            self.assertTrue(frozen_quoted_after == frozen_quoted_before + price)
            time.sleep(5)

            cancel_order_response = self.customer.postman.order_service.cancel_order(str(external_order_id))
            canceled_status_error = cancel_order_response['error']
            self.assertIsNone(canceled_status_error)
            status_canceled_order_history = self.customer.postman.order_service.get_order_history()
            external_canceled_order_id = status_canceled_order_history['result']['ordersForHistory'][0]['order'][
                'status']
            status_order = status_canceled_order_history['result']['ordersForHistory'][0]['order']['externalOrderId']
            self.assertTrue(external_canceled_order_id == 2)
            self.assertTrue(status_order)
            time.sleep(2)

            available_base_after_cancel = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)['result'][
                    'balance']['available'])
            quoted_after_cancel = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                                             2)
            available_quoted_after_cancel = float(quoted_after_cancel['result']['balance']['available'])
            frozen_quoted_after_cancel = float(quoted_after_cancel['result']['balance']['frozen'])

            self.assertTrue(available_base_after_cancel == available_base_before)
            self.assertTrue(available_quoted_after_cancel == available_quoted_before)
            self.assertTrue(frozen_quoted_after_cancel == frozen_quoted_before)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            Instruments.set_price_last_trade(self.instrument_id, self.price_origin)
            Instruments.set_ticker_last_price(self.instrument_id, self.price_origin)
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
