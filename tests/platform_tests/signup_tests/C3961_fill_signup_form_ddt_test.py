import allure
import pytest
import unittest
from src.base import logger
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signup_page import SignUpPage

test_case = '3961'


@pytest.mark.skip
@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sign Up UI - Check all possible non valid combinations for username/password (Negative)')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/C3961_fill_signup_form_ddt_test.py", "TestFillSignUpFormDD")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN UP")
@allure.description("""
    Negative test.
    Verify negative pairs of email/password types/formats/prefixes.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_up_page
@pytest.mark.negative
@ddt
class TestFillSignUpFormDD(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_fill_sign_up_form_ddt")
    @data(*Instruments.get_csv_data(BaseConfig.OPEN_ACCOUNT_DATA))
    @unpack
    @automation_logger(logger)
    def test_fill_sign_up_form_ddt(self, first_last_name, email, password):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_fill_sign_up_form_ddt, with: first_last_name- {0}, email- {1}, password- {2} "
                           .format(first_last_name, email, password))
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(email)
        result = 0
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed.")
            self.assertFalse(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form NEGATIVE failed.")
            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
