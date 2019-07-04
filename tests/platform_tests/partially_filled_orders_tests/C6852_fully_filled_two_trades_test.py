import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.equipment.trade import Trade

test_case = "6852"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_sell_10 = quantity_buy * 0.1
quantity_sell_90 = quantity_buy * 0.9

PROCESSING_ORDERS_DELAY = 6


@allure.feature("Order is fully filled - two trades are created and splitted to 'Buy' and 'Sell'. ")
@allure.story("Trade is created each time an order is matched. ")
@allure.title("Order is fully filled - two trades are created and splitted to 'Buy' and 'Sell'.")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders
    3. Add funds to customer's available balance and verify
    4. Change current reference price to 'price_for_buy'.
    5. Place the Buy order, quantity - 700.
    6. Place the Sell_10 order, quantity - 70.
    7. Place the Sell_90 order, quantity - 630.
    8. Restore the original last trade  price and ticker last.
    9. Two 'Sell' trades are created - trade parameters verification.
    10. Two 'Buy' trades are created - trade parameters verification.
    11. Verify 'Buy' order parameters in DB. 
  """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6852_fully_filled_two_trades_test.py",
                 "TestPartiallyFilled_TwoTrades")
@pytest.mark.usefixtures("r_customer")
class TestTwoTradesCreated(object):

    original_last_trade_price = ""
    original_ticker_last = ""

    order_buy = Order()
    order_buy.set_order(1, instrument_id, quantity_buy, price_for_buy)

    order_sell_10 = Order()
    order_sell_10.set_order(2, instrument_id, quantity_sell_10, price_for_sell)

    order_sell_90 = Order()
    order_sell_90.set_order(2, instrument_id, quantity_sell_90, price_for_sell)

    # Those class variables are used to save placed orders ID's.
    placed_buy_order_id = ""

    placed_sell_10_order_id = ""
    placed_sell_90_order_id = ""

    @allure.step("Clear the Order Book for the selected instrument.")
    @automation_logger(logger)
    def test_janitor(self, r_customer):
        r_customer.clean_instrument(instrument_id, base_currency, quoted_currency)

    @allure.step("Clear the balance of the customer used for this test, cancel all orders")
    @automation_logger(logger)
    def test_clean_up_customer(self, r_customer):
        r_customer.clean_up_customer()
        cur_orders = r_customer.postman.order_service.get_open_orders()
        assert len(cur_orders['result']['orders']) == 0
        print(F"Clean Customer method - existing orders: {cur_orders['result']['orders']}")

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

    @allure.step("Change current reference price to 'price_for_buy'.")
    @automation_logger(logger)
    def test_change_reference_price(self, r_customer):
        TestTwoTradesCreated.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        Instruments.set_price_last_trade(instrument_id, price_for_buy)
        assert int(Instruments.get_price_last_trade(instrument_id)) == price_for_buy

        TestTwoTradesCreated.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)
        Instruments.set_ticker_last_price(instrument_id, price_for_buy)
        assert int(Instruments.get_ticker_last_price(instrument_id)) == price_for_buy

    @allure.step("Place the Buy order, quantity - 700.")
    @automation_logger(logger)
    def test_place_order_buy(self, r_customer):
        order_response = r_customer.postman.order_service.create_order_sync(TestTwoTradesCreated.order_buy)
        assert order_response['error'] is None

        TestTwoTradesCreated.placed_buy_order_id = order_response['result']['orderId']

    @allure.step("Place the Sell_10 order, quantity - 70.")
    @automation_logger(logger)
    def test_place_order_10_sell(self, r_customer):
        order_response = r_customer.postman.order_service.create_order_sync(TestTwoTradesCreated.order_sell_10)
        assert order_response['error'] is None

        TestTwoTradesCreated.placed_sell_10_order_id = order_response['result']['orderId']

    @allure.step("Place the Sell_60 order, quantity - 630.")
    @automation_logger(logger)
    def test_place_order_90_sell(self, r_customer):
        order_response = r_customer.postman.order_service.create_order_sync(TestTwoTradesCreated.order_sell_90)
        assert order_response['error'] is None

        TestTwoTradesCreated.placed_sell_90_order_id = order_response['result']['orderId']

    @allure.step("Restore the original last trade  price and ticker last.")
    @automation_logger(logger)
    def test_restore_original_price(self):
        # Wait for trade to be processed before the original price is restored.
        time.sleep(PROCESSING_ORDERS_DELAY)

        Instruments.set_price_last_trade(instrument_id, TestTwoTradesCreated.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestTwoTradesCreated.original_ticker_last)

    @allure.step("Two 'Sell' trades are created - trade parameters verification")
    @automation_logger(logger)
    def test_verify_sell_trade_in_db(self, r_customer):
        # Bringing "Sell" trade from MySQL DB - 70 XRP were sold.
        sell_trade_10 = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(TestTwoTradesCreated.placed_sell_10_order_id))

        # Verifying "Sell" trade quantity and price.
        assert len(sell_trade_10) == 1
        assert sell_trade_10[0].direction == "sell"
        assert sell_trade_10[0].price == price_for_sell
        assert sell_trade_10[0].quantity == quantity_sell_10

        # Bringing "Sell" trade from MySQL DB - 420 XRP were sold.
        sell_trade_90 = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(TestTwoTradesCreated.placed_sell_90_order_id))

        # Verifying "Sell" trade quantity and price.
        assert len(sell_trade_90) == 1
        assert sell_trade_90[0].direction == "sell"
        assert sell_trade_90[0].price == price_for_sell
        assert sell_trade_90[0].quantity == quantity_sell_90

    @allure.step("Two 'Buy' trades are created - trade parameters verification")
    @automation_logger(logger)
    def test_verify_buy_trade_in_db(self, r_customer):
        # Bringing trades from MySQL DB.
        buy_trades = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(TestTwoTradesCreated.placed_buy_order_id))

        # Verifying "Buy" trade quantity and price.
        assert len(buy_trades) == 2

        # Verifying the first "Buy" trade - 70 XRP were bough.
        assert buy_trades[0].direction == "buy"
        assert buy_trades[0].price == price_for_buy
        assert buy_trades[0].quantity == quantity_sell_10

        # Verifying the second "Buy" trade - 420 XRP were bough.
        assert buy_trades[1].direction == "buy"
        assert buy_trades[1].price == price_for_buy
        assert buy_trades[1].quantity == quantity_sell_90

    @allure.step("Verify 'Buy' order parameters in DB")
    @automation_logger(logger)
    def test_verify_buy_order_in_db(self, r_customer):
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(TestTwoTradesCreated.placed_buy_order_id))

        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == TestTwoTradesCreated.order_buy.quantity
        # "Buy" order has matched with both "Sell" orders. Filled quantity must be updated accordingly.
        assert buy_order_in_db[0].filled_quantity == quantity_sell_10 + quantity_sell_90

        logger.logger.info(f"================== TEST CASE IS PASSED {test_case} ===================")
        print(f"================== TEST CASE IS PASSED {test_case} ===================")
