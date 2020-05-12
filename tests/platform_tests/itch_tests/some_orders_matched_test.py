import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "some_orders_matched_itch_test"

"""
This test comes to verify that record in Order Book is updated accordingly when
some of the orders placed with a given price are matched and no longer open. The record shouldn't be removed, record
quantity should be updated accordingly.

Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Set the reference price to the REFERENCE_PRICE.
    5. Place the 'Buy' order.
    6. Place the 'Sell' order.
    7. Verify 'Buy' Order Book is updated accordingly.
    8. Verify 'Sell' Order Book is updated accordingly.
    9. Make sure that the 'Buy' and the 'Sell' orders are partially filled.
    10. Verify Order book is updated accordingly.
"""

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

reference_price = 5
price_for_buy = reference_price - 2
price_for_sell = reference_price + 2
quantity_buy = 160.0
quantity_sell = 140.0

CANCELLING_ORDERS_DELAY = 5
TRADE_PROCESSING_DELAY = 4


@pytest.mark.incremental
@allure.feature("Order Book update - end to end test.")
@allure.story("Partially Matched orders are updated in Order Book - end to end test.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Verify 'Buy' Order Book is updated accordingly.
    2. Verify 'Sell' Order Book is updated accordingly.
    3. Make sure that the 'Buy' and the 'Sell' orders are partially filled.
    4. Verify Order book is updated accordingly.
    5. Restore the original last trade  price and ticker last.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/itch_tests/some_orders_matched_test.py",
                 "TestOrderBook_update_verification")
@pytest.mark.usefixtures("r_customer")
class TestSomeOrdersMatched(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    @automation_logger(logger)
    @allure.step("Verify 'Buy' Order Book is updated accordingly.")
    @pytest.mark.parametrize('itch_order_buy', [[instrument_id, quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('itch_order_sell', [[instrument_id, quantity_sell, price_for_sell]], indirect=True)
    def test_buy_order_book(self, r_customer, create_customer, itch_order_buy, itch_order_sell):
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "sell", 2)
        # Only one record must be added to the Order Book.
        assert len(order_book) == 1

        for record in order_book:
            # Price verification
            assert record[0] == price_for_buy
            # Quantity verification
            assert record[1] == quantity_buy

    @allure.step("Verify 'Sell' Order Book is updated accordingly.")
    @automation_logger(logger)
    def test_sell_order_book(self):
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert len(order_book) == 1

        for record in order_book:
            assert record[0] == price_for_sell
            assert record[1] == quantity_sell

    @allure.step("Make sure that the 'Buy' and the 'Sell' orders are partially filled.")
    @automation_logger(logger)
    def test_place_matching_orders(self, r_customer):

        # Waiting for the trades to be processed.
        time.sleep(TRADE_PROCESSING_DELAY)

        TestSomeOrdersMatched.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        TestSomeOrdersMatched.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)

        Instruments.set_price_last_trade(instrument_id, reference_price)
        Instruments.set_ticker_last_price(instrument_id, reference_price)

        match_buy = Order().set_order(2, instrument_id, quantity_buy/2, price_for_buy)
        response = r_customer.postman.order_service.create_order(match_buy)
        assert response['error'] is None

        match_sell = Order().set_order(1, instrument_id, quantity_sell/2, price_for_sell)
        response = r_customer.postman.order_service.create_order(match_sell)
        assert response['error'] is None

        Instruments.set_price_last_trade(instrument_id, TestSomeOrdersMatched.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestSomeOrdersMatched.original_ticker_last)

    @allure.step("Verify Order book is updated accordingly.")
    @automation_logger(logger)
    def test_order_book_updated(self, r_customer):

        order_book_buy = Instruments.get_orders_best_price_and_quantity(instrument_id, "sell", 2)
        # Only one record must be added to the Order Book.
        assert len(order_book_buy) == 1
        for record in order_book_buy:
            # Price verification
            assert record[0] == price_for_buy
            # Quantity verification
            assert record[1] == quantity_buy/2

        order_book_sell = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert len(order_book_sell) == 1

        for record in order_book_sell:
            assert record[0] == price_for_sell
            assert record[1] == quantity_sell/2

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
