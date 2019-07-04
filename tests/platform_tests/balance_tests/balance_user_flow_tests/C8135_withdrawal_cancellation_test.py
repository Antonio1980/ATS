import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8135"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

balance_added = 1111.11


@allure.feature("Balance - User Flow. ")
@allure.story("Balance is unfrozen when withdrawal is cancelled .")
@allure.title("Balance is unfrozen when withdrawal is cancelled .")
@allure.description("""
    Functional tests.

    1. Performing a withdrawal.
    2. Cancelling the withdrawal, verifying balance is unfrozen.

       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C8135_withdrawal_cancellation_test.py",
                 "Cancel withdrawal, verify balance.")
class TestPlaceCancelWithdraw(object):
    """
    This test comes to verify that balance is unfrozen when the withdrawal is cancelled.
    Non round sum is used in order to verify there are no rounding problems.

    """

    withdrawal_token = None

    @allure.step("Performing a withdrawal.")
    @automation_logger(logger)
    def test_perform_withdrawal(self, r_customer_sql):

        balance_response = r_customer_sql.postman.balance_service. \
            add_balance(r_customer_sql.customer_id, quoted_currency, balance_added)

        logger.logger.info(f"Balance response: {balance_response}")
        print(f"Balance response: {balance_response}")

        withdrawal_response = r_customer_sql.postman.payment_service. \
            withdrawal_wire(r_customer_sql.bank, quoted_currency, balance_added)

        assert withdrawal_response['error'] is None

        TestPlaceCancelWithdraw.withdrawal_token = withdrawal_response['result']['token']

        balance_response = r_customer_sql.postman.balance_service \
            .get_currency_balance(r_customer_sql.customer_id, quoted_currency)

        assert float(balance_response['result']['balance']['available']) == 0
        assert float(balance_response['result']['balance']['frozen']) == balance_added

        logger.logger.info(f"Available balance after withdrawal: {balance_response['result']['balance']['available']}")
        print(f"Available balance after withdrawal: {balance_response['result']['balance']['available']}")

    @allure.step("Cancelling the withdrawal, verifying balance is unfrozen.")
    @automation_logger(logger)
    def test_cancel_withdrawal(self, r_customer_sql):
        withdrawal_id = int(Instruments.run_mysql_query(
            f"select id from withdrawals where customerId = {r_customer_sql.customer_id}"
            f" order by withdrawals.dateUpdated desc limit 1")[0][0])

        withdrawal_cancel_response = r_customer_sql.postman.payment_service.withdrawal_cancel(withdrawal_id)

        logger.logger.info(f"Withdrawal cancel response: {withdrawal_cancel_response}")
        print(f"Withdrawal cancel response: {withdrawal_cancel_response}")

        balance_response = r_customer_sql.postman.balance_service \
            .get_currency_balance(r_customer_sql.customer_id, quoted_currency)

        logger.logger.info(
            f"Available balance after withdrawal cancellation: {balance_response['result']['balance']['available']}")
        print(f"Available balance after withdrawal cancellation: {balance_response['result']['balance']['available']}")

        assert float(balance_response['result']['balance']['available']) == balance_added
        assert float(balance_response['result']['balance']['frozen']) == 0

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
