import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Exchange And Customer Data")
@allure.story("Not authorized client able to receive info about Trading Platform")
@allure.title("PLATFORM DATA")
@allure.description("""
    Functional api test.
    Coverage:
    trade_service, exchange_and_customer_data, public_api
    1 test_platform_data
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Platform Data')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/trade_service_tests/platform_data_test.py", "TestCustomerData")
@pytest.mark.usefixtures("r_time_count", "customer")
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.trade_service
@pytest.mark.exchange_and_customer_data
class TestPlatformData(object):
    test_case = "Platform Data Validation"

    @allure.step("Verifying valid platform data provided")
    @automation_logger(logger)
    def test_platform_data(self, customer):
        response = customer.postman.trade_service.platform_data()
        assert response['error'] is None

        # Verifying assets
        assert isinstance(response['result']['assets'], list)
        assert response['result']['assets'] != []
        assert response['result']['assets'][0]['name'] == "BTC/USD"

        for asset in response['result']['assets']:
            assert isinstance(asset['id'], int)
            assert isinstance(asset['name'], str)
            assert isinstance(asset['fullName'], str)
            assert isinstance(asset['assetTypeId'], int)
            assert isinstance(asset['baseCurrencyId'], int)
            assert isinstance(asset['quotedCurrencyId'], int)
            assert isinstance(asset['tailDigits'], int)
            assert isinstance(asset['significantDigit'], int)

        logger.logger.info("Assets verified")

        # Verifying asset types
        assert isinstance(response['result']['assetTypes'], list)
        assert response['result']['assetTypes'] != []
        assert response['result']['assetTypes'][0]['name'] == 'Cryptocurrencies'
        assert response['result']['assetTypes'][1]['name'] == 'DigitalStocks'
        assert response['result']['assetTypes'][2]['name'] == 'ETF'

        logger.logger.info("Asset types verified")

        # Verifying currencies
        assert isinstance(response['result']['currencies'], list)
        assert response['result']['currencies'] != []

        for currency in response['result']['currencies']:
            assert isinstance(currency['id'], int)
            assert isinstance(currency['name'], str)
            assert isinstance(currency['code'], str)
            assert isinstance(currency['symbol'], str)
            assert isinstance(currency['isCryptoCurrency'], bool)
            assert isinstance(currency['tailDigits'], int)
            assert isinstance(currency['description'], str)
            assert isinstance(currency['videoUrl'], str)

        logger.logger.info("Currencies verified")

        # Verifying instruments
        assert isinstance(response['result']['instruments'], list)
        assert response['result']['instruments'] != []

        for instrument in response['result']['instruments']:
            assert isinstance(instrument['id'], int)
            assert isinstance(instrument['productId'], int)
            assert isinstance(instrument['name'], str)
            assert isinstance(instrument['assetId'], int)
            assert isinstance(instrument['statusId'], int)
            assert isinstance(instrument['dateInserted'], int)
            assert isinstance(instrument['dateUpdated'], int)
            assert isinstance(instrument['asset'], dict)
            assert isinstance(instrument['meQuantityMultiplier'], int)
            assert isinstance(instrument['referencePriceParameter'], float)

        logger.logger.info("Instruments verified ")

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
