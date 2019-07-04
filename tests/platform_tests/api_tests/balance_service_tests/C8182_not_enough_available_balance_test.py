import allure
import pytest
from src.base import logger
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "8182"

test_currency = 1

# Frozen funds can't be frozen twice.
# The sum that needs to be frozen must be on customer's AVAILABLE balance.
# If the customer possesses the funds, but they are frozen - "Not enough funds" error will be presented.


@allure.feature("Balance")
@allure.story("No balance is frozen if the requested sum is greater than available  balance, 'Not enough funds' error.")
@allure.title("Frozen BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1. Clear the balance of the customer used for this test, cancel all orders.
    2. Add and freeze 100 USD.
    3. Try to freeze the sum that is already frozen.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8153_freeze_failure_no_GUID_test.py",
                 "Invalid freeze request has no effect.")
@pytest.mark.usefixtures("r_customer")
class TestNoFreeze(object):

    test_customer_balance_available = ""
    test_customer_balance_frozen = ""


    @allure.step("Add 100 to available balance.")
    @automation_logger(logger)
    def test_add_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, test_currency, 100)

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)
        assert float(response['result']['balance']['available']) >= 0

        TestNoFreeze.test_customer_balance_available = float(response['result']['balance']['available'])
        TestNoFreeze.test_customer_balance_frozen = float(response['result']['balance']['frozen'])

        logger.logger.info(F"Customer's balance available in test currency - response: {TestNoFreeze.test_customer_balance_available}")
        print(F"Customer's  available balance in test currency - response: {TestNoFreeze.test_customer_balance_available}")

    @allure.step("Freeze all funds.")
    @automation_logger(logger)
    def test_freeze_all_funds(self,r_customer):
        response = r_customer.postman.balance_service.subtract_transaction_initialize(r_customer.customer_id, test_currency, TestNoFreeze.test_customer_balance_available)
        assert response['result'], "Not enough funds"


    @allure.step("Try to freeze the sum that is already frozen.")
    @automation_logger(logger)
    def test_freeze_twice(self, r_customer):
        response = r_customer.postman.balance_service.subtract_transaction_initialize(r_customer.customer_id, test_currency, TestNoFreeze.test_customer_balance_available)

        assert response['error']['code'] == 106
        assert response['error']['message'] == "Not enough funds"
        assert response['error']['data']['customerId'] == r_customer.customer_id
        assert response['error']['data']['currencyId'] == test_currency
        assert float(response['error']['data']['balance']['total']) == TestNoFreeze.test_customer_balance_available + TestNoFreeze.test_customer_balance_frozen
        assert float(response['error']['data']['balance']['available']) == 0
        assert float(response['error']['data']['balance']['frozen']) == TestNoFreeze.test_customer_balance_frozen + TestNoFreeze.test_customer_balance_available

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
