import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8161"


@pytest.mark.incremental
@allure.feature("Balance")
@allure.story("Ability to add balance for the given account per customer_id, currency and amount.")
@allure.title("ADD BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1 test Add Balance(To add balance and verify that available balance also updated and frozen exists without changes)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Add Balance')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8161_add_balance_test.py",
                 "TestAddBalance")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestAddBalance(object):
    currency_id = 3
    amount = 10
    error = 103
    total_balance, frozen_balance, available_balance = None, None, None

    @allure.step("Starting with: Getting balance (total amount, available balance and frozen) "
                 "by customer_id,currency_id")
    @automation_logger(logger)
    def test_getting_balance(self, r_customer):
        get_balance = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, self.currency_id)
        TestAddBalance.total_balance = get_balance['result']['balance']['total']
        TestAddBalance.frozen_balance = get_balance['result']['balance']['frozen']
        TestAddBalance.available_balance = get_balance['result']['balance']['available']
        assert get_balance['result'] is not None
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: Adding balance (updating total amount and available balance) "
                 "by customer_id,currency_id and amount")
    @automation_logger(logger)
    def test_adding_balance(self, r_customer):
        add_balance = r_customer.postman.balance_service.add_balance(r_customer.customer_id, self.currency_id,
                                                                     self.amount)
        total_after = add_balance['result']['balance']['total']
        frozen_after = add_balance['result']['balance']['frozen']
        available_after = add_balance['result']['balance']['available']
        assert float(total_after) == float(TestAddBalance.total_balance) + float(self.amount)
        assert float(frozen_after) == float(TestAddBalance.frozen_balance)
        assert float(available_after) == float(TestAddBalance.available_balance) + float(self.amount)
        assert add_balance['result'] is not None
        assert add_balance['result']['transactionGuid'] is not None
        assert isinstance(add_balance, dict)
        assert isinstance(add_balance["result"]['balance'], dict)
        assert r_customer.customer_id == add_balance['result']['customerId']
        assert self.currency_id == add_balance['result']['currencyId']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: Adding balance with negative amount (Negative test)")
    @automation_logger(logger)
    def test_adding_balance_negative_amount(self, r_customer):
        add_balance_negative = r_customer.postman.balance_service.add_balance(r_customer.customer_id, self.currency_id,
                                                                              -10)
        assert add_balance_negative['error']['code'] is not None
        assert add_balance_negative['error']['code'] == self.error
        assert add_balance_negative['error']['message'] == "Given amount is negative"
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))