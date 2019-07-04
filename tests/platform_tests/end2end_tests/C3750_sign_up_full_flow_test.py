import allure
import pytest
import unittest
from src.base import logger
from src.base.enums import Browsers
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.signup_page import SignUpPage

test_case = '3750'


@allure.feature('Authorization')
@allure.story('Client able to create customer account into Web Trading Platform.')
@allure.title("END TO END")
@allure.description("""
    Functional end to end test.
    Registration via browser (can be executed on Chrome, Firefox, IE Edge etc.).
    At the end the customer account will be verified by log in to Web Platform.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name="Full Registration Flow - Positive - the last steps need to update waiting for spec")
@allure.testcase(BaseConfig.GITLAB_URL + "/end2end_tests/C3750_sign_up_full_flow_test.py",  "TestSignUpFullFlow")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.sign_up_page
@pytest.mark.authorization
class TestSignUpFullFlow(unittest.TestCase):
    @allure.step("SetUp: sitting up customer details (email, password, phone etc.)")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.signin_page = SignInPage()
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with registration: test_sign_up_full_flow")
    @automation_logger(logger)
    def test_sign_up_full_flow(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_up_full_flow with: browser- {0} ".format(self.driver.name))
        result = 0
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed")
            self.assertTrue(self.signup_page.fill_signup_form(self.driver, self.customer.username, self.customer.email,
                                                              self.customer.password, self.element), "fill_signup_form "
                                                                                                     "failed")
            self.customer.customer_id = self.browser.execute_js(self.driver, self.customer.scripts.script_customer_id)
            self.assertTrue(self.customer.customer_id, "customer_id not received")
            url = Utils.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url)
            self.assertTrue(self.signup_page.go_by_token_url(self.driver, url), "go_by_token_url failed")
            self.assertTrue(self.signup_page.add_phone(self.driver, self.customer.phone), "add_phone failed")
            self.assertTrue(self.signup_page.enter_phone_code(self.driver, "123456"), "enter_phone_code failed")
            self.assertTrue(self.signup_page.fill_personal_details(self.driver, self.customer.birthday, self.customer.zip_,
                                                                   self.customer.city), "fill_personal_details failed")
            self.assertTrue(self.signup_page.fill_client_checklist_1(self.driver, self.customer.scripts.checklist),
                                                                     "fill_client_checklist_1 failed")
            self.assertTrue(self.signup_page.fill_client_checklist_2(self.driver), "fill documents failed")
            self.assertTrue(self.signup_page.finish_registration(self.driver), "finish_registration failed")
            self.assertTrue(self.home_page.sign_out(self.driver), "sign_out failed")
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed")
            self.assertTrue(self.signin_page.sign_in(self.driver, self.customer.email, self.customer.password), "sign_in"
                                                                                                                " failed")

            logger.logger.info("============= TEST CASE - {0} IS PASSED !!! =============".format(test_case))
            logger.logger.info("{0}, {1}, {2}".format(self.customer.email, self.customer.password,
                                                      self.customer.customer_id))
            Instruments.save_into_file(self.customer.email + "," + self.customer.password + "," +
                                       str(self.customer.customer_id) + "\n", self.customer.customers_file)
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
