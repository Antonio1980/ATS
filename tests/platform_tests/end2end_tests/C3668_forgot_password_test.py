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
from tests.platform_tests_base.forgot_password_page import ForgotPasswordPage
from tests.platform_tests_base import wtp_signin_page_url, wtp_open_account_url

test_case = '3668'


@allure.feature('Forgot Password')
@allure.story('Client able to request to change his password and after to log in with it.')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("END TO END")
@allure.description("""
    Check if 'Forgot Password' functionality works (can be executed on Chrome, Firefox, IE Edge etc.).
    Pure functional, positive end to end test.
    1. SignUp step1 - creates customer account with status "new".
    2. ForgotPassword step1- reset password and send ver_token.
    3. Check Guerrilla and get ver token. 
    3. ForgotPassword step2- confirmation with ver_token.
    At the end the customer account will be verified by log in to Web Platform with new password.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/end2end_tests/C3668_forgot_password_test.py", "TestForgotPasswordFullFlow")
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name="Full Flow Forgot Password Functionality")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.authorization
@pytest.mark.forgot_password_page
class TestForgotPassword(unittest.TestCase):
    @allure.step("SetUp: sitting up customer and page objects.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.signup_page = SignUpPage()
        self.forgot_password_page = ForgotPasswordPage()
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with test: test_forgot_password")
    @automation_logger(logger)
    def test_forgot_password(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_forgot_password with: browser- {0} ".format(self.driver.name))
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed")
            self.assertTrue(self.signup_page.fill_signup_form(self.driver, self.customer.username, self.customer.email,
                                                      self.customer.password, self.element), "fill_signup_form failed")
            url = Utils.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url)
            self.customer.auth_token = self.driver.get_cookie('dx_jwt')['value']
            self.customer.get_postman_access(self.customer.auth_token)
            step2_response = self.customer.postman.authorization_service.verify_email_step_2(self.customer.email,
                                                                                    self.customer.ver_token)
            self.assertIsNone(step2_response['error'] and step2_response['result']['errors'], "verify_email_step_2 failed")
            self.assertTrue(self.signin_page.go_by_token_url(self.driver, wtp_signin_page_url), "go_by_token_url")
            # Option 1- forgot password, Option 2- register link
            self.assertTrue(self.signin_page.click_on_link(self.driver, 1), "click_on_link on 1- forgot failed")
            self.assertTrue(self.forgot_password_page.fill_email_address_form(self.driver, self.customer.email),
                            "fill_email_address_form failed")
            url = Utils.get_mail_gun_item(self.customer, forgot=True)
            self.assertTrue(self.forgot_password_page.go_by_token_url(self.driver, url), "go_by_token_url failed")
            self.assertTrue(self.forgot_password_page.set_new_password(self.driver, self.customer.password, url),
                            "set_new_password failed")
            self.assertTrue(self.home_page.open_home_page(self.driver), "open_home_page failed")
            self.assertTrue(self.home_page.sign_out(self.driver), "sign_out failed")
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed.")
            self.assertFalse(self.signin_page.sign_in(
                self.driver, self.customer.email, self.customer.password), "sign_in failed.")
            self.assertTrue(self.browser.wait_url_contains(self.driver, wtp_open_account_url, delay))
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
