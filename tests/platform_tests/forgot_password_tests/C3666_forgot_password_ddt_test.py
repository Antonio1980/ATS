import allure
import pytest
import unittest
from src.base import logger
from ddt import unpack, data, ddt
from src.base.enums import Browsers
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.forgot_password_page import ForgotPasswordPage

test_case = '3666'


@pytest.mark.skip
@allure.feature('Forgot Password')
@allure.story('Client able to change his password via Trading Platform.')
@allure.title("FORGOT PASSWORD")
@allure.description("""
    Negative test.
    Verify negative combinations of customer password.
    """)
@allure.severity(allure.severity_level.MINOR)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Forgot Password Input Field Validation')
@allure.testcase(BaseConfig.WTP_BASE_URL, "TestForgotPasswordDDT")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.negative
@pytest.mark.forgot_password_page
@ddt
class TestForgotPasswordDDT(unittest.TestCase):
    @allure.step("SetUp: sitting up customer details (email, password, phone etc.) and pages")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.forgot_password_page = ForgotPasswordPage()
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_forgot_password_ddt")
    @data(*Instruments.get_csv_data(BaseConfig.FORGOT_PASSWORD_DATA))
    @unpack
    @automation_logger(logger)
    def test_forgot_password_ddt(self, email):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_forgot_password_ddt, with: email- {0} ".format(email))
        result = 0
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page has failed")
            # Option 1- forgot password, Option 2- register link
            self.assertTrue(self.signin_page.click_on_link(self.driver, 1), "click_on_link has failed")
            self.assertFalse(self.forgot_password_page.fill_email_address_form(self.driver, email),
                             "fill_email_address_form has failed")
            
            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
