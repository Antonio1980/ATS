import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "tail_digits_itch_test"

# The parameters below are used for test configuration
instrument_id = 1012  # BTC/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

reference_price = 5000.11
price_for_buy = reference_price - 2
price_for_sell = reference_price + 2
quantity_buy = 1.111111
quantity_sell = 1.111111

CANCELLING_ORDERS_DELAY = 5


@pytest.mark.incremental
@allure.feature("Order Book update - end to end test.")
@allure.story("Verifying that Order Book is updated correctly when quantity and price are fractions.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Set the reference price to the REFERENCE_PRICE.
    5. Place the 'Buy' order.
    6. Place the 'Sell' order.
    7. Verify 'Buy' Order Book is updated accordingly, including price and quantity Tail Digits.
    8. Verify 'Sell' Order Book is updated accordingly, including price and quantity Tail Digits. 
    9. Restore the original last trade  price and ticker last.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/itch_tests/tail_digits_test.py",
                 "Tail_Digits_verification")
@pytest.mark.usefixtures("r_customer")
class TestTailDigits(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    order_buy = Order()
    order_buy.set_order(1, instrument_id, quantity_buy, price_for_buy)

    order_sell = Order()
    order_sell.set_order(2, instrument_id, quantity_sell, price_for_sell)

    # Those class variables are used to save the time when the order ID's.
    placed_buy_order_id = ""
    redis_buy_order_id = ""

    placed_sell_order_id = ""
    redis_sell_order_id = ""

    @allure.step("Clear the Order Book for the selected instrument.")
    @automation_logger(logger)
    def test_janitor(self, r_customer):
        TestTailDigits.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        TestTailDigits.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)

        r_customer.clean_instrument(instrument_id, base_currency, quoted_currency)

    @allure.step("Clear the balance of the customer used for this test, cancel all orders.")
    @automation_logger(logger)
    def test_clean_up_customer(self, r_customer):
        r_customer.clean_up_customer()
        cur_orders = r_customer.postman.order_service.get_open_orders()
        assert len(cur_orders['result']['orders']) == 0
        print(F"Existing orders: {cur_orders['result']['orders']}")

    @allure.step("Add funds to customer's available balance and verify.")
    @automation_logger(logger)
    def test_add_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, quoted_currency, 10000)
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, base_currency, 10000)

        current_balance = \
            r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, quoted_currency)['result'][
                'balance']['available']

        assert float(current_balance) >= 10000
        current_balance = \
            r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, base_currency)['result'][
                'balance']['available']
        assert float(current_balance) >= 10000

    @allure.step("Set the reference price to the REFERENCE_PRICE")
    @automation_logger(logger)
    def test_change_reference_price(self, r_customer):

        Instruments.set_price_last_trade(instrument_id, reference_price)
        assert float(Instruments.get_price_last_trade(instrument_id)) == reference_price


        Instruments.set_ticker_last_price(instrument_id, reference_price)
        assert float(Instruments.get_ticker_last_price(instrument_id)) == reference_price

    @allure.step("Place the 'Buy' order")
    @automation_logger(logger)
    def test_place_order_buy(self, r_customer):

        order_response = r_customer.postman.order_service.create_order_sync(TestTailDigits.order_buy)
        assert order_response['error'] is None

        TestTailDigits.placed_buy_order_id = order_response['result']['orderId']

    @allure.step("Place the 'Sell' order")
    @automation_logger(logger)
    def test_place_order_sell(self, r_customer):

        order_response = r_customer.postman.order_service.create_order_sync(TestTailDigits.order_sell)
        assert order_response['error'] is None

        TestTailDigits.placed_sell_order_id = order_response['result']['orderId']

    @allure.step("Verify 'Buy' Order Book is updated accordingly, including price and quantity Tail Digits.")
    @automation_logger(logger)
    def test_buy_order_book(self):
        order_book = Instruments.get_orders_best_price_and_quantity(1012, "sell", 2)
        # Only one record must be added to the Order Book.
        assert len(order_book) == 1
        for record in order_book:
            # Price verification
            assert record[0] == price_for_buy
            # Quantity verification
            assert record[1] == quantity_buy

    @allure.step("Verify 'Sell' Order Book is updated accordingly, including price and quantity Tail Digits.")
    @automation_logger(logger)
    def test_sell_order_book(self):
        order_book = Instruments.get_orders_best_price_and_quantity(1012, "buy", 2)
        assert len(order_book) == 1

        for record in order_book:
            assert record[0] == price_for_sell
            assert record[1] == quantity_sell

    @allure.step("Orders cancellation.")
    @automation_logger(logger)
    def test_cancel_placed_orders(self, r_customer):
        # Five seconds must pass before the order can be cancelled.
        time.sleep(CANCELLING_ORDERS_DELAY)
        cancel_sell_order = r_customer.postman.order_service.cancel_order(
            TestTailDigits.placed_sell_order_id)

        assert cancel_sell_order['error'] is None
        cancel_buy_order = r_customer.postman.order_service.cancel_order(TestTailDigits.placed_buy_order_id)
        assert cancel_buy_order['error'] is None

    @allure.step("Restore the original last trade  price and ticker last.")
    @automation_logger(logger)
    def test_restore_original_price(self):

        Instruments.set_price_last_trade(instrument_id, TestTailDigits.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestTailDigits.original_ticker_last)

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
