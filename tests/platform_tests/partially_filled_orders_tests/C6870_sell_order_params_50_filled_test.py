import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.utils.calculator import Calculator
import json

test_case = "6870"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 5
price_for_sell = price_for_buy
quantity_sell = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_buy = quantity_sell / 2  # For this test "quantity_buy" must be 50% of "quantity_sell".

ORDERS_PROCESSING_DELAY = 5


@allure.feature("Sell Order is 50% filled - order parameters are updated")
@allure.story("Half filled order parameters are updated - Sell.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Change current reference price to 'price_for_buy' .
    5. Place the Sell order, quantity - 700.
    6. Place the Buy order, quantity - 350.
    7. Restore the original last trade  price and ticker last.
    8. Verify Quantity and Filled Quantity of both orders in DB.
    9. Verify Quantity and Filled Quantity of the open order in Redis. 
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6870_sell_order_params_50_filled_test.py",
                 "TestPartiallyFilledSell_50")
@pytest.mark.usefixtures("r_customer")
class TestOrderHalfFilled(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    order_buy = Order()
    order_buy.set_order(1, instrument_id, quantity_buy, price_for_buy)

    order_sell = Order()
    order_sell.set_order(2, instrument_id, quantity_sell, price_for_sell)

    # Those class variables are used to save placed orders ID's.
    placed_buy_order_id = ""
    redis_buy_order_id = ""

    placed_sell_order_id = ""
    redis_sell_order_id = ""

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
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, quoted_currency, 100000)
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, base_currency, 100000)
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
        TestOrderHalfFilled.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        Instruments.set_price_last_trade(instrument_id, price_for_buy)
        assert int(Instruments.get_price_last_trade(instrument_id)) == price_for_buy

        TestOrderHalfFilled.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)
        Instruments.set_ticker_last_price(instrument_id, price_for_buy)
        assert int(Instruments.get_ticker_last_price(instrument_id)) == price_for_buy

    @allure.step("Place the Sell order, quantity - 700.")
    @automation_logger(logger)
    def test_place_order_sell(self, r_customer):
        balance = r_customer.postman.balance_service.get_all_currencies_balance(r_customer.customer_id)
        logger.logger.info("BALANCE", balance)
        order_response = r_customer.postman.order_service.create_order_sync(TestOrderHalfFilled.order_sell)
        assert order_response['error'] is None

        TestOrderHalfFilled.placed_sell_order_id = order_response['result']['orderId']

    @allure.step("Place the Buy order, quantity - 350.")
    @automation_logger(logger)
    def test_place_order_buy(self, r_customer):
        order_response = r_customer.postman.order_service.create_order_sync(TestOrderHalfFilled.order_buy)
        assert order_response['error'] is None

        TestOrderHalfFilled.placed_buy_order_id = order_response['result']['orderId']

    @allure.step("Restore the original last trade  price and ticker last.")
    @automation_logger(logger)
    def test_restore_original_price(self):
        # Wait for trade to be processed before the original price is restored.
        time.sleep(ORDERS_PROCESSING_DELAY)
        Instruments.set_price_last_trade(instrument_id, TestOrderHalfFilled.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestOrderHalfFilled.original_ticker_last)

    @allure.step("Verify Quantity and Filled Quantity of both orders in DB.")
    @automation_logger(logger)
    def test_find_orders_in_db(self, r_customer):
        # Get order by Order ID from DB and verify filled quantity and status.

        # "Buy" order, 100% filled.
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(TestOrderHalfFilled.placed_buy_order_id))
        print(F"Buy Order In DB: {buy_order_in_db}")
        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == quantity_buy
        assert buy_order_in_db[0].filled_quantity == quantity_buy

        # "Sell" order, 50% filled
        sell_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(TestOrderHalfFilled.placed_sell_order_id))
        print(F"Sell Order In DB: {sell_order_in_db}")
        assert len(sell_order_in_db) == 1
        assert sell_order_in_db[0].quantity == quantity_sell
        assert sell_order_in_db[0].filled_quantity == quantity_buy

    @allure.step("Verify Quantity and Filled Quantity of the open order in Redis.")
    @automation_logger(logger)
    def test_find_orders_in_redis(self, r_customer):
        orders_in_redis = Instruments.get_orders_by_customer_redis(r_customer.customer_id)
        print(F"Orders in Redis: {orders_in_redis}")

        # Only the "Buy" order should remain open, since it's 50% filled.
        assert len(orders_in_redis) == 1

        # Converting data to JSON format
        orders_verification = json.loads(orders_in_redis[0])

        print(F"Order Control: {TestOrderHalfFilled.placed_sell_order_id}")

        # Verifying order details in Redis
        assert orders_verification['id'] == TestOrderHalfFilled.placed_sell_order_id
        assert orders_verification['direction'] == "SELL"
        assert orders_verification['status'] == "OPEN"

        redis_price = Calculator.value_decimal(orders_verification['price'])
        assert redis_price == price_for_sell

        redis_quantity = Calculator.value_decimal(orders_verification['quantity'])
        assert redis_quantity == quantity_sell

        redis_filled_quantity = Calculator.value_decimal(orders_verification['filledQuantity'])
        assert redis_filled_quantity == quantity_buy

        assert float(quantity_sell * 0.5) == float(redis_filled_quantity)

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
