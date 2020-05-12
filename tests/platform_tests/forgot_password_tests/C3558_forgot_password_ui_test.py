import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.forgot_password_page import ForgotPasswordPage

test_case = '3558'


@allure.feature('Forgot Password')
@allure.story('Client able to change his password via Trading Platform.')
@allure.title("FORGOT PASSWORD")
@allure.description("""
    UI Functional test.
    Verify that web elements presented at the ForgotPassword page.
    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Forgot Password Screen UI')
@allure.testcase(BaseConfig.GITLAB_URL + "/forgot_password_tests/C3558_forgot_password_ui_test.py",
                 "TestForgotPasswordUI")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.smoke
@pytest.mark.forgot_password_page
@ddt
class TestForgotPasswordUI(unittest.TestCase):
    @allure.step("SetUp: sitting up customer details (email, password, phone etc.) and pages")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.forgot_password_page = ForgotPasswordPage()
        self.locators = self.forgot_password_page.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_forgot_password_page_ui")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_forgot_password_page_ui(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_forgot_password_page_ui, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed.")
            # Option 1- forgot password, Option 2- register link
            self.assertTrue(self.signin_page.click_on_link(self.driver, 1), "click_on_link forgot failed.")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.FORGOT_PASSWORD_TITLE,
                                                                     delay), "FORGOT_PASSWORD_TITLE not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.EMAIL_TEXT_FIELD, delay),
                                                                     "EMAIL_TEXT_FIELD not found.")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.SUBMIT_BUTTON, delay),
                                                                    "SUBMIT_BUTTON not found.")

            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
