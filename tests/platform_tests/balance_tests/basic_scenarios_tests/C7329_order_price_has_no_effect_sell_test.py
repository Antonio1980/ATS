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

test_case = '7329'


@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'total', 'frozen' balance if a customer places a "limit" order,  part of his balance
     is frozen. The amount of assets that are to be frozen isn't affected by the order price, via API
    1. Checking of 'available', 'total', 'frozen' balances before orders.
    2. Place 'Sell' Limit order with price_1.
    3. Place 'Sell' Limit order with price_2.
    5. Checking of 'available', 'total', 'frozen' balances after orders. 
    Calculation formula: available_balance_after = available_balance_before - quantity1 -  quantity2
                         total_balance_after = total_balance_before
                         frozen_balance_after = frozen_balance_before + quantity1 +  quantity2)
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Order Price Has No Effect - Sell')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7329_order_price_has_no_effect_sell_test.py",
                 "TestOrderPriceHasNoEffectSell")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestOrderPriceHasNoEffectSell(unittest.TestCase):
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

    @allure.step("Starting with: test_order_price_has_no_effect_sell")
    @automation_logger(logger)
    def test_order_price_has_no_effect_sell(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_order_price_has_no_effect_sell")
        result = 0
        try:
            balance_before = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 4)
            available_before = balance_before['result']['balance']['available']
            total_before = balance_before['result']['balance']['total']
            frozen_before = balance_before['result']['balance']['frozen']

            best_price_from_order_book = Instruments.get_price_last_trade(self.instrument_id)
            price_1 = best_price_from_order_book + best_price_from_order_book * 0.25
            price_2 = best_price_from_order_book + best_price_from_order_book * 0.29
            order_limit_1 = Order().set_order(2, self.instrument_id, 10, price_1)
            order_response_1 = self.customer.postman.order_service.create_order(order_limit_1)
            order_status_1 = order_response_1['result']['status']
            external_order_id_1 = order_response_1['result']['externalOrderId']
            self.assertTrue(order_status_1)

            open_orders_1 = self.customer.postman.order_service.get_open_orders()
            filled_quantity_1 = open_orders_1['result']['orders'][-1]['filledQuantity']['value']
            external_open_order_id_1 = open_orders_1['result']['orders'][-1]['externalOrderId']
            self.assertTrue(filled_quantity_1 == 0)
            self.assertTrue(external_open_order_id_1 == external_order_id_1)

            order_limit_2 = Order().set_order(2, self.instrument_id, 35, price_2)
            order_response_2 = self.customer.postman.order_service.create_order(order_limit_2)
            order_status_2 = order_response_2['result']['status']
            external_order_id_2 = order_response_2['result']['externalOrderId']
            self.assertTrue(order_status_2)
            time.sleep(2)

            open_orders_buy_2 = self.customer.postman.order_service.get_open_orders()
            filled_quantity_2 = open_orders_buy_2['result']['orders'][-1]['filledQuantity']['value']
            external_open_order_id_2 = open_orders_buy_2['result']['orders'][-1]['externalOrderId']
            self.assertTrue(filled_quantity_2 == 0 and external_order_id_2 == external_open_order_id_2)

            balance_after = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 4)
            available_after = balance_after['result']['balance']['available']
            total_after = balance_after['result']['balance']['total']
            frozen_after = balance_after['result']['balance']['frozen']

            self.assertTrue(float(available_after) == float(available_before) - 10 - 35)
            self.assertTrue(float(total_after) == float(total_before))
            self.assertTrue(float(frozen_after) == float(frozen_before) + 45)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1

        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
