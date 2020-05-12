import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '7313'


@allure.title("API BALANCE")
@allure.description("""
        Functional negative test
        Validation of 'available', 'total', 'frozen' base and quoted currency balances after trying "Buy" and "Sell"
        Limit orders if not enough available balance via API.
        1. Checking of 'available', 'total', 'frozen' base and quoted currency balances before 'Buy' and 'Sell' order 
        2. Trying to place 'Buy' Limit order.
        3. Trying to place 'Sell' Limit order
        4. Checking of 'available', 'total', 'frozen' base and quoted currency balances after 'Buy' and 'Sell' order 
        Calculation formula:total_balance_base_currency_after_order = no change 
                            total_balance_quoted_currency_after_order = no change 
                            available_balance_base_currency_after_order = no change
                            available_balance_quoted_currency_after_order = no change 
                            frozen_balance_quoted_currency_after_order = no change 
                            frozen_balance_base_currency_after_order = no change; 
        """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Not Enough Available Balance')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7313_balance_after_order_buy_redjected_test.py",
                 "TestBalanceAfterOrderBuyRejected")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestBalanceAfterOrderBuyRejected(unittest.TestCase):

    @allure.step("SetUp:  registration new customer, increase him USD and BTC balance."
                 " Define ID of instrument for order")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id = 1007
        self.customer = RegisteredCustomer()
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 500)  # USD
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 1)  # BTC
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_not_enough_available_balance")
    @automation_logger(logger)
    def test_not_enough_available_balance(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_not_enough_available_balance")
        result = 0
        try:
            balance_base_before = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 3)
            total_base_before = float(balance_base_before['result']['balance']['total'])
            available_base_before = float(balance_base_before['result']['balance']['available'])
            frozen_base_before = float(balance_base_before['result']['balance']['frozen'])

            balance_quoted_before = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 1)
            total_quoted_before = float(balance_quoted_before['result']['balance']['total'])
            available_quoted_before = float(balance_quoted_before['result']['balance']['available'])
            frozen_quoted_before = float(balance_quoted_before['result']['balance']['frozen'])

            price = Instruments.get_price_last_trade(self.instrument_id)
            quantity = 8
            order_limit = Order().set_order(1, self.instrument_id, quantity, price)
            order_response_buy = self.customer.postman.order_service.create_order(order_limit)
            order_error_buy = order_response_buy['error']
            self.assertNotEqual(order_error_buy.find('error freezing balance'), -1, "error freezing balance")

            base_after_buy = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 3)
            total_base_after = float(base_after_buy['result']['balance']['total'])
            available_base_after = float(base_after_buy['result']['balance']['available'])
            frozen_base_after = float(base_after_buy['result']['balance']['frozen'])

            quoted_after_buy = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 1)
            total_quoted_after = float(quoted_after_buy['result']['balance']['total'])
            available_quoted_after = float(quoted_after_buy['result']['balance']['available'])
            frozen_quoted_after = float(quoted_after_buy['result']['balance']['frozen'])

            self.assertTrue(total_base_before == total_base_after)
            self.assertTrue(total_quoted_before == total_quoted_after)
            self.assertTrue(available_base_before == available_base_after)
            self.assertTrue(available_quoted_before == available_quoted_after)
            self.assertTrue(frozen_quoted_before == frozen_quoted_after)
            self.assertTrue(frozen_base_before == frozen_base_after)

            order_limit.set_order(2, self.instrument_id, quantity, price)
            order_response_sell = self.customer.postman.order_service.create_order(order_limit)
            order_error_sell = order_response_sell['error']
            self.assertNotEqual(order_error_sell.find('error freezing balance'), -1, 'error freezing balance')

            base_after_sell = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 3)
            total_base_after_sell = float(base_after_sell['result']['balance']['total'])
            available_base_after_sell = float(base_after_sell['result']['balance']['available'])
            frozen_base_after_sell = float(base_after_sell['result']['balance']['frozen'])

            quoted_after_sell = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 1)
            total_quoted_after_sell = float(quoted_after_sell['result']['balance']['total'])
            available_quoted_after_sell = float(quoted_after_sell['result']['balance']['available'])
            frozen_quoted_after_sell = float(quoted_after_sell['result']['balance']['frozen'])

            self.assertTrue(total_base_before == total_base_after_sell)
            self.assertTrue(total_quoted_before == total_quoted_after_sell)
            self.assertTrue(available_base_before == available_base_after_sell)
            self.assertTrue(available_quoted_before == available_quoted_after_sell)
            self.assertTrue(frozen_quoted_before == frozen_quoted_after_sell)
            self.assertTrue(frozen_base_before == frozen_base_after_sell)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
