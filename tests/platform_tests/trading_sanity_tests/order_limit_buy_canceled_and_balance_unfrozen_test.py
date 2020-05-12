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


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST 'TS- 1'")
@allure.description("""
    Verify that customer balance unfrozen when limit buy order created and cancelled.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_sanity_tests/order_limit_buy_canceled_and_balance_unfrozen_test.py",
                 "TestBuyLimitCanceledOrderUnfrozenBalance")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
@pytest.mark.functional
@pytest.mark.trading_sanity
class TestBuyLimitCanceledOrderUnfrozenBalance(unittest.TestCase):
    test_case = "TS- 1"

    @allure.step("SetUp: calling registered customer and adding USD to balance.")
    @automation_logger(logger)
    def setUp(self):
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.instrument_id = 1007  # BTC/USD
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 1, 10000.0)

    @allure.step("Starting with: test_buy_limit_canceled_order_unfrozen_balance")
    @automation_logger(logger)
    def test_buy_limit_canceled_order_unfrozen_balance(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(self.test_case))
        logger.logger.info("method test_buy_limit_canceled_order_unfrozen_balance =['trading_sanity', ]), ")
        result = 0
        try:
            available_base_before = float(
                self.customer.postman.balance_service.get_currency_balance(int(self.customer.customer_id), 3)['result'][
                    'balance']['available'])
            quoted_currency_before = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 1)
            available_quoted_before = float(quoted_currency_before['result']['balance']['available'])
            frozen_quoted_before = float(quoted_currency_before['result']['balance']['frozen'])
            best_price_from_order_book = float(
                round(Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 2)[0][0]))
            price = best_price_from_order_book - best_price_from_order_book * 0.50
            quantity = 1
            order_limit_buy = Order().set_order(1, self.instrument_id, quantity, price)
            order_response = self.customer.postman.order_service.create_order(order_limit_buy)
            order_status = order_response['result']['status']

            assert order_status

            external_order_id = order_response['result']['externalOrderId']
            time.sleep(3)
            available_base_currency_after_order = float(
                self.customer.postman.balance_service.get_currency_balance(int(self.customer.customer_id), 3)['result'][
                    'balance']['available'])
            quoted_after = self.customer.postman.balance_service.get_currency_balance(int(self.customer.customer_id), 1)
            available_quoted_after = float(quoted_after['result']['balance']['available'])
            frozen_quoted_after = float(quoted_after['result']['balance']['frozen'])

            assert available_base_before == available_base_currency_after_order
            assert available_quoted_after == available_quoted_before - price
            assert frozen_quoted_after == frozen_quoted_before + price
            time.sleep(5.0)
            cancel_order_response = self.customer.postman.order_service.cancel_order(str(external_order_id))
            canceled_status_error = cancel_order_response['error']

            assert canceled_status_error is None

            status_canceled_order_history = self.customer.postman.order_service.get_order_history()
            external_canceled_order_id = status_canceled_order_history['result']['ordersForHistory'][0]['order'][
                'status']
            status_order = status_canceled_order_history['result']['ordersForHistory'][0]['order']['externalOrderId']

            assert external_canceled_order_id == 2 and status_order

            time.sleep(2)
            available_base_after_cancel = float(
                self.customer.postman.balance_service.get_currency_balance(int(self.customer.customer_id), 3)['result'][
                    'balance']['available'])
            quoted_after_cancel = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 1)
            available_quoted_after_cancel = float(quoted_after_cancel['result']['balance']['available'])
            frozen_quoted_after_cancel = float(quoted_after_cancel['result']['balance']['frozen'])

            assert available_base_after_cancel == available_base_before
            assert available_quoted_after_cancel == available_quoted_before
            assert frozen_quoted_after_cancel == frozen_quoted_before
            logger.logger.info("Test {0}, with CustomerID {1}".format(self.test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, self.test_case, result)
