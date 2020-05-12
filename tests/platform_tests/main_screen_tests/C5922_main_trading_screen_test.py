import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.main_screen_page import MainScreenPage

test_case = '5922'


@allure.feature('Main Trading Screen')
@allure.severity(allure.severity_level.NORMAL)
@allure.title("MAIN TRADING SCREEN")
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Best 30 orders are presented - Sell')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/C5922_main_trading_screen_test.py",
                 "MainTradingScreenTest")
@allure.description("""
    Verify web elements at the Home page.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.home_page
@pytest.mark.smoke
@pytest.mark.ui
@ddt
class TestMainTradingScreen(unittest.TestCase):
    @allure.step("SetUp: calling RegisteredCustomer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.main_screen_page = MainScreenPage()
        self.locators = self.main_screen_page.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_main_trading_screen")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_main_trading_screen(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_in_page_ui with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = self.home_page.ui_delay
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "Open Sign In page is failed")
            self.assertTrue(self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password),
                            "Sign In page is failed")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.UPPER_RULER, delay),
                            "UPPER_RULER is not found")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.ASSET_PANEL, delay),
                            "ASSET_PANEL is not found")
            self.assertTrue(self.browser.wait_element_presented(self.driver,
                                                                self.locators.INSTRUMENT_QUICK_INFO_PANEL, delay),
                            "INSTRUMENT_QUICK is not found")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.GRAPH_AREA, delay),
                            "GRAPH_AREA is not found")
            # assert self.browser.wait_element_presented(self.driver, self.locators.MARKET_ORDER_PANEL, delay)
            self.assertTrue(self.browser.find_element(self.driver, self.locators.LIMIT_BUTTON),
                            "LIMIT_ORDER is not found")
            # self.browser.try_click(self.driver, limit_button, 2)
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.LIMIT_ORDER_PANEL, delay),
                            "LIMIT_ORDER is not found")
            self.assertTrue(self.browser.find_element_by(self.driver, self.locators.CURRENT_PORTFOLIO_ID, "id"),
                            "CURRENT_PORTFOLIO is not found")
            self.assertTrue(self.browser.find_element_by(self.driver, self.locators.ORDER_BOOK_PANEL_ID, "id"),
                            "ORDER_BOOK is not found")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.OPEN_ORDER_TABLE, delay),
                            "OPEN_ORDER is not found")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.ORDERS_HISTORY_TABLE, delay),
                            "ORDERS_HISTORY is not found")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.TRADES_HISTORY_TABLE, delay),
                            "TRADES_HISTORY is not found")
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.LAST_TRADES_PANEL, delay),
                            "LAST_TRADES is not found ")

            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
