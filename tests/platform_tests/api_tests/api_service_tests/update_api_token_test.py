import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, "Update Api Token")
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/api_service_tests/update_api_token_test.py",
                 "TestUpdateTokenAPI")
@pytest.mark.usefixtures("r_time_count", "customer_app")
@pytest.mark.regression
@pytest.mark.api_service
class TestUpdateTokenAPI(object):

    @automation_logger(logger)
    def test_update_existing_api_token(self, customer_app):
        update_response = customer_app.postman.api_service.update_api_token(customer_app.api_token_id, customer_app.api_key)
        logger.logger.info("update_api_token", update_response)
        assert update_response['error'] is None

        logger.logger.info("============ TEST CASE {0} PASSED ===========".format(test_case))
