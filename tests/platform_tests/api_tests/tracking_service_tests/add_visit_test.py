import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Tracker")
@allure.title("TRACKING VISIT")
@allure.description("""
    Sanity API test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Add Visit')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/tracking_service_tests/add_visit_test.py", "TestAddVisit")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.tracking_service
class TestAddVisit(object):

    @allure.step("Starting: test_add_visit_public_method_works")
    @automation_logger(logger)
    def test_add_visit_public_method_works(self, customer):
        response = customer.postman.tracking_service.add_visit()
        assert response['error'] is None

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Starting: test_add_visit_method_works")
    @automation_logger(logger)
    def test_add_visit_method_works(self, r_customer):
        response = r_customer.postman.tracking_service.add_visit()
        assert response['error'] is None

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
