import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "6078"


@allure.feature("Order Management")
@allure.story("Client able to request records about his not opened orders.")
@allure.title("ORDER HISTORY")
@allure.description("""
    Functional api test.
    Coverage:
    order_service, order_management, public_api
    1 test_order_history: 
    2 test_order_history2: 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='OrdersHistory')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/order_service_tests/order_history_test.py", "TestOrdersHistory")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestOrdersHistory(object):

    @allure.step("Starting: test_order_history")
    @automation_logger(logger)
    def test_order_history_default(self, r_customer):
        response = r_customer.postman.order_service.get_order_history()
        assert response['error'] is None
        assert response['result']['ordersForHistory'] is not None
        assert isinstance(response['result']['ordersForHistory'], list)
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))

    @allure.step("Starting: test_order_history2")
    @automation_logger(logger)
    def test_order_history(self, r_customer, create_order_limit_buy):
        time.sleep(5.0)
        cancel_response = r_customer.postman.order_service.cancel_order(create_order_limit_buy.internal_id)
        assert cancel_response['error'] is None
        time.sleep(5.0)
        response = r_customer.postman.order_service.get_order_history()
        assert response['error'] is None
        assert response['result']['ordersForHistory'] is not None
        assert response['result']['total']['count'] > 0
        assert response['result']['ordersForHistory'][0]['order']['id'] == str(create_order_limit_buy.internal_id)
        logger.logger.info("TEST CASE {0} IS PASSED".format(test_case))
        