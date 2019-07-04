import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.data_bases.sql_db import SqlDb
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 1


@allure.feature("Withdrawal")
@allure.title("Withdrawal Cancel")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
    API Functional Tests
    1. Verify that customer able to cancell withdrawal wire (SQL status=2)
    2. Verify that customer able to cancell withdrawal sepa (SQL status=4)
    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Cancel Withdrawal')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/withdrawal_cancel_test.py",
                 "TestCancelWithdrawal")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.withdrawal
@pytest.mark.regression
@pytest.mark.payment_service
class TestCancelWithdrawal(object):

    @allure.step("Starting with: test_cancel_withdrawal")
    @automation_logger(logger)
    @pytest.mark.parametrize('add_balance', [[currency_id]], indirect=True)
    @pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
    def test_cancel_withdrawal_wire(self, r_customer, min_withdrawal_for_currency, add_balance):
        withdrawal_response = r_customer.postman.payment_service.withdrawal_wire(
            r_customer.bank, currency_id, min_withdrawal_for_currency)
        assert withdrawal_response['error'] is None
        time.sleep(2.0)

        withdrawals = SqlDb.get_withdrawals_by_customer(r_customer.customer_id, 2, currency_id)
        logger.logger.info(F"Customer wire withdrawals before cancellation: {withdrawals}")
        assert int(withdrawals[0][10]) == 5, "Withdrawal status != 5"
        withdrawal_id = int(withdrawals[0][0])
        logger.logger.info(F"Withdrawal wire ID: {withdrawal_id}")

        cancel_response = r_customer.postman.payment_service.withdrawal_cancel(withdrawal_id)
        assert cancel_response['error'] is None

        withdrawals = SqlDb.get_withdrawals_by_customer(r_customer.customer_id, 2, currency_id)
        logger.logger.info(F"Customer wire withdrawals after cancellation: {withdrawals}")
        withdrawal_status = int(withdrawals[0][10])
        assert withdrawal_status == 4, "Withdrawal status != 4"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_cancel_withdrawal")
    @automation_logger(logger)
    @pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
    def test_cancel_withdrawal_sepa(self, r_customer, min_withdrawal_for_currency, add_balance):
        time.sleep(10)
        withdrawal_response = r_customer.postman.payment_service.withdrawal_sepa(
            r_customer.bank, currency_id, min_withdrawal_for_currency)
        assert withdrawal_response['error'] is None
        time.sleep(2.0)

        withdrawals = SqlDb.get_withdrawals_by_customer(r_customer.customer_id, 4, currency_id)
        logger.logger.info(F"Customer sepa withdrawals before cancellation: {withdrawals}")
        assert int(withdrawals[0][10]) == 5, "Withdrawal status != 5"
        withdrawal_id = int(withdrawals[0][0])
        logger.logger.info(F"Withdrawal sepa ID: {withdrawal_id}")
        cancel_response = r_customer.postman.payment_service.withdrawal_cancel(withdrawal_id)
        assert cancel_response['error'] is None

        withdrawals = SqlDb.get_withdrawals_by_customer(r_customer.customer_id, 4, currency_id)
        logger.logger.info(F"Customer sepa withdrawals after cancellation: {withdrawals}")
        withdrawal_status = int(withdrawals[0][10])
        assert withdrawal_status == 4, "Withdrawal status != 4"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
