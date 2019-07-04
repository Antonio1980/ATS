import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = "6036"


@allure.feature("Authorization")
@allure.story("Client able to provide documents and to get mandatory KYC files.")
@allure.title("QUESTIONNAIRE.")
@allure.description("""
    Functional tests.
    1. test_get_needed_files 
    2. test_get_needed_files_negative
    3. test_get_questionnaire
    4. test_get_questionnaire_negative
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='GetQuestionnaire')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/questionnaire_and_files_test.py",
                 "TestQuestionnaire")
@pytest.mark.usefixtures("customer", "r_time_count")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestQuestionnaire(object):

    @pytest.fixture()
    @automation_logger(logger)
    def r_customer_(self):
        return RegisteredCustomer()

    @allure.step("Starting with: test_get_needed_files")
    @automation_logger(logger)
    def test_get_needed_files(self, r_customer_):
        response = r_customer_.postman.authorization_service.get_needed_files()
        assert response['error'] is None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_get_needed_files_negative")
    @automation_logger(logger)
    def test_get_needed_files_negative(self, customer):
        response = customer.postman.authorization_service.get_needed_files()
        assert response['error'] is None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_get_questionnaire")
    @automation_logger(logger)
    def test_get_questionnaire(self, r_customer_):
        response = r_customer_.postman.authorization_service.get_questionnaire()
        assert response['error'] is None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Starting with: test_get_questionnaire_negative")
    @automation_logger(logger)
    def test_get_questionnaire_negative(self, customer):
        response = customer.postman.authorization_service.get_questionnaire()
        assert response['error'] is None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))

    @allure.step("Comes to verify the information that is provided on documents that customer is required to upload")
    @automation_logger(logger)
    def test_get_files(self, r_customer):
        """
        This test comes to verify, that the date provided by Auth. service
        regarding the documents that are to be uploaded is valid.
        :param r_customer: any registered customer
        """
        response = r_customer.postman.authorization_service.get_needed_files()

        assert response['error'] is None

        logger.logger.info('Verifying the Personal ID document requirements')
        assert isinstance(response['result']['docs'][0]['regulationDocsTypeId'], int)
        assert isinstance(response['result']['docs'][0]['regulationDocsTypeName'], str)
        assert isinstance(response['result']['docs'][0]['regulationDocsPageTypes'], list)
        assert response['result']['docs'][0]['regulationDocsPageTypes'] != []
        assert isinstance(response['result']['docs'][0]['regulationDocsPageTypes'][0]['required'], bool)
        assert isinstance(response['result']['docs'][0]['regulationDocsPageTypes'][1]['required'], bool)

        logger.logger.info('Verifying the Proof of residence document requirements')
        assert isinstance(response['result']['docs'][1]['regulationDocsTypeId'], int)
        assert isinstance(response['result']['docs'][1]['regulationDocsTypeName'], str)
        assert isinstance(response['result']['docs'][1]['regulationDocsPageTypes'], list)
        assert response['result']['docs'][1]['regulationDocsPageTypes'] != 0
        assert isinstance(response['result']['docs'][1]['regulationDocsPageTypes'][0]['required'], bool)

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
