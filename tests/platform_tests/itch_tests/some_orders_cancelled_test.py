import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "some_orders_cancelled_itch_test"

"""
This test comes to verify that record in Order Book is updated accordingly when
some of the orders placed with a given price are cancelled. The record shouldn't be removed, record
quantity should be updated accordingly.

Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Set the reference price to the REFERENCE_PRICE.
    5. Place the 'Buy' order twice.
    6. Place the 'Sell' order twice.
    7. Verify 'Buy' Order Book is updated accordingly.
    8. Verify 'Sell' Order Book is updated accordingly.
    9. Cancelling some of the orders that were placed.
    10. Verifying that the Order Book is updated accordingly.
"""


# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

reference_price = 5
price_for_buy = reference_price - 2
price_for_sell = reference_price + 2
quantity_buy = 80.0
quantity_sell = 70.0

CANCELLING_ORDERS_DELAY = 5


@allure.feature("Order Book update after order cancellation - end to end test.")
@allure.story("Half of the orders that have the same price are cancelled - Order Book updated")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests 
    1. Place the 'Buy' order twice.
    2. Place the 'Sell' order twice.
    3. Verify 'Buy' Order Book is updated accordingly.
    4. Verify 'Sell' Order Book is updated accordingly.
    5. Cancelling some of the orders that were placed.
    6. Verifying that the Order Book is updated accordingly.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/itch_tests/some_orders_cancelled_test.py",
                 "TestSomeOrdersCancelled_OrderBook_verification")
@pytest.mark.usefixtures("r_customer")
class TestSomeOrdersCancelled(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    order_buy = Order()
    order_buy.set_order(1, instrument_id, quantity_buy, price_for_buy)

    order_sell = Order()
    order_sell.set_order(2, instrument_id, quantity_sell, price_for_sell)

    # Those class variables are used to save the time when the order ID's.
    placed_buy_order_id = ""
    placed_sell_order_id = ""

    @automation_logger(logger)
    @allure.step("Place the 'Buy' order twice")
    @pytest.mark.parametrize('itch_order_buy', [[instrument_id, quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('itch_order_sell', [[instrument_id, quantity_sell, price_for_sell]], indirect=True)
    def test_place_order_buy(self, r_customer, create_customer, itch_order_buy, itch_order_sell):

        TestSomeOrdersCancelled.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        TestSomeOrdersCancelled.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)

        Instruments.set_price_last_trade(instrument_id, reference_price)
        Instruments.set_ticker_last_price(instrument_id, reference_price)

        order_response = r_customer.postman.order_service.create_order_sync(TestSomeOrdersCancelled.order_buy)
        assert order_response['error'] is None

        TestSomeOrdersCancelled.placed_buy_order_id = order_response['result']['orderId']

    @allure.step("Place the 'Sell' order twice ")
    @automation_logger(logger)
    def test_place_order_sell(self, r_customer):

        order_response = r_customer.postman.order_service.create_order_sync(TestSomeOrdersCancelled.order_sell)
        assert order_response['error'] is None

        TestSomeOrdersCancelled.placed_sell_order_id = order_response['result']['orderId']

        Instruments.set_price_last_trade(instrument_id, TestSomeOrdersCancelled.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestSomeOrdersCancelled.original_ticker_last)

    @allure.step("Verify 'Buy' Order Book is updated accordingly.")
    @automation_logger(logger)
    def test_buy_order_book(self):
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "sell", 2)

        assert len(order_book) == 1
        for record in order_book:
            # Price verification
            assert record[0] == price_for_buy
            # Quantity verification
            assert record[1] == quantity_buy * 2

    @allure.step("Verify 'Sell' Order Book is updated accordingly.")
    @automation_logger(logger)
    def test_sell_order_book(self):
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert len(order_book) == 1

        for record in order_book:
            assert record[0] == price_for_sell
            assert record[1] == quantity_sell * 2

    @allure.step("Cancelling some of the orders that were placed.")
    @automation_logger(logger)
    def test_some_orders_cancelled(self, r_customer):
        # Five seconds must pass before the order can be cancelled.
        time.sleep(CANCELLING_ORDERS_DELAY)
        cancel_sell_order = r_customer.postman.order_service.cancel_order(TestSomeOrdersCancelled.placed_sell_order_id)

        assert cancel_sell_order['error'] is None
        cancel_buy_order = r_customer.postman.order_service.cancel_order(TestSomeOrdersCancelled.placed_buy_order_id)
        assert cancel_buy_order['error'] is None

    @allure.step("Verifying that the Order Book is updated accordingly")
    @automation_logger(logger)
    def test_verify_order_book(self, r_customer):
        order_book_buy = Instruments.get_orders_best_price_and_quantity(instrument_id, "sell", 2)

        # Orders that weren't cancelled must still be presented in Order Book
        assert len(order_book_buy) == 1
        for record in order_book_buy:
            # Price verification
            assert record[0] == price_for_buy
            # Quantity verification
            assert record[1] == quantity_buy

        order_book_sell = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert len(order_book_sell) == 1

        for record in order_book_sell:
            assert record[0] == price_for_sell
            assert record[1] == quantity_sell

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
