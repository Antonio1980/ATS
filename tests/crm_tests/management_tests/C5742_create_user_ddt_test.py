import allure
import pytest
import unittest
from src.base import logger
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.crm_tests_base.create_user_page import CreateUserPage
from tests.crm_tests_base.users_management_page import UsersManagementPage

test_case = '5742'


@pytest.mark.skip
@pytest.mark.crm_smoke
@pytest.mark.crm_negative
@ddt
class TestCreateNewUserDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = []

    @automation_logger(logger)
    @allure.step("SetUp: sitting up test details.")
    def setUp(self):
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.create_user_page = CreateUserPage()
        self.user_management_page = UsersManagementPage()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_create_new_user_ddt")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(Instruments.write_file_preconditions(2, "@sandbox7e64c317900647609c225574db67437b.mailgun.org")))
    @unpack
    def test_create_new_user_ddt(self, first_last_name, phone, email, username, language, permissions, status, user_type):
        customer = Customer(None, email, "1Aa@<>12", "00000")
        result = 0
        user_details = {
            'first_last_name': first_last_name,
            'phone': phone,
            'username': username,
            'language': language,
            'permissions': permissions,
            'status': status,
            'user_type': user_type
        }
        try:
            self.assertTrue(self.login_page.login(
                self.driver, self.login_page.crm_username, self.login_page.crm_password), "login has failed")
            self.assertTrue(self.home_page.go_to_management_inset_with_users_option(self.driver),
                            "go_to_management_inset_with_users_option has failed")
            self.assertTrue(self.user_management_page.click_on_create_new_user(self.driver),
                            "click_on_create_new_user has failed")
            self.assertTrue(self.create_user_page.fill_user_details(self.driver, email, user_details),
                            "fill_user_details has failed")
            self.assertTrue(self.home_page.logout(self.driver), "logout has failed")
            parsed_html = Instruments.get_mail_gun_item(customer, crm=True)
            new_password = parsed_html.find_all('span')[0].text
            self.assertTrue(self.login_page.login(self.driver, username, new_password), "login failed")
            self.assertTrue(self.login_page.set_new_password(self.driver, new_password, customer.password),
                            "set_new_password failed")
            self.assertTrue(self.home_page.logout(self.driver), "logout failed")
            self.assertTrue(self.login_page.login(self.driver, username, customer.password), "last login failed")
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
