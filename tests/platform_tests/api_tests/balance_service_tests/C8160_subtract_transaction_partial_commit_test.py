import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8160"


@pytest.mark.incremental
@allure.feature("Balance")
@allure.story("Ability to subtract frozen and total amount balance for the given account per customer_id, currency and "
              "amount.")
@allure.title("SUBTRACT TRANSACTION PARTIAL COMMIT")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1 test Subtract Transaction Partial Commit (To Subtract Frozen and Total amount balance per action - send order,
     withdrawal, fees transaction)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Subtract Transaction Partial Commit')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8160_subtract_transaction_partial_commit_test.py",
                 "TestSubtractTransactionPartialCommit")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestSubtractTransactionPartialCommit(object):
    currency_id = 3
    amount = 10.0209475
    total_balance, frozen_balance, transaction_guid = None, None, None

    @allure.step("Starting with: Adding balance (updating total amount) by customer_id,currency_id and amount")
    @automation_logger(logger)
    def test_add_balance(self, r_customer):
        add_balance = r_customer.postman.balance_service.add_balance(r_customer.customer_id, self.currency_id,
                                                                     self.amount)
        TestSubtractTransactionPartialCommit.total_balance = float(add_balance['result']['balance']['total'])
        assert add_balance['result'] is not None

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: Frozen balance (updating frozen amount) by customer_id,currency_id and amount")
    @automation_logger(logger)
    def test_frozen_balance(self, r_customer):
        frozen_transaction = r_customer.postman.balance_service.subtract_transaction_initialize(r_customer.customer_id,
                                                                                                self.currency_id,
                                                                                                self.amount)
        TestSubtractTransactionPartialCommit.frozen_balance = float(frozen_transaction['result']['balance']['frozen'])
        TestSubtractTransactionPartialCommit.transaction_guid = frozen_transaction['result']['transactionGuid']
        assert frozen_transaction['result'] is not None

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: Subtract transaction for customer by specific transactionGuid id, currency and amount")
    @automation_logger(logger)
    def test_subtract_transaction_partial_commit(self, r_customer):
        response = r_customer.postman.balance_service.subtract_transaction_partial_commit(
            TestSubtractTransactionPartialCommit.transaction_guid, r_customer.customer_id, self.currency_id, self.amount)
        total_after = float(response['result']['balance']['total'])
        frozen_after = float(response['result']['balance']['frozen'])
        assert round(float(total_after), 4) == round(float(TestSubtractTransactionPartialCommit.total_balance -
                                                     self.amount), 4)
        assert round(float(frozen_after), 4) == round(float(TestSubtractTransactionPartialCommit.frozen_balance -
                                                   self.amount), 4)
        assert response['result'] is not None
        assert response['result']['transactionGuid'] is not None
        assert isinstance(response, dict)
        assert isinstance(response['result']['balance'], dict)
        assert response['result']['balance'] is not None
        assert r_customer.customer_id == response['result']['customerId']
        assert self.currency_id == response['result']['currencyId']

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))