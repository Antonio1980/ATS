import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Exchange And Customer Data")
@allure.story("Client able to receive his current account details.")
@allure.title("CUSTOMER DATA")
@allure.description("""
    Functional api test.
    Coverage:
    trade_service, exchange_and_customer_data, public_api
    1 test_customer_data
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Update Credit Card Status')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/trade_service_tests/customer_data_test.py", "TestCustomerData")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.public_api
@pytest.mark.regression
@pytest.mark.trade_service
@pytest.mark.exchange_and_customer_data
class TestCustomerData(object):

    @allure.step("Starting: test_customer_data")
    @automation_logger(logger)
    def test_customer_data(self, r_customer):
        response = r_customer.postman.trade_service.customer_data()
        assert response['error'] is None
        assert response['result']['customer']

        assert response['result']['customer']['id'] == str(r_customer.customer_id)
        assert response['result']['customer']['email'] == r_customer.email
        assert response['result']['customer']['birthday'] == r_customer.birthday_timestamp # Crashes always, incorrect value.
        assert response['result']['customer']['firstName'] == r_customer.first_name # Crashes from time to time.

        assert response['result']['customer']['lastName'] == r_customer.last_name
        assert response['result']['customer']['gender'] == r_customer.gender
        assert response['result']['customer']['country'] == r_customer.country_code

        if r_customer.state_code:
            assert response['result']['customer']['state'] == r_customer.state_code

        assert response['result']['customer']['city'] == r_customer.city
        assert response['result']['customer']['street'] == r_customer.street

        assert response['result']['customer']['phone'] == r_customer.phone  #Crashes
