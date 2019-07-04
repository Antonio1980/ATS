import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory

test_case = '2694'


@pytest.mark.skip
@ddt
@pytest.mark.crm_smoke
@pytest.mark.crm_negative
class TestForgotPasswordDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = []

    @allure.step("Preconditions")
    @automation_logger(logger)
    def setUp(self):
        self.login_page = LogInPage()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Verify possible negative variations for client email.")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.FORGOT_PASSWORD_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        result = 0
        try:
            self.assertFalse(self.login_page.forgot_password(self.driver, email),
                             "forgot_password must failed (negative)")
            result = 1
        finally:
            self.results.append(result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)

    @classmethod
    @automation_logger(logger)
    @allure.step("Checking results of ddt test.")
    def tearDownClass(cls):
        logger.logger.info(F"Test Results are: {cls.results}")
        if 0 in cls.results:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, 0)
        else:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, 1)
