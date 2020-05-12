import time
import allure
import pytest
import unittest
from src.base import logger
from src.base.enums import Browsers
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory

test_case = '3440'


@pytest.mark.crm_e2e
class TestForgotPasswordFullFlow(unittest.TestCase):
    @allure.step("SetUp: sitting up test details.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.customer.insert_new_crm_user_sql()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_login_with_new_password")
    @automation_logger(logger)
    def test_forgot_password_full_flow(self):
        result = 0
        try:
            self.assertTrue(self.login_page.forgot_password(self.driver, self.customer.email), "forgot_password failed")
            parsed_html = Instruments.get_mail_gun_item(self.customer, crm=True)
            password_url = str(parsed_html.find('a').contents[0])
            url_response = Instruments.get_true_url(password_url)
            assert password_url.split(':')[1] == url_response.split(':')[1]
            time.sleep(5.0)
            parsed_html2 = Instruments.get_mail_gun_item(self.customer, crm=True)
            new_password = parsed_html2.find('strong').text
            self.assertTrue(self.login_page.login(self.driver, self.customer.username, new_password), "login has failed")
            self.assertTrue(self.login_page.set_new_password(self.driver, new_password, self.customer.password),
                            "login has failed")
            self.assertTrue(self.home_page.logout(self.driver), "logout has failed")
            self.assertTrue(self.login_page.login(self.driver, self.customer.username, self.customer.password),
                            "login has failed")
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
