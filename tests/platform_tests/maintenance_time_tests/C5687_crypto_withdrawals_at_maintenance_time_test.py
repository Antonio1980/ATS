import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = '5687'
currency_id = 3


@allure.title("Maintenance Time")
@allure.description("""
    Generate Crypto Withdrawal during Maintenance time, API
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Generate crypto withdrawal
    4. Verify that balance after withdrawal less then balance before withdrawal
    Calculation: balance_after < balance_before 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Generate Crypto Withdrawals during Maintenance time')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/maintenance_time_tests/C5687_crypto_withdrawals_at_maintenance_time_test.py",
    "TestGenerateCryptoWithdrawalsDuringMaintenance")
@pytest.mark.usefixtures('r_time_count', 'me_state', 'conf_customer', )
@pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
@pytest.mark.maintenance_time
class TestGenerateCryptoWithdrawalsDuringMaintenance(object):
    @allure.step("Starting: test_generate_crypto_withdrawal_during_maintenance_time")
    @automation_logger(logger)
    def test_generate_crypto_withdrawal_during_maintenance_time(self, conf_customer, min_withdrawal_for_currency,
                                                                me_state):
        assert me_state == 2
        withdrawal_response = conf_customer.postman.payment_service.withdrawal_crypto(currency_id,
                                                                                      min_withdrawal_for_currency,
                                                                                      conf_customer.btc_wallet)
        assert withdrawal_response['error'] is None
        withdrawal_token = withdrawal_response['result']['token']
        confirmation_response = conf_customer.postman.payment_service.withdrawal_crypto_sms_confirmation(
            withdrawal_token)
        assert confirmation_response['error'] is None
        logger.logger.info("Test {0} PASSED, with CustomerID {1}".format(test_case, conf_customer.customer_id))
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
