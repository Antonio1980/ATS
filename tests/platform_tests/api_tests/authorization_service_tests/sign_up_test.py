import time
import pytest
import allure
from src.base import logger
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "6037"


@pytest.mark.incremental
@allure.feature("Authorization")
@allure.story("Client able to create customer account into Web Trading Platform.")
@allure.title("API REGISTRATION.")
@allure.description("""
    Functional end to end test.
    Registration using only ACL API methods (without opening browser).
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='SignUp')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/sign_up_test.py", "TestSignUp")
@pytest.mark.usefixtures("r_time_count", "customer")
@pytest.mark.e2e
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestSignUp(object):
    link1, link2, link3 = None, None, None

    @allure.step("Starting with registration: sign_up_step_1")
    @automation_logger(logger)
    def test_step_1(self, customer):
        step1 = customer.postman.authorization_service.sign_up_step_1(customer)
        assert step1['error'] is None and step1['result']['errors'] is None
        customer.customer_id = step1['result']['customerId']
        assert customer.customer_id
        customer.auth_token = step1['result']['token']
        customer.get_postman_access(customer.auth_token)

    @allure.step("Proceed with registration: verify_email_step_2")
    @automation_logger(logger)
    def test_step2(self, customer):
        Utils.get_mail_gun_item(customer)
        step2 = customer.postman.authorization_service.verify_email_step_2(customer.email, customer.ver_token)
        assert step2['error'] is None and step2['result']['errors'] is None

    @allure.step("Proceed with registration: add_phone_step_3")
    @automation_logger(logger)
    def test_step3(self, customer):
        logger.logger.info("Customer phone adding... {0}".format(customer.full_phone))
        time_phone = time.perf_counter() + float(BaseConfig.PHONE_DELAY)
        step3 = customer.postman.authorization_service.add_phone_step_3(customer)
        while step3['error'] is not None or step3['result']['errors'] is not None and time_phone > time.time():
            step3 = customer.postman.authorization_service.add_phone_step_3(customer)

    @allure.step("Proceed with registration: verify_phone_step_4")
    @automation_logger(logger)
    def test_step4(self, customer):
        logger.logger.info("Customer phone verified. {0}".format(customer.full_phone))
        step4 = customer.postman.authorization_service.verify_phone_step_4()
        assert step4['error'] is None and step4['result']['errors'] is None

    @allure.step("Proceed with registration: update_personal_details_step_5")
    @automation_logger(logger)
    def test_step5(self, customer):
        step5 = customer.postman.authorization_service.update_personal_details_step_5(customer)
        assert step5['error'] is None and step5['result']['errors'] is None

    @allure.step("Proceed with registration: answer_question_step_6_1 and answer_question_step_6_2")
    @automation_logger(logger)
    def test_step6(self, customer):
        step6 = customer.postman.authorization_service.client_checklist_step6()
        assert step6['error'] is None and step6['result']['errors'] is None

    @allure.step("FileService: uploading files -> upload_file")
    @automation_logger(logger)
    def test_upload_files(self, customer):
        TestSignUp.link1 = customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
        time.sleep(2.0)
        TestSignUp.link2 = customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_JPG)['link']
        time.sleep(2.0)
        TestSignUp.link3 = customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']

    @allure.step("Proceed with registration: upload_documents_step_7")
    @automation_logger(logger)
    def test_step7(self, customer):
        logger.logger.info("FileService returned file links: {0}, {1}, {2}".format(TestSignUp.link1, TestSignUp.link2,
                                                                                   TestSignUp.link3))
        step7 = customer.postman.authorization_service.upload_documents_step_7(TestSignUp.link1, TestSignUp.link2,
                                                                               TestSignUp.link3)
        assert step7['error'] is None and step7['result']['errors'] is None
        logger.logger.info("==================== TEST CASE {0} PASSED ====================".format(test_case))
        logger.logger.info("{0}, {1}, {2}".format(customer.email, customer.password, customer.customer_id))
        Utils.save_into_file(customer.email + "," + customer.password + "," + str(customer.customer_id) + "\n",
                             BaseConfig.WTP_TESTS_CUSTOMERS)
