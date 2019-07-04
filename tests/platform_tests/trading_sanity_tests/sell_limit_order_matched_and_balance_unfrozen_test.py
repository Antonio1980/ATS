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

test_case = "TS- 12"


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST 'TS- 12'")
@allure.description("""
    Verify that customer balance unfrozen after sell order matched.
    10 Iterations (configurable by "iterations" local test variable).
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_sanity_tests/sell_limit_order_matched_and_balance_unfrozen_test.py",
                 "TestSellOrderMatchedWithBalanceUnfrozen")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
@pytest.mark.functional
@pytest.mark.trading_sanity
class TestSellOrderMatchedWithBalanceUnfrozen(unittest.TestCase):

    @allure.step("SetUp: registration new customer, adding credit card with EUR and BTC to balance.")
    @automation_logger(logger)
    def setUp(self):
        self.currency_id = 2
        self.c_currency_id = 3
        self.instrument_id = 1012
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, self.c_currency_id, 100.0)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, self.currency_id, 5000.0)

    @allure.step("Starting with: test_sell_order_matched_with_balance_unfrozen")
    @automation_logger(logger)
    def test_sell_order_matched_with_balance_unfrozen(self):
        frozen_delay = 240.0
        price = Instruments.get_price_last_trade(self.instrument_id)
        iterations = 10
        sleep_delay = 1.0
        sell = 2
        buy = 1

        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))

        balance_before_trade = self.customer.postman.p_balance_service.get_balance(self.c_currency_id)
        frozen_before_trade = float(balance_before_trade['result']['balance'][str(self.c_currency_id)]['frozen'])

        logger.logger.info("method test_sell_order_matched_with_balance_unfrozen ".format(frozen_before_trade))

        result = 0
        try:
            for i in range(iterations):
                order_quantity = Instruments.get_min_order_amount(self.instrument_id)

                limit_order_sell = Order().set_order(sell, self.instrument_id, order_quantity, price)
                limit_order_buy = Order().set_order(buy, self.instrument_id, order_quantity, price)

                time.sleep(sleep_delay)
                order_sell = self.customer.postman.order_service.create_order(limit_order_sell)

                assert order_sell['result']['status']

                time.sleep(sleep_delay)
                order_buy = self.customer.postman.order_service.create_order(limit_order_buy)

                assert order_buy['result']['status']

                time.sleep(sleep_delay)
                trades_order_response = self.customer.postman.order_service.get_trades_history()

                assert trades_order_response['result']['trades'][0]['id']

                balance_after_trade = self.customer.postman.p_balance_service.get_balance(self.c_currency_id)
                frozen_after_trade = float(balance_after_trade['result']['balance'][str(self.c_currency_id)]['frozen'])

                logger.logger.info("----- frozen_balance2----- {0}:".format(frozen_after_trade))

                delay_time = time.perf_counter() + frozen_delay
                while frozen_after_trade != frozen_before_trade and time.perf_counter() <= delay_time:
                    frozen_after_trade = float(self.customer.postman.balance_service.get_currency_balance(
                        self.customer.customer_id, self.c_currency_id)['result']['balance']['frozen'])
                    logger.logger.info("----- frozen_balance2----- {0}:".format(frozen_after_trade))

                assert frozen_after_trade == frozen_before_trade

                logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
                logger.logger.info("==================== TEST IS PASSED ====================")
                result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

