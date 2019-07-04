import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.data_bases.sql_db import SqlDb
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger

test_case = "6076"
instrument_id = 1008
currency_id = 1
c_currency_id = 4


@allure.feature("Order Management")
@allure.story("Client able to create limit sell/buy order.")
@allure.title("CREATE ORDER- LIMIT")
@allure.description("""
    Functional api test.
    Coverage:
    order_service, order_management, public_api
    1 test_create_order_limit_buy: 1, 1007, 10, 3400.0
    2 test_create_order_limit_sell: 2, 1007, 10, 3900.0
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Create limit order')
@allure.testcase(BaseConfig.API_BASE_URL, "TestCreateOrderLimit")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.parametrize('prices_from_orderbook', [[instrument_id]], indirect=True)
@pytest.mark.parametrize('min_order_quantity_for_instrument', [[instrument_id]], indirect=True)
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestCreateOrderLimit(object):

    @allure.step("Starting: test_create_order_limit_buy")
    @automation_logger(logger)
    @pytest.mark.parametrize('add_balance', [[currency_id, c_currency_id, ]], indirect=True)
    def test_create_order_limit_buy(self, r_customer, add_balance, min_order_quantity_for_instrument, prices_from_orderbook):
        safe_price = prices_from_orderbook["buy"]
        order = Order().set_order(1, instrument_id, min_order_quantity_for_instrument, safe_price)
        order_response = r_customer.postman.order_service.create_order(order)

        assert order_response['error'] is None
        assert order_response['result']['error'] is None
        assert order_response['result']['status'] is True
        assert 'AAAAA' in order_response['result']['externalOrderId']
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Starting: test_create_order_limit_sell")
    @automation_logger(logger)
    def test_create_order_limit_sell(self, r_customer, min_order_quantity_for_instrument, prices_from_orderbook):
        safe_price = prices_from_orderbook["sell"]
        order = Order().set_order(2, instrument_id, min_order_quantity_for_instrument, safe_price)
        order_response = r_customer.postman.order_service.create_order(order)

        assert order_response['error'] is None
        assert order_response['result']['error'] is None
        assert order_response['result']['status'] is True
        assert 'AAAAA' in order_response['result']['externalOrderId']
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Starting: test_create_order_limit_buy_sync")
    @automation_logger(logger)
    def test_create_order_limit_buy_sync(self, r_customer, min_order_quantity_for_instrument, prices_from_orderbook):
        safe_price = prices_from_orderbook["buy"]
        order = Order().set_order(1, instrument_id, min_order_quantity_for_instrument, safe_price)
        create_response = r_customer.postman.order_service.create_order_sync(order)

        assert create_response['error'] is None
        order_id = create_response['result']['orderId']
        time.sleep(5.0)
        query = "SELECT id FROM orders where customerId=" + str(r_customer.customer_id) + " AND statusId=1 ORDER BY " \
                                                                                          "executionDate DESC;"

        query_result = SqlDb.run_mysql_query(query)[0][0]
        assert query_result == int(order_id)
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Starting: test_create_order_limit_sell_sync")
    @automation_logger(logger)
    def test_create_order_limit_sell_sync(self, r_customer, min_order_quantity_for_instrument, prices_from_orderbook):
        safe_price = prices_from_orderbook["sell"]
        order = Order().set_order(2, instrument_id, min_order_quantity_for_instrument, safe_price)
        order_response = r_customer.postman.order_service.create_order_sync(order)

        assert order_response['error'] is None
        order_id = order_response['result']['orderId']
        time.sleep(5.0)
        query = "SELECT id FROM orders where customerId=" + str(r_customer.customer_id) + " AND statusId=1 ORDER BY " \
                                                                                          "executionDate DESC;"
        query_result = SqlDb.run_mysql_query(query)[0][0]
        assert query_result == int(order_id)
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))
