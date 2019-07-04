import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.crm_tests_base import login_page_url
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.crm_tests_base.locators import login_page_locators

test_case = '3437'


@ddt
@pytest.mark.crm_smoke
class TestForgotPasswordPopUp(unittest.TestCase):
    @allure.step("Preconditions")
    @automation_logger(logger)
    def setUp(self):
        self.login_page = LogInPage()
        self.locators = login_page_locators

    @allure.step("")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_forgot_password_popup(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        header = "Forgot your password?"
        result = 0
        delay = float(BaseConfig.CRM_DELAY)
        try:
            self.login_page.go_to_url(self.driver, self.login_page.crm_base_url)
            assert Browser.wait_url_contains(self.driver, login_page_url, delay)
            assert Browser.wait_element_visible(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
            Browser.click_on_element_by_locator(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
            popup = Browser.wait_element_presented(self.driver, self.locators.POPUP_FORGOT_PASSWORD, delay)
            message = Browser.wait_element_presented(self.driver, self.locators.POPUP_MESSAGE, delay)
            send = Browser.find_element_by(self.driver, self.locators.POPUP_SEND_BUTTON_ID, "id")
            note = Browser.wait_element_presented(self.driver, self.locators.POPUP_NOTE_MESSAGE, delay)
            close = Browser.wait_element_presented(self.driver, self.locators.POPUP_CLOSE_BUTTON, delay)
            popup_html = Browser.get_element_span_html(popup)
            pop_up_html = Instruments.parse_html(popup_html)
            assert header == pop_up_html.find('div').parent('h4')[0].text
            assert message
            assert send
            assert note
            assert close
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
