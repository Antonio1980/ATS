import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8446"

# The parameters below are used for test configuration
currency_id = 3

balance_added = 2
withdrawn_amount = 1.888888

# Time it takes to cancel the withdrawal and to perform a roll back.
ROLL_BACK_DELAY = 60


@allure.feature("Balance - User Flow.")
@allure.story("Roll back performed after failed crypto withdrawal.")
@allure.title("Roll back performed after failed crypto withdrawal.")
@allure.description("""
    Functional tests.

    1. Performing a withdrawal.
    2. Verifying rollback.

       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C8446_rolback_crypto_withdrawal_test.py",
                 "Roll back performed after failed withdrawal")
class TestPlaceCancelWithdraw(object):
    """
    This test comes to verify roll back after failed crypto withdrawal.
    Customer used for this test have 2 BTC on system balance, and no BTC on CMP balance.
    When a withdrawal of 1.888888 is attempted it will fail. Correct roll back is expected.
    """


    @allure.step("Performing a withdrawal.")
    @automation_logger(logger)
    def test_perform_withdrawal(self, r_customer_sql):

        balance_response = r_customer_sql.postman.balance_service. \
            add_balance(r_customer_sql.customer_id, currency_id, balance_added)

        logger.logger.info(f"Balance response: {balance_response}")
        print(f"Balance response: {balance_response}")

        withdrawal_response = r_customer_sql.postman.payment_service. \
            withdrawal_wire(r_customer_sql.bank, currency_id, withdrawn_amount)

        print(f"Withdrawal response: {withdrawal_response}")


        balance_response = r_customer_sql.postman.balance_service \
            .get_currency_balance(r_customer_sql.customer_id, currency_id)


        logger.logger.info(f"Available balance after withdrawal: {balance_response['result']['balance']['available']}")
        print(f"Available balance after withdrawal: {balance_response['result']['balance']['available']}")

    @allure.step("Verifying rollback.")
    @automation_logger(logger)
    def test_cancel_withdrawal(self, r_customer_sql):

        time.sleep(ROLL_BACK_DELAY)

        balance_response = r_customer_sql.postman.balance_service \
            .get_currency_balance(r_customer_sql.customer_id, currency_id)

        print(f"Balance response after {ROLL_BACK_DELAY} : {balance_response}")

        assert float(float(balance_response['result']['balance']['available'])) == balance_added
        assert float(float(balance_response['result']['balance']['frozen'])) == 0


        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
