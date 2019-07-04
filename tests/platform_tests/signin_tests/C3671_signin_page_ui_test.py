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

test_case = '3671'


@allure.feature('Sign In')
@allure.story('Registered customer able to log in to Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Sign-In Screen UI test')
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C3671_signin_page_ui_test.py", "TestUISignInPage")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN IN")
@allure.description("""
    UI Functional test.
    Verify that elements on Sign In page are presented and loaded.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_in_page
@pytest.mark.smoke
@ddt
class TestUISignInPage(unittest.TestCase):
    @allure.step("SetUp: calling Customer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signin_page.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_sign_in_page_ui")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_sign_in_page_ui(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_in_page_ui with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed")
            assert self.browser.wait_url_contains(self.driver, wtp_signin_page_url, delay)
            assert self.browser.search_element(self.driver, self.locators.SIGNIN_TITLE, delay)
            assert self.browser.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
            assert self.browser.search_element(self.driver, self.locators.PASSWORD_FIELD, delay)
            assert self.browser.search_element(self.driver, self.locators.CAPTCHA_FRAME, delay)
            assert self.browser.search_element(self.driver, self.locators.SIGNIN_BUTTON, delay)
            assert self.browser.search_element(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
            assert self.browser.search_element(self.driver, self.locators.REGISTER_LINK, delay)
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
