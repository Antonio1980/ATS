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
    In this test 2 orders are placed - the Buy order and the Sell order.
    Two orders are matched, while Buy order is 10% filled and Sell order is 100% filled.
    This test comes to verify, that both orders data is updated accordingly in DB and in Redis
"""

test_case = "6831"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_sell = quantity_buy / 10  # For this test "quantity_sell" must be 10% of "quantity_buy".

TRADE_PROCESS_DELAY = 5


@allure.feature("Order is 10% filled - order parameters are updated")
@allure.story("Partially filled order parameters are updated.")
@allure.title("Order is 10% filled - order parameters are updated")
@allure.description("""
    Functional tests.
    
    1. Verify Quantity and Filled Quantity of both orders in DB.
    2. Verify Quantity and Filled Quantity of the open order in Redis. 
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6828_filled_10_balance_update_test.py",
                 "TestPartiallyFilled_10")
@pytest.mark.usefixtures("r_customer")
class TestOrderPartiallyFilled(object):

    @allure.step("Verify Quantity and Filled Quantity of both orders in DB.")
    @automation_logger(logger)
    @pytest.mark.parametrize('place_order_buy', [[quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('place_order_sell', [[quantity_sell, price_for_sell]], indirect=True)
    def test_find_orders_in_db(self, r_customer, make_customer, place_order_buy, place_order_sell):
        TestOrderPartiallyFilled.buyer = make_customer[0]
        TestOrderPartiallyFilled.buyer_token = make_customer[0].static_token

        TestOrderPartiallyFilled.seller = make_customer[1]
        TestOrderPartiallyFilled.seller_token = make_customer[1].static_token

        # Wait for the orders to be processed and saved in DB.
        time.sleep(TRADE_PROCESS_DELAY)

        # Get order by Order ID from DB and verify filled quantity and status.

        # "Buy" order, partially filled.
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(place_order_buy.internal_id))
        print(F"Buy Order In DB: {buy_order_in_db}")
        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == place_order_buy.quantity
        assert buy_order_in_db[0].filled_quantity == place_order_sell.quantity

        # "Sell" order, 100% filled
        sell_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(place_order_sell.internal_id))
        print(F"Sell Order In DB: {sell_order_in_db}")
        assert len(sell_order_in_db) == 1
        assert sell_order_in_db[0].quantity == place_order_sell.quantity
        assert sell_order_in_db[0].filled_quantity == place_order_sell.quantity

    @allure.step("Verify Quantity and Filled Quantity of the open order in Redis.")
    @automation_logger(logger)
    def test_find_orders_in_redis(self, r_customer, make_customer, place_order_buy, place_order_sell):
        orders_in_redis = Instruments.get_orders_by_customer_redis(TestOrderPartiallyFilled.buyer.customer_id)
        print(F"Orders in Redis: {orders_in_redis}")

        # Only the "Buy" order should remain open, since it's 10% filled.
        assert len(orders_in_redis) == 1

        # Converting data to JSON format
        orders_verification = json.loads(orders_in_redis[0])

        logger.logger.info(F"Buy order in Redis: {place_order_buy.internal_id}")
        print(F"Buy order in Redis: {place_order_buy.internal_id}")

        # Verifying order details in Redis
        assert orders_verification['id'] == place_order_buy.internal_id
        assert orders_verification['direction'] == "BUY"
        assert orders_verification['status'] == "OPEN"

        redis_price = Calculator.value_decimal(orders_verification['price'])
        assert redis_price == price_for_buy

        redis_quantity = Calculator.value_decimal(orders_verification['quantity'])
        assert redis_quantity == quantity_buy

        redis_filled_quantity = Calculator.value_decimal(orders_verification['filledQuantity'])
        assert redis_filled_quantity == quantity_sell

        assert float(quantity_buy * 0.1) == float(redis_filled_quantity)

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
