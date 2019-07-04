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

test_case = "7330"


@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'frozen' balance after frozen balance calculation, via API
    1. Checking of 'available', 'frozen' balances before order.
    2. Place 'Buy' Limit order with price.
    3. Checking of 'available', 'frozen' balances after order.
    4. Place 'Buy' Limit order with price.
    5. Checking of 'available', 'frozen' balances after order_2.
    Calculation formula: available_balance_base_after_order_2 = available_balance_base_after 
                         available_balance_quoted_after_order_2 = available_balance_quoted_before - price - price 
                         frozen_balance_quoted_after_order_2 = frozen_balance_quoted_before + price + price 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Frozen Balance Calculation - Buy')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7330_frozen_balance_calculation_buy_test.py",
                 "TestFrozenBalanceCalculationBuy")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestFrozenBalanceCalculationBuy(unittest.TestCase):
    @allure.step("SetUp:  registration new customer, increase him USD and LTC balance."
                 "Define ID of instrument for order")
    def setUp(self):
        self.instrument_id = 1011
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 1000)  # USD
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 7, 2)  # LTC

    @allure.step("Starting with: test_frozen_balance_calculation_buy_test")
    @automation_logger(logger)
    def test_frozen_balance_calculation_buy_test(self):
        result = 0
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method_frozen_balance_calculation_buy_test")
        try:
            available_base_before = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)['result'][
                    'balance']['available'])
            quoted_before = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 1)
            available_quoted_before = float(quoted_before['result']['balance']['available'])
            frozen_quoted_before = float(quoted_before['result']['balance']['frozen'])
            price = Instruments.get_price_last_trade(self.instrument_id)
            quantity = 1
            order_limit_buy_1 = Order().set_order(1, self.instrument_id, quantity, price)
            order_response_1 = self.customer.postman.order_service.create_order_sync(order_limit_buy_1)
            order_status_2 = order_response_1['error']
            self.assertIsNone(order_status_2)
            time.sleep(5.0)

            available_base_after = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)['result'][
                    'balance']['available'])
            quoted_after = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 1)
            available_quoted_after = float(quoted_after['result']['balance']['available'])
            frozen_quoted_after = float(quoted_after['result']['balance']['frozen'])

            self.assertTrue(available_base_before == available_base_after)
            self.assertTrue(available_quoted_after == available_quoted_before - price)
            self.assertTrue(frozen_quoted_after == frozen_quoted_before + price)

            order_limit_buy_2 = Order().set_order(1, self.instrument_id, quantity, price)
            order_response_2 = self.customer.postman.order_service.create_order_sync(order_limit_buy_2)
            order_status_2 = order_response_2['error']
            self.assertIsNone(order_status_2)
            time.sleep(5.0)

            available_base_after_order_2 = float(
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)['result'][
                    'balance']['available'])
            quoted_after_order_2 = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                                              1)
            available_quoted_after_order_2 = float(quoted_after_order_2['result']['balance']['available'])
            frozen_quoted_after_order_2 = float(quoted_after_order_2['result']['balance']['frozen'])

            self.assertTrue(available_base_after_order_2 == available_base_after)
            self.assertTrue(available_quoted_after_order_2 == available_quoted_after - price)
            self.assertTrue(frozen_quoted_after_order_2 == frozen_quoted_after + price)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1

        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
