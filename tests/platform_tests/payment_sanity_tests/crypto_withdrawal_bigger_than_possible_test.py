import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""
cmp_balance = 0
currency_id = 3


@allure.story("Client able to perform withdrawal from his trading account.")
@allure.title("WITHDRAWAL CRYPTO")
@allure.description("""
    Functional tests.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Withdrawal Crypto Negative')
@allure.testcase(BaseConfig.GITLAB_URL + "/payment_sanity_tests/crypto_withdrawal_bigger_than_possible_test.py",
                 "TestWithdrawalCryptoNegative")
@pytest.mark.usefixtures("r_time_count", "conf_customer", )
@pytest.mark.withdrwal
@pytest.mark.payment_sanity
class TestWithdrawalCryptoNegative(object):

    @pytest.mark.parametarize("max_withdrawal_for_currency", [[currency_id]], indirect=True)
    @allure.step("Starting with: test_withdrawal_crypto_negative")
    @automation_logger(logger)
    def test_withdrawal_crypto_negative(self, conf_customer, max_withdrawal_for_currency):
        updated_cmp_balance = 0
        logger.logger.info("test case {0} method test_withdrawal_crypto_negative".format(test_case))

        cmp_balance_response = conf_customer.postman.coins_marketplace.get_customer_cmp_balance(conf_customer.customer_id)
        assert isinstance(cmp_balance_response, list)
        if cmp_balance_response[0]['currency'] == "BTC":
            updated_cmp_balance = cmp_balance_response[0]['balance']

            logger.logger.info("Customer CMP balance: {0}".format(updated_cmp_balance))

        cmp_balance_bigger = updated_cmp_balance + 0.001
        if cmp_balance_bigger <= float(max_withdrawal_for_currency):
            withdrawal_response = conf_customer.postman.payment_service.withdrawal_crypto(
                currency_id, cmp_balance_bigger, conf_customer.btc_wallet)
            assert withdrawal_response['error'] is not None

            logger.logger.info("=================TEST IS PASSED==========================")
