import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory

test_case = '2591'


@ddt
@pytest.mark.crm_smoke
class TestForgotPassword(unittest.TestCase):
    @allure.step("Preconditions")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.login_page = LogInPage()
        self.customer.insert_new_crm_user_sql()

    @allure.step("Starting with: test_forgot_password")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_forgot_password(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(self.login_page.forgot_password(self.driver, self.customer.email),
                            "forgot_password has failed")
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
