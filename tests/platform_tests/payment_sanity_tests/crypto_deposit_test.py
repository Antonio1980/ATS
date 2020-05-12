import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

btc_id = 3
ltc_id = 7
test_case = "7587"


@pytest.mark.incremental
@allure.story("Client able to perform deposit on his crypto wallet.")
@allure.title("DEPOSIT CRYPTO")
@allure.description("""
    Functional tests.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Crypto Deposit')
@allure.testcase(BaseConfig.GITLAB_URL + "/payment_sanity_tests/crypto_deposit_test.py", "TestCryptoDeposit")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.deposit
@pytest.mark.payment_sanity
class TestCryptoDeposit(object):

    @allure.step("Proceed with: test_btc_deposit")
    @automation_logger(logger)
    def test_btc_deposit(self, r_customer):
        btc_deposit_response = r_customer.postman.payment_service.add_deposit_crypto(btc_id)
        assert btc_deposit_response['error'] is None
        first_deposit = btc_deposit_response['result']['link']

        logger.logger.info("1 DEPOSIT ADDRESS SUCCESS: {0}".format(first_deposit))

    @allure.step("Proceed with: test_ltc_deposit")
    @automation_logger(logger)
    def test_ltc_deposit(self, r_customer, max_deposit_for_currency):
        ltc_deposit_response = r_customer.postman.payment_service.add_deposit_crypto(ltc_id)
        assert ltc_deposit_response['error'] is None
        second_deposit = ltc_deposit_response['result']['link']

        logger.logger.info("2 DEPOSIT ADDRESS SUCCESS: {0}".format(second_deposit))
