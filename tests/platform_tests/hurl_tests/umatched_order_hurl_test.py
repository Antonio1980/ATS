import time
import json
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.utils.calculator import Calculator
from src.base.log_decorator import automation_logger

test_case = "unmatched_order_hurl_test"

# This test comes to verify, that order parameters are saved correctly to MySQL DB and to Redis
# when the order is placed and isn't matched.
# Original Test Flow:

#     1. Clear the balance of the customer used for this test, cancel all orders.
#     2. Add funds to customer's available balance and verify.
#     3. Change current reference price 1 in order to place an order with a unique price.
#     4. Place a BUY order with price 1 that won't match with any of the existing orders.
#     5. Restore the original Reference Price.
#     6. Find the order that was place in MySQL DB and verify it's parameters.
#     7. Find the order that was place in Redis and verify it's parameters.


# The parameters below are used for test configuration
instrument_id = 1014
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]

price_for_buy = 5
quantity = 80
direction = 1
limit_order_ME_type = "GOOD_TILL_DATE"


@pytest.mark.incremental
@allure.feature("Order Flow - end to end test.")
@allure.story("Placed order is received via HURL and saved in DB and Redis")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Find the order that was place in MySQL DB and verify it's parameters.
    2. Find the order that was place in Redis and verify it's parameters.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/hurl_tests/unmatched_order_hurl_test.py",
                 "TestFullFlow_order_unmatched")
@pytest.mark.usefixtures("r_customer")
@pytest.mark.e2e
@pytest.mark.hurl
class TestUnmatchedOrder(object):

    @allure.step("Find the order that was place in MySQL DB and verify it's parameters")
    @automation_logger(logger)
    @pytest.mark.parametrize('filled_quantity_hurl_order_buy', [[instrument_id, quantity, price_for_buy]],
                             indirect=True)
    def test_find_order_in_db(self, r_customer, create_customer, filled_quantity_hurl_order_buy):

        time.sleep(5)
        orders_in_db = Instruments.get_orders_by_customer_mysql(r_customer.customer_id, 1)
        orders_list = Order.orders_data_converter(orders_in_db)
        print(F"Orders list: {orders_list}")
        assert len(orders_list) == 1
        assert orders_list[0].price == price_for_buy
        assert orders_list[0].quantity == quantity
        assert orders_list[0].direction == 'buy'
        assert orders_list[0].instrument_id == instrument_id
        assert orders_list[0].type == 2
        assert orders_list[0].filled_quantity == 0

    @allure.step("Find the order that was place in Redis and verify it's parameters")
    @automation_logger(logger)
    def test_find_order_in_redis(self, r_customer, filled_quantity_hurl_order_buy):
        orders_in_redis = Instruments.get_orders_by_customer_redis(r_customer.customer_id)
        print(F"Orders in Redis: {orders_in_redis}")
        assert len(orders_in_redis) == 1

        # Converting data to JSON format
        orders_verification = json.loads(orders_in_redis[0])
        TestUnmatchedOrder.redis_order_id = orders_verification['id']
        assert str(filled_quantity_hurl_order_buy.internal_id) == TestUnmatchedOrder.redis_order_id
        assert orders_verification['instrumentId'] == str(instrument_id)
        assert orders_verification['customerId'] == str(r_customer.customer_id)
        assert orders_verification['status'] == "OPEN"
        assert orders_verification['orderType'] == "LIMIT"
        assert orders_verification['timeInForce'] == limit_order_ME_type
        assert orders_verification['externalOrderId'] == str(filled_quantity_hurl_order_buy.external_id)

        if direction == 1:
            assert orders_verification['direction'] == "BUY"
        else:
            assert orders_verification['direction'] == "SELL"

        redis_price = Calculator.value_decimal(orders_verification['price'])
        assert redis_price == price_for_buy
        redis_quantity = Calculator.value_decimal(orders_verification['quantity'])
        assert redis_quantity == quantity
        redis_filled_quantity = Calculator.value_decimal(orders_verification['filledQuantity'])
        assert redis_filled_quantity == 0
        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
