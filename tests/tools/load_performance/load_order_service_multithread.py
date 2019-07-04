import time
from src.base import logger
from threading import Thread
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.utils.calculator import Calculator

num_threads = 1
instrument_id = 1008

l_customer = RegisteredCustomer(None, "James_King@sandbox7e64c317900647609c225574db67437b.mailgun.org", "1Aa@<>12",
                                "100001100000023976")

min_order_quantity_for_instrument = float(Instruments.run_mysql_query(
        "SELECT minOrderQuantity FROM instruments WHERE id=" + str(instrument_id) + ";")[0][0])

price = l_customer.postman.order_service.get_order_book(instrument_id)['result']
price_sell = Calculator.calculate_from_decimals(price['sell'][0]['price']['value'], price['sell'][0]['price']['decimals'])
price_buy = Calculator.calculate_from_decimals(price['buy'][0]['price']['value'], price['sell'][0]['price']['decimals'])

@automation_logger(logger)
def test_performance_for_order_service():

    order_buy = Order().set_order(1, instrument_id, min_order_quantity_for_instrument, price_sell)
    order_sell = Order().set_order(2, instrument_id, min_order_quantity_for_instrument, price_buy)
    time_out = time.perf_counter() + 90000.0

    while time.perf_counter() < time_out:

        try:
            l_customer.postman.order_service.create_order(order_buy)
            l_customer.postman.order_service.create_order(order_sell)
        except Exception as e:
            logger.logger.error(e)
            pass
        
    logger.logger.info("LOAD TEST OVER TO RUN!")


for i in range(num_threads):
    worker = Thread(target=test_performance_for_order_service)
    worker.setDaemon(True)
    worker.start()
