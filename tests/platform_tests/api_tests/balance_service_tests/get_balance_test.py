import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Balance")
@allure.story("Ability to receive balance for the given account per currency and by default (for all).")
@allure.title("GET BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1 test_get_all_currency_balance
    2 test_get_currency_balance
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Get Balance')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/get_balance_test.py", "TestGetBalance")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestGetBalance(object):
    currency_id = 2

    @allure.step("Starting with: test_get_all_currency_balance")
    @automation_logger(logger)
    def test_get_all_currency_balance(self, r_customer):
        response = r_customer.postman.balance_service.get_all_currencies_balance(r_customer.customer_id)
        assert isinstance(response["result"], list) and len(response["result"]) > 0
        for customer_id in response['result']:
            assert customer_id.get('customerId') == r_customer.customer_id
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: test_get_currency_balance")
    @automation_logger(logger)
    def test_get_currency_balance(self, r_customer):
        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, self.currency_id)
        assert response["result"] is not None
        keys_list = list(response['result'].keys())
        assert keys_list == ['customerId', 'currencyId', 'balance']
        assert response["result"]['currencyId'] == self.currency_id
        assert response["result"]['customerId'] == r_customer.customer_id
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
