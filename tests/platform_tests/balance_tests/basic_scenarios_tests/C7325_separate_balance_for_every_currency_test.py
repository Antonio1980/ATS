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

test_case = '7325'


@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'total' balances EUR, DX, USD  using different currencies for trades, via API
    1. Checking of available', 'total' balances EUR, DX, USD  before 'Buy' Limit trade.
    2. Make 'Buy' Limit trade with DX CASH/USD.
    3. Checking of available', 'total' balances EUR, DX, USD  after 'Buy' Limit trade.
    4. Make 'Sell' Limit trade with DX CASH/EUR.
    5. Checking of available', 'total' balances EUR, DX, USD  after 'Sell' Limit trade.
    Calculation formula: available_balance_EUR_after_orders_2 = total_balance_EUR_after_orders_1 + price2 * quantity2 
                         total_balance_EUR_after_orders_2 = total_balance_EUR_after_orders_1  + price2 * quantity2 
                         available_balance_DXCASH_after_orders_2 = available_balance_DXCASH_after_orders_1 - quantity2
                         total_balance_DXCASH_after_orders_2 = total_balance_DXCASH_after_orders_1 - quantity2
                         available_balance_USD_after_orders_2 = available_balance_USD_after_orders_1
                         total_balance_USD_after_orders_2 =  total_balance_USD_after_orders_1
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Separate Balance For Every Currency')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7325_separate_balance_for_every_currency_test.py",
                 "TestLimitOrderPlacedSell")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestSeparateBalanceForEveryCurrency(unittest.TestCase):
    @allure.step("SetUp: registration new customer, increase him USD and EUR balance."
                 " Define ID of instrument for 'Buy' trade"
                 " Define ID of instrument for 'Sell' trade"
                 " Update Reference Price config")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id_1 = 1022
        self.instrument_id_2 = 1023
        self.custom = RegisteredCustomer()
        self.custom.clean_instrument(self.instrument_id_1)
        self.custom.clean_instrument(self.instrument_id_2)
        self.two_customers = Instruments.create_two_customers()
        self.pre_customer = self.two_customers[0][0]
        self.pre_customer_token = self.two_customers[0][1]
        self.customer = self.two_customers[1][0]
        self.customer_token = self.two_customers[1][1]
        self.customer.postman.get_static_postman(self.customer_token).balance_service.add_balance(
            self.customer.customer_id, 1, 10000)  # USD
        self.customer.postman.get_static_postman(self.customer_token).balance_service.add_balance(
            self.customer.customer_id, 2, 20000)  # EUR
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_separate_balance_for_every_currency")
    @automation_logger(logger)
    def test_separate_balance_for_every_currency(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method test_separate_balance_for_every_currency =['balance', ]), ")
        result = 0
        try:
            self.pre_customer.postman.get_static_postman(self.pre_customer_token).balance_service.add_balance(
                self.pre_customer.customer_id, 8, 500)
            estimated_price = Instruments.get_price_last_trade(self.instrument_id_1)
            order_limit_sell = Order().set_order(2, self.instrument_id_1, 105, estimated_price)
            order_response = self.pre_customer.postman.get_static_postman(
                self.pre_customer_token).order_service.create_order_sync(order_limit_sell)
            time.sleep(3.0)
            assert order_response['error'] is None, 'Create Order is failed'

            self.pre_customer.postman.get_static_postman(self.pre_customer_token).balance_service.add_balance(
                self.pre_customer.customer_id, 2, 10000)
            estimated_price = Instruments.get_price_last_trade(self.instrument_id_2)
            order_limit_buy = Order().set_order(1, self.instrument_id_2, 105, estimated_price)
            order_response = self.pre_customer.postman.get_static_postman(
                self.pre_customer_token).order_service.create_order_sync(
                order_limit_buy)
            time.sleep(3.0)
            assert order_response['error'] is None, 'Create Order is failed'

            eur_before_order_1 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            available_eur_before_order_1 = float(eur_before_order_1['result']['balance']['available'])
            total_eur_before_order_1 = float(eur_before_order_1['result']['balance']['total'])

            dx_before_order_1 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 8)
            available_dx_before_order_1 = float(dx_before_order_1['result']['balance']['available'])
            total_dx_before_order_1 = float(dx_before_order_1['result']['balance']['total'])

            usd_before_orders_1 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 1)
            available_usd_before_orders_1 = float(usd_before_orders_1['result']['balance']['available'])
            total_usd_before_orders_1 = float(usd_before_orders_1['result']['balance']['total'])

            price_from_order_book_1 = Instruments.get_orders_best_price_and_quantity(self.instrument_id_1, "buy", 1)
            price1 = float(price_from_order_book_1[0])
            quantity1 = 15

            order_limit1 = Order().set_order(1, self.instrument_id_1, quantity1, price1)
            order_response1 = self.customer.postman.get_static_postman(self.customer_token).order_service.create_order(
                order_limit1)
            time.sleep(5.0)
            order_status1 = order_response1['result']['status']
            self.assertTrue(order_status1)
            external_order_id_1 = order_response1['result']['externalOrderId']

            status_order_history_1 = self.customer.postman.get_static_postman(
                self.customer_token).order_service.get_order_history()
            status_order_1 = status_order_history_1['result']['ordersForHistory'][0]['order']['externalOrderId']
            self.assertEqual(external_order_id_1, status_order_1)

            eur_after_orders_1 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            available_eur_after_orders_1 = float(eur_after_orders_1['result']['balance']['available'])
            total_eur_after_orders_1 = float(eur_after_orders_1['result']['balance']['total'])

            dx_after_orders_1 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 8)
            available_dx_after_orders_1 = float(dx_after_orders_1['result']['balance']['available'])
            total_dx_after_orders_1 = float(dx_after_orders_1['result']['balance']['total'])

            usd_after_orders_1 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 1)
            available_usd_after_orders_1 = float(usd_after_orders_1['result']['balance']['available'])
            total_usd_after_orders_1 = float(usd_after_orders_1['result']['balance']['total'])

            self.assertTrue(available_usd_after_orders_1 == available_usd_before_orders_1 - price1 * quantity1)
            self.assertTrue(total_usd_after_orders_1 == total_usd_before_orders_1 - price1 * quantity1)
            self.assertTrue(available_dx_after_orders_1 == available_dx_before_order_1 + quantity1)
            self.assertTrue(total_dx_after_orders_1 == total_dx_before_order_1 + quantity1)
            self.assertTrue(available_eur_after_orders_1 == available_eur_before_order_1)
            self.assertTrue(total_eur_after_orders_1 == total_eur_before_order_1)

            price_from_order_book_2 = Instruments.get_orders_best_price_and_quantity(self.instrument_id_2, "sell", 1)
            price2 = float(price_from_order_book_2[0])
            quantity2 = 15
            order_limit2 = Order().set_order(2, self.instrument_id_2, quantity2, price2)
            order_response2 = self.customer.postman.get_static_postman(self.customer_token).order_service.create_order(
                order_limit2)
            time.sleep(5.0)
            order_status2 = order_response2['result']['status']
            self.assertTrue(order_status2)
            external_order_id_2 = order_response2['result']['externalOrderId']

            status_order_history_2 = self.customer.postman.get_static_postman(
                self.customer_token).order_service.get_order_history()
            status_order_2 = status_order_history_2['result']['ordersForHistory'][0]['order']['externalOrderId']
            self.assertEqual(external_order_id_2, status_order_2)

            eur_after_orders_2 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 2)
            available_eur_after_orders_2 = float(eur_after_orders_2['result']['balance']['available'])
            total_eur_after_orders_2 = float(eur_after_orders_2['result']['balance']['total'])

            dx_after_orders_2 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 8)
            available_dx_after_orders_2 = float(dx_after_orders_2['result']['balance']['available'])
            total_dx_after_orders_2 = float(dx_after_orders_2['result']['balance']['total'])

            usd_after_orders_2 = self.customer.postman.get_static_postman(
                self.customer_token).balance_service.get_currency_balance(
                self.customer.customer_id, 1)
            available_usd_after_orders_2 = float(usd_after_orders_2['result']['balance']['available'])
            total_usd_after_orders_2 = float(usd_after_orders_2['result']['balance']['total'])

            self.assertTrue(available_eur_after_orders_2 == total_eur_after_orders_1 + price2 * quantity2)
            self.assertTrue(total_eur_after_orders_2 == total_eur_after_orders_1 + price2 * quantity2)
            self.assertTrue(available_dx_after_orders_2 == available_dx_after_orders_1 - quantity2)
            self.assertTrue(total_dx_after_orders_2 == total_dx_after_orders_1 - quantity2)
            self.assertTrue(available_usd_after_orders_2 == available_usd_after_orders_1)
            self.assertTrue(total_usd_after_orders_2 == total_usd_after_orders_1)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
