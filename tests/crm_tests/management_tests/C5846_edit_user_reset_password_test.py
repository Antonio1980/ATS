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
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.crm_tests_base.create_user_page import CreateUserPage
from tests.crm_tests_base.users_management_page import UsersManagementPage
from tests.crm_tests_base.locators import create_user_page_locators, users_management_page_locators

test_case = '5846'


@ddt
@pytest.mark.crm_sanity
class TestEditUserResetPassword(unittest.TestCase):
    @allure.step("SetUp: sitting up test details.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.customer = Customer()
        self.create_user_page = CreateUserPage()
        self.locators2 = create_user_page_locators
        self.locators = users_management_page_locators
        self.user_management_page = UsersManagementPage()
        self.customer.insert_new_crm_user_sql()

    @allure.step("Starting with: test_edit_user_reset_password")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_edit_user_reset_password(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(
                self.login_page.login(self.driver, self.customer.username, self.customer.password), "login has failed")

            self.assertTrue(self.home_page.go_to_management_inset_with_users_option(self.driver),
                            "go_to_management_inset_with_users_option has failed")

            search_field = Browser.find_element(self.driver, self.locators.SEARCH_FIELD)
            Browser.click_on_element(search_field)
            Browser.send_keys(search_field, self.customer.username)
            Browser.send_enter_key(search_field)
            user = Browser.find_element(self.driver, self.locators.USER)
            Browser.click_on_element(user)
            reset_button = Browser.find_element_by(self.driver, self.locators2.RESET_PASSWORD_BUTTON_ID, "id")
            Browser.click_on_element(reset_button)

            self.assertTrue(self.home_page.logout(self.driver), "logout has failed")
            parsed_html = Instruments.get_mail_gun_item(self.customer, crm=True)
            new_password = parsed_html.find_all('span')[0].text
            self.assertTrue(self.login_page.login(self.driver, self.customer.username, new_password),
                            "new login has failed")
            self.assertTrue(self.login_page.set_new_password(self.driver, new_password, self.customer.password),
                            "new set_new_password has failed")
            self.assertTrue(self.home_page.logout(self.driver), "new logout has failed)")
            self.assertTrue(self.login_page.login(self.driver, self.customer.username, self.customer.password),
                            "new login has failed")
            logger.logger.info(
                F"CRM User created successful: Email: {self.customer.email} Password: {self.customer.password} "
                F"Username: {self.customer.username}")
            Instruments.save_into_file(self.customer.email + "," + self.customer.password + "," + self.customer.username
                                       + "\n", self.customer.crm_users_file)
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
