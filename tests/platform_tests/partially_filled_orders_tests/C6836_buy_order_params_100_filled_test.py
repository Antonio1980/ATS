import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "6836"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 1000.00

# The parameters below are mandatory to sustain test conditions.
quantity_30_sell = quantity_buy * 0.3  # For this test "quantity_30_sell" must be 30% of "quantity_buy".
quantity_70_sell = quantity_buy * 0.7  # For this test "quantity_70_sell" must be 70% of "quantity_buy".

CANCELLING_ORDERS_DELAY = 5


@allure.feature("Order is 100% filled - order parameters are updated")
@allure.story("Order filled in two steps, order parameters are updated.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Change current reference price to 'price_for_buy' in order to place an order with a unique price..
    5. Place the Buy orders.
    6. Place the Sell orders.
    7. Restore the original last trade  price and ticker last.
    8. Verify Quantity and Filled Quantity of all the three orders in DB.
    9. Verify Filled Order are removed from Redis.
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6836_buy_order_params_100_filled_test.py",
                 "TestOrderFilled_100")
@pytest.mark.usefixtures("r_customer")
class TestOrderFilled(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    # Those class variables are used to save placed orders ID's.
    placed_buy_order_id = ""
    redis_buy_order_id = ""

    placed_sell_30_order_id = ""
    redis_sell_30_order_id = ""

    placed_sell_70_order_id = ""
    redis_sell_70_order_id = ""

    order_buy = Order().set_order(1, instrument_id, quantity_buy, price_for_buy)
    order_30_sell = Order().set_order(2, instrument_id, quantity_30_sell, price_for_sell)
    order_70_sell = Order().set_order(2, instrument_id, quantity_70_sell, price_for_sell)

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
        print(F"Existing orders: {cur_orders['result']['orders']}")


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
        TestOrderFilled.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        Instruments.set_price_last_trade(instrument_id, price_for_buy)
        assert int(Instruments.get_price_last_trade(instrument_id)) == price_for_buy

        TestOrderFilled.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)
        Instruments.set_ticker_last_price(instrument_id, price_for_buy)
        assert int(Instruments.get_ticker_last_price(instrument_id)) == price_for_buy

    @allure.step("Place the Buy order.")
    @automation_logger(logger)
    def test_place_order_buy(self, r_customer):
        order_response = r_customer.postman.order_service.create_order_sync(TestOrderFilled.order_buy)
        assert order_response['error'] is None

        TestOrderFilled.placed_buy_order_id = order_response['result']['orderId']

    @allure.step("Place the Sell orders.")
    @automation_logger(logger)
    def test_place_orders_sell(self, r_customer):
        order_30_response = r_customer.postman.order_service.create_order_sync(TestOrderFilled.order_30_sell)
        assert order_30_response['error'] is None

        TestOrderFilled.placed_sell_30_order_id = order_30_response['result']['orderId']

        order_70_response = r_customer.postman.order_service.create_order_sync(TestOrderFilled.order_70_sell)
        assert order_70_response['error'] is None

        TestOrderFilled.placed_sell_70_order_id = order_70_response['result']['orderId']

    @allure.step("Restore the original last trade  price and ticker last.")
    @automation_logger(logger)
    def test_restore_original_price(self):
        # Wait for trade to be processed before the original price is restored.
        time.sleep(3)
        Instruments.set_price_last_trade(instrument_id, TestOrderFilled.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestOrderFilled.original_ticker_last)

    @allure.step("Verify Quantity and Filled Quantity of all the three orders in DB.")
    @automation_logger(logger)
    def test_find_orders_in_db(self, r_customer):
        # Wait for the orders to be processed and saved in DB.
        time.sleep(2)

        # Get order by Order ID from DB and verify filled quantity and status.

        # "Buy" order, 100% filled.
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(TestOrderFilled.placed_buy_order_id))
        print(F"Buy Order In DB: {buy_order_in_db}")

        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == TestOrderFilled.order_buy.quantity
        assert buy_order_in_db[0].filled_quantity == (
                TestOrderFilled.order_30_sell.quantity + TestOrderFilled.order_70_sell.quantity)

        # Filled Quantity in MySQL DB must be 100% of the Total Quantity.
        assert buy_order_in_db[0].filled_quantity == quantity_buy

        # "Sell" 30 order, 100% filled
        sell_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(TestOrderFilled.placed_sell_30_order_id))
        print(F"Sell Order In DB: {sell_order_in_db}")
        assert len(sell_order_in_db) == 1
        assert sell_order_in_db[0].quantity == TestOrderFilled.order_30_sell.quantity
        assert sell_order_in_db[0].filled_quantity == TestOrderFilled.order_30_sell.quantity

        # "Sell" 70 order, 100% filled
        sell_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(TestOrderFilled.placed_sell_70_order_id))
        print(F"Sell Order In DB: {sell_order_in_db}")
        assert len(sell_order_in_db) == 1
        assert sell_order_in_db[0].quantity == TestOrderFilled.order_70_sell.quantity
        assert sell_order_in_db[0].filled_quantity == TestOrderFilled.order_70_sell.quantity

    @allure.step("Verify Filled Order are removed from Redis.")
    @automation_logger(logger)
    def test_find_orders_in_redis(self, r_customer):
        orders_in_redis = Instruments.get_orders_by_customer_redis(r_customer.customer_id)
        print(F"Orders in Redis: {orders_in_redis}")

        assert len(orders_in_redis) == 0

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")

