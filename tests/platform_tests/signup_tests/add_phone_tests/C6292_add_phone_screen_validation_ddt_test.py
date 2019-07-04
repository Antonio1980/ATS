import time
import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signup_page import SignUpPage

test_case = "6292"


@pytest.mark.skip
@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Add Phone Number" Fields Validation')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/add_phone_tests/C6292_add_phone_screen_validation_ddt_test.py",
                 "TestAddPhoneValidationDDT")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN UP - ADD PHONE")
@allure.description("""
    Negative test.
    Verify negative variations of not valid phone types/formats/prefixes.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.add_phone_page
@pytest.mark.negative
@ddt
class TestAddPhoneValidationDDT(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with: test_add_phone_validation_ddt")
    @data(*Instruments.get_csv_data(BaseConfig.PHONES))
    @unpack
    @automation_logger(logger)
    def test_add_phone_validation_ddt(self, phone):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_add_phone_validation_ddt, with: phone- {0} ".format(phone))
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed.")
            self.assertTrue(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form failed.")
            url = Instruments.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url, "MAilGun issue (URL returned as None.)")
            self.assertTrue(self.signup_page.go_by_token_url(self.driver, url), "go_by_token_url failed")
            time.sleep(2.0)
            send_button = self.browser.find_element(self.driver, self.locators.SEND_BUTTON)
            self.browser.click_on_element(send_button)
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.FIELD_ERROR, delay),
                            "FIELD_ERROR not found.")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.PHONE_FIELD_DISABLED,
                                                                delay), "PHONE_FIELD_DISABLED not found.")
            country_dropdown = self.browser.find_element(self.driver, self.locators.SELECT_COUNTRY_DROPDOWN)
            self.browser.click_on_element(country_dropdown)
            self.browser.type_text_by_locator(self.driver, self.locators.SELECT_COUNTRY_FIELD, 'isra')
            phone_field = self.browser.find_element(self.driver, self.locators.PHONE_FIELD)
            self.browser.send_keys(phone_field, '')
            send_button = self.browser.find_element(self.driver, self.locators.SEND_BUTTON)
            self.browser.click_on_element(send_button)
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.FIELD_ERROR, delay),
                            "FIELD_ERROR not found.")
            self.browser.refresh_browser(self.driver)
            self.assertFalse(self.signup_page.add_phone(self.driver, phone), "add_phone failed.")
            result = 1
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
