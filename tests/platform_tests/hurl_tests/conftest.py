import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

instrument_id = 1014
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]


@pytest.fixture(scope="class")
@automation_logger(logger)
def create_customer(r_customer):
    r_customer.clean_instrument(instrument_id)
    r_customer.clean_up_customer()
    # cur_orders = r_customer.postman.order_service.get_open_orders()
    # assert len(cur_orders['result']['orders']) == 0


@pytest.fixture(scope="class", params=[[quoted_currency,base_currency]])
@automation_logger(logger)
def add_balance_hurl(request, r_customer):
    if request.param:
        for i in request.param:
            response = r_customer.postman.balance_service.add_balance(r_customer.customer_id, int(i), 50000.0)
            assert response['result']['transactionGuid']
            assert "AAAAA" in response['result']['transactionGuid']
            logger.logger.info("GUID: {0}".format(response['result']['transactionGuid']))


@pytest.fixture(scope="class")
@pytest.mark.parametrize('add_balance_hurl', [[quoted_currency]], indirect=True)
@automation_logger(logger)
def create_order_limit_buy_hurl(request, r_customer, add_balance_hurl):
    instrument_id_, min_order_quantity_for_instrument = request.param[0], request.param[1]

    price = 5
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


@pytest.fixture(scope="class")
@pytest.mark.parametrize('add_balance_hurl', [[quoted_currency]], indirect=True)
@automation_logger(logger)
def filled_quantity_hurl_order_buy(request, r_customer, add_balance_hurl):
    instrument_id_, buy_quantity, buy_price = request.param[0], request.param[1], request.param[2]

    original_reference_price = Instruments.get_price_last_trade(instrument_id_)
    original_ticker_price = Instruments.get_ticker_last_price(instrument_id_)

    r_customer.clean_instrument(instrument_id_, base_currency, quoted_currency)

    Instruments.set_price_last_trade(instrument_id_, buy_price)
    Instruments.set_ticker_last_price(instrument_id_, buy_price)

    assert Instruments.get_price_last_trade(instrument_id_) == buy_price

    order = Order().set_order(1, instrument_id_, buy_quantity, buy_price)
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


@pytest.fixture(scope="class")
@pytest.mark.parametrize('add_balance_hurl', [[base_currency]], indirect=True)
@automation_logger(logger)
def filled_quantity_hurl_order_sell(request, r_customer, add_balance_hurl):
    instrument_id_, sell_quantity, sell_price = request.param[0], request.param[1], request.param[2]

    original_reference_price = Instruments.get_price_last_trade(instrument_id_)
    original_ticker_price = Instruments.get_ticker_last_price(instrument_id_)

    Instruments.set_price_last_trade(instrument_id_, sell_price)
    Instruments.set_ticker_last_price(instrument_id_, sell_price)

    assert Instruments.get_price_last_trade(instrument_id_) == sell_price

    order = Order().set_order(2, instrument_id_, sell_quantity, sell_price)
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
