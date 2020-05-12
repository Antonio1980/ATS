import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8142"


@allure.feature("Balance")
@allure.story("Ability to frozen balance for the given account per customer_id, currency and amount.")
@allure.title("Frozen BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1 test Subtract Transaction Initialize (To Frozen balance per action - send order, withdrawal,fees transaction)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8142_subtract_transaction_initialize_test.py",
                 "Subtract Transaction Initialize")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestSubtractTransactionInitialize(object):
    currency_id = 3
    amount = 10

    @allure.step("Starting with: subtract_transaction_initialize")
    @automation_logger(logger)
    def test_subtract_transaction_initialize(self, r_customer):

        # Added by Evgeniy to prevent a situation where customer has no funds in BTC and the test fails.
        r_customer.postman.balance_service.\
            add_balance(r_customer.customer_id,
                        TestSubtractTransactionInitialize.currency_id, TestSubtractTransactionInitialize.amount)

        get_frozen_balance = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id,
                                                                                     self.currency_id)
        frozen = get_frozen_balance['result']['balance']['frozen']

        response = r_customer.postman.balance_service.subtract_transaction_initialize(r_customer.customer_id,
                                                                                      self.currency_id, self.amount)
        frozen_after = response['result']['balance']['frozen']
        assert float(frozen_after) == float(frozen) + float(self.amount)
        assert response['result'] is not None
        assert response['result']['transactionGuid'] is not None
        assert isinstance(response, dict)
        assert isinstance(response["result"]['balance'], dict)
        assert response['result']['balance'] is not None
        assert r_customer.customer_id == response['result']['customerId']
        assert self.currency_id == response['result']['currencyId']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))
