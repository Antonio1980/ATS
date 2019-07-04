import time
import pytest
from src.base import logger
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.data_bases.redis_db import RedisDb
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

orders_dict = Utils.read_json_config(BaseConfig.MM_CONFIG)


@automation_logger(logger)
def set_redis_price():
    for order in list(orders_dict["orders"]):
        RedisDb.set_price_last_trade(order["instrument_id"], order["price"])
        assert RedisDb.get_price_last_trade(order["instrument_id"]) == order["price"]
        time.sleep(0.5)
        RedisDb.set_ticker_last_price(order["instrument_id"], order["price"])
        assert RedisDb.get_ticker_last_price(order["instrument_id"]) == order["price"]


orders = Order.orders_builder(orders_dict, 1)
sell_orders = Order.orders_builder(orders_dict, 2)
orders.extend(sell_orders)
orders = tuple(orders)


@pytest.fixture
@automation_logger(logger)
def another_customer():
    another_customer = RegisteredCustomer(None, "Colton_Murphy@guerrillamailblock.com", "1Aa@<>12",
                                          "100001100000022877")
    return another_customer


@pytest.fixture
@automation_logger(logger)
def add_customer_balance(request, another_customer):
    logger.logger.info(request.param)
    for i in request.param:
        cur_balance = float(another_customer.postman.balance_service.get_currency_balance(
            another_customer.customer_id, int(i))['result']['balance']['available'])
        if cur_balance < 5000000.0:
            another_customer.postman.balance_service.add_balance(another_customer.customer_id, int(i), 5000000.0)


@pytest.mark.parametrize('add_customer_balance', [[i for i in range(1, 18)]], indirect=True)
@automation_logger(logger)
def test_market_maker(add_customer_balance, another_customer):
    set_redis_price()

    time_out = time.perf_counter() + float(BaseConfig.MM_DELAY)

    while time.perf_counter() < time_out:

        for order in orders:
            try:
                order.add_random_price_coefficient()
                another_response = another_customer.postman.order_service.create_order(order)
                order.clean_up_order_price()
                assert another_response['error'] is None
            except Exception as e:
                logger.logger.error("Error {0}".format(e))
                pass
