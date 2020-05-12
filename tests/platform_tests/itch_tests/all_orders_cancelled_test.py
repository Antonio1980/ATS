import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "all_orders_cancelled_itch_test"

"""
This test comes to verify, that when all orders with a given price are cancelled
the record related to that price is removed from the Order Book. Updated are received
from ME and the Order Book on our side is updated accordingly.

Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Set the reference price to the REFERENCE_PRICE.
    5. Place the 'Buy' order.
    6. Place the 'Sell' order.
    7. Verify 'Buy' Order Book is updated accordingly.
    8. Verify 'Sell' Order Book is updated accordingly.
    9. Sell Order Cancellation - Order Book verified.
    10. Buy Order Cancellation - Order Book verified.
    11. Restore the original last trade  price and ticker last.
"""


# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

reference_price = 5
price_for_buy = reference_price - 2
price_for_sell = reference_price + 2
quantity_buy = 80.0
quantity_sell = 70.0

CANCELLING_ORDERS_DELAY = 5.0


@pytest.mark.incremental
@allure.feature("Order Book update - end to end test.")
@allure.story("Order Book updated when all orders are cancelled - end to end test.")
@allure.title("Order Book update - end to end test.")
@allure.description("""
    Functional tests:
    1. Sell Order Cancellation - Order Book verified.
    2. Buy Order Cancellation - Order Book verified.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/itch_tests/all_orders_cancelled_test.py",
                 "TestOrdersCancelled_OrderBook_update_verification")
@pytest.mark.usefixtures("r_customer")
class TestOrdersCancelled(object):

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
    def test_sell_order_book(self, r_customer, create_customer, itch_order_buy, itch_order_sell):
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert len(order_book) == 1

        for record in order_book:
            assert record[0] == price_for_sell
            assert record[1] == quantity_sell

    @allure.step("Sell Order Cancellation - Order Book verified.")
    @automation_logger(logger)
    def test_sell_order_cancelled(self, r_customer, create_customer, itch_order_buy, itch_order_sell):
        # Five seconds must pass before the order can be cancelled.
        time.sleep(CANCELLING_ORDERS_DELAY)
        cancel_sell_order = r_customer.postman.order_service.cancel_order(
            itch_order_sell.internal_id)
        assert cancel_sell_order['error'] is None

        # Verifying that "Sell" Order Book is empty.
        order_book_sell = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert order_book_sell is None

        # Verifying that "Buy" Order Book wasn't modified.
        order_book_buy = Instruments.get_orders_best_price_and_quantity(instrument_id, "sell", 2)
        assert len(order_book_buy) == 1

        for record in order_book_buy:
            # Price verification
            assert record[0] == price_for_buy
            # Quantity verification
            assert record[1] == quantity_buy

    @allure.step("Buy Order Cancellation - Order Book verified.")
    @automation_logger(logger)
    def test_buy_order_cancelled(self, r_customer, create_customer, itch_order_buy, itch_order_sell):
        cancel_buy_order = r_customer.postman.order_service.cancel_order(
            itch_order_buy.internal_id)
        assert cancel_buy_order['error'] is None

        buy_order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "sell", 2)
        assert buy_order_book is None

        sell_order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert sell_order_book is None

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
