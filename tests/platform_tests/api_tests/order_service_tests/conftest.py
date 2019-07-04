import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

instrument_id = 1008


@pytest.fixture(params=[[instrument_id, ]])
@pytest.mark.parametrize('safe_price', [[instrument_id]], indirect=True)
@automation_logger(logger)
def create_order_limit_buy(request, r_customer, add_balance, min_order_quantity_for_instrument, safe_price):
    instrument_id_ = request.param[0] if hasattr(request, "param") else None
    price = safe_price
    original_reference_price = Instruments.get_price_last_trade(instrument_id_)
    original_ticker_price = Instruments.get_ticker_last_price(instrument_id_)
    Instruments.set_price_last_trade(instrument_id_, price)
    Instruments.set_ticker_last_price(instrument_id_, price)
    assert Instruments.get_price_last_trade(instrument_id_) == price
    order = Order().set_order(1, instrument_id_, min_order_quantity_for_instrument, price)
    order_response = r_customer.postman.order_service.create_order_sync(order)
    Instruments.set_price_last_trade(instrument_id_, original_reference_price)
    Instruments.set_ticker_last_price(instrument_id_, original_ticker_price)
    assert Instruments.get_price_last_trade(instrument_id_) == original_reference_price
    assert order_response['error'] is None
    assert 'AAAAA' in order_response['result']['externalOrderId']
    assert isinstance(order_response['result']['orderId'], str)
    order.external_id = order_response['result']['externalOrderId']
    order.internal_id = int(order_response['result']['orderId'])
    return order


@pytest.fixture(params=[[instrument_id, ]])
@pytest.mark.parametrize('safe_price', [[instrument_id]], indirect=True)
@automation_logger(logger)
def create_order_limit_sell(request, r_customer, add_balance, min_order_quantity_for_instrument, safe_price):
    instrument_id_ = request.param[0] if hasattr(request, "param") else None
    price = safe_price
    original_ticker_price = Instruments.get_ticker_last_price(instrument_id_)
    Instruments.set_ticker_last_price(instrument_id_, price)
    assert Instruments.get_ticker_last_price(instrument_id_) == float(price)
    order = Order().set_order(2, instrument_id_, min_order_quantity_for_instrument, price)
    order_response = r_customer.postman.order_service.create_order_sync(order)
    Instruments.set_ticker_last_price(instrument_id_, original_ticker_price)
    assert Instruments.get_ticker_last_price(instrument_id_) == original_ticker_price
    assert order_response['error'] is None
    assert 'AAAAA' in order_response['result']['externalOrderId']
    assert isinstance(order_response['result']['orderId'], str)
    order.external_id = order_response['result']['externalOrderId']
    order.internal_id = int(order_response['result']['orderId'])
    return order
