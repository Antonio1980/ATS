import allure
import pytest
from src.base import logger
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "8180"
test_currency = 1
amount = 100

"""
Frozen funds can't be unfrozen twice.
After frozen balance was fully unfrozen by GUID, the same GUID can't be used again to unfreeze balance.
When Balance Service client tries to use invalid or expired GUID to unfreeze balance he should be responded
with "Transaction not found" error.
"""


@allure.feature("Balance")
@allure.story("No balance is frozen if the requested sum is greater than available  balance, 'Not enough funds' error.")
@allure.title("Frozen BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1. Add 100 to available balance.
    2. Freeze all funds that aren't already frozen.
    3. Unfreeze the frozen sum.
    4. Verifying that transaction ID can't be used twice to unfreeze funds that are already unfrozen.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8180_transaction_unfreeze_negative_test.py",
                 "Invalid freeze request has no effect.")
@pytest.mark.usefixtures("r_customer")
class TestTransactionUnfreezeNegative(object):

    freeze_transaction_id = ""
    test_customer_balance_available = ""
    test_customer_balance_frozen = ""

    @allure.step("Add 100 to available balance.")
    @automation_logger(logger)
    def test_add_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, test_currency, 100)

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)
        assert float(response['result']['balance']['available']) >= 0

        TestTransactionUnfreezeNegative.test_customer_balance_available =\
            float(response['result']['balance']['available'])
        TestTransactionUnfreezeNegative.test_customer_balance_frozen = \
            float(response['result']['balance']['frozen'])

        logger.logger.info(
            F"Customer's balance available in test currency - response: "
            F"{TestTransactionUnfreezeNegative.test_customer_balance_available}")
        print(
            F"Customer's  available balance in test currency - response: "
            F"{TestTransactionUnfreezeNegative.test_customer_balance_available}")

    @allure.step("Freeze all funds that aren't already frozen.")
    @automation_logger(logger)
    def test_freeze_all_funds(self, r_customer):
        response = r_customer.postman.balance_service.\
            subtract_transaction_initialize(r_customer.customer_id, test_currency, TestTransactionUnfreezeNegative.test_customer_balance_available)

        print(f"Freeze response {response}")
        logger.logger.info(f"Freeze response {response}")

        TestTransactionUnfreezeNegative.freeze_transaction_id = response['result']['transactionGuid']
        assert len(TestTransactionUnfreezeNegative.freeze_transaction_id) > 0


    @allure.step("Unfreeze the frozen sum.")
    @automation_logger(logger)
    def test_unfreeze_first(self, r_customer):
        response = r_customer.postman.balance_service.subtract_transaction_commit(
            TestTransactionUnfreezeNegative.freeze_transaction_id, r_customer.customer_id, test_currency)

        # Verifying that all the sum that was frozen in previous step is  unfrozen and removed from customer's balance

        assert float(response['result']['balance']['total']) == TestTransactionUnfreezeNegative.test_customer_balance_frozen
        assert float(response['result']['balance']['available']) == 0
        assert float(response['result']['balance']['frozen']) == TestTransactionUnfreezeNegative.test_customer_balance_frozen

        logger.logger.info(F" Frozen sum unfrozen and removed from customer's balance - response: {response}")
        print(F" Frozen sum unfrozen and removed from customer's balance - response: {response}")

    @allure.step("Verifying that transaction ID can't be used twice to unfreeze funds that are already unfrozen.")
    @automation_logger(logger)
    def test_unfreeze_second(self, r_customer):
        response = r_customer.postman.balance_service.subtract_transaction_commit(
            TestTransactionUnfreezeNegative.freeze_transaction_id, r_customer.customer_id, test_currency)

        logger.logger.info(F"Failed to unfreeze funds by transaction that is expired - response: {response}")
        print(F"Failed to unfreeze funds by transaction that is expired - response: {response}")

        assert "result" not in response.keys()
        assert response['error']['code'] == 104
        assert response['error']['message'] == 'Transaction not found'

        # Verifying that customer's balance wasn't modified following the illegal unfreeze attempt

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)

        assert float(response['result']['balance']['total']) == TestTransactionUnfreezeNegative.test_customer_balance_frozen
        assert float(response['result']['balance']['available']) == 0
        assert float(response['result']['balance']['frozen']) == TestTransactionUnfreezeNegative.test_customer_balance_frozen

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
