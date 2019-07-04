import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.data_bases.sql_db import SqlDb
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 2


@allure.feature("Withdrawal")
@allure.title("Withdrawal Sepa")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
    Verify that customer able to withdrawal his balance using SEPA.
    1) Withdrawal SEPA with approved customer
    2) Withdrawal SEPA with customer has status "Pending"
    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Withdrawal Sepa')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/withdrawal_sepa_test.py",
                 "TestWithdrawalSepa")
@pytest.mark.usefixtures("r_time_count", "conf_customer")
@pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
@pytest.mark.withdrawal
@pytest.mark.regression
@pytest.mark.payment_service
class TestWithdrawalSepa(object):

    @pytest.fixture(scope="class")
    @automation_logger(logger)
    def another_customer(self, customer):
        customer = Customer()
        customer.insert_customer_new()
        return customer

    @allure.step("Starting with: test_withdrawal_sepa_with_approved_customer")
    @automation_logger(logger)
    def test_withdrawal_sepa_with_approved_customer(self, conf_customer, min_withdrawal_for_currency):
        time.sleep(10.0)
        withdrawal_response = conf_customer.postman.payment_service.withdrawal_sepa(
            conf_customer.bank, currency_id, min_withdrawal_for_currency)
        assert withdrawal_response['error'] is None
        withdrawal_token = withdrawal_response['result']['token']

        logger.logger.info(F"Withdrawal Token: {withdrawal_token}")
        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 4, currency_id)
        logger.logger.info(F"Customer sepa withdrawals before confirmation: {withdrawals}")
        assert int(withdrawals[0][10]) == 5, "Withdrawal status != 5"

        confirmation_response = conf_customer.postman.payment_service.withdrawal_sepa_sms_confirmation(withdrawal_token)
        assert confirmation_response['error'] is None

        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 4, currency_id)
        logger.logger.info(F"Customer wire withdrawals after confirmation: {withdrawals}")
        assert int(withdrawals[0][10]) == 1, "Withdrawal status != 1"

        time.sleep(30.0)

        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, 4, currency_id)
        assert int(withdrawals[0][10]) == 2, "Withdrawal status != 2"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_withdrawal_sepa_customer_not_approved")
    @automation_logger(logger)
    def test_withdrawal_sepa_customer_not_approved(self, another_customer, min_withdrawal_for_currency):
        balance_response = another_customer.postman.balance_service.add_balance(
            another_customer.customer_id, currency_id, 1000)
        assert int(balance_response['result']['balance']['available']) == 1000

        withdrawal_response = another_customer.postman.payment_service.withdrawal_sepa(
            another_customer.bank, currency_id, min_withdrawal_for_currency)

        assert withdrawal_response['error'].find('your account has not been approved yet') != -1

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

