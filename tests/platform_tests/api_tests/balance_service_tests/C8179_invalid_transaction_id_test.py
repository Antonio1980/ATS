import allure
import pytest
from src.base import logger
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "8179"
test_currency = 1

# An error is presented when trying to unfreeze funds using invalid transaction ID .


@allure.feature("Balance")
@allure.story("Balance can't be unfrozen using invalid transaction ID, 'Invalid transaction ID.")
@allure.title("Frozen BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1. Add 100 to available balance.
    2. Freeze all funds that aren't already frozen.
    3. Verifying that invalid transaction ID can't be used to unfreeze funds that are frozen.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8179_invalid_transaction_id_test.py",
                 "Balance can't be unfrozen by invalid transaction ID")
@pytest.mark.usefixtures("r_customer")
class TestTransactionIdInvalid(object):

    freeze_transaction_id = ""
    test_customer_balance_available = ""
    test_customer_balance_frozen = ""

    @allure.step("Add 100 to available balance.")
    @automation_logger(logger)
    def test_add_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, test_currency, 100)

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)
        assert float(response['result']['balance']['available']) >= 0

        TestTransactionIdInvalid.test_customer_balance_available =\
            float(response['result']['balance']['available'])
        TestTransactionIdInvalid.test_customer_balance_frozen = \
            float(response['result']['balance']['frozen'])

        logger.logger.info(
            F"Customer's balance available in test currency - response: "
            F"{TestTransactionIdInvalid.test_customer_balance_available}")
        print(
            F"Customer's  available balance in test currency - response: "
            F"{TestTransactionIdInvalid.test_customer_balance_available}")

    @allure.step("Freeze all funds that aren't already frozen.")
    @automation_logger(logger)
    def test_freeze_all_funds(self, r_customer):
        response = r_customer.postman.balance_service. \
            subtract_transaction_initialize(r_customer.customer_id, test_currency, TestTransactionIdInvalid.test_customer_balance_available)

        print(f"Freeze response {response}")
        logger.logger.info(f"Freeze response {response}")

        TestTransactionIdInvalid.freeze_transaction_id = response['result']['transactionGuid']
        assert len(TestTransactionIdInvalid.freeze_transaction_id) > 0

    @allure.step("Verifying that invalid transaction ID can't be used to unfreeze funds that are frozen.")
    @automation_logger(logger)
    def test_unfreeze_illegal(self, r_customer):
        response = r_customer.postman.balance_service.subtract_transaction_commit("", r_customer.customer_id, test_currency)

        logger.logger.info(F"Failed to unfreeze funds by transaction that is invalid - response: {response}")
        print(F"Failed to unfreeze funds by transaction that is invalid - response: {response}")

        assert "result" not in response.keys()
        assert response['error']['code'] == 107
        assert response['error']['message'] == 'Invalid transaction id format'

        # Verifying that customer's balance wasn't modified following the illegal unfreeze attempt

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, 1)

        assert float(response['result']['balance']['total']) == TestTransactionIdInvalid.test_customer_balance_available + TestTransactionIdInvalid.test_customer_balance_frozen
        assert float(response['result']['balance']['available']) == 0
        assert float(response['result']['balance']['frozen']) ==TestTransactionIdInvalid.test_customer_balance_available + TestTransactionIdInvalid.test_customer_balance_frozen

    logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
    print(f"================== TEST CASE PASSED: {test_case}===================")
