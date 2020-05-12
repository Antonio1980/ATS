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

test_case = '5926'


@allure.title("Upper Ruler")
@allure.description("""
    UI test.
    Upper Ruler Functionality, UI
    1. Open WTP
    2. Click button "Sign Up"..
    3. Log On to the Web Platform and verify that upon the Sign In and Sign Up buttons are replaces
     with the first name of the user and a small arrow next to the name .
    4. Click on the first name of the user button. 
    5. Verify that the Upper Ruler exists in all screen as used for main navigation functionality, 
    navigate to other screen and see that Upper Ruler still exists at the up of the Screen of Trading Platform.
    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Upper Ruler Functionality')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/upper_ruler_tests/C5926_upper_ruler_functionality_test.py",
                 "TestUpperRulerFunctional")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.upper_ruler
@ddt
class TestUpperRulerFunctional(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.main_screen_page = MainScreenPage()
        self.locators = self.main_screen_page.locators
        self.email = self.customer.email
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_upper_ruler_functional")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_upper_ruler_functional(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = self.home_page.ui_delay
        result = 0
        try:
            self.home_page.open_home_page(self.driver)
            sign_up_button = self.browser.wait_element_presented(self.driver, self.locators.SIGH_UP_BUTTON, delay)
            self.browser.try_click(self.driver, sign_up_button, 2.0)
            assert self.browser.find_element(self.driver, self.locators.REGISTRATION_FORM)
            self.browser.go_back(self.driver)
            sign_in_button = self.browser.wait_element_presented(self.driver, self.locators.SIGH_IN_BUTTON, delay)
            self.browser.try_click(self.driver, sign_in_button, 2.0)
            assert self.sign_in_page.sign_in(self.driver, self.email, self.password)
            self.browser.execute_js(self.driver, self.main_screen_page.script_signin_button)
            self.browser.execute_js(self.driver, self.main_screen_page.script_signup_button)
            assert self.browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
            user_name_on_upper_ruler_small_arrow = self.browser.find_element(self.driver,
                                                                             self.locators.USER_NAME_ON_UPPER_RULER)
            self.browser.try_click(self.driver, user_name_on_upper_ruler_small_arrow, 2.0)
            assert self.browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
            assert self.browser.wait_element_presented(self.driver, self.locators.USER_PROFILE_PANEL, delay)
            funds_button = self.browser.find_element(self.driver, self.locators.FUNDS_BUTTON)
            self.browser.try_click(self.driver, funds_button, 2.0)
            assert self.browser.find_element_by(self.driver, self.locators.FUNDS_PANEL_ID, "id")
            self.browser.try_click(self.driver, funds_button, 2.0)
            self.browser.execute_js(self.driver, self.main_screen_page.script_signin_button)
            self.browser.execute_js(self.driver, self.main_screen_page.script_signup_button)
            assert self.browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
            assert self.browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
            assert self.browser.wait_element_presented(self.driver, self.locators.TIME_ON_UPPER_RULER, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.DATE_ON_UPPER_RULER, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.LANGUAGE_FLAG, delay)
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
