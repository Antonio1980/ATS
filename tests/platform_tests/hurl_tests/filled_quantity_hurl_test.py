import time
import json
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.utils.calculator import Calculator
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "filled_quantity_hurl_test"

# In this test we are placing two orders: Buy and Sell.
# Sell order quantity is half of Buy order quantity.
# Price is the same price.
# After both orders are placed Buy order is partially filled, Sell order is fully filled.
# First - we are verifying the data saved in MySQL DB for both orders.
# Second - we are verifying that "Buy" order is in Redis plus verifying the data in Redis.

# Original test flow:

#     1. Clear the Order Book for the selected instrument.
#     2. Clear the balance of the customer used for this test, cancel all orders.
#     3. Add funds to customer's available balance and verify.
#     4. Change current reference price to 1 in order to place an order with a unique price.
#     5. Place the "Buy" order.
#     6. Place the "Sell" order.
#     7. Restore the original last trade  price and ticker last.
#     8. Verify Quantity and Filled Quantity of both orders in DB.
#     9. Verify Quantity and Filled Quantity of the open order in Redis.



# The parameters below are used for test configuration
instrument_id = 1014

price_for_buy = 5.0
quantity_buy = 144.0
quantity_sell = quantity_buy * 0.5

ORDER_PROCESSING_DELAY = 5


@allure.feature("Filled and Partially Filled order - test")
@allure.story("Order Filled Quantity and order status are updated")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Verify Quantity and Filled Quantity of both orders in DB.
    2. Verify Quantity and Filled Quantity of the open order in Redis. 
          """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/hurl_tests/filled_quantity_hurl_test.py",
                 "TestFilledQuantity_updated")
@pytest.mark.incremental
@pytest.mark.e2e
@pytest.mark.hurl
@pytest.mark.usefixtures("r_customer")
class TestPartiallyMatchedOrder(object):

    @allure.step("Verify Quantity and Filled Quantity of both orders in DB.")
    @automation_logger(logger)
    @pytest.mark.parametrize('filled_quantity_hurl_order_buy', [[instrument_id, quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('filled_quantity_hurl_order_sell', [[instrument_id, quantity_sell, price_for_buy]], indirect=True)
    def test_find_orders_in_db(self, r_customer, create_customer, filled_quantity_hurl_order_buy,
                               filled_quantity_hurl_order_sell):
        #Wait for the orders to be processed and saved in DB.
        time.sleep(5)

        # Get order by Order ID from DB and verify filled quantity and status.

        # "Buy" order, partially filled.
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(filled_quantity_hurl_order_buy.internal_id))
        print(F"Buy Order In DB: {buy_order_in_db}")
        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == filled_quantity_hurl_order_buy.quantity
        assert buy_order_in_db[0].filled_quantity == filled_quantity_hurl_order_sell.quantity

        # "Sell" order, 100% filled
        sell_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(filled_quantity_hurl_order_sell.internal_id))
        print(F"Sell Order In DB: {sell_order_in_db}")
        assert len(sell_order_in_db) == 1
        assert sell_order_in_db[0].quantity == filled_quantity_hurl_order_sell.quantity
        assert sell_order_in_db[0].filled_quantity == filled_quantity_hurl_order_sell.quantity

    @allure.step("Verify Quantity and Filled Quantity of the open order in Redis.")
    @automation_logger(logger)
    def test_find_orders_in_redis(self, r_customer, filled_quantity_hurl_order_buy, filled_quantity_hurl_order_sell):
        orders_in_redis = Instruments.get_orders_by_customer_redis(r_customer.customer_id)
        print(F"Orders in Redis: {orders_in_redis}")

        # Only the "Buy" order should remain open, since it's 50% filled.
        assert len(orders_in_redis) == 1

        # Converting data to JSON format
        orders_verification = json.loads(orders_in_redis[0])

        # Verifying order details in Redis
        assert orders_verification['id'] == str(filled_quantity_hurl_order_buy.internal_id)
        assert orders_verification['direction'] == "BUY"
        assert orders_verification['status'] == "OPEN"

        redis_price = Calculator.value_decimal(orders_verification['price'])
        assert redis_price == price_for_buy

        redis_quantity = Calculator.value_decimal(orders_verification['quantity'])
        assert redis_quantity == quantity_buy

        redis_filled_quantity = Calculator.value_decimal(orders_verification['filledQuantity'])
        assert redis_filled_quantity == quantity_sell
        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")


