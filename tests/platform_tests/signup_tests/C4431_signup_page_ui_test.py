import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base import wtp_open_account_url
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signup_page import SignUpPage

test_case = '4431'


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='UI Elements Verification Sign Up Screen')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/C4431_signup_page_ui_test.py", "TestUISignUpPage")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN UP")
@allure.description("""
    UI Functional test.
    Verify elements at the Sign Up page.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_up_page
@pytest.mark.smoke
@ddt
class TestUISignUpPage(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_links_on_verify_email_screen")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_sign_up_page_ui(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_up_page_ui, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed.")
            self.assertIsNotNone(self.browser.wait_url_contains(self.driver, wtp_open_account_url, delay),
                                 "wtp_open_account_url not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.FIRST_NAME_FIELD, delay),
                                 "FIRST_NAME_FIELD not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.LAST_NAME_FIELD, delay),
                                 "LAST_NAME_FIELD not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.EMAIL_FIELD, delay),
                                 "EMAIL_FIELD not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.PASSWORD_FIELD, delay),
                                 "PASSWORD_FIELD not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.CAPTCHA_FRAME, delay),
                                 "CAPTCHA_FRAME not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.NEWSLETTERS_CHECKBOX,
                                                                     delay), "NEWSLETTERS_CHECKBOX not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.CERTIFY_CHECKBOX, delay),
                                 "CERTIFY_CHECKBOX not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.TERM_OF_USE_LINK, delay),
                                 "TERM_OF_USE_LINK not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.PRIVACY_POLICY_LINK,
                                                                     delay), "PRIVACY_POLICY_LINK not found")
            self.assertIsNotNone(self.browser.wait_element_presented(self.driver, self.locators.SIGNIN_LINK, delay),
                                 "SIGNIN_LINK not found")
            self.assertIsNotNone(self.browser.wait_element_clickable(self.driver, self.locators.CREATE_ACCOUNT_BUTTON,
                                                                     delay), "CREATE_ACCOUNT_BUTTON not found")
            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
