import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.main_screen_page import MainScreenPage

test_case = '6214'


@allure.title("Upper Ruler")
@allure.description("""
    UI test.
    Upper Ruler (In Logged in Mode), UI
    1. Open WTP
    2. Verify that the Upper Ruler exists at the up line of Trading Platform.
    3. Verify that the Upper Ruler have the following parts (left to right):
        Hamburger - no functionality at the moment 
        Logo
        Fund button - clicking the button will redirect to Funds 
        User Account Indicator (displays user full name with matching local time and date)
        Language flag
        Portfolio
    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Upper Ruler (In Logged in Mode) UI')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/main_screen_tests/upper_ruler_tests/C6214_upper_ruler_in_logged_mode_test.py",
    "TestUpperRulerFunctional")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.upper_ruler
@ddt
class TestUpperRulerInLoggedMode(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.email = self.customer.email
        self.main_screen_page = MainScreenPage()
        self.locators = self.main_screen_page.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_upper_ruler_in_logged_mode")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_upper_ruler_in_logged_mode(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = self.home_page.ui_delay
        result = 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            assert self.browser.wait_element_presented(self.driver, self.locators.LOGO, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.FUNDS_BUTTON, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.TIME_ON_UPPER_RULER, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.DATE_ON_UPPER_RULER, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.LANGUAGE_FLAG, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.CURRENT_PORTFOLIO, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.LOGOUT_BUTTON, delay)
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        Browser.close_browser(self.driver)
