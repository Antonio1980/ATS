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
from tests.crm_tests_base.locators import create_user_page_locators, users_management_page_locators

test_case = '5845'


@ddt
@pytest.mark.crm_smoke
class TestEditNewUserUI(unittest.TestCase):
    @allure.step("SetUp: sitting up test details.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.locators2 = create_user_page_locators
        self.locators = users_management_page_locators
        crm_users_file = self.login_page.crm_users_file
        self.username = crm_users_file[0][2]
        self.email = crm_users_file[0][0]

    @allure.step("Starting with: test_ui_edit_new_user")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_ui_edit_new_user(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(
                self.login_page.login(
                    self.driver, self.login_page.crm_username, self.login_page.crm_password), "login has failed")
            self.assertTrue(self.home_page.go_to_management_inset_with_users_option(self.driver),
                            "go_to_management_inset_with_users_option has failed")
            search_field = Browser.find_element(self.driver, self.locators.SEARCH_FIELD)
            Browser.click_on_element(search_field)
            Browser.send_keys(search_field, self.username)
            Browser.send_enter_key(search_field)
            user = Browser.find_element(self.driver, self.locators.USER)
            Browser.click_on_element(user)
            first_name_field = Browser.find_element_by(self.driver, self.locators2.FIRST_NAME_ID, "id")
            Browser.clear_field(first_name_field)
            Browser.send_keys(first_name_field, "QAtestQA")
            last_name_field = Browser.find_element_by(self.driver, self.locators2.LAST_NAME_ID, "id")
            Browser.clear_field(last_name_field)
            Browser.send_keys(last_name_field, "__QA__TEST__QA__")
            email_field = Browser.find_element_by(self.driver, self.locators2.EMAIL_ID, "id")
            Browser.clear_field(email_field)
            Browser.send_keys(email_field, self.email)
            phone_field = Browser.find_element_by(self.driver, self.locators2.PHONE_ID, "id")
            Browser.clear_field(phone_field)
            Browser.send_keys(phone_field, self.login_page.phone)
            username_field = Browser.find_element_by(self.driver, self.locators2.USERNAME_ID, "id")
            Browser.clear_field(username_field)
            Browser.send_keys(username_field, self.username)
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
