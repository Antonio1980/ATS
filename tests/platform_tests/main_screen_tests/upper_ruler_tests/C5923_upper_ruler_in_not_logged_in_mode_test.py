import time
import allure
import pytest
import unittest
from src.base import logger
from src.base.browser import Browser
from src.base.enums import Browsers
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.main_screen_page import MainScreenPage

test_case = '5923'


@allure.title("Upper Ruler")
@allure.description("""
    UI test.
    Upper Ruler (In Not Logged in Mode), UI
    1. Open WTP, home page
    2. Verify that the Upper Ruler exists at the up line of Trading Platform.
    3. Verify that the Upper Ruler has the following parts:
        Logo
        Sigh In
        SignUp
        Crypto Button
        Digital Stocks button
        Language Flag
     4. Verify that the Upper Ruler doesn't have the following parts:
        User Account Indicator (displays user full name with matching local time and date)
        Portfolio
        Funds Button
        LogoutButton
    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Upper Ruler (In Not Logged in Mode) UI')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/main_screen_tests/upper_ruler_tests/C5923_upper_ruler_in_not_logged_in_mode_test.py",
    "TestUpperRulerFunctional")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.upper_ruler
class TestMainTradingScreen(unittest.TestCase):
    @allure.step("SetUp: Set Browser ")
    @automation_logger(logger)
    def setUp(self):
        self.browser = Browser()
        self.home_page = HomePage()
        self.main_screen_page = MainScreenPage()
        self.locators = self.main_screen_page.locators

    @allure.step("Starting with: test_main_trading_screen")
    @automation_logger(logger)
    def test_main_trading_screen(self):
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
        delay = self.home_page.ui_delay
        self.home_page.open_home_page(self.driver)
        time.sleep(3)
        assert self.browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
        assert self.browser.wait_element_presented(self.driver, self.locators.SIGH_UP_BUTTON, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.SIGH_IN_BUTTON, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.LOGO, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.CRYPTO_BUTTON, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.DIGITAL_STOCKS_BUTTON, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.LANGUAGE_FLAG, delay)
        assert self.browser.execute_js(self.driver, self.locators.FUNDS_VISIBLE) is False
        assert self.browser.execute_js(self.driver, self.locators.USER_NAME_VISIBLE) is False
        assert self.browser.execute_js(self.driver, self.locators.LOGOUT_VISIBLE) is False
        assert self.browser.execute_js(self.driver, self.locators.USER_PROFILE_VISIBLE) is False
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        self.browser.close_browser(self.driver)
