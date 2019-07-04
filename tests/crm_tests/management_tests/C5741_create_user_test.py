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

test_case = '5741'


@ddt
@pytest.mark.crm_sanity
class TestCreateNewUser(unittest.TestCase):
    @allure.step("SetUp: sitting up test details.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.phone = self.customer.full_phone
        self.new_email = self.customer.email
        self.new_username = self.customer.username
        self.create_user_page = CreateUserPage()
        self.user_management_page = UsersManagementPage()
        self.first_last_name = self.customer.user_first_last_name

    @allure.step("Starting with: test_create_new_user")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_create_new_user(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        user_details = {
            'first_last_name': self.first_last_name,
            'phone': self.phone,
            'username': self.new_username,
            'language': "eng",
            'permissions': "sup",
            'status': "act",
            'user_type': "Admin"
        }
        try:
            self.assertTrue(self.login_page.login(self.driver, self.login_page.crm_username,
                                                  self.login_page.crm_password), "login failed")

            self.assertTrue(self.home_page.go_to_management_inset_with_users_option(self.driver),
                            "go_to_management_inset_with_users_option failed")

            self.assertTrue(self.user_management_page.click_on_create_new_user(self.driver),
                            "click_on_create_new_user failed")

            self.assertTrue(self.create_user_page.fill_user_details(self.driver, self.new_email, user_details),
                            "fill_user_details failed")

            self.assertTrue(self.home_page.logout(self.driver), "logout failed")
            
            parsed_html = Instruments.get_mail_gun_item(self.customer, crm=True)
            new_password = parsed_html.find_all('span')[0].text

            self.assertTrue(self.login_page.login(self.driver, self.new_username, new_password), "login failed")

            self.assertTrue(self.login_page.set_new_password(self.driver, new_password, self.customer.password),
                            "set_new_password failed")

            self.assertTrue(self.home_page.logout(self.driver), "logout failed")

            self.assertTrue(self.login_page.login(self.driver, self.new_username, self.customer.password),
                            "last login failed")
            logger.logger.info(
                F"CRM User created successful: Email: {self.new_email} Password: {self.customer.password} "
                F"Username: {self.customer.username}")
            Instruments.save_into_file(self.new_email + "," + self.customer.password + "," + self.new_username + "\n",
                                       self.customer.crm_users_file)
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
