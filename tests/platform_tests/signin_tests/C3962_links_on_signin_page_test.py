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
from tests.platform_tests_base.signin_page import SignInPage

test_case = '3962'


@allure.feature('Sign In')
@allure.story('Registered customer able to log in to Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Links Verification at Sign-In Screen')
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C3962_links_on_signin_page_test.py", "TestLinksOnSignInPage")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN IN")
@allure.description("""
    Functional test.
    Verify links on Sign In page: 
    Option 1- forgot password, Option 2- register link.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_in_page
@pytest.mark.smoke
@ddt
class TestLinksOnSignInPage(unittest.TestCase):
    @allure.step("SetUp: calling Customer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_links_on_sign_in_page")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_links_on_sign_in_page(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_links_on_sign_in_page, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed.")
            # Option 1- forgot password, Option 2- register link
            self.assertTrue(self.signin_page.click_on_link(self.driver, 1), "forgot password link failed.")
            self.browser.go_back(self.driver)
            self.assertTrue(self.signin_page.click_on_link(self.driver, 2), "register link failed.")
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)