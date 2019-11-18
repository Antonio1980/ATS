import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from tests.me_tests_base.home_page import HomePage
from src.base.log_decorator import automation_logger
from tests.me_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@ddt
@pytest.mark.smoke
@pytest.mark.sign_in_page
class TestLogIn(unittest.TestCase):
    @allure.step("SetUp: calling RegisteredCustomer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.login_page = LogInPage()
        self.home_page = HomePage()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_sign_in")
    @data(*Utils.get_csv_data(BaseConfig.ME_LOGIN_DATA))
    @unpack
    @automation_logger(logger)
    def test_login(self, username, password):
        delay = 1
        self.login_page.login(self.driver, delay, username, password)
        self.home_page.logout(self.driver, delay)
        self.login_page.login(self.driver, delay, username, password)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.login_page.close_browser(self.driver)
