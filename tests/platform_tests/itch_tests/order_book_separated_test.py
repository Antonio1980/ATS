import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "order_book_separated_test"

"""
This test comes to verify that each instrument Order Book is independent.
For example - when XRP/EUR Order Book is updated the Order Book on BTC/EUR shouldn't be affected.

Original test flow:

    1. Clear the Order Book for two instruments.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Set the reference price to the REFERENCE_PRICE.
    5. Place the 'Buy' order.
    6. Place the 'Sell' order.
    7. Verify 'Buy' Order Book is updated accordingly.
    8. Verify 'Sell' Order Book is updated accordingly.
    9. Verify test instrument Order Book remains empty.
"""


# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

standart_price = 5
price_for_buy = standart_price - 2
price_for_sell = standart_price + 2
quantity_buy = 80.0
quantity_sell = 70.0

# This instrument is used for comparison - it's Order Book shouldn't be modified.
test_instrument_id = 1012
test_base_currency = 3
test_quoted_currency = 2


@pytest.mark.incremental
@allure.feature("Order Book update - end to end test.")
@allure.story("Order Book updated when an order is placed - end to end test.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
  
    1. Verify 'Buy' Order Book is updated accordingly.
    2. Verify 'Sell' Order Book is updated accordingly.
    3. Verify test instrument Order Book remains empty.
   
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/itch_tests/order_book_separated_test.py",
                 "TestOrderBook_separated_verification")
@pytest.mark.usefixtures("r_customer")
class TestOrderBookSeparated(object):

    @automation_logger(logger)
    @allure.step("Verify 'Buy' Order Book is updated accordingly.")
    @pytest.mark.parametrize('itch_order_buy', [[instrument_id, quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('itch_order_sell', [[instrument_id, quantity_sell, price_for_sell]], indirect=True)
    def test_buy_order_book(self, r_customer, create_customer, itch_order_buy, itch_order_sell):

        # Cleaning the Order Book for test_instrument. After it's done, Order Book is empty for both instruments.
        r_customer.clean_instrument(test_instrument_id, test_base_currency, test_quoted_currency)

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

    @allure.step("Verify test instrument Order Book remains empty.")
    @automation_logger(logger)
    def test_verify_order_book_separated(self, r_customer):
        order_book = Instruments.get_orders_best_price_and_quantity(test_instrument_id, "buy", 2)
        assert order_book is None

        order_book = Instruments.get_orders_best_price_and_quantity(test_instrument_id, "sell", 2)
        assert order_book is None

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
