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
from tests.crm_tests_base.locators import create_user_page_locators
from tests.crm_tests_base.create_user_page import CreateUserPage
from tests.crm_tests_base.users_management_page import UsersManagementPage

test_case = '5844'


@ddt
@pytest.mark.crm_smoke
class TestCreateNewUserUI(unittest.TestCase):
    @allure.step("SetUp: sitting up test details.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.locators = create_user_page_locators
        self.message = CreateUserPage.password_message
        self.user_management_page = UsersManagementPage()

    @allure.step("Starting with: test_ui_create_new_user")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_ui_create_new_user(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.CRM_DELAY)
        try:
            self.assertTrue(self.login_page.login(
                self.driver, self.login_page.crm_username, self.login_page.crm_password), "login has failed")
            self.assertTrue(self.home_page.go_to_management_inset_with_users_option(self.driver),
                            "go_to_management_inset_with_users_option has failed")
            self.assertTrue(self.user_management_page.click_on_create_new_user(self.driver),
                            "click_on_create_new_user has failed")
            assert Browser.find_element(self.driver, self.locators.PAGE_TITLE_1)
            assert Browser.find_element(self.driver, self.locators.PAGE_TITLE_2)
            assert Browser.find_element_by(self.driver, self.locators.FIRST_NAME_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.LAST_NAME_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.EMAIL_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.PHONE_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.USERNAME_ID, "id")
            password_message = Browser.find_element(self.driver, self.locators.PASSWORD_MESSAGE)
            assert self.message == password_message.text
            Browser.find_element(self.driver, self.locators.LANGUAGE_DROPDOWN)
            Browser.find_element(self.driver, self.locators.PERMISSION_GROUP_DROPDOWN)
            Browser.find_element(self.driver, self.locators.STATUS_DROPDOWN)
            Browser.choose_option_from_dropdown(self.driver, self.locators.USER_TYPE_DROPDOWN,
                                                self.locators.USER_TYPE_FIELD, "regular")
            Browser.find_element(self.driver, self.locators.DESKS_DROPDOWN)
            create_user_button = Browser.search_element(self.driver, self.locators.CREATE_USER_BUTTON, delay)
            Browser.click_with_wait_and_offset(self.driver, create_user_button, 5, 5)
            Browser.wait_element_presented(self.driver, self.locators.FIRST_NAME_ERROR, delay)
            Browser.wait_element_presented(self.driver, self.locators.LAST_NAME_ERROR, delay)
            Browser.wait_element_presented(self.driver, self.locators.EMAIL_ERROR, delay)
            Browser.wait_element_presented(self.driver, self.locators.PHONE_ERROR, delay)
            Browser.wait_element_presented(self.driver, self.locators.USERNAME_ERROR, delay)
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
