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

test_case = '7686'


@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'frozen' balance after "Buy" Limit trading if part of balance when total Less Then OrderPrice via API.
    Pre - condition : order book for that instrument must be empty
    1. Checking of 'frozen' balances before order.
    2. Place 'Sell' Limit order with price = 60,  quantity = 100.
    3. Place 'Sell' Limit order with price = 56, quantity = 80.
    4. PLace 'Buy' Limit trade with price = 60, quantity = 180.
    3. Checking of 'frozen' balances after orders. 
    Calculation formula: frozen_balance_base_before = frozen_balance_base_after; 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/7686", name='Limit Buy Matched Trading Total Less Then'
                                                                            'Order Price - Balance Unfrozen')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/balance_tests/C7686_balance_unfrozen_after_trade_with_total_less_than_order_price_test.py",
                 "TestLimitBuyMatchedTradingTotalLessThenOrderPriceBalanceUnfrozen")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestLimitBuyMatchedTradingTotalLessThenOrderPriceBalanceUnfrozen(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance."
                 " Define ID of instrument for order"
                 " Update Reference Price config")
    def setUp(self):
        self.instrument_id = 1055
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 10, 100000)  # JPY
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 6, 10000)  # XRP
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_limit_buy_matched_trading_total_less_then_order_price_balance_unfrozen")
    @automation_logger(logger)
    def test_limit_buy_matched_trading_total_less_then_order_price_balance_unfrozen(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method limit_buy_matched_trading_total_less_then_order_price_balance_unfrozen")
        result = 0
        try:
            frozen_base_before = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 10)['result'][
                    'balance']['frozen'])

            order_limit_sell = Order().set_order(2, self.instrument_id, 100, 60)
            order_response_sell = self.customer.postman.order_service.create_order(order_limit_sell)
            order_limit_sell_1 = Order().set_order(2, self.instrument_id, 80, 56)
            order_response_sell_1 = self.customer.postman.order_service.create_order(order_limit_sell_1)
            time.sleep(3)
            self.assertTrue(order_response_sell['result']['status'])
            self.assertTrue(order_response_sell_1['result']['status'])
            time.sleep(3)

            order_limit_buy = Order().set_order(1, self.instrument_id, 180, 60)
            order_response_buy = self.customer.postman.order_service.create_order(order_limit_buy)
            self.assertTrue(order_response_buy['result']['status'])
            frozen_base_after = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 10)['result'][
                    'balance']['frozen'])
            logger.logger.info("----- frozen_balance_base_currency_after_order----- {0}:".format(
                frozen_base_after))

            try:
                delay_time = time.perf_counter() + 240.0
                while frozen_base_before != frozen_base_after and time.perf_counter() <= delay_time:
                    frozen_base_after = float(
                        self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 10)[
                            'result']['balance']['frozen'])
                    logger.logger.info("----- frozen_balance_base_currency_after_order----- {0}:".format(
                        frozen_base_after))
                self.assertEqual(frozen_base_before, frozen_base_after)
            except KeyError or ValueError as e:
                logger.logger.fatal(
                    "failed balance is frozen: {0}".format(frozen_base_after), e)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
