import time
import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger

currency_id = 1
c_currency_id = 4
instrument_id = 1008


# @pytest.mark.skip
@pytest.mark.load
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.parametrize('add_customer_balance', [[currency_id, c_currency_id]], indirect=True)
@pytest.mark.parametrize('min_order_quantity_for_instrument', [[instrument_id]], indirect=True)
@pytest.mark.parametrize("best_price_and_quantity", [[instrument_id, "buy", 1]], indirect=True)
@automation_logger(logger)
def test_load_order_service(load_customer, add_customer_balance, best_price_and_quantity,
                            min_order_quantity_for_instrument):
    price = best_price_and_quantity[0]
    order_buy = Order().set_order(1, instrument_id, min_order_quantity_for_instrument, price)
    order_sell = Order().set_order(2, instrument_id, min_order_quantity_for_instrument, price)
    orders = 10000
    try:
        for i in range(orders):
            logger.logger.info(F"Iteration number: {i}")
            load_customer.postman.order_service.create_order(order_buy)
            time.sleep(1.0)
            load_customer.postman.order_service.create_order(order_sell)
    except Exception as e:
        logger.logger.error(e)
        pass
    logger.logger.info("LOAD TEST FINISHED RUN!")
