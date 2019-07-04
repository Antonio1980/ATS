import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8153"


@allure.feature("Balance")
@allure.story("No balance is frozen if the requested sum is greater than available  balance.")
@allure.title("Frozen BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1. Clear the balance of the customer used for this test, cancel all orders.
    2. Try to freeze more than the customer has and verify response.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8153_freeze_failure_no_GUID_test.py",
                 "Invalid freeze request has no effect.")
@pytest.mark.usefixtures("r_customer")
@pytest.mark.parametrize('two_customers', [[True]], indirect=True)
class TestFreezeFailure(object):

    joe = None
    joe_token = ""

    @allure.step("Try to freeze more than the customer has and verify response.")
    @automation_logger(logger)
    def test_freeze_failure(self, r_customer, two_customers):
        TestFreezeFailure.joe = two_customers[0][0]
        TestFreezeFailure.joe_token = two_customers[0][1]
        r_customer.postman.balance_service.add_balance(TestFreezeFailure.joe.customer_id, 1, 100)

        response = r_customer.postman.balance_service.get_currency_balance(TestFreezeFailure.joe.customer_id, 1)
        assert float(response['result']['balance']['available']) == 100

        unfreeze_response = r_customer.postman.balance_service.\
            subtract_transaction_initialize(TestFreezeFailure.joe.customer_id, 1, 1000)

        logger.logger.info(F"Trying to unfreeze 1000 USD while 100 available - response: {unfreeze_response}")
        print(F"Trying to unfreeze 1000 USD while 100 available - response: {unfreeze_response}")

        # Transaction ID is placed under "result". If there is no "result" , there is no transaction in response.
        assert "result" not in unfreeze_response.keys()

        assert unfreeze_response['error']['code'] == 106
        assert unfreeze_response['error']['message'] == "Not enough funds"
        assert str(unfreeze_response['error']['data']['customerId']) == TestFreezeFailure.joe.customer_id
        assert unfreeze_response['error']['data']['currencyId'] == 1
        assert float(unfreeze_response['error']['data']['balance']['total']) == 100
        assert float(unfreeze_response['error']['data']['balance']['available']) == 100
        assert float(unfreeze_response['error']['data']['balance']['frozen']) == 0

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
