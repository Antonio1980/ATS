import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Withdrawal")
@allure.title("Withdrawal Sepa")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
    Verify that customer able to withdrawal his balance using Withdrawal Sepa.
    1) Withdrawal Sepa with approved customer
    2)Check balance before and after withdrawal.
    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Withdrawal Sepa')
@allure.testcase(BaseConfig.GITLAB_URL + "/payment_sanity_tests/fiat_withdrawal_sepa_test.py",
                 "TestWithdrawalSepaFiat")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.withdrawal
@pytest.mark.payment_service
class TestWithdrawalWireFiat(object):
    currency_id = 2
    amount_withdrawal = 500
    payment_method_id = 4

    @allure.step("Starting with: test_withdrawal_sepa_with_approved_customer")
    @automation_logger(logger)
    def test_withdrawal_sepa_with_approved_customer(self, r_customer):
        logger.logger.info("method test_withdrawal_sepa_approved")
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, self.currency_id,
                                                       self.amount_withdrawal * 2)
        available_balance_before = r_customer.postman.balance_service.get_currency_balance(int(r_customer.customer_id),
                                                                                           self.currency_id)
        available_before = float(available_balance_before['result']['balance']['available'])
        assert available_before > self.amount_withdrawal
        withdrawal_response = r_customer.postman.payment_service.withdrawal_sepa(r_customer.bank, self.currency_id,
                                                                                 self.amount_withdrawal)
        assert withdrawal_response['error'] is None
        withdrawal_id = withdrawal_response['result']['withdrawalId']
        currency_name = Instruments.get_currency_name_by_currency_id(self.currency_id)
        withdrawal_approval = r_customer.postman.crm.update_customer_withdrawal(r_customer.customer_id, withdrawal_id,
                                                                                self.payment_method_id, currency_name,
                                                                                self.currency_id,
                                                                                self.amount_withdrawal)
        assert "success" in withdrawal_approval
        withdrawal_token = withdrawal_response['result']['token']
        confirmation_response = r_customer.postman.payment_service.withdrawal_wire_sms_confirmation(withdrawal_token)
        assert confirmation_response['error'] is None
        available_balance_after = r_customer.postman.balance_service.get_currency_balance(int(r_customer.customer_id),
                                                                                          self.currency_id)
        available_after = float(available_balance_after['result']['balance']['available'])
        assert available_after == available_before - self.amount_withdrawal
        logger.logger.info("Test {0} PASSED, with CustomerID {1}".format(test_case, r_customer.customer_id))
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))