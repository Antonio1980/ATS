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
from tests.platform_tests_base import wtp_open_account_url
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signup_page import SignUpPage
from selenium.webdriver.remote.webelement import WebElement

test_case = '3963'


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='UI Elements Verification of "Email Verification" Screen')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/C3963_email_verification_screen_test.py", "TestEmailVerificationScreen")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN UP")
@allure.description("""
    UI Functional test.
    Verify elements of the "email verification" screen.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_up_page
@pytest.mark.smoke
@ddt
class TestEmailVerificationScreen(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with: test_email_verification_screen")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_email_verification_screen(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_email_verification_screen, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page")
            self.assertTrue(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form failed.")
            self.assertTrue(self.browser.wait_url_contains(self.driver, wtp_open_account_url, delay),
                            "wtp_open_account_url not found.")
            self.assertIsInstance(self.browser.wait_element_presented(self.driver, self.locators.EMAIL_NOT_ARRIVED,
                                                                      delay), WebElement, "EMAIL_NOT_ARRIVED not found")
            self.assertIsInstance(self.browser.wait_element_presented(
                self.driver, self.locators.EMAIL_ALREADY_VERIFIED, delay), WebElement, "EMAIL_ALREADY_VERIFIED failed.")
            self.assertIsInstance(self.browser.wait_element_presented(self.driver, self.locators.GO_BACK_LINK, delay),
                                  WebElement, "GO_BACK_LINK not found.")
            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
