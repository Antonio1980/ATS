import time
import json
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.utils.calculator import Calculator

"""
    In this test 3 orders are placed - one Buy order and two Sell orders.
    Buy order quantity is 700, and it's half filled.
    Sell orders quantities are 70 and 280 , each of them is fully filled.
    This test comes to verify, that buy and sell orders data is updated correctly
    in MySQL DB and redis after orders are matched.

    Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Change current reference price to 'price_for_buy' in order to place an order with a unique price..
    5. Place the Buy orders.
    6. Place the Sell orders.
    7. Restore the original last trade  price and ticker last.
    8. Verify Quantity and Filled Quantity of all the three orders in DB.
    9. Verify Quantity and Filled Quantity of the 'Buy' order in Redis - the only one that remains open.
"""

test_case = "6832"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_10_sell = quantity_buy / 10  # For this test "quantity_10_sell" must be 10% of "quantity_buy".
quantity_40_sell = quantity_buy * 0.4  # For this test "quantity_40_sell" must be 40% of "quantity_buy".

TRADE_PROCESSING_DELAY = 5


@allure.feature("Order is 50% filled - order parameters are updated")
@allure.story("Partially filled order parameters are updated.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    
    1. Verify Quantity and Filled Quantity of all the three orders in DB.
    2. Verify Quantity and Filled Quantity of the 'Buy' order in Redis - the only one that remains open.
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6832_buy_order_params_50_filled_test.py",
                 "TestHalfFilled_50")
@pytest.mark.usefixtures("r_customer")
class TestOrderHalfFilled(object):

    @allure.step("Verify Quantity and Filled Quantity of all the three orders in DB.")
    @automation_logger(logger)
    @pytest.mark.parametrize('place_order_buy', [[quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize(
        'place_two_sell_orders', [[quantity_10_sell, quantity_40_sell, price_for_sell, price_for_sell]], indirect=True)
    def test_find_orders_in_db(self, r_customer, make_customer, place_order_buy, place_two_sell_orders):
        # Wait for the orders to be processed and saved in DB.
        time.sleep(TRADE_PROCESSING_DELAY)

        # Get order by Order ID from DB and verify filled quantity and status.

        # "Buy" order, 50% filled.
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(place_order_buy.internal_id))
        print(F"Buy Order In DB: {buy_order_in_db}")

        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == place_order_buy.quantity
        assert buy_order_in_db[0].filled_quantity == (
                place_two_sell_orders[0].quantity + place_two_sell_orders[1].quantity)

        # Filled Quantity in MySQL DB must be 60% of the Total Quantity.
        assert buy_order_in_db[0].filled_quantity == quantity_buy * 0.5

        # "Sell" 10 order, 100% filled
        sell_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(place_two_sell_orders[0].internal_id))

        print(F"Sell Order In DB: {sell_order_in_db}")
        logger.logger.info(F"Sell Order In DB: {sell_order_in_db}")

        assert len(sell_order_in_db) == 1
        assert sell_order_in_db[0].quantity == place_two_sell_orders[0].quantity
        assert sell_order_in_db[0].filled_quantity == place_two_sell_orders[0].quantity

        # "Sell" 50 order, 100% filled
        sell_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(place_two_sell_orders[1].internal_id))

        print(F"Sell Order In DB: {sell_order_in_db}")
        logger.logger.info(F"Sell Order In DB: {sell_order_in_db}")

        assert len(sell_order_in_db) == 1
        assert sell_order_in_db[0].quantity == place_two_sell_orders[1].quantity
        assert sell_order_in_db[0].filled_quantity == place_two_sell_orders[1].quantity

    @allure.step("Verify Quantity and Filled Quantity of the 'Buy' order in Redis - the only one that remains open.")
    @automation_logger(logger)
    def test_find_orders_in_redis(self, r_customer, make_customer, place_order_buy, place_two_sell_orders):
        orders_in_redis = Instruments.get_orders_by_customer_redis(make_customer[0].customer_id)
        print(F"Orders in Redis: {orders_in_redis}")

        # Only the "Buy" order should remain open, since it's 50% filled.
        assert len(orders_in_redis) == 1

        # Converting data to JSON format
        orders_verification = json.loads(orders_in_redis[0])

        logger.logger.info(f"Orders in Redis: {orders_verification}")
        print(f"Orders in Redis: {orders_verification}")

        # Verifying order details in Redis
        assert orders_verification['id'] == place_order_buy.internal_id
        assert orders_verification['direction'] == "BUY"
        assert orders_verification['status'] == "OPEN"

        redis_price = Calculator.value_decimal(orders_verification['price'])
        assert redis_price == price_for_buy

        redis_quantity = Calculator.value_decimal(orders_verification['quantity'])
        assert redis_quantity == quantity_buy

        # Filled Quantity in Redis must be 50% of the Total Quantity.
        redis_filled_quantity = Calculator.value_decimal(orders_verification['filledQuantity'])
        assert redis_filled_quantity == quantity_10_sell + quantity_40_sell

        assert float(quantity_buy * 0.5) == float(redis_filled_quantity)

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
