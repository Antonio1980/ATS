import allure
import pytest
from src.base import logger
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "8176"
expected_error = 105
test_currency = 1

# In this test we are verifying that there is no option to unfreeze a greater sum than the sum that was frozen by GUID.


@allure.feature("Balance")
@allure.story("No option to unfreeze a greater sum than the sum that was frozen.")
@allure.title("Unfreeze Balance - Negative")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1. Add 100 to available balance.
    2. Freeze all funds that aren't already frozen.
    3. Verify the unfrozen sum can't be greater than the frozen sum.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8176_unfreeze_more_than_frozen_test.py",
                 "Unfreeze Balance - Negative")
@pytest.mark.usefixtures("r_customer")
class TestUnfreezeAmountNegative(object):
    freeze_transaction_id = ""
    test_customer_balance_available = ""
    test_customer_balance_frozen = ""

    @allure.step("Add 100 to available balance.")
    @automation_logger(logger)
    def test_add_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, test_currency, 100)

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)
        assert float(response['result']['balance']['available']) >= 0

        TestUnfreezeAmountNegative.test_customer_balance_available = \
            float(response['result']['balance']['available'])
        TestUnfreezeAmountNegative.test_customer_balance_frozen = \
            float(response['result']['balance']['frozen'])

        logger.logger.info(
            F"Customer's balance available in test currency - response: "
            F"{TestUnfreezeAmountNegative.test_customer_balance_available}")
        print(
            F"Customer's  available balance in test currency - response: "
            F"{TestUnfreezeAmountNegative.test_customer_balance_available}")

    @allure.step("Freeze all funds that aren't already frozen.")
    @automation_logger(logger)
    def test_freeze_all_funds(self, r_customer):
        response = r_customer.postman.balance_service. \
            subtract_transaction_initialize(r_customer.customer_id, test_currency,
                                            TestUnfreezeAmountNegative.test_customer_balance_available)

        print(f"Freeze response {response}")
        logger.logger.info(f"Freeze response {response}")

        TestUnfreezeAmountNegative.freeze_transaction_id = response['result']['transactionGuid']
        assert len(TestUnfreezeAmountNegative.freeze_transaction_id) > 0

    @allure.step("Verify the unfrozen sum can't be greater than the frozen sum.")
    @automation_logger(logger)
    def test_invalid_unfreeze_attempted(self, r_customer):

        # Attempting illegal unfreeze using "transaction partial commit" method.
        response = r_customer. \
            postman.balance_service.subtract_transaction_partial_commit(
            TestUnfreezeAmountNegative.freeze_transaction_id, r_customer.customer_id, test_currency,
            TestUnfreezeAmountNegative.test_customer_balance_available + 1)

        assert response['error']['code'] == expected_error
        assert response['error']['message'] == 'Operation leads to negative frozen remainder'

        # Attempting illegal unfreeze using "transaction partial rollback" method.
        response = r_customer.postman.balance_service.subtract_transaction_partial_rollback(
            TestUnfreezeAmountNegative.freeze_transaction_id, r_customer.customer_id, test_currency,
            TestUnfreezeAmountNegative.test_customer_balance_available + 1)

        assert response['error']['code'] == expected_error
        assert response['error']['message'] == 'Operation leads to negative frozen remainder'

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)

        assert float(response['result']['balance'][
                         'total']) == TestUnfreezeAmountNegative.test_customer_balance_available + TestUnfreezeAmountNegative.test_customer_balance_frozen
        assert float(response['result']['balance']['available']) == 0
        assert float(response['result']['balance'][
                         'frozen']) == TestUnfreezeAmountNegative.test_customer_balance_available + TestUnfreezeAmountNegative.test_customer_balance_frozen

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
