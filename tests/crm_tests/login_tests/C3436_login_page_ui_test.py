import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base import login_page_url
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.crm_tests_base.locators import login_page_locators

test_case = '3436'


@ddt
@pytest.mark.crm_smoke
class TestLogInUI(unittest.TestCase):
    @allure.step("SetUp: sitting up test details.")
    @automation_logger(logger)
    def setUp(self):
        self.login_page = LogInPage()
        self.locators = login_page_locators

    @allure.step("Starting with: test_ui_login_page")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_ui_login_page(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.CRM_DELAY)
        try:
            Browser.go_to_url(self.driver, self.login_page.crm_base_url)
            assert Browser.wait_url_contains(self.driver, login_page_url, delay)
            assert Browser.wait_element_visible(self.driver, self.login_page.base_locators.CRM_LOGO, delay)
            assert Browser.find_element_by(self.driver, self.locators.USERNAME_FIELD_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.PASSWORD_FIELD_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.LOGIN_BUTTON_ID, "id")
            username_field_ps = int(self.driver.execute_script("return window.$(\'input[id=\"username\"]\').position()")
                                    .get('left'))
            password_field_ps = int(self.driver.execute_script("return window.$(\'input[id=\"password\"]\').position()")
                                    .get('left'))
            login_button_pos = int(self.driver.execute_script("return window.$(\'button[id=\"loginBtn\"]\').position()")
                                   .get('left'))
            self.assertTrue(username_field_ps == 20 and password_field_ps == 20, "")
            self.assertTrue(login_button_pos == 215, "")
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
