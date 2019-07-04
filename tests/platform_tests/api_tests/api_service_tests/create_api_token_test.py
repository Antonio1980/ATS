import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = ""


@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, "Create Api Token")
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/api_service_tests/create_api_token_test.py",
                 "TestCreateTokenAPI")
@pytest.mark.usefixtures("r_time_count", "r_customer_sql")
@pytest.mark.regression
@pytest.mark.api_service
class TestCreateTokenAPI(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        customer = Customer()
        return customer

    @automation_logger(logger)
    def test_create_api_token(self, r_customer_sql):
        response = r_customer_sql.postman.api_service.create_api_token(r_customer_sql.username)
        assert response['error'] is None

        api_token = response['result']['token']
        assert len(api_token) > 0

        secret = response['result']['secret']
        assert len(secret) > 0
        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))

    @automation_logger(logger)
    def test_create_api_token_negative(self, another_customer):
        response = another_customer.postman.api_service.create_api_token(another_customer.username)
        assert response['error'] is not None
        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))
        
