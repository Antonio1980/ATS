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
from tests.platform_tests_base import wtp_dashboard_url, wtp_home_page_url, wtp_signin_page_url

test_case = '6121'


@allure.feature('Sign In')
@allure.story('Registered customer able to log in to Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name="Cookie Expiration")
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C6121_cookie_expiration_test.py", "TestCookieExpiration")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN IN")
@allure.description("""
    Functional test.
    Verify that JWT (auth_token) token is valid and saved after closing browser.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_in_page
@pytest.mark.smoke
@ddt
class TestCookieExpiration(unittest.TestCase):

    @allure.step("SetUp: calling Customer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.locators = self.signin_page.locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_expiration_cookie")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_expiration_cookie(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_expiration_cookie, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed.")

            assert self.browser.wait_url_contains(self.driver, wtp_signin_page_url, delay)
            username_field = self.browser.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
            self.browser.click_on_element(username_field)
            self.browser.send_keys(username_field, self.customer.email)
            password_field_true = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD_TRUE)
            password_field = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD)
            self.browser.click_on_element(password_field)
            self.browser.click_on_element(password_field_true)
            self.browser.send_keys(password_field_true, self.customer.password)
            self.browser.execute_js(self.driver, self.customer.scripts.script_signin)
            self.browser.execute_js(self.driver, self.customer.script_test_token)
            login_button = self.browser.wait_element_clickable(self.driver, self.locators.SIGNIN_BUTTON, delay)
            self.browser.click_on_element(login_button)

            self.assertTrue(self.browser.wait_url_contains(self.driver, wtp_dashboard_url, delay),
                            "wtp_dashboard_url not found.")

            cookie_jwt = self.driver.get_cookie('dx_jwt')
            cookie_cid = self.driver.get_cookie('dx_cid')
            self.browser.close_driver(self.driver)
            self.driver = WebDriverFactory.get_driver(browser)
            self.home_page.open_home_page(self.driver)
            self.driver.add_cookie(cookie_jwt)
            self.driver.add_cookie(cookie_cid)
            self.browser.refresh_browser(self.driver)
            time.sleep(2.0)

            self.assertTrue(self.browser.wait_url_contains(self.driver, wtp_home_page_url, delay),
                            "wtp_home_page_url not found.")
            self.assertTrue(self.browser.execute_js(self.driver, self.customer.scripts.script_is_signed),
                            "Customer isn't Signed In. FAILED!")

            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
