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
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signup_page import SignUpPage
from selenium.common.exceptions import InvalidElementStateException

test_case = '6198'


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Add Phone Number" - Change Country Code Manually - Negative')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/add_phone_tests/C6198_auto_fill_phone_negative_test.py",
                 "TestAutoFillPhoneNegative")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN UP - ADD PHONE")
@allure.description("""
    Negative test.
    Verify that user can't type another phone prefix if country already chosen.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.add_phone_page
@pytest.mark.smoke
@ddt
class TestAutoFillPhoneNegative(unittest.TestCase):

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

    @allure.step("Starting with: test_negative_auto_fill_phone")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_negative_auto_fill_phone(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_negative_auto_fill_phone, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed")
            self.assertTrue(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form failed.")
            url = Instruments.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url, "MAilGun issue (URL returned as None.)")
            self.assertTrue(self.signup_page.go_by_token_url(self.driver, url), "go_by_token_url failed")
            time.sleep(2.0)
            country_dropdown = self.browser.find_element(self.driver, self.locators.SELECT_COUNTRY_DROPDOWN)
            self.browser.click_on_element(country_dropdown)
            self.browser.type_text_by_locator(self.driver, self.locators.SELECT_COUNTRY_FIELD, "Australia")
            text = self.browser.execute_js(self.driver, '''return $("input[name='phonePrefix']").val();''')
            self.assertEqual(text, "+61", "")
            prefix_phone = self.browser.find_element(self.driver, self.locators.PHONE_PREFIX)
            # self.assertRaises(InvalidElementStateException, prefix_phone.send_keys("+63"))
            try:
                prefix_phone.send_keys("+63")
            except InvalidElementStateException:
                result = 1
                logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
