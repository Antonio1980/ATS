import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = '7317'


@allure.title("API BALANCE")
@allure.description("""
    Validation of 'available', 'total', 'frozen' balance after placing "Sell" Limit order via API if "tail digits"
     for quantity was generated.
    1. Generate 'tail digits' for quantity according to configuration.
    2. Place 'Sell' Limit order.
    3. Check of 'available', 'total', 'frozen' base  currency balances after 'Sell' order.
    4. Place 'Sell' Limit order.
    5. Check of 'available', 'total', 'frozen' base  currency balances after 'Sell' order
    Calculation: available balance = 0.0
                 total balance = 'total balance' added in SetUp
                 frozen balance = total balance
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + '/index.php?/cases/view/' + test_case, name='Frozen Balance - Fractions')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7317_frozen_balance_fractions_test.py",
                 "TestFrozenBalanceFractions")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestFrozenBalanceFractions(unittest.TestCase):

    @allure.step("SetUp:  registration new customer, increase him USD and BTC balance.")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id = 1007
        self.customer = Customer()
        self.customer.customer_registration()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 1000)  # USD
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 2)  # BTC
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_frozen_balance_fractions")
    @automation_logger(logger)
    def test_frozen_balance_fractions(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_frozen_balance_fractions")
        result = 0
        try:
            tail_digits_currency_1 = Instruments.get_quantity_tail_digits(self.instrument_id)
            balance_decimals_quantity = str(tail_digits_currency_1 - 1)
            quantity_1 = float(str(format(1.0000000000, "." + balance_decimals_quantity + "f")) + '1')
            best_price_from_order_book = float(
                round(Instruments.get_orders_best_price_and_quantity(self.instrument_id, "sell", 1)[0]))
            price = best_price_from_order_book + best_price_from_order_book * 0.30
            order_limit_1 = Order().set_order(2, self.instrument_id, quantity_1, price)
            order_response_1 = self.customer.postman.order_service.create_order(order_limit_1)
            order_status_1 = order_response_1['result']['status']
            self.assertTrue(order_status_1, "Status Order1: failed with Error")

            all_balance_1 = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)
            available_balance_1 = all_balance_1['result']['balance']['available']
            total_balance_1 = all_balance_1['result']['balance']['total']
            frozen_balance_1 = all_balance_1['result']['balance']['frozen']

            self.assertTrue(float(available_balance_1) == round(2 - quantity_1, tail_digits_currency_1))
            self.assertTrue(float(total_balance_1) == 2)
            self.assertTrue(float(frozen_balance_1) == quantity_1)

            order_limit_2 = Order().set_order(2, self.instrument_id, round(2 - quantity_1, tail_digits_currency_1),
                                              price)
            order_response_2 = self.customer.postman.order_service.create_order(order_limit_2)
            order_status_2 = order_response_2['result']['status']
            self.assertTrue(order_status_2, "Status Order2: failed with Error")

            all_balance_2 = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 3)
            available_balance_2 = all_balance_2['result']['balance']['available']
            total_balance_2 = all_balance_2['result']['balance']['total']
            frozen_balance_2 = all_balance_2['result']['balance']['frozen']

            self.assertTrue(float(available_balance_2) == 0.0)
            self.assertTrue(float(total_balance_2) == 2)
            self.assertTrue(float(frozen_balance_2) == 2)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
