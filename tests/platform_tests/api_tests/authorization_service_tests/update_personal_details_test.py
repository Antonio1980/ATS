import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "6041"


@allure.feature("Authorization")
@allure.story("Client able to update his customer details via API.")
@allure.title("UPDATE PERSONAL DETAILS.")
@allure.description("""
    Functional tests.
    1. test_update_personal_details - positive test.
    2. test_update_personal_details_negative- negative test.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='UpdatePersonalDetails')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/update_personal_details_test.py",
                 "TestUpdatePersonalDetails")
@pytest.mark.usefixtures("r_customer", "r_time_count")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestUpdatePersonalDetails(object):

    @pytest.fixture
    @automation_logger(logger)
    def customer_(self):
        return Customer()

    @allure.step("Starting with: test_update_personal_details")
    @automation_logger(logger)
    def test_update_personal_details(self, r_customer):
        customer_data_response_before = r_customer.postman.trade_service.customer_data()
        logger.logger.info(F"Customer details before update {customer_data_response_before}")
        
        r_customer.first_name, r_customer.last_name  = r_customer.last_name, r_customer.first_name

        response = r_customer.postman.authorization_service.update_personal_details(r_customer)
        assert response['error'] is None

        customer_data_response = r_customer.postman.trade_service.customer_data()
        logger.logger.info(F"Customer details after update {customer_data_response}")
        
        assert customer_data_response['result']['customer']['firstName'] == r_customer.last_name, "Knownen issue."
        assert customer_data_response['result']['customer']['lastName'] == r_customer.first_name

        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_update_personal_details_negative")
    @pytest.mark.usefixtures("customer")
    @automation_logger(logger)
    def test_update_personal_details_negative(self, customer):
        response = customer.postman.authorization_service.update_personal_details(customer)
        assert response['error'] is not None
        logger.logger.info("==================== TEST CASE {0}  PASSED ====================".format(test_case))
