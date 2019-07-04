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

test_case = "cancelled_order_hurl_test"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
price_for_buy = 5
quantity = 10
direction = 1
limit_order_ME_type = "GOOD_TILL_DATE"

# In this test an order is placed, verified and cancelled.
# After the order is cancelled we are verifying that it is removed from Redis and it's status updated in DB.


@pytest.mark.incremental
@allure.feature("Order Flow, Order cancellation - end to end test.")
@allure.story("Placed order is received via HURL and saved in DB and Redis")
@allure.title("Order cancellation, End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Find the order that was placed in MySQL DB and verify it's parameters.
    2. Find the order that was placde in Redis and verify it's parameters.
    3. Verify that order is removed from Redis and order status is updated after cancellation
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/hurl_tests/cancelled_order_hurl_test.py",
                 "TestFullFlow_order_cancelled")
@pytest.mark.usefixtures("r_customer")
@pytest.mark.e2e
@pytest.mark.hurl
class TestCancelUnmatchedOrder(object):
    # The original reference price is changed and restored during the test.
    original_reference_price = ""

    order_buy = Order()
    order_buy.set_order(direction, instrument_id, quantity, price_for_buy)

    @allure.step("Find the order that was place in MySQL DB and verify it's parameters")
    @automation_logger(logger)
    @pytest.mark.parametrize('create_order_limit_buy_hurl', [[instrument_id, quantity]], indirect=True)
    def test_find_order_in_db(self, r_customer, create_customer, create_order_limit_buy_hurl):
        time.sleep(2)
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
    def test_find_order_in_redis(self, r_customer, create_order_limit_buy_hurl):
        orders_in_redis = Instruments.get_orders_by_customer_redis(r_customer.customer_id)
        print(F"Orders in Redis: {orders_in_redis}")
        assert len(orders_in_redis) == 1
        
        # Converting data to JSON format
        orders_verification = json.loads(orders_in_redis[0])
        TestCancelUnmatchedOrder.redis_order_id = orders_verification['id']
        assert str(create_order_limit_buy_hurl.internal_id) == TestCancelUnmatchedOrder.redis_order_id
        assert orders_verification['instrumentId'] == str(instrument_id)
        assert orders_verification['customerId'] == str(r_customer.customer_id)
        assert orders_verification['status'] == "OPEN"
        assert orders_verification['orderType'] == "LIMIT"
        assert orders_verification['timeInForce'] == limit_order_ME_type
        assert orders_verification['externalOrderId'] == create_order_limit_buy_hurl.external_id

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


    @allure.step("Verify that order is removed from Redis and order status is updated after cancellation")
    @automation_logger(logger)
    def test_cancellation_received(self, r_customer, create_order_limit_buy_hurl):

        # Order Cancellation delay
        time.sleep(5)
        response_cancellation = r_customer.postman.order_service.cancel_order(create_order_limit_buy_hurl.internal_id)
        assert response_cancellation['error'] is None

        # DB update after order cancellation delay
        time.sleep(5)

        # Verifying there are no open orders in DB for that customer.
        orders_in_db = Instruments.get_orders_by_customer_mysql(r_customer.customer_id, 1)
        assert orders_in_db is None

        # Verifying there are no open orders in Redis for that customer.
        orders_in_redis = Instruments.get_orders_by_customer_redis(r_customer.customer_id)
        print(F"Orders in Redis: {orders_in_redis}")
        assert orders_in_redis == []

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
