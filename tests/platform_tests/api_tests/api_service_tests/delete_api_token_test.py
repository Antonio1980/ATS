import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, "Delete Api Token")
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/api_service_tests/delete_api_token_test.py",
                 "TestDeleteTokenAPI")
@pytest.mark.usefixtures("r_time_count", "customer_app")
@pytest.mark.regression
@pytest.mark.api_service
class TestDeleteTokenAPI(object):

    @automation_logger(logger)
    def test_delete_api_token(self, customer_app):
        response = customer_app.postman.api_service.delete_api_token(customer_app.api_token_id)
        assert response['error'] is None

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))

    @automation_logger(logger)
    def test_delete_api_token_negative(self, customer_app):
        response = customer_app.postman.api_service.delete_api_token(789567)
        assert response['error'] is not None

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))
