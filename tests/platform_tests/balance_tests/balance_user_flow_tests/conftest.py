import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger




@pytest.fixture(scope="class")
@automation_logger(logger)
def make_customer(request, r_customer):

    instrument_id = request.param[0]

    r_customer.clean_instrument(instrument_id)

    customer_created = Instruments.create_two_customers(1)

    make_customer = customer_created[0][0]
    make_customer_token = customer_created[0][1]

    make_customer.static_token = make_customer_token

    return make_customer


@pytest.fixture(scope="class")
@automation_logger(logger)
def make_two_customers(request, r_customer):

    instrument_id = request.param[0]

    r_customer.clean_instrument(instrument_id)

    make_customers = Instruments.create_two_customers()

    boris = make_customers[0][0]
    stas = make_customers[1][0]

    boris.static_token = make_customers[0][1]
    stas.static_token = make_customers[1][1]

    return boris, stas


@pytest.fixture(scope="class")
@automation_logger(logger)
def add_balance_fill(request, make_customer):
    if request.param:
        for i in request.param:
            response = make_customer.postman.get_static_postman(make_customer.static_token).balance_service.add_balance(make_customer.customer_id, int(i),50000)
            assert response['result']['transactionGuid']
            assert "AAAAA" in response['result']['transactionGuid']
            logger.logger.info("GUID: {0}".format(response['result']['transactionGuid']))


@pytest.fixture(scope="function")
def fill_order_book_buy(request, make_customer, add_balance_fill):
    buy_quantity = request.param[0]

    instrument_id_ = request.param[1]

    tail_digits_allowed = Instruments.get_quantity_tail_digits(instrument_id_)
    reference_price = Instruments.get_ticker_last_price(instrument_id_)


    buy_price_1 = round(reference_price * 0.95, tail_digits_allowed)
    buy_price_2 = round(reference_price * 0.9, tail_digits_allowed)
    buy_price_3 = round(reference_price * 0.85, tail_digits_allowed)

    first_order_response = make_customer.postman.get_static_postman(make_customer.static_token).\
        order_service.create_order(Order().set_order(1, instrument_id_, buy_quantity, buy_price_1))
    assert first_order_response['error'] is None, "Failed to fill Buy Order Book"

    second_order_response = make_customer.postman.get_static_postman(make_customer.static_token). \
        order_service.create_order(Order().set_order(1, instrument_id_, buy_quantity, buy_price_2))
    assert second_order_response['error'] is None, "Failed to fill Buy Order Book"

    third_order_response = make_customer.postman.get_static_postman(make_customer.static_token). \
        order_service.create_order(Order().set_order(1, instrument_id_, buy_quantity, buy_price_3))
    assert third_order_response['error'] is None, "Failed to fill Buy Order Book"

    Instruments.set_price_last_trade(instrument_id_,reference_price)
    Instruments.set_ticker_last_price(instrument_id_,reference_price)


@pytest.fixture(scope="function")
def fill_order_book_sell(request, make_customer, add_balance_fill):
    sell_quantity = request.param[0]

    instrument_id_ = request.param[1]

    tail_digits_allowed = Instruments.get_quantity_tail_digits(instrument_id_)
    reference_price = Instruments.get_ticker_last_price(instrument_id_)

    buy_price_1 = round(reference_price * 1.05, tail_digits_allowed)
    buy_price_2 = round(reference_price * 1.1, tail_digits_allowed)
    buy_price_3 = round(reference_price * 1.15, tail_digits_allowed)

    first_order_response = make_customer.postman.get_static_postman(make_customer.static_token). \
        order_service.create_order(Order().set_order(2, instrument_id_, sell_quantity, buy_price_1))
    assert first_order_response['error'] is None, "Failed to fill Sell Order Book"

    second_order_response = make_customer.postman.get_static_postman(make_customer.static_token). \
        order_service.create_order(Order().set_order(2, instrument_id_, sell_quantity, buy_price_2))
    assert second_order_response['error'] is None, "Failed to fill Sell Order Book"

    third_order_response = make_customer.postman.get_static_postman(make_customer.static_token). \
        order_service.create_order(Order().set_order(2, instrument_id_, sell_quantity, buy_price_3))
    assert third_order_response['error'] is None, "Failed to fill Sell Order Book"

    Instruments.set_price_last_trade(instrument_id_, reference_price)
    Instruments.set_ticker_last_price(instrument_id_, reference_price)







