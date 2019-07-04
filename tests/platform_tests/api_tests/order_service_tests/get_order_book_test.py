import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""
instrument = 1008


@allure.feature("Order Management")
@allure.story("Client able to request records of order book")
@allure.title("Order Book")
@allure.description("""
    Functional api test.

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Get Order Book')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/order_service_tests/get_order_book_test.py", "TestGetOrderBook")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestGetOrderBook(object):
    instrument_id = 1008

    @allure.step("")
    @automation_logger(logger)
    def test_get_order_book_method_works(self, r_customer):
        response = r_customer.postman.order_service.get_order_book(self.instrument_id)
        assert response['error'] is None

        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("")
    @automation_logger(logger)
    def test_get_order_book_method(self, r_customer):
        response = r_customer.postman.order_service.get_order_book(self.instrument_id)
        assert response['error'] is None

        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Verify Order Book is received.")
    @automation_logger(logger)
    def test_buy_order_book(self, r_customer):
        response = r_customer.postman.order_service.get_order_book(instrument)

        assert response['error'] is None
        assert isinstance(response['result'], dict)
        result = response['result']
        assert 'sell' in result.keys()
        assert 'buy' in result.keys()

        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))
