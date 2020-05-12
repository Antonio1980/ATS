# Import dependencies
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

test_case = '3983'


# Allure reports annotations.
@allure.feature('Sign In')
@allure.story('Registered customer able to log in to Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sign-In Form Functionality Positive')
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C3983_signin_test.py", "TestSignIn")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN IN")
@allure.description("""
    Functional test.
    Verify that registered customer able to sign in to Web Platform.
    """)
@pytest.mark.usefixtures("r_time_count")
# Data Driven injection.
@ddt
# Tests ordering - per test suites.
@pytest.mark.smoke
@pytest.mark.sign_in_page
# LogInTest class declaration.
# Inheritance from unittest framework class.
class TestSignIn(unittest.TestCase):
    # SetUp function definition (executes before test).
    @allure.step("SetUp: calling RegisteredCustomer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        # Composition technique:
        # Local instance of the RegisteredCustomer class.
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.browser = self.customer.get_browser_functionality()

    # Allure step will be written in report.
    @allure.step("Starting with: test_sign_in")
    # Data from csv file injection (browser names).
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    # Unpacking data from csv file and passing it to test method.
    @unpack
    # Calling logger.
    @automation_logger(logger)
    # Test method, name must start with "test..."
    def test_sign_in(self, browser):
        # Saving test case info into automation log file.
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_in, with: browser- {0} ".format(browser))
        # Set up browser via WebDriverFactory class.
        self.driver = WebDriverFactory.get_driver(browser)
        # Test result be default is zero (False), if test passed will be overwritten to one and sent to TestRail.
        result = 0
        try:
            # Calling open_signin_page method from HomePage class,
            # If sign_in passed successfully it will return True
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed.")
            # Calling sign_in method from SignInPage class,
            # If sign_in passed successfully it will return True.
            self.assertTrue(self.signin_page.sign_in(
                self.driver, self.customer.email, self.customer.password), "sign_in failed.")
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            # If asserts are passed, result is True.
            result = 1
        finally:
            # Update test rail report with actual result.
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    # CleanUp method executes after test.
    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
