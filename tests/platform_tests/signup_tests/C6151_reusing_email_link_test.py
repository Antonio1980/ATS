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

test_case = '6151'


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Reusing of email verification link')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/C6151_reusing_email_link_test.py", "TestReusingEmailLink")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN UP")
@allure.description("""
    Negative test.
    Verify that reusing of the JWT token is not available.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.sign_up_page
@ddt
class TestReusingEmailLink(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.customer.customer_registration()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with: test_reusing_email_link")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_reusing_email_link(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_reusing_email_link, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            url = Instruments.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url, "MAilGun issue (URL returned as None.)")
            self.assertTrue(self.signup_page.go_by_token_url(self.driver, url), "go_by_token_url failed.")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.TOKEN_ERROR, delay),
                            "TOKEN_ERROR is not presented.")
            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
