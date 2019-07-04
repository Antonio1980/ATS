import time
import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signup_page import SignUpPage

test_case = "6308"


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='UI Elements Verification of the "Enter Code" Screen')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/add_phone_tests/C6308_enter_code_screen_ui_test.py",
                 "TestUIEnterCodeScreen")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN UP - ADD PHONE")
@allure.description("""
    UI Functional test.
    Verify elements at the AddPhone page.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.add_phone_page
@pytest.mark.smoke
@ddt
class TestUIEnterCodeScreen(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with: test_enter_code_screen_ui")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_enter_code_screen_ui(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_enter_code_screen_ui,with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed.")
            self.assertTrue(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form failed.")
            url = Instruments.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url, "MAilGun issue (URL returned as None.)")
            self.assertTrue(self.signup_page.go_by_token_url(self.driver, url), "go_by_token_url failed.")
            time.sleep(2.0)
            self.assertTrue(self.signup_page.add_phone(self.driver, self.customer.phone), "add_phone failed.")
            text = "Please enter the 6 digit code we just  sent to your number"
            attribute = self.browser.execute_js(self.driver, self.signup_page.script_text_on_enter_phone_code)
            self.assertEqual(text, attribute, "text didn't match the given attribute.")
            self.assertIsNotNone(self.browser.search_element(self.driver, self.locators.CODE_FIELD, delay),
                                 "CODE_FIELD not found")
            self.assertIsNotNone(self.browser.search_element(self.driver, self.locators.RESEND_LINK, delay),
                                 "RESEND_LINK not found")
            self.assertIsNotNone(self.browser.search_element(self.driver, self.locators.ANOTHER_PHONE_LINK, delay),
                                 "ANOTHER_PHONE_LINK not found")
            self.assertIsNotNone(self.browser.search_element(self.driver, self.locators.SUBMIT_BUTTON, delay),
                                 "SUBMIT_BUTTON not found")
            self.assertIsNotNone(self.browser.search_element(self.driver, self.locators.GO_BACK_LINK_E, delay),
                                 "GO_BACK_LINK_E not found")
            result = 1
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
