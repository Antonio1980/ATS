import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Balance")
@allure.story("Client able to receive balance for the authorized account per currency and by default (for all).")
@allure.title("GET PUBLIC BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, public_api
    1 test_get_all_currency_balance
    2 test_get_currency_balance
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Get Public Balance')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/get_balance_test.py", "TestGetPublicBalance")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.balance_service
class TestGetPublicBalance(object):
    currency_id = 2
    several_currencies_id = 1, 3, 6

    @allure.step("Starting with: test_get_all_currency_balance")
    @automation_logger(logger)
    def test_get_all_currency_balance(self, r_customer):
        response = r_customer.postman.p_balance_service.get_balance()
        assert response["error"] is None
        assert response["result"] is not None
        balance = response["result"]["balance"]
        assert isinstance(balance, dict)
        for key in balance:
            keys = balance.get(key).keys()
            assert "total" in keys
            assert "frozen" in keys
            assert "available" in keys
            logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_get_currency_balance")
    @automation_logger(logger)
    def test_get_currency_balance(self, r_customer):
        response = r_customer.postman.p_balance_service.get_balance(self.currency_id)
        assert response["error"] is None
        assert response["result"] is not None
        balance = response["result"]["balance"]
        assert isinstance(balance, dict)
        for key in balance:
            keys = balance.get(key).keys()
            assert "total" in keys
            assert "frozen" in keys
            assert "available" in keys
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_get_several_currencies_balance")
    @automation_logger(logger)
    def test_get_several_currencies_balance(self, r_customer):
        response = r_customer.postman.p_balance_service.get_balance(*self.several_currencies_id)
        assert response["error"] is None
        balance = response["result"]["balance"]
        assert isinstance(balance, dict)
        balance_keys = balance.keys()
        key_list = [int(i) for i in balance_keys]
        assert tuple(key_list) == self.several_currencies_id
        for key in balance:
            keys = balance.get(key).keys()
            assert "total" in keys
            assert "frozen" in keys
            assert "available" in keys
            logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
