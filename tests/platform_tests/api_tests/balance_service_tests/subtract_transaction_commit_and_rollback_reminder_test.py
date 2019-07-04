import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 3
amount = 10.7832


@pytest.mark.incremental
@allure.feature("Balance")
@allure.story("Ability to ")
@allure.title("SUBTRACT TRANSACTION COMMIT AND ROLLBACK REMINDER")
@allure.description("""
    Functional api test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Subtract Transaction Commit And Rollback Reminder')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/subtract_transaction_commit_and_rollback_reminder_test.py",
                 "TestSubtractTransactionCommitAndRollbackReminder")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestSubtractTransactionCommitAndRollbackReminder(object):

    @allure.step("Starting with: ")
    @automation_logger(logger)
    def test_subtract_transaction_commit_and_rollback_reminder_method_works(self, r_customer):
        subtract_commit = r_customer.postman.balance_service.subtract_transaction_commit_and_rollback_reminder(
            "587756e2-47c9-4ff7-9c6d-77410ba636a0", r_customer.customer_id, currency_id, amount)
        assert subtract_commit['error']
        assert subtract_commit['error']['code'] == 104
        # assert subtract_commit['error']['message'] == "Operation leads to negative frozen balance"

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: ")
    @automation_logger(logger)
    @pytest.mark.parametrize('add_balance', [[currency_id]], indirect=True)
    def test_subtract_transaction_commit_and_rollback_reminder_functional(self, r_customer, add_balance):
        # Save current balance
        cur_balance = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, currency_id)
        assert cur_balance['result']['customerId'] == r_customer.customer_id
        assert cur_balance['result']['currencyId'] == currency_id

        total = float(cur_balance['result']['balance']['total'])
        available = float(cur_balance['result']['balance']['available'])

        # Make freeze
        sub_transaction = r_customer.postman.balance_service.subtract_transaction_initialize(r_customer.customer_id,
                                                                                             currency_id, amount)
        assert sub_transaction['result']['customerId'] == r_customer.customer_id
        guid = sub_transaction['result']['transactionGuid']

        subtract_commit = r_customer.postman.balance_service.subtract_transaction_commit_and_rollback_reminder(
            guid, r_customer.customer_id, currency_id, amount / 2)
        assert subtract_commit['result']['customerId'] == r_customer.customer_id
        assert subtract_commit['result']['currencyId'] == currency_id
        assert subtract_commit['result']['transactionGuid']

        # Check updated balance
        cur_balance_after = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, currency_id)
        assert cur_balance_after['result']['customerId'] == r_customer.customer_id
        total_after = float(cur_balance_after['result']['balance']['total'])
        available_after = float(cur_balance_after['result']['balance']['available'])

        # Verify results
        assert total_after == round(total - (amount / 2), 4)
        assert available_after == round(available - (amount / 2), 4)

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))
