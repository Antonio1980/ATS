import time
import allure
import pytest
import unittest
from src.base import logger
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "7686"


@allure.feature('Authorization')
@allure.story('Client able to create customer account into Web Trading Platform.')
@allure.title("END TO END")
@allure.description("""
    Functional end to end test.
    Registration using only ACL API methods (without opening browser.
    At the end the customer account will be approved via CRM (HTTP component).
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='SignUp- Full flow')
@allure.testcase(BaseConfig.GITLAB_URL + "/end2end_tests/sign_up_and_approvment_via_api_test.py",
                 "Customer Registration via API and after it approvment via CRM.")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.e2e
@pytest.mark.authorization
class TestRegistrationViaAPI(unittest.TestCase):

    @allure.step("SetUp: sitting up customer.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()

    @allure.step("Starting with registration: test_registration_via_api")
    @automation_logger(logger)
    def test_registration_via_api(self):
        result = 0
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_registration_via_api")
        try:
            step1_response = self.customer.postman.authorization_service.sign_up_step_1(self.customer)
            assert step1_response['error'] is None and step1_response['result']['errors'] is None
            self.customer.customer_id = step1_response['result']['customerId']
            self.customer.auth_token = step1_response['result']['token']
            self.customer.get_postman_access(self.customer.auth_token)

            Utils.get_mail_gun_item(self.customer)
            step2_response = self.customer.postman.authorization_service.verify_email_step_2(self.customer.email,
                                                                                    self.customer.ver_token)
            assert step2_response['error'] is None and step2_response['result']['errors'] is None
            time_phone = time.perf_counter() + float(BaseConfig.PHONE_DELAY)
            step3_response = self.customer.postman.authorization_service.add_phone_step_3(self.customer)
            while step3_response['error'] is not None or step3_response['result'][
                'errors'] is not None and time_phone > time.time():
                step3_response = self.customer.postman.authorization_service.add_phone_step_3(self.customer)
            step4_response = self.customer.postman.authorization_service.verify_phone_step_4()
            assert step4_response['error'] is None and step4_response['result']['errors'] is None
            # 1- country_code, 2- city, 3- zip_, 4- phone, 5- state_code
            step5_response = self.customer.postman.authorization_service.update_personal_details_step_5(self.customer)
            assert step5_response['error'] is None and step5_response['result']['errors'] is None
            step6 = self.customer.postman.authorization_service.client_checklist_step6()
            assert step6['error'] is None and step6['result']['errors'] is None
            link1 = self.customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
            time.sleep(1.0)
            link2 = self.customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_JPG)['link']
            time.sleep(1.0)
            link3 = self.customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
            step7_response = self.customer.postman.authorization_service.upload_documents_step_7(link1, link2, link3)
            assert step7_response['error'] is None and step7_response['result']['errors'] is None
            step8_response = self.customer.postman.authorization_service.login_by_credentials(self.customer.email,
                                                                                     self.customer.password)
            assert step8_response['error'] is None and step8_response['result']['token'] is not None
            self.customer.auth_token = step8_response['result']['token']
            crm_response = self.customer.postman.crm.approve_customer(self.customer.customer_id)
            logger.logger.info("CRM responded with: {0}".format(crm_response))
            assert crm_response['status'] == "success"
            result = 1
            logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
            logger.logger.info("Customer successfully created.")
            logger.logger.info("{0}, {1}, {2}".format(self.customer.email, self.customer.password,
                                                      self.customer.customer_id))
            Utils.save_into_file(self.customer.email + "," + self.customer.password + "," +
                                 str(self.customer.customer_id) + "\n", self.customer.customers_file)
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)
