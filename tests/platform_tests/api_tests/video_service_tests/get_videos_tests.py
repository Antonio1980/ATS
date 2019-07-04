import pytest
import allure
from src.base import logger
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = ""


@allure.feature("Media")
@allure.title("VIDEO")
@allure.description("""
    Sanity API test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Get Videos')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/video_service_tests/get_videos_test.py", "TestGetVideos")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.video_service
class TestGetVideos(object):

    @allure.step("Starting: test_get_video_public_method_works")
    @automation_logger(logger)
    def test_get_video_public_method_works(self, customer):
        response = customer.postman.video_service.get_videos()
        assert response['error'] is None

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Starting: test_get_video_method_works")
    @automation_logger(logger)
    def test_get_video_method_works(self, r_customer):
        response = r_customer.postman.video_service.get_videos()
        assert response['error'] is None

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
