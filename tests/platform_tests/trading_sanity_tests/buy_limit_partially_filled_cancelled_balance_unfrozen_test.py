import time
import unittest

import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.data_bases.sql_db import SqlDb
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST 'TS- 3'")
@allure.description("""
    Verify that customer balance unfrozen after buy order (limit) partially matched and partially cancelled.
    """)
@allure.testcase(
    BaseConfig.GITLAB_URL + "/balance_sanity_tests/buy_limit_partially_filled_cancelled_and_balance_unfrozen_test.py",
    "TestBuyLimitPartiallyFilledCanceledBalanceUnfrozen")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
@pytest.mark.functional
@pytest.mark.trading_sanity
class TestBuyLimitPartiallyFilledCanceledBalanceUnfrozen(unittest.TestCase):
    test_case = "TS- 3"
    instrument_id = 1014
    q_currency_id = 2
    b_currency_id = 6

    @allure.step("SetUp: calling registered customer and adding USD to balance.")
    @automation_logger(logger)
    def setUp(self):
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, self.q_currency_id, 900000.0)

    @allure.step("Starting with: test_buy_limit_partially_filled_canceled_balance_unfrozen")
    @automation_logger(logger)
    def test_buy_limit_partially_filled_canceled_balance_unfrozen(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(self.test_case))
        logger.logger.info(
            "method_buy_limit_partially_filled_canceled_balance_unfrozen, ")
        result = 0
        price_tail_digits = SqlDb.get_price_tail_digits(self.instrument_id)
        quantity_tail_digits = SqlDb.get_quantity_tail_digits(self.instrument_id)
        price_1 = Instruments.get_price_last_trade(self.instrument_id)
        quantity = Instruments.get_min_order_amount(self.instrument_id)
        try:
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, self.b_currency_id, 5.0)

            order_limit_1 = Order().set_order(2, self.instrument_id, quantity + 1, price_1)
            order_response_1 = self.customer.postman.order_service.create_order(order_limit_1)
            order_status_1 = order_response_1['result']['status']
            assert order_status_1

            price_2 = round((price_1 + (price_1 * 0.2)), price_tail_digits)
            order_limit_2 = Order().set_order(2, self.instrument_id, quantity + 2, price_2)
            order_response_2 = self.customer.postman.order_service.create_order(order_limit_2)
            order_status_2 = order_response_2['result']['status']
            assert order_status_2

            time.sleep(5.0)

            frozen_quoted_before = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                           self.q_currency_id)['result'][
                    'balance']['frozen'])

            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 2)
            if quantity_tail_digits == 0:
                quantity = round((best_price_and_quantity[0][1] + best_price_and_quantity[1][1]) / 2)
            else:
                quantity = round((best_price_and_quantity[0][1] + best_price_and_quantity[1][1]) / 2,
                                 quantity_tail_digits)

            price = round((best_price_and_quantity[0][0] + best_price_and_quantity[1][0]) / 2, price_tail_digits)

            order_limit_buy = Order()
            order_limit_buy.set_order(1, self.instrument_id, quantity, price)

            while quantity <= best_price_and_quantity[0][1]:
                order_limit_buy.set_order(1, self.instrument_id, quantity, best_price_and_quantity[0][0])
                o_response = self.customer.postman.order_service.create_order(order_limit_buy)
                o_status = o_response['error']
                if o_status is not None:
                    break
                best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 2)
                if quantity_tail_digits == 0:
                    quantity = round((best_price_and_quantity[0][1] + best_price_and_quantity[1][1]) / 2)
                else:
                    quantity = round((best_price_and_quantity[0][1] + best_price_and_quantity[1][1]) / 2,
                                     quantity_tail_digits)
                price = round((best_price_and_quantity[0][0] + best_price_and_quantity[1][0]) / 2,
                              price_tail_digits)
                order_limit_buy.set_order(1, self.instrument_id, quantity, price)

            order_response = self.customer.postman.order_service.create_order(order_limit_buy)
            order_status = order_response['result']['status']

            time.sleep(3)
            assert order_status

            external_order_id = order_response['result']['externalOrderId']
            time.sleep(5)
            cancel_order_response = self.customer.postman.order_service.cancel_order(str(external_order_id))
            canceled_status_error = cancel_order_response['error']

            assert canceled_status_error is None

            time.sleep(5)
            status_canceled_order_history = self.customer.postman.order_service.get_order_history()
            external_canceled_order_id = status_canceled_order_history['result']['ordersForHistory'][0]['order'][
                'status']
            status_order = status_canceled_order_history['result']['ordersForHistory'][0]['order']['externalOrderId']

            assert external_canceled_order_id == 2
            assert status_order == external_order_id

            frozen_quoted_after_cancel = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                           self.q_currency_id)[
                    'result']['balance']['frozen'])

            assert frozen_quoted_before == frozen_quoted_after_cancel

            logger.logger.info("Test {0}, with CustomerID {1}".format(self.test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, self.test_case, result)
