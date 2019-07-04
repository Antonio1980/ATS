import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger


test_case = "7786"
instrument_id = 1007
quantity_for_buy = 4500.0
quantity_for_sell = 4700.0


@pytest.mark.skip
@allure.feature("Order Management")
@allure.story("Client able to create market sell/buy order.")
@allure.title("CREATE ORDER- MARKET")
@allure.description("""
    Functional api test.
    Coverage:
    order_service, order_management, public_api
    1 test_create_order_market_buy: 1, 1012, 0.007
    2 test_create_order_market_sell: 2, 1012, 0.007
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Create market order')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/order_service_tests/create_order_market_test.py",
                 "TestCreateOrderMarket")
@pytest.mark.usefixtures("r_time_count", "r_customer", "conf_customer")
@pytest.mark.parametrize('add_balance', [['1', '3']], indirect=True)
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestCreateOrderMarket(object):

    @allure.step("Starting: test_create_order_market_buy")
    @automation_logger(logger)
    def test_create_order_market_buy(self, r_customer, add_balance):
        order = Order()
        order.set_order(1, instrument_id, quantity_for_buy)
        order_response = r_customer.postman.order_service.create_order(order)
        assert order_response['error'] is None
        assert order_response['result']['error'] is None
        assert order_response['result']['status'] is True
        assert 'AAAAA' in order_response['result']['externalOrderId']
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Starting: test_create_order_market_sell")
    @automation_logger(logger)
    def test_create_order_market_sell(self, r_customer, add_balance):
        order = Order()
        order.set_order(2, instrument_id, quantity_for_sell)
        order_response = r_customer.postman.order_service.create_order(order)
        assert order_response['error'] is None
        assert order_response['result']['error'] is None
        assert order_response['result']['status'] is True
        assert 'AAAAA' in order_response['result']['externalOrderId']
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Starting: test_create_order_market_buy_sync")
    @automation_logger(logger)
    def test_create_order_market_buy_sync(self, r_customer, add_balance):
        order = Order()
        order.set_order(1, instrument_id, quantity_for_buy)
        create_response = r_customer.postman.order_service.create_order_sync(order)
        assert create_response['error'] is None
        assert create_response['result']['orderId']
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Starting: test_create_order_market_sell_sync")
    @automation_logger(logger)
    def test_create_order_market_sell_sync(self, r_customer, add_balance):
        order = Order()
        order.set_order(2, instrument_id, quantity_for_sell)
        create_response = r_customer.postman.order_service.create_order_sync(order)
        assert create_response['error'] is None
        assert create_response['result']['orderId']
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))
