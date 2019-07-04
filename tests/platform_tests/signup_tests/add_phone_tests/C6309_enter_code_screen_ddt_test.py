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

test_case = "6309"


@pytest.mark.skip
@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Enter Code" Screen - Fields Validation')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/add_phone_tests/C6309_enter_code_screen_ddt_test.py",
                 "TestEnterCodeScreenDDT")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN UP - ADD PHONE")
@allure.description("""
    Negative test.
    Verify negative not valid iterations with broken phone code.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.add_phone_page
@pytest.mark.negative
@ddt
class TestEnterCodeScreenDDT(unittest.TestCase):
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

    @data(*Instruments.get_csv_data(BaseConfig.PHONE_CODES))
    @unpack
    @automation_logger(logger)
    def test_enter_code_screen_ddt(self, code):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_enter_code_screen_ddt, with: code- {0} ".format(code))
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
            submit_button = self.browser.wait_element_clickable(self.driver, self.locators.SUBMIT_BUTTON, delay)
            self.browser.click_on_element(submit_button)
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.FIELD_ERROR, delay),
                            "FIELD_ERROR not presented.")
            self.assertFalse(self.signup_page.enter_phone_code(self.driver, code),
                             "enter_phone_code NEGATIVE failed.")
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)

