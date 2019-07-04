# Import dependencies
import allure
import pytest
import unittest
from src.base import logger
from src.base.enums import Browsers
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory

test_case = '2590'


# LogInTest class declaration.
# Inheritance from unittest framework class.
@pytest.mark.crm_smoke
class TestLogIn(unittest.TestCase):
    @allure.step("Preconditions")
    @automation_logger(logger)
    # SetUp function definition (executes before test).
    def setUp(self):
        # Local instance of the LogInPage class.
        self.login_page = LogInPage()
        # Set up browser via WebDriverFactory class.
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_login_positive")
    @automation_logger(logger)
    # Test method, name must start with "test..."
    def test_login_positive(self):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_login_positive started")
        # Test step result before execution (by default).
        result = 0
        try:
            # Calling login method from LogInPage class,
            # If sign_in passed successfully it will return True.
            self.assertTrue(self.login_page.login(self.driver, self.login_page.crm_username,
                                                  self.login_page.crm_password), "login failed.")
            result = 1
        finally:
            # Update test rail report.
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    # CleanUp method executes after test.
    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        # Calling clean up method from Browser class.
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
