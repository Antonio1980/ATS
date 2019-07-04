import time
import unittest

import allure
import pytest
from ddt import ddt, data, unpack

from config_definitions import BaseConfig
from src.base import logger
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.signin_page import SignInPage

test_case = '7414'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Asset Panel UI - Digital Stocks Selected, UI
    1. Open WTP
    2. Verify that each currency entry holds the following elements:
        - 24 Hour Change 
        - Last Price 
        - last price USD 
        - 24 Hour Volume in the quoted currency 
        - Currency symbol
        - Currency name
        - Currency code 
        - Favorites
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Asset Panel UI - Digital Stocks Selected')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/asset_panel_tests/C7414_digital_stocks_selected_test.py",
                 "TestDigitalStocksSelected")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.asset_panel
@ddt
class TestDigitalStocksSelected(unittest.TestCase):
    @allure.step("SetUp:  calling of registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer(None, 'Andrew_Smith@sand.org', '1Aa@<>12', '100001100000024504')
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.main_screen_page = MainScreenPage()
        self.locators = self.main_screen_page.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_asset_panel_ui")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_asset_panel_ui(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = self.home_page.ui_delay

        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_asset_panel_ui), "
                           "with: browser- {0} ".format(browser))
        assert self.home_page.open_signin_page(self.driver)
        assert self.sign_in_page.sign_in(self.driver, self.customer.email,
                                         self.customer.password)
        digital_stocks_button = self.browser.wait_element_presented(self.driver, self.locators.DIGITAL_STOCKS_BUTTON,
                                                                    delay)
        self.browser.click_on_element(digital_stocks_button)
        time.sleep(5)

        self.browser.execute_js(self.driver, self.main_screen_page.script_stocks_usd)
        currencies_items_stocks_usd = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_stocks_usd)

        self.browser.execute_js(self.driver, self.main_screen_page.script_stocks_btc)
        currencies_items_stocks_btc = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_stocks_btc)

        self.browser.execute_js(self.driver, self.main_screen_page.script_etf_usd)
        currencies_items_etf_usd = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_etf_usd)

        self.browser.execute_js(self.driver, self.main_screen_page.script_etf_btc)
        currencies_items_etf_btc = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_etf_btc)

        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        self.browser.close_browser(self.driver)
