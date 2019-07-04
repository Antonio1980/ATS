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

test_case = '6246'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verify Asset Panel, UI
    1. Open WTP
    2. Verify that the main currencies (quoted currencies) panel hold the following default currencies: 
       BTC, ETH, USDT,Drop-down - USD option selected by default.
    3. Verify that below the main currencies list there is the "Search" text box. .
    4. Verify that below the "Search" field there are the following filter/sorting options:
        Favorites icon "star" 
        "24H Change"
        "24H Volume"
    5. Verify that below the filter/sorting options appear currencies list.
    6. Compare available funds from Buy/Sell section to available funds from 'Funds' section 
    7. Verify that each currency entry holds the following elements:
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
             name='Asset Panel UI')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/asset_panel_tests/C6246_asset_panel_ui_test.py",
                 "TestAssetPanelUi")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.asset_panel
@ddt
class TestAssetPanelUi(unittest.TestCase):
    @allure.step("SetUp:  calling of registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
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
        assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
        assert self.browser.wait_element_presented(self.driver, self.locators.BTC_CURRENCY_NOT_SELECTED, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.ETH_CURRENCY_NOT_SELECTED, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.USDT_CURRENCY_NOT_SELECTED, delay)
        assert self.browser.wait_element_presented(self.driver,
                                                   self.locators.USD_DEFAULT_CURRENCY_DROPDOWN_NOT_SELECTED,
                                                   delay)
        assert self.browser.find_element(self.driver, self.locators.LEADING_CURRENCY_MENU)
        assert self.browser.find_element(self.driver, self.locators.SEARCH_BOX)
        assert self.browser.wait_element_presented(self.driver, self.locators.STAR_ICON_FAV, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.TWENTY_FOUR_H_CHANGE_NOT_SELECTED, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.TWENTY_FOUR_H_VOLUME_SELECTED, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.CURRENCIES_LIST_PANEL, delay)

        currencies_items_usd = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_usd)

        btc = self.browser.wait_element_presented(self.driver, self.locators.BTC_CURRENCY_NOT_SELECTED, delay)
        self.browser.click_on_element(btc)
        currencies_items_btc = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_btc)

        eth = self.browser.wait_element_presented(self.driver, self.locators.ETH_CURRENCY_NOT_SELECTED, delay)
        self.browser.click_on_element(eth)
        currencies_items_eth = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_eth)

        usdt = self.browser.wait_element_presented(self.driver, self.locators.USDT_CURRENCY_NOT_SELECTED, delay)
        self.browser.click_on_element(usdt)
        currencies_items_usdt = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_usdt)

        self.browser.execute_js(self.driver, self.main_screen_page.script_eur)
        currencies_items_eur = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_eur)

        self.browser.execute_js(self.driver, self.main_screen_page.script_gbp)
        currencies_items_gbp = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_gbp)

        self.browser.execute_js(self.driver, self.main_screen_page.script_jpy)
        currencies_items_jpy = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        self.main_screen_page.check_asset_panel_by_tab(currencies_items_jpy)

        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        self.browser.close_browser(self.driver)
