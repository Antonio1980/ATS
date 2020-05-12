import time
import unittest
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = '7326'


@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'total', 'frozen' balance after frozen in several step, via API
    1. Checking of 'available', 'total', 'frozen' balances before orders.
    2. Place 'Sell' Limit order.
    3. Place 'Sell' Limit order.
    4. Place 'Sell' Limit order.
    5. Checking of 'available', 'total', 'frozen' balances after orders. 
    Calculation formula: available_balance_after orders = total balance added in SetUp 
                         total_balance_after orders  = total_balance_before orders
                         frozen_balance_after orders = frozen_balance_before + available_balance_before 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='All Balance Is Frozen In Several Steps')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7326_all_balance_is_frozen_in_several_steps_test.py",
                 "TestAllBalanceIsFrozenInSeveralSteps")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestAllBalanceIsFrozenInSeveralSteps(unittest.TestCase):
    @allure.step("SetUp:  registration new customer, increase him ETH balance."
                 "Define ID of instrument for order"
                 "Update Reference Price config")
    def setUp(self):
        self.instrument_id = 1015  # ETH/BTC
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 4, 100)  # ETH
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_all_balance_is_frozen_in_several_steps")
    @automation_logger(logger)
    def test_all_balance_is_frozen_in_several_steps(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method all_balance_is_frozen_in_several_steps")
        result = 0
        try:
            balance_before = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 4)
            available_before = balance_before['result']['balance']['available']
            total_before = balance_before['result']['balance']['total']
            frozen_before = balance_before['result']['balance']['frozen']

            price = Instruments.get_price_last_trade(self.instrument_id)

            order_limit_1 = Order().set_order(2, self.instrument_id, 10, price)
            order_response_1 = self.customer.postman.order_service.create_order(order_limit_1)
            order_status_1 = order_response_1['result']['status']
            external_order_id_1 = order_response_1['result']['externalOrderId']
            self.assertTrue(order_status_1)

            open_orders_1 = self.customer.postman.order_service.get_open_orders()
            time.sleep(5)
            filled_quantity_1 = open_orders_1['result']['orders'][-1]['filledQuantity']['value']
            external_open_order_id_1 = open_orders_1['result']['orders'][-1]['externalOrderId']
            self.assertTrue(filled_quantity_1 == 0 and external_open_order_id_1 == external_order_id_1)

            order_limit_2 = Order().set_order(2, self.instrument_id, 40, price)
            order_response_2 = self.customer.postman.order_service.create_order(order_limit_2)
            order_status_2 = order_response_2['result']['status']
            external_order_id_2 = order_response_2['result']['externalOrderId']
            self.assertTrue(order_status_2)

            open_orders_buy_2 = self.customer.postman.order_service.get_open_orders()
            filled_quantity_2 = open_orders_buy_2['result']['orders'][-1]['filledQuantity']['value']
            external_open_order_id_2 = open_orders_buy_2['result']['orders'][-1]['externalOrderId']
            self.assertTrue(filled_quantity_2 == 0 and external_order_id_2 == external_open_order_id_2)

            order_limit_3 = Order().set_order(2, self.instrument_id, 50, price)
            order_response_3 = self.customer.postman.order_service.create_order(order_limit_3)
            order_status_3 = order_response_3['result']['status']
            external_order_id_3 = order_response_3['result']['externalOrderId']
            self.assertTrue(order_status_3)

            open_orders_buy_3 = self.customer.postman.order_service.get_open_orders()
            filled_quantity_3 = open_orders_buy_3['result']['orders'][-1]['filledQuantity']['value']
            external_open_order_id_3 = open_orders_buy_3['result']['orders'][-1]['externalOrderId']
            self.assertTrue(filled_quantity_3 == 0 and external_order_id_3 == external_open_order_id_3)

            balance_after = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 4)
            available_after = balance_after['result']['balance']['available']
            total_after = balance_after['result']['balance']['total']
            frozen_after = balance_after['result']['balance']['frozen']

            self.assertTrue(float(available_after) == float(available_before) - 100)
            self.assertTrue(float(total_after) == float(total_before))
            self.assertTrue(float(frozen_after) == float(frozen_before) + 100)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
