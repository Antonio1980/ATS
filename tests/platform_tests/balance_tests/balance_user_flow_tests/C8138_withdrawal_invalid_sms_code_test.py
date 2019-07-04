import allure
from src.base import logger
from src.base.instruments import Instruments
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8138"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

balance_added = 1111.11


@allure.feature("Balance - User Flow. ")
@allure.story("Balance is not affected by failed SMS confirmation.")
@allure.title("Balance is not affected by failed SMS confirmation.")
@allure.description("""
    Functional tests.

    1. Performing a withdrawal.
    2. Sending confirmation request with invalid SMS code.

       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C8138_withdrawal_invalid_sms_code_test.py",
                 "SMS confirmation failed, verify balance.")
class TestWithdrawWrongSms(object):
    """
    This test comes to verify, that customer's balance isn't affected
    by failed FIAT withdrawal confirmation. The flow is to request a withdrawal
    and to send a confirmation with incorrect SMS code.
    The confirmation request is to be rejected, customer's balance
    shall remain frozen until the SMS code is valid - currently for 5 minutes.

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

        TestWithdrawWrongSms.withdrawal_token = withdrawal_response['result']['token']

        balance_response = r_customer_sql.postman.balance_service \
            .get_currency_balance(r_customer_sql.customer_id, quoted_currency)

        assert float(balance_response['result']['balance']['available']) == 0
        assert float(balance_response['result']['balance']['frozen']) == balance_added

        logger.logger.info(
            f"Available balance after withdrawal requested: {balance_response['result']['balance']['available']}")
        print(f"Available balance after withdrawal requested: {balance_response['result']['balance']['available']}")

    @allure.step("Sending confirmation request with invalid SMS code.")
    @automation_logger(logger)
    def test_cancel_withdrawal(self, r_customer_sql):

        # Getting the withdrawal ID from DB.
        withdrawal_id = int(Instruments.run_mysql_query(
            f"select id from withdrawals where customerId = {r_customer_sql.customer_id}"
            f" order by withdrawals.dateUpdated desc limit 1")[0][0])

        # Sending invalid withdrawal confirmation with wrong SMS code.
        r_customer_sql.postman.payment_service.headers['Test-Token'] = None

        withdrawal_invalid_confirmation = r_customer_sql. \
            postman.payment_service.withdrawal_wire_sms_confirmation(TestWithdrawWrongSms.withdrawal_token)

        withdrawal_invalid_confirmation['error'] == 'sms code is wrong'

        balance_response = r_customer_sql.postman.balance_service \
            .get_currency_balance(r_customer_sql.customer_id, quoted_currency)

        print(f"Invalid withdrawal response: {withdrawal_invalid_confirmation}")

        # Verifying customer's balance wasn't affected.
        assert float(balance_response['result']['balance']['available']) == 0
        assert float(balance_response['result']['balance']['frozen']) == balance_added

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
