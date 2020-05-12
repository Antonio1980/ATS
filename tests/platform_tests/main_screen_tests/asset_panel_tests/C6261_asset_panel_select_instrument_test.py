import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.data_bases.sql_db import SqlDb
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.main_screen_page import MainScreenPage
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '6261'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verification Value "Last Price", UI
    1. Open WTP
    2. Select some quoted currency from the main currencies panel.
    3. Select some related base currency.
    4. Verify that all data on the trading platform updated with the selected instrument.
    5. Repeat step from 2 till 4 for some over instrument
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Asset Panel - Select Instrument"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6261_asset_panel_select_instrument_test.py",
                 "TestAssetPanelSelectInstrument")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.asset_panel
@ddt
class TestAssetPanelSelectInstrument(unittest.TestCase):
    @allure.step("SetUp:  calling of registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.main_screen = MainScreenPage()
        self.locators = self.main_screen.locators
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.email = self.customer.email
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_asset_panel_select_instrument")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_asset_panel_select_instrument(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = self.home_page.ui_delay
        assert self.home_page.open_signin_page(self.driver)
        assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
        time.sleep(4)
        currencies_items = self.browser.find_elements(self.driver, self.locators.ALL_CURRENCIES)
        instrument_1 = currencies_items[0].get_attribute('data-instrumentid')
        instrument_2 = currencies_items[1].get_attribute('data-instrumentid')
        id_instrument_list = [instrument_1, instrument_2]
        for id_instrument in id_instrument_list:
            name_instrument_query = "SELECT name FROM instruments WHERE id = " + id_instrument + " ;"
            name_instrument = SqlDb.run_mysql_query(name_instrument_query)[0][0]
            base_currency = name_instrument.split('/')[0]
            quoted_currency = name_instrument.split('/')[1]
            a = "SELECT name FROM currencies WHERE currencies.code = "+ base_currency +";"
            name_base_currency = SqlDb.run_mysql_query("SELECT name FROM currencies WHERE currencies.code = '"
                                                       + base_currency + "';")[0][0]
            assert self.browser.wait_element_presented(self.driver, self.locators.UPPER_RULER, delay)

            instrument = self.browser.wait_element_presented(self.driver,
                                                             "//*[@class = 'assetsList ps-container']//li[@data-instrumentid = '" + id_instrument + "']",
                                                             delay)
            self.browser.click_on_element(instrument)
            time.sleep(3)
            assert self.browser.wait_element_presented(self.driver,
                                                       "//*[@class = 'assetsList ps-container']//li[@data-instrumentid = '" + id_instrument + "']",
                                                       delay)
            asset_title = self.browser.find_element(self.driver, "//*[@id='dx_platform']//li[@data-instrumentid= '"
                                                    + id_instrument +
                                                    "']/div[2]/div[@class='assetFullTitle']").get_attribute(
                'innerText')
            underlying_currency = self.browser.find_element(self.driver,
                                                            self.locators.UNDERLYING_CURRENCY_SELECTED).get_attribute(
                'innerText')
            asset_name = self.browser.find_element(self.driver, self.locators.ASSET_NAME).get_attribute('innerText')
            base_currency_code_limit_list = self.browser.find_elements(self.driver,
                                                                       self.locators.BASE_CURRENCY_CODE_LIMIT_LIST)
            for i in base_currency_code_limit_list:
                base_cur = i.get_attribute('innerText')
                assert base_cur == base_currency

            currency_symbol_buy_limit = self.browser.find_element(self.driver,
                                                                  self.locators.QUOTED_BUY).get_attribute(
                'innerText')
            currency_symbol_sell_limit = self.browser.find_element(self.driver,
                                                                   self.locators.QUOTED_SELL).get_attribute(
                'innerText')
            # self.browser.execute_js(self.driver,
            #                         '''$('[id="exchangeEntity_0"] div[class = "tradeType market"]').click()''')

            quoted_currency_info_list = self.browser.find_elements(self.driver,
                                                                   self.locators.QUOTED_CURRENCY_MARKET_INFO_LIST)
            for i in quoted_currency_info_list:
                quot_cur = i.get_attribute('innerText')
                assert quot_cur == quoted_currency

            base_currency_market_info_buyers = self.browser.find_element(self.driver,
                                                                         self.locators.BASE_CURRENCY_MARKET_INFO_BUYERS).get_attribute(
                'innerText')
            base_currency_market_info_sellers = self.browser.find_element(self.driver,
                                                                          self.locators.BASE_CURRENCY_MARKET_INFO_SELLERS).get_attribute(
                'innerText')
            assert asset_name == name_instrument
            assert underlying_currency == currency_symbol_buy_limit == currency_symbol_buy_limit == quoted_currency
            assert asset_title == name_base_currency
            assert currency_symbol_sell_limit == currency_symbol_sell_limit == base_currency
            assert base_currency_market_info_buyers == base_currency_market_info_sellers == base_currency
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        self.browser.close_browser(self.driver)
