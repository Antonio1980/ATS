import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Files")
@allure.title("FILES")
@allure.description("""
    Sanity API test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Upload Files')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/file_service_tests/currency_converter_test.py", "TestUploadFiles")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.regression
@pytest.mark.file_service
@pytest.mark.timeout(60)
class TestUploadFiles(object):

    @allure.step("Starting: test_upload_files_method_works")
    @automation_logger(logger)
    def test_upload_files_method_works(self, customer):
        response = customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)
        assert response['link']
        
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

    @allure.step("Starting: test_upload_files_negative")
    @automation_logger(logger)
    def test_upload_files_negative(self, customer):
        response = customer.postman.file_service.upload_file(BaseConfig.WTP_TESTS_CUSTOMERS)
        assert response['error']
        assert response['error'] == 'Unsupported format ,file format should be gif, jpg, jpeg, tif, tiff, pdf, png'
        
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")

