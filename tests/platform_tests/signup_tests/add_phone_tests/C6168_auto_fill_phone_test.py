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

test_case = '6168'


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Add Phone Number" - Auto-fill Country Code By Selected Country')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/add_phone_tests/C6168_auto_fill_phone_test.py", "TestAutoFillPhone")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN UP - ADD PHONE")
@allure.description("""
    Functional test.
    Verify that if user filled country field then phone prefix set accordingly.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.add_phone_page
@pytest.mark.smoke
@ddt
class TestAutoFillPhone(unittest.TestCase):
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

    @allure.step("Starting with: test_auto_fill_phone")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_auto_fill_phone(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_auto_fill_phone, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed.")
            self.assertTrue(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form failed.")
            url = Instruments.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url, "MAilGun issue (URL returned as None.)")
            self.assertTrue(self.signup_page.go_by_token_url(self.driver, url), "go_by_token_url failed.")
            time.sleep(2.0)
            country_dropdown = self.browser.find_element(self.driver, self.locators.SELECT_COUNTRY_DROPDOWN)
            self.browser.click_on_element(country_dropdown)
            self.browser.type_text_by_locator(self.driver, self.locators.SELECT_COUNTRY_FIELD, "Australia")
            text = self.browser.execute_js(self.driver, '''return $("input[name='phonePrefix']").val();''')
            self.assertEqual(text, "+61", "text returned not matched to expected.")
            result = 1
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
