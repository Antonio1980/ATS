import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

bitcoin_id = 3
litecoin_id = 7
test_case = ""


@allure.feature("Deposit")
@allure.title("Deposit Crypto")
@allure.description("""
    Functional tests.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Deposit Crypto')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/deposit_crypto_test.py", "TestDepositCrypto")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.deposit
@pytest.mark.regression
@pytest.mark.payment_service
class TestDepositCrypto(object):

    @allure.step("Proceed with: test_bitcoin_deposit")
    @automation_logger(logger)
    def test_bitcoin_deposit(self, r_customer):
        bitcoin_deposit_response = r_customer.postman.payment_service.add_deposit_crypto(bitcoin_id)
        assert bitcoin_deposit_response['error'] is None
        first_deposit = bitcoin_deposit_response['result']['link']

        logger.logger.info("1 DEPOSIT ADDRESS SUCCESS: {0}".format(first_deposit))

    @allure.step("Proceed with: test_lightcoin_deposit")
    @automation_logger(logger)
    def test_lightcoin_deposit(self, r_customer):
        time.sleep(15.0)
        lightcoin_deposit_response = r_customer.postman.payment_service.add_deposit_crypto(litecoin_id)
        assert lightcoin_deposit_response['error'] is None
        second_deposit = lightcoin_deposit_response['result']['link']

        logger.logger.info("2 DEPOSIT ADDRESS SUCCESS: {0}".format(second_deposit))
