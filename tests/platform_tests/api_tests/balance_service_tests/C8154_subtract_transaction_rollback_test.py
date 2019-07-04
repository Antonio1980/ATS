import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8154"
currency_id = 3
amount = 5


@allure.feature("Balance")
@allure.story("Ability to ")
@allure.title("SUBTRACT TRANSACTION ROLLBACK")
@allure.description("""
    Functional api test.
    Coverage:
    
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Subtract Transaction Rollback')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8154_subtract_transaction_rollback_test.py",
                                         "TestSubtractTransactionRollback")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestSubtractTransactionRollback(object):

    @allure.step("Starting with: ")
    @automation_logger(logger)
    def test_subtract_transaction_rollback_method_works(self, r_customer):
        subtract_rollback = r_customer.postman.balance_service.subtract_transaction_rollback(
            "587756e2-47c9-4ff7-9c6d-77410ba636a0", r_customer.customer_id, currency_id)
        assert subtract_rollback['error']
        assert subtract_rollback['error']['code'] == 104
        assert subtract_rollback['error']['message'] == "Transaction not found"

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: ")
    @automation_logger(logger)
    @pytest.mark.parametrize('add_balance', [[currency_id, amount]], indirect=True)
    def test_subtract_transaction_rollback_balance_check(self, r_customer, add_balance):
        amount = 1.0
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

        # Make rollback
        subtract_rollback = r_customer.postman.balance_service.subtract_transaction_rollback(
            guid, r_customer.customer_id, currency_id)
        assert subtract_rollback['result']['customerId'] == r_customer.customer_id
        assert subtract_rollback['result']['currencyId'] == currency_id

        # Check updated balance
        cur_balance_after = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, currency_id)
        assert cur_balance_after['result']['customerId'] == r_customer.customer_id
        total_after = float(cur_balance_after['result']['balance']['total'])
        available_after = float(cur_balance_after['result']['balance']['available'])

        # Verify result
        assert total_after == total
        assert available_after == available

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))