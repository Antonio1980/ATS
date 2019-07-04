import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = '7318'


@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'total', 'frozen' balance after "Buy" Limit orders using several instruments, via API.
    1. Place 'Buy' Limit order with BTC/USD instrument.
    2. Checking of 'available', 'total', 'frozen' quoted currency balances after order.
    3. Place 'Buy' Limit order with LTC/USD instrument.
    4. Checking of 'available', 'total', 'frozen'quoted currency balances after order. 
    Calculation: available_balance_quoted_currency_after_orders_2 = 
                    = total balance - price*quantity of order1 - price*quantity of order2 
                 frozen_balance_quoted_currency_after_orders_2 = price*quantity of order1 + price*quantity of order2 
                 total_balance_quoted_currency_after_orders_2 = total balance added in setUp
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + '/index.php?/cases/view/' + test_case,
             name='Currency Used In Several Instruments')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7318_currency_used_in_several_instruments_test.py",
                 "TestCurrencyUsedInSeveralInstruments")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestCurrencyUsedInSeveralInstruments(unittest.TestCase):
    @allure.step("SetUp:  registration new customer, increase him USD balance."
                 " Define ID of instrument for order_1"
                 " Define ID of instrument for order_2")
    def setUp(self):
        self.customer = Customer()
        self.customer.customer_registration()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 3000)  # USD
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.instrument_id_1 = 1007  # BTC/USD
        self.instrument_id_2 = 1011  # LTC/USD

    @allure.step("Starting with: test_currency_used_in_several_instruments")
    @automation_logger(logger)
    def test_currency_used_in_several_instruments(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method test_currency_used_in_several_instruments")
        result = 0
        try:
            order_limit1 = Order().set_order(1, self.instrument_id_1, 1, 2500)
            order_response1 = self.customer.postman.order_service.create_order(order_limit1)
            order_status1 = order_response1['result']['status']
            self.assertTrue(order_status1, "Status Order1: failed with Error")

            quoted_after_orders_1 = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 1)
            available_quoted_after_orders_1 = float(quoted_after_orders_1['result']['balance']['available'])
            frozen_quoted_after_orders_1 = float(quoted_after_orders_1['result']['balance']['frozen'])
            total_quoted_after_orders_1 = float(quoted_after_orders_1['result']['balance']['total'])

            self.assertTrue(available_quoted_after_orders_1 == 500.0)
            self.assertTrue(frozen_quoted_after_orders_1 == 2500.0)
            self.assertTrue(total_quoted_after_orders_1 == 3000.0)

            order_limit2 = Order().set_order(1, self.instrument_id_2, 5, 20)
            order_response2 = self.customer.postman.order_service.create_order(order_limit2)
            order_status2 = order_response2['result']['status']
            self.assertTrue(order_status2, "Status Order2: failed with Error")

            quoted_after_orders_2 = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 1)
            available_quoted_after_orders_2 = float(quoted_after_orders_2['result']['balance']['available'])
            frozen_quoted_after_orders_2 = float(quoted_after_orders_2['result']['balance']['frozen'])
            total_quoted_after_orders_2 = float(quoted_after_orders_2['result']['balance']['total'])

            self.assertTrue(available_quoted_after_orders_2 == 400.0)
            self.assertTrue(frozen_quoted_after_orders_2 == 2600.0)
            self.assertTrue(total_quoted_after_orders_2 == 3000.0)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
