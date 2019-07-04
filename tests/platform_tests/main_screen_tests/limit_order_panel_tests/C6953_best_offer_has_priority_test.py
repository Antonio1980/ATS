import time

import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

instrument_id = 1014
test_case = '6953'


@pytest.mark.incremental
@allure.feature("Limit Order")
@allure.title("API LIMIT")
@allure.description("""
    Functional test.
    Validation of trade price that best price has priority ,  via API
    1. Check positive balance .
    2. Place 'Buy' Limit order with price greater then the best price from order book .
    3. Check the best price from order book must be equal price from trade. 
    Calculation formula: the best price from order book = price_from_trade; 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Best Offer Has Priority')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6953_best_offer_has_priority_test.py",
    "TestBestOfferHasPriority")
@pytest.mark.usefixtures('r_time_count', 'r_customer', )
@pytest.mark.functional
@pytest.mark.limit_order
@pytest.mark.limit_order_api
@pytest.mark.order_management
class TestBestOfferHasPriority(object):
    price_amount = None
    result = 0

    @automation_logger(logger)
    def test_place_orders(self, r_customer):
        r_customer.clean_instrument(instrument_id)
        price_tail_digits = Instruments.get_price_tail_digits(instrument_id)
        price_1 = Instruments.get_price_last_trade(instrument_id)
        quantity_1 = Instruments.get_min_order_amount(instrument_id)
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 6, quantity_1 + 6)
        order_limit_1 = Order().set_order(2, instrument_id, quantity_1 + 5, price_1)
        order_response_1 = r_customer.postman.order_service.create_order(order_limit_1)
        time.sleep(3.0)
        order_status_1 = order_response_1['result']['status']
        assert order_status_1

        price_2 = round((price_1 + (price_1 * 0.1)), price_tail_digits)
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 6, quantity_1 + 20)
        order_limit_2 = Order().set_order(2, instrument_id, quantity_1 + 16, price_2)
        order_response_2 = r_customer.postman.order_service.create_order(order_limit_2)
        time.sleep(3.0)
        order_status_2 = order_response_2['result']['status']
        assert order_status_2

        price_3 = round((price_1 + (price_1 * 0.2)), price_tail_digits)
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 6, quantity_1 + 20)
        order_limit_3 = Order().set_order(2, instrument_id, quantity_1 + 16, price_3)
        order_response_3 = r_customer.postman.order_service.create_order(order_limit_3)
        time.sleep(3.0)
        order_status_3 = order_response_3['result']['status']
        assert order_status_3

    @automation_logger(logger)
    def test_check_cur_customer_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 2, 50000)  # USD
        cur_balance = r_customer.postman.p_balance_service.get_balance(2)
        logger.logger.info(cur_balance)
        available_quoted = float(cur_balance['result']['balance'][str(2)]['available'])

        assert cur_balance['error'] is None
        assert available_quoted != 0

    @automation_logger(logger)
    def test_create_price_and_quantity_for_order(self):
        TestBestOfferHasPriority.price_amount = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        logger.logger.info(self.price_amount)
        assert isinstance(self.price_amount, list)
        assert len(self.price_amount) != 0

    @automation_logger(logger)
    def test_create_limit_order_buy(self, r_customer):
        order = Order().set_order(1, instrument_id, self.price_amount[0][1],
                                  self.price_amount[2][0])
        logger.logger.info(self.price_amount[0][1])
        logger.logger.info(self.price_amount[2][0])
        order_response = r_customer.postman.order_service.create_order_sync(order)
        logger.logger.info(order_response)
        time.sleep(3.0)
        assert order_response['error'] is None
        TestBestOfferHasPriority.order_id = order_response['result']['orderId']

    @automation_logger(logger)
    def test_check_best_price_equal_matched_price(self, r_customer):
        price_from_trade = float(Instruments.run_mysql_query(
            "SELECT price FROM trades_crypto WHERE orderId = " + str(
                self.order_id) + " AND direction = 'buy' GROUP BY price;")[0][0])

        assert float(self.price_amount[0][0]) == price_from_trade

        logger.logger.info("Test {0},CustomerID {1}".format(test_case, r_customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")

