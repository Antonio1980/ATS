import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = ""


@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, "Get Api Token")
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/api_service_tests/get_api_token_test.py",
                 "TestGetTokenAPI")
@pytest.mark.usefixtures("r_time_count", "customer_app")
@pytest.mark.regression
@pytest.mark.api_service
class TestGetTokenAPI(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_r_customer(self):
        r_customer = RegisteredCustomer()
        return r_customer

    @automation_logger(logger)
    def test_get_existing_api_token(self, customer_app):
        response = customer_app.postman.api_service.get_api_tokens()
        assert response['error'] is None
        assert response["result"]["apiToken"]
        assert response["result"]["apiToken"][0]["token"]

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))

    @automation_logger(logger)
    def test_get_api_token_method_works(self, another_r_customer):
        response = another_r_customer.postman.api_service.get_api_tokens()
        assert response['error'] is None

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))
