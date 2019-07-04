import time
import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

instrument_id = 1014
test_case = '6950'


@pytest.mark.incremental
@allure.feature("Limit Order")
@allure.title("API LIMIT")
@allure.description("""
    Functional test.
    Validation of trade price that best price has priority ,  via API
    1. Check positive balance .
    2. Place 'Buy' Limit order with price greater then the best price from order book(Buy).
    3. Make 'Sell' Limit trade with price less then price from 'Buy' Limit order.
    3. Check the price buy is equal price sell from order   
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='New Best Price In Order Book')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6950_new_best_price_in_order_book_test.py",
    "TestNewBestPriceInOrderBook")
@pytest.mark.usefixtures('r_time_count', 'r_customer', )
@pytest.mark.functional
@pytest.mark.limit_order
@pytest.mark.limit_order_api
@pytest.mark.order_management
class TestNewBestPriceInOrderBook(object):
    order_id = None
    price_buy = None
    price_sell = None
    price_1 = None
    quantity = None
    price_origin = None
    waiting_time = 3.0

    @automation_logger(logger)
    def test_place_order(self, r_customer):
        r_customer.clean_instrument(instrument_id)
        TestNewBestPriceInOrderBook.price_origin = Instruments.get_price_last_trade(instrument_id)
        Instruments.set_price_last_trade(instrument_id, 5)
        Instruments.set_ticker_last_price(instrument_id, 5)
        time.sleep(3.0)

        TestNewBestPriceInOrderBook.price_1 = Instruments.get_price_last_trade(instrument_id)
        TestNewBestPriceInOrderBook.quantity = Instruments.get_min_order_amount(instrument_id)
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 6, self.quantity + 6)
        order_limit_1 = Order().set_order(2, instrument_id, self.quantity + 5, round((self.price_1 + 0.8), 5))
        order_response_1 = r_customer.postman.order_service.create_order(order_limit_1)
        time.sleep(self.waiting_time)
        order_status_1 = order_response_1['result']['status']
        assert order_status_1

        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 2, self.quantity + 6)
        order_limit_2 = Order().set_order(1, instrument_id, self.quantity + 5, round(self.price_1 - 0.5), 5)
        order_response_2 = r_customer.postman.order_service.create_order(order_limit_2)
        time.sleep(self.waiting_time)
        order_status_2 = order_response_2['result']['status']
        assert order_status_2

    @automation_logger(logger)
    def test_create_buy_sell_price(self):
        TestNewBestPriceInOrderBook.price_buy = self.price_1
        TestNewBestPriceInOrderBook.price_sell = round((self.price_1 - 0.2), 5)

        assert self.price_buy is not None
        assert self.price_sell is not None

    @automation_logger(logger)
    def test_check_cur_customer_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 6, 50000)
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, 2, 100000)
        quoted_balance = r_customer.postman.p_balance_service.get_balance(2)
        base_balance = r_customer.postman.p_balance_service.get_balance(6)
        available_quoted = float(quoted_balance['result']['balance'][str(2)]['available'])
        available_base = float(base_balance['result']['balance'][str(6)]['available'])

        assert available_quoted and available_base != 0

    @automation_logger(logger)
    def test_create_buy_limit_order(self, r_customer):
        buy_order = Order().set_order(1, instrument_id, self.quantity, self.price_buy)
        buy_order_response = r_customer.postman.order_service.create_order_sync(buy_order)
        logger.logger.info(buy_order_response)
        time.sleep(3)
        TestNewBestPriceInOrderBook.order_id = buy_order_response['result']['orderId']
        logger.logger.info(self.order_id)

        assert self.order_id is not None

    @automation_logger(logger)
    def test_filled_quantity_is_zero(self, r_customer):
        order_response = r_customer.postman.order_service.get_open_orders()
        filled_quantity = order_response['result']['orders'][-1]['filledQuantity']['value']
        order_id = order_response['result']['orders'][-1]['id']

        assert self.order_id == order_id
        assert filled_quantity == 0

    @automation_logger(logger)
    def test_create_sell_limit_order(self, r_customer):
        sell_order = Order().set_order(2, instrument_id, self.quantity, self.price_sell)
        sell_order_response = r_customer.postman.order_service.create_order_sync(sell_order)
        logger.logger.info(sell_order_response)
        time.sleep(3)
        TestNewBestPriceInOrderBook.order_id = sell_order_response['result']['orderId']

        assert self.order_id is not None

    @automation_logger(logger)
    def test_price_buy_is_equal_price_sell_from_order(self, r_customer):
        price_from_order = float(Instruments.run_mysql_query(
            "SELECT price FROM trades_crypto WHERE orderId = " + str(
                self.order_id) + " AND direction = 'sell' GROUP BY price;")[0][0])
        assert float(self.price_buy) == price_from_order
        Instruments.set_price_last_trade(instrument_id, self.price_origin)
        Instruments.set_ticker_last_price(instrument_id, self.price_origin)
        logger.logger.info("order_id {0}".format(self.order_id))
        logger.logger.info("price_buy {0} == price_from_order {1}".format(self.price_buy, price_from_order))
        logger.logger.info("Test {0},CustomerID {1}".format(test_case, r_customer.customer_id))

        logger.logger.info("==================== TEST IS PASSED ====================")
