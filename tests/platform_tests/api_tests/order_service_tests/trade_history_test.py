import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "6080"
instrument_id = 1008


@allure.feature("Order Management")
@allure.story("Client able to request records about his trades.")
@allure.title("TRADES HISTORY.")
@allure.description("""
    Functional api test.
    Coverage:
    order_service, order_management, public_api
    1 test_trade_history_default: 
    2 test_trade_history: 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='TradesHistory')
@allure.testcase(BaseConfig.API_BASE_URL, "TestTradesHistory")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestTradesHistory(object):

    @allure.step("Starting: test_trade_history")
    @automation_logger(logger)
    def test_trade_history_default(self, r_customer):
        response = r_customer.postman.order_service.get_trades_history()
        assert response['error'] is None
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Starting: test_trade_history2")
    @pytest.mark.parametrize('add_balance', [[1, 4]], indirect=True)
    @pytest.mark.parametrize('min_order_quantity_for_instrument', [[instrument_id]], indirect=True)
    @pytest.mark.parametrize('safe_price', [[instrument_id]], indirect=True)
    @automation_logger(logger)
    def test_trade_history(self, r_customer, add_balance, create_order_limit_buy, min_order_quantity_for_instrument,
                           safe_price):
        price = safe_price
        original_ticker_price = Instruments.get_ticker_last_price(instrument_id)
        Instruments.set_ticker_last_price(instrument_id, price)
        order = Order().set_order(2, instrument_id, min_order_quantity_for_instrument, price)
        create_response = r_customer.postman.order_service.create_order_sync(order)
        time.sleep(1.0)
        Instruments.set_ticker_last_price(instrument_id, original_ticker_price)
        assert Instruments.get_ticker_last_price(instrument_id) == original_ticker_price
        assert create_response['error'] is None
        order_id = create_response['result']['orderId']
        ex_order_id = create_response['result']['externalOrderId']
        time.sleep(5.0)
        response = r_customer.postman.order_service.get_trades_history()
        assert response['error'] is None
        assert response['result']['trades']
        assert response['result']['total']['count'] > 0
        assert order_id == response['result']['trades'][0]['sellOrderId']
        assert ex_order_id == response['result']['trades'][0]['sellExternalOrderId']

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
