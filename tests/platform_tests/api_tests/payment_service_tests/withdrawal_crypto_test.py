import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.data_bases.sql_db import SqlDb
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 4


@pytest.mark.incremental
@allure.feature("Withdrawal")
@allure.title("Withdrawal Crypto")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
    Verify that customer able to withdrawal his balance using crypto wallet.
    Verify that customer able to cancell withdrawal crypto (SQL status=3)
    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Withdrawal Crypto')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/withdrawal_crypto_test.py",
                 "TestWithdrawalCryptoApproved")
@pytest.mark.usefixtures("r_time_count", "conf_customer")
@pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
@pytest.mark.withdrawal
@pytest.mark.regression
@pytest.mark.payment_service
class TestWithdrawalCryptoApproved(object):

    @allure.step("Starting with: test_withdrawal_crypto_approved")
    @automation_logger(logger)
    def test_withdrawal_crypto_approved(self, conf_customer, min_withdrawal_for_currency):
        withdrawal_response = conf_customer.postman.payment_service.withdrawal_crypto(currency_id,
                                                                                      min_withdrawal_for_currency,
                                                                                      conf_customer.eth_wallet)
        assert withdrawal_response['error'] is None
        withdrawal_token = withdrawal_response['result']['token']
        logger.logger.info(F"Withdrawal Token: {withdrawal_token}")
        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 3, currency_id)
        logger.logger.info(F"Customer crypto withdrawals before confirmation: {withdrawals}")
        assert int(withdrawals[0][10]) == 5, "Withdrawal status != 5"

        confirmation_response = conf_customer.postman.payment_service.withdrawal_crypto_sms_confirmation(
            withdrawal_token)
        assert confirmation_response['error'] is None

        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 3, currency_id)
        logger.logger.info(F"Customer crypto withdrawals after confirmation: {withdrawals}")
        assert int(withdrawals[0][10]) == 1, "Withdrawal status != 1"

        time.sleep(30.0)

        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 3, currency_id)
        assert int(withdrawals[0][10]) == 2, "Withdrawal status != 2"
        
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_cancel_withdrawal")
    @automation_logger(logger)
    def test_cancel_withdrawal_crypto(self, conf_customer, min_withdrawal_for_currency):
        withdrawal_response = conf_customer.postman.payment_service.withdrawal_crypto(currency_id,
                                                                                      min_withdrawal_for_currency,
                                                                                      conf_customer.eth_wallet)
        assert withdrawal_response['error'] is None

        time.sleep(1.0)
        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 3, currency_id)
        logger.logger.info(F"Customer crypto withdrawals before confirmation: {withdrawals}")
        assert int(withdrawals[0][10]) == 5, "Withdrawal status != 5"
        withdrawal_id = int(withdrawals[0][0])
        logger.logger.info(F"Withdrawal crypto ID: {withdrawal_id}")
        cancel_response = conf_customer.postman.payment_service.withdrawal_cancel(withdrawal_id)
        assert cancel_response['error'] is None

        time.sleep(1.0)
        withdrawal_status = int(SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 3, currency_id)[0][10])
        assert withdrawal_status == 4, "Withdrawal status != 4"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
