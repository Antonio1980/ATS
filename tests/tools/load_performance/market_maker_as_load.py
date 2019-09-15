import time
from src.base import logger
from threading import Thread
from src.base.data_bases.redis_db import RedisDb
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

num_threads = 50
orders_dict = Utils.read_json_config(BaseConfig.MM_CONFIG)


@automation_logger(logger)
def test_set_redis_price():
    for order in list(orders_dict["orders"]):
        RedisDb.set_price_last_trade(order["instrument_id"], order["price"])
        assert RedisDb.get_price_last_trade(order["instrument_id"]) == order["price"]

        RedisDb.set_ticker_last_price(order["instrument_id"], order["price"])
        assert RedisDb.get_ticker_last_price(order["instrument_id"]) == order["price"]


orders = Order.orders_builder(orders_dict, 1)
sell_orders = Order.orders_builder(orders_dict, 2)
orders.extend(sell_orders)
orders = tuple(orders[:20])

l_customer = RegisteredCustomer(None, "James_King@sandbox7e64c317900647609c225574db67437b.mailgun.org", "1Aa@<>12",
                                "100001100000023976")


@automation_logger(logger)
def test_add_customer_balance():
    for curr in range(1, 18):
        cur_balance = float(l_customer.postman.balance_service.get_currency_balance(
            l_customer.customer_id, int(curr))['result']['balance']['available'])
        if cur_balance < 5000000.0:
            l_customer.postman.balance_service.add_balance(l_customer.customer_id, int(curr), 5000000.0)


@automation_logger(logger)
def test_market_maker_as_load():

    time_out = time.perf_counter() + 90000.0

    while time.perf_counter() < time_out:

        for order in range(len(orders)):
            try:
                logger.logger.info(F"Iteration number: {order}")
                orders[order].add_random_price_coefficient()
                l_customer.postman.order_service.create_order_sync(orders[order])
                orders[order].clean_up_order_price()
            except Exception as e:
                logger.logger.error(e)
                pass
    logger.logger.info("LOAD TEST OVER TO RUN!")


for i in range(num_threads):
    worker = Thread(target=test_market_maker_as_load)
    worker.setDaemon(True)
    worker.start()
