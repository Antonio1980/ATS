import time
import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '3984'


@allure.feature('Sign In')
@allure.story('Registered customer able to log in to Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sign-In with Not Completed Captcha - Negative')
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C3984_signin_without_captcha_test.py", "TestSignInWithoutCaptcha")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN IN")
@allure.description("""
    Negative test.
    Verify that customer can't sign in without checked captcha and captcha error displayed.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_in_page
@pytest.mark.negative
@pytest.mark.smoke
@ddt
class TestSignInWithoutCaptcha(unittest.TestCase):
    @allure.step("SetUp: calling RegisteredCustomer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signin_page.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_sign_in_without_captcha")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_sign_in_without_captcha(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_in_without_captcha, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed.")
            username_field = self.browser.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
            self.browser.click_on_element(username_field)
            self.browser.send_keys(username_field, self.customer.email)
            password_true_field = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD_TRUE)
            password_field = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD)
            self.browser.click_on_element(password_field)
            self.browser.send_keys(password_true_field, self.customer.password)
            self.browser.execute_js(self.driver, self.customer.scripts.script_signin)
            login_button = self.browser.find_element(self.driver, self.locators.SIGNIN_BUTTON)
            self.browser.click_on_element(login_button)
            assert self.browser.search_element(self.driver, self.locators.CAPTCHA_ERROR, delay)
            time.sleep(5.0)
            captcha_error_text = self.browser.execute_js(
                self.driver, '''return $("[class='errorMessage hidden'] span[class='errorText']").text();''')
            logger.logger.info(f"captcha_error_text: {captcha_error_text}")
            self.assertNotEqual(captcha_error_text, "", "Failed- no error message is appeared.")
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
