import time
import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.data_bases.redis_db import RedisDb
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '7311'


@allure.title("BALANCE")
@allure.description("""
    Functional test.
    Validation of 'available', 'total', 'frozen' balance after placing 'Buy' Limit order via API
    1. Checking of 'available', 'total', 'frozen' balances before order.
    2. Place 'Buy' Limit order.
    3. Checking of 'available', 'total', 'frozen' balances after order. 
    Calculation formula: available_balance_after_order = available_balance_before_order - order_price;
                         total_balance_after_order = no change; 
                         frozen_balance_after_order = frozen_balance_before_order + order_price; 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Limit Order Placed - Buy')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7311_balance_after_order_limit_buy_placed_test.py",
                 "TestBalanceAfterOrderLimitBuyPlaced")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestBalanceAfterOrderLimitBuyPlaced(unittest.TestCase):

    @allure.step("SetUp:  calling registered customer and increase USD balance."
                 "Define ID of instrument for 'Buy' order")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id = 1012
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 2, 10000.0)
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_limit_order_placed_buy")
    @automation_logger(logger)
    def test_balance_after_order_limit_buy_placed(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_limit_order_placed_buy")
        result = 0
        try:
            price = Instruments.get_price_last_trade(self.instrument_id)
            amount = 1
            before_order = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 2)
            available_before_order = before_order['result']['balance']['available']
            total_before_order = before_order['result']['balance']['total']
            frozen_before_order = before_order['result']['balance']['frozen']

            order_limit = Order().set_order(1, self.instrument_id, amount, price)
            order_response = self.customer.postman.order_service.create_order(order_limit)
            order_status = order_response['result']['status']
            external_order_id = order_response['result']['externalOrderId']
            self.assertTrue(order_status, "Status Order failed with Error")
            time.sleep(5.0)

            open_orders = self.customer.postman.order_service.get_open_orders()
            filled_quantity = open_orders['result']['orders'][-1]['filledQuantity']['value']
            external_order_id_ = open_orders['result']['orders'][-1]['externalOrderId']
            self.assertTrue(filled_quantity == 0)
            self.assertTrue(external_order_id == external_order_id_)
            all_balance_after = self.customer.postman.balance_service.get_currency_balance(
                int(self.customer.customer_id), 2)

            available_after = all_balance_after['result']['balance']['available']
            total_after = all_balance_after['result']['balance']['total']
            frozen_after = all_balance_after['result']['balance']['frozen']

            frozen_redis = float(
                RedisDb.redis_client.execute_command('hget frozen_balance_{' + str(self.customer.customer_id) + '} 2'))
            total_redis = float(
                RedisDb.redis_client.execute_command('hget balance_{' + str(self.customer.customer_id) + '} 2'))

            available_redis = total_redis - frozen_redis
            self.assertTrue(float(available_after) == float(available_before_order) - price == available_redis)
            self.assertTrue(float(total_before_order) == float(total_after) == total_redis)
            self.assertTrue(float(frozen_after) == float(frozen_before_order) + price == frozen_redis,
                            "Checking of balance is failed ")

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
