import pytest
import allure
from src.base import logger
from datetime import datetime
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""
oldest_asset_date_introduced: datetime = datetime(2009, 1, 3)


@allure.feature("Exchange And Customer Data")
@allure.story("Client able to receive relevant currency data")
@allure.title("CRYPTO CURRENCY DATA")
@allure.description("""
    Functional api test.
    Coverage:
    trade_service, crypto currency data  
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Cryptocurrency Data')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/trade_service_tests/cryptocurrency_data_test.py",
                 "TestCryptoCurrencyData")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.trade_service
@pytest.mark.exchange_and_customer_data
class TestCryptoData(object):
    # List of existing crypto in the system
    crypto_currencies_list = [3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]
    # crypto_currencies_list = [3, 4, 5]

    # Please note - right now the test fails because of a bug.
    # If you want it to pass - use the shorter currencies list : [3, 4, 5]

    # Comes to verify that valid crypto currency data is provided for each currency
    @allure.step("Starting: test_crypto_currency_data")
    @automation_logger(logger)
    def test_crypto_currency_data(self, customer):
        logger.logger.info("Starting wityh: test_cryptocurrency_data_test")

        for crypto in TestCryptoData.crypto_currencies_list:
            response = customer.postman.trade_service.crypto_currency_data(crypto)
            assert response['error'] is None
            assert isinstance(response['result'], dict)

            # Veifying that currency data isn't null
            currency_data = response['result']['data']
            assert currency_data is not None

            date_introduced = response['result']['data']['dateIntroduced']
            date_introduced_conventional = datetime.fromtimestamp(date_introduced)

            # Verifying that date introduced is valid - currency can't be older than BTC
            assert date_introduced_conventional > oldest_asset_date_introduced

            # Verifying that the events list related to crypto currency isn't empty.
            events = response['result']['events']
            assert events != []

            logger.logger.info("---------------TEST CASE {0} PASSED!--------------".format(test_case))
