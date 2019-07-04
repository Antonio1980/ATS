import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "6081"
instrument_id = 1008


@allure.feature("Order Management")
@allure.story("Client able to request records about his open orders.")
@allure.title("OPEN ORDERS")
@allure.description("""
    Functional api test.
    Coverage:
    order_service, order_management, public_api
    1 test_open_orders: 1, 1012, 0.007
    2 test_order_open_orders: 2, 1012, 0.007
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='OpenOrders')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/order_service_tests/open_orders_test.py", "TestOpenOrders")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestOpenOrders(object):

    @allure.step("Starting test_open_orders: check that open orders responding to authorized customer.")
    @automation_logger(logger)
    def test_open_orders(self, r_customer):
        response = r_customer.postman.order_service.get_open_orders()
        assert response['error'] is None
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @pytest.mark.parametrize('add_balance', [[1, 4]], indirect=True)
    @pytest.mark.parametrize('min_order_quantity_for_instrument', [[instrument_id]], indirect=True)
    @allure.step("Starting test_order_open_orders: ckeck that existing open order returned in the response. ")
    @automation_logger(logger)
    def test_order_open_orders(self, r_customer, add_balance, min_order_quantity_for_instrument):
        price = 1

        original_reference_price = Instruments.get_price_last_trade(instrument_id)
        original_ticker_price = Instruments.get_ticker_last_price(instrument_id)

        Instruments.set_price_last_trade(instrument_id, price)
        Instruments.set_ticker_last_price(instrument_id, price)

        order = Order().set_order(1, instrument_id, min_order_quantity_for_instrument, price)
        
        order_response = r_customer.postman.order_service.create_order_sync(order)
        Instruments.set_price_last_trade(instrument_id, original_reference_price)
        Instruments.set_ticker_last_price(instrument_id, original_ticker_price)

        assert order_response['error'] is None
        order_id = order_response['result']['orderId']
        time.sleep(5.0)
        open_orders_response = r_customer.postman.order_service.get_open_orders()
        assert open_orders_response['error'] is None
        assert open_orders_response['result']['orders']
        assert isinstance(open_orders_response['result']['orders'], list)
        id_ = open_orders_response['result']['orders'][-1]['id']
        assert order_id == id_
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))