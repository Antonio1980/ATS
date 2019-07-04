import pytest
import allure
from src.base import logger
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "country_data"


@allure.feature("Exchange And Customer Data")
@allure.title("COUNTRY DATA")
@allure.description("""
    Sanity API test.
    Coverage:
    trade_service, test_country_data
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Country Data')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/trade_service_tests/country_data_test.py", "TestCountryData")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.trade_service
@pytest.mark.exchange_and_customer_data
class TestCountryData(object):

    @allure.step("Starting: test_country_data")
    @automation_logger(logger)
    def test_country_data(self, customer):
        """
        We are sending a request to Trade Service and asking for Country Data.
        JSON with country data should be received.
        We verify that the data is provided and valid.
        :param customer: any unregistred customer
        """
        response = customer.postman.trade_service.country_data()

        countries = response['result']['countries']
        assert isinstance(countries, list)

        assert countries != []

        assert response['error'] is None

        amount_of_countries = len(countries)

        # Verifying the response format for every country
        for index in range(amount_of_countries):
            assert isinstance(response['result']['countries'][index]['id'], int)
            assert isinstance(response['result']['countries'][index]['iso'], str)
            assert isinstance(response['result']['countries'][index]['name'], str)
            assert isinstance(response['result']['countries'][index]['block'], bool)
            assert isinstance(response['result']['countries'][index]['allowRegistration'], bool)
            assert isinstance(response['result']['countries'][index]['allowDeposit'], bool)
            assert isinstance(response['result']['countries'][index]['prefix'], str)

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
