import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8162"


@pytest.mark.incremental
@allure.feature("Balance")
@allure.story("Ability to subtract balance for the given account per customer_id, currency and amount.")
@allure.title("SUBTRACT BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1 test Add Balance(To add balance and verify that available balance also updated and frozen exists without changes)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Subtract Balance')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8162_subtract_balance_test.py",
                 "TestSubtractBalance")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestSubtractBalance(object):
    currency_id = 3
    amount = 10
    total_balance, frozen_balance, available_balance = None, None, None

    @allure.step("Starting with: Adding balance (updating total amount and available balance) "
                 "by customer_id,currency_id and amount")
    @automation_logger(logger)
    def test_adding_balance(self, r_customer):
        add_balance = r_customer.postman.balance_service.add_balance(r_customer.customer_id, self.currency_id,
                                                                     self.amount)
        TestSubtractBalance.total_balance = add_balance['result']['balance']['total']
        TestSubtractBalance.frozen_balance = add_balance['result']['balance']['frozen']
        TestSubtractBalance.available_balance = add_balance['result']['balance']['available']
        assert add_balance['result'] is not None
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: Subtract balance (updating total amount and available balance) "
                 "by customer_id,currency_id and amount")
    @automation_logger(logger)
    def test_subtract_balance(self, r_customer):
        subtract_balance = r_customer.postman.balance_service.subtract_balance(r_customer.customer_id, self.currency_id,
                                                                               self.amount)
        total_after = subtract_balance['result']['balance']['total']
        frozen_after = subtract_balance['result']['balance']['frozen']
        available_after = subtract_balance['result']['balance']['available']
        assert float(total_after) == float(TestSubtractBalance.total_balance) - float(self.amount)
        assert float(frozen_after) == float(TestSubtractBalance.frozen_balance)
        assert float(available_after) == float(TestSubtractBalance.available_balance) - float(self.amount)
        assert subtract_balance['result'] is not None
        assert subtract_balance['result']['transactionGuid'] is not None
        assert isinstance(subtract_balance, dict)
        assert isinstance(subtract_balance["result"]['balance'], dict)
        assert r_customer.customer_id == subtract_balance['result']['customerId']
        assert self.currency_id == subtract_balance['result']['currencyId']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))