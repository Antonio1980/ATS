import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

# Instrument configuration
instrument_id = 1014
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)
tail_digits_allowed = Instruments.get_quantity_tail_digits(instrument_id)
instrument_reference_price = Instruments.get_ticker_last_price(instrument_id)


# buy_quantity = 100
# sell_quantity = 100


@pytest.fixture(scope="class")
@automation_logger(logger)
def make_customer(r_customer):
    r_customer.clean_instrument(instrument_id)

    make_customers = Instruments.create_two_customers()

    boris = make_customers[0][0]
    stas = make_customers[1][0]

    boris.static_token = make_customers[0][1]
    stas.static_token = make_customers[1][1]

    return boris, stas


@pytest.fixture(scope="class", params=[[quoted_currency]])
@automation_logger(logger)
def add_balance_fill_buyer(request, r_customer, make_customer):
    if request.param:
        for i in request.param:
            response = make_customer[0].postman.get_static_postman(
                make_customer[0].static_token).balance_service.add_balance(make_customer[0].customer_id, int(i), 10000)
            assert response['result']['transactionGuid']
            assert "AAAAA" in response['result']['transactionGuid']
            logger.logger.info("GUID: {0}".format(response['result']['transactionGuid']))


@pytest.fixture(scope="class", params=[[base_currency]])
@automation_logger(logger)
def add_balance_fill_seller(request, r_customer, make_customer):
    if request.param:
        for i in request.param:
            response = make_customer[1].postman.get_static_postman(
                make_customer[1].static_token).balance_service.add_balance(make_customer[1].customer_id, int(i), 10000)
            assert response['result']['transactionGuid']
            assert "AAAAA" in response['result']['transactionGuid']
            logger.logger.info("GUID: {0}".format(response['result']['transactionGuid']))


@pytest.fixture(scope="class")
@pytest.mark.parametrize('add_balance_fill_buyer', [[quoted_currency]], indirect=True)
def place_order_buy(request, make_customer, add_balance_fill_buyer):
    instrument_id_ = instrument_id

    buy_quantity = request.param[0]
    buy_price = request.param[1]

    # Saving the original reference price
    original_reference_price = Instruments.get_price_last_trade(instrument_id_)
    original_ticker_price = Instruments.get_ticker_last_price(instrument_id_)

    # Set the reference price required to place an order.
    Instruments.set_price_last_trade(instrument_id_, buy_price)
    Instruments.set_ticker_last_price(instrument_id_, buy_price)

    assert Instruments.get_price_last_trade(instrument_id_) == buy_price

    # Place the order
    order = Order().set_order(1, instrument_id_, buy_quantity, buy_price)

    order_response = make_customer[0].postman.get_static_postman(
        make_customer[0].static_token).order_service.create_order_sync(order)

    assert order_response['error'] is None

    # Restore the original reference price
    Instruments.set_price_last_trade(instrument_id_, original_reference_price)
    Instruments.set_ticker_last_price(instrument_id_, original_ticker_price)

    return order


@pytest.fixture(scope="class")
@pytest.mark.parametrize('add_balance_fill_seller', [[base_currency]], indirect=True)
def place_order_sell(request, make_customer, add_balance_fill_seller):
    instrument_id_ = instrument_id

    sell_quantity = request.param[0]
    sell_price = request.param[1]

    # Saving the original reference price
    original_reference_price = Instruments.get_price_last_trade(instrument_id_)
    original_ticker_price = Instruments.get_ticker_last_price(instrument_id_)

    # Set the reference price required to place an order.
    Instruments.set_price_last_trade(instrument_id_, sell_price)
    Instruments.set_ticker_last_price(instrument_id_, sell_price)

    assert Instruments.get_price_last_trade(instrument_id_) == sell_price

    # Place the order
    order = Order().set_order(2, instrument_id_, sell_quantity, sell_price)

    order_response = make_customer[1].postman.get_static_postman(
        make_customer[1].static_token).order_service.create_order_sync(order)

    assert order_response['error'] is None

    # Restore the original reference price
    Instruments.set_price_last_trade(instrument_id_, original_reference_price)
    Instruments.set_ticker_last_price(instrument_id_, original_ticker_price)

    return order


@pytest.fixture(scope="class")
@pytest.mark.parametrize('add_balance_fill_seller', [[base_currency]], indirect=True)
def place_two_sell_orders(request, make_customer, add_balance_fill_seller):
    instrument_id_ = instrument_id

    sell_quantity_1 = request.param[0]
    sell_quantity_2 = request.param[1]

    sell_price_1 = request.param[2]
    sell_price_2 = request.param[3]

    # Saving the original reference price
    original_reference_price = Instruments.get_price_last_trade(instrument_id_)
    original_ticker_price = Instruments.get_ticker_last_price(instrument_id_)

    # Set the reference price required to place an order.
    Instruments.set_price_last_trade(instrument_id_, sell_price_1)
    Instruments.set_ticker_last_price(instrument_id_, sell_price_1)

    assert Instruments.get_price_last_trade(instrument_id_) == sell_price_1

    # Place the first order
    order_1 = Order().set_order(2, instrument_id_, sell_quantity_1, sell_price_1)

    order_response = make_customer[1].postman.get_static_postman(
        make_customer[1].static_token).order_service.create_order_sync(order_1)

    assert order_response['error'] is None

    # Set the reference price required to place an order.
    Instruments.set_price_last_trade(instrument_id_, sell_price_2)
    Instruments.set_ticker_last_price(instrument_id_, sell_price_2)

    assert Instruments.get_price_last_trade(instrument_id_) == sell_price_2

    # Place the second order
    order_2 = Order().set_order(2, instrument_id_, sell_quantity_2, sell_price_2)

    order_response = make_customer[1].postman.get_static_postman(
        make_customer[1].static_token).order_service.create_order_sync(order_2)

    assert order_response['error'] is None

    # Restore the original reference price
    Instruments.set_price_last_trade(instrument_id_, original_reference_price)
    Instruments.set_ticker_last_price(instrument_id_, original_ticker_price)

    return order_1, order_2
