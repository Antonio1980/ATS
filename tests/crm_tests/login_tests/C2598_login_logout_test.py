import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory

test_case = '2598'


@ddt
@pytest.mark.crm_smoke
class TestLogInLogOutLogIn(unittest.TestCase):
    @allure.step("SetUp: sitting up test details.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.username = self.login_page.crm_username
        self.password = self.login_page.crm_password

    @allure.step("Starting with: test_login_logout_login")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_login_logout_login(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(self.login_page.login(self.driver, self.username, self.password), "login has failed.")
            self.assertTrue(self.home_page.logout(self.driver), "logout has failed.")
            self.assertTrue(self.login_page.login(self.driver, self.username, self.password), "login has failed.")
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)

