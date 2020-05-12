import time
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

test_case = '6005'


@allure.feature('Sign In')
@allure.story('Registered customer able to log in to Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name="User Isn't Signed In By Default (Negative)")
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C6005_default_signin_test.py", "TestDefaultSignIn")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TRADING SANITY TEST 'TS- 1'")
@allure.description("""
    Negative test.
    Verify that user can't be redirected to Sign In page by default (from Home page).
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_in_page
@pytest.mark.negative
@pytest.mark.smoke
@ddt
class TestDefaultSignIn(unittest.TestCase):
    @allure.step("SetUp: calling Customer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_sign_in_default")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_sign_in_default(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_in_default, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed.")
            time.sleep(2.0)
            self.assertFalse(self.browser.execute_js(self.driver, self.customer.scripts.script_is_signed),
                             "Customer signed in (NEGATIVE) failed.")
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
