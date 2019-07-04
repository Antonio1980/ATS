import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Customer")
@allure.title("Customer Update")
@allure.description("""
    Sanity API test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Customer Update')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/customer_service_tests/update_customer_test.py",
                 "TestUpdateCustomer")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.file_service
class TestUpdateCustomer(object):

    @allure.step("Starting: test_crypto_panic_method_works")
    @automation_logger(logger)
    def test_update_customer_method_works(self, customer):
        response = customer.postman.customer_service.update_customer(False, False)
        assert response['error'] is not None
        assert response['error'] == 'forbidden'
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Starting: test_deactivate_dxex_and_api_modes")
    @automation_logger(logger)
    def test_deactivate_dxex_and_api_modes(self, r_customer):
        response = r_customer.postman.customer_service.update_customer(False, False)
        assert response['error'] is None

        tr_response = r_customer.postman.trade_service.customer_data()
        assert tr_response['result']['customer']['dxexFeesEnabled'] is False
        assert tr_response['result']['customer']['enableAPI'] is False
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Starting: test_activate_dxex_and_api_modes")
    @automation_logger(logger)
    def test_activate_dxex_and_api_modes(self, r_customer):
        response = r_customer.postman.customer_service.update_customer(True, True)
        assert response['error'] is None

        tr_response = r_customer.postman.trade_service.customer_data()
        assert tr_response['result']['customer']['dxexFeesEnabled'] is True
        assert tr_response['result']['customer']['enableAPI'] is True
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

