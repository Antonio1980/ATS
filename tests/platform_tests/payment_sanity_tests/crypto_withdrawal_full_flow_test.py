import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 4


@pytest.mark.incremental
@allure.story("Client able to perform withdrawal from his trading account.")
@allure.title("WITHDRAWAL CRYPTO")
@allure.description("""
    Functional tests.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Withdrawal Crypto Full Flow')
@allure.testcase(BaseConfig.GITLAB_URL + "/payment_sanity_tests/crypto_withdrawal_full_flow_test.py", "TestWithdrawalCrypto")
@pytest.mark.usefixtures("r_time_count", "conf_customer", )
@pytest.mark.withdrwal
@pytest.mark.payment_sanity
class TestWithdrawalCryptoFullFlow(object):
    available_balance_before, cmp_balance_before = None, None

    @allure.step("Starting with: test_get_customer_balance")
    @automation_logger(logger)
    def test_get_customer_balance(self, conf_customer):

        balance = conf_customer.postman.coins_marketplace.get_customer_cmp_balance(conf_customer.customer_id)
        TestWithdrawalCryptoFullFlow.cmp_balance_before = balance[1]['balance']
        balance_response_before = conf_customer.postman.p_balance_service.get_balance(currency_id)
        assert balance_response_before['error'] is None

        TestWithdrawalCryptoFullFlow.available_balance_before = float(balance_response_before['result']['balance'][str(
            currency_id)]['available'])

    @pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
    @allure.step("Proceed with: test_withdrawal_min_amount_crypto")
    @automation_logger(logger)
    def test_withdrawal_min_amount_crypto(self, conf_customer, min_withdrawal_for_currency):
        logger.logger.info("min_withdrawal_for_currency {0} amount".format(min_withdrawal_for_currency))

        withdrawal_response = conf_customer.postman.payment_service.withdrawal_crypto(
            currency_id, min_withdrawal_for_currency, conf_customer.eth_wallet)
        assert withdrawal_response['error'] is None
        withdrawal_token = withdrawal_response['result']['token']
        time.sleep(5.0)

        withdrawal_confirmation_response = conf_customer.postman.payment_service.withdrawal_crypto_sms_confirmation(
            withdrawal_token)

        assert withdrawal_confirmation_response['error'] is None

    @pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
    @allure.step("Proceed with: test_approve_withdrawal_via_crm")
    @automation_logger(logger)
    def test_approve_withdrawal_via_crm(self, conf_customer, min_withdrawal_for_currency):
        payment_method = 3
        logger.logger.info("min_withdrawal_for_currency {0} amount".format(min_withdrawal_for_currency))

        assert conf_customer.postman.crm.log_in_to_crm()
        customer_withdrawals = conf_customer.postman.crm.get_customer_withdrawals(conf_customer.customer_id)
        withdrawal_html = customer_withdrawals['aaData'][0]['transid']
        parsed_html = Instruments.parse_html(withdrawal_html)
        withdrawal_id = parsed_html.span.text
        logger.logger.info("Withdrawal ID is: {0}".format(withdrawal_id))
        # args: 1- customer_id, 2- withdrawal_id, 3- payment_method_id, 4- currency_name, 5- currency_id,
        # 6- withdrawal_amount
        conf_customer.postman.crm.update_customer_withdrawal(conf_customer.customer_id, withdrawal_id, payment_method,
                                                             'BTC', currency_id, min_withdrawal_for_currency)

    @pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
    @allure.step("Proceed with: test_check_customer_balance")
    @automation_logger(logger)
    def test_check_customer_balance(self, conf_customer, min_withdrawal_for_currency):
        time.sleep(5.0)
        
        balance_response2 = conf_customer.postman.p_balance_service.get_balance(currency_id)
        available_balance_after = float(balance_response2['result']['balance'][str(
            currency_id)]['available'])
        assert round(available_balance_after,1) == round((TestWithdrawalCryptoFullFlow.available_balance_before - float(min_withdrawal_for_currency)),1)
        cmp_balance_after = conf_customer.postman.coins_marketplace.get_customer_cmp_balance(conf_customer.customer_id)[
            1]['balance']
        assert cmp_balance_after == TestWithdrawalCryptoFullFlow.cmp_balance_before - float(min_withdrawal_for_currency)

        logger.logger.info("Test {0} PASSED, with CustomerID {1}".format(test_case, conf_customer.customer_id))
