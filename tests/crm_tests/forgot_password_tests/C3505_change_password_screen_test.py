import time
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
from tests.crm_tests_base import new_password_url

test_case = '3505'


@ddt
@pytest.mark.crm_smoke
class TestChangePasswordScreen(unittest.TestCase):
    @allure.step("Preconditions")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.customer.insert_new_crm_user_sql()
        self.locators = self.login_page.locators

    @allure.step("test_change_password_screen")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_change_password_screen(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.CRM_DELAY)
        try:
            self.assertTrue(self.login_page.forgot_password(self.driver, self.customer.email),
                            "forgot_password has failed.")
            parsed_html = Instruments.get_mail_gun_item(self.customer, crm=True)
            password_url = str(parsed_html.find('a').contents[0])
            url_response = Instruments.get_true_url(password_url)
            assert password_url.split(':')[1] == url_response.split(':')[1]
            time.sleep(5.0)
            parsed_html2 = Instruments.get_mail_gun_item(self.customer, crm=True)
            new_password = parsed_html2.find('strong').text
            self.assertTrue(self.login_page.login(self.driver, self.customer.username, new_password),
                            "login has failed")
            assert Browser.wait_url_contains(self.driver, new_password_url, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.CURRENT_PASSWORD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.NEW_PASSWORD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.CONFIRM_PASSWORD, delay)
            assert Browser.wait_element_clickable(self.driver, self.locators.CONFIRM_BUTTON, delay)
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        Browser.close_browser(self.driver)
