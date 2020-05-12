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
from tests.platform_tests_base import wtp_signin_page_url
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.signup_page import SignUpPage
from tests.platform_tests_base.forgot_password_page import ForgotPasswordPage

test_case = '3669'


@allure.feature('Forgot Password')
@allure.story('Client able to change his password via Trading Platform.')
@allure.title("FORGOT PASSWORD")
@allure.description("""
    Functional test.
    Verify that customer received requested email with token. 
    """)
@allure.severity(allure.severity_level.MINOR)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Forgot Password - Reset Password Email')
@allure.testcase(BaseConfig.GITLAB_URL + "/forgot_password_tests/C3669_reset_password_email_test.py", "TestWrongEmail")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.smoke
@pytest.mark.forgot_password_page
@ddt
class TestResetPasswordEmail(unittest.TestCase):
    @allure.step("SetUp: sitting up customer details (email, password, phone etc.) and pages")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.forgot_password_page = ForgotPasswordPage()
        self.locators = self.forgot_password_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with: test_reset_password_email")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_reset_password_email(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_reset_password_email, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page")
            self.assertTrue(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form failed.")
            self.assertTrue(self.signin_page.go_by_token_url(self.driver, wtp_signin_page_url), "go_by_token_url failed.")
            # Option 1- forgot password, Option 2- register link
            self.assertTrue(self.signin_page.click_on_link(self.driver, 1), "click_on_link forgot failed.")
            self.assertTrue(self.forgot_password_page.fill_email_address_form(self.driver, self.customer.email),
                            "fill_email_address_form failed.")
            verification_url = Instruments.get_mail_gun_item(self.customer, forgot=True)
            self.browser.go_to_url(self.driver, verification_url)
            self.assertIsNotNone(self.browser.search_element(self.driver, self.locators.CONFIRM_BUTTON, delay),
                                 "CONFIRM_BUTTON not found.")

            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
