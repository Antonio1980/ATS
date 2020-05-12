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
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '6253'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verification Value "Last Price", UI
    1. Open WTP
    2. Select some quoted currency on the main assets panel. (BTC)
    3. Select some base currency. (DXCASH/BTC)
    4. Find the price of the last instrument's trade in DB.
    5. Get value of "last price" field on the platform.
    6. Verify that Price from DB equal Price on the platform
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification Value "Last Price USD" - Quoted Currency Has Instrument With Base "USD"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6252_verification_value_last_price_test.py",
                 "TestVerificationValueLastPrice")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.asset_panel
@ddt
class TestVerificationValueLastPriceUsd(unittest.TestCase):
    @allure.step("SetUp:  calling of registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.market_order_panel = MarketOrderPanelPage()
        self.locators_market_order = self.market_order_panel.locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.main_screen_page = MainScreenPage()
        self.locators = self.main_screen_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.id_instrument_quoted = "1015"  # ETH/BTC
        self.id_instrument = "1007"  # BTC/USD

    @allure.step("Starting with: test_verification_value_last_price_usd_usd")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_verification_value_last_price_usd_usd(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = self.home_page.ui_delay
        assert self.home_page.open_signin_page(self.driver)
        assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
        assert self.browser.wait_element_presented(self.driver, self.locators.UPPER_RULER, delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.CURRENCIES_LIST_PANEL, delay)
        last_price_quoted_query = ("SELECT price FROM trades_crypto WHERE instrumentId = "
                                   + self.id_instrument_quoted + " ORDER BY executionDate  DESC limit 1;")
        last_price_quoted = float(SqlDb.run_mysql_query(last_price_quoted_query)[0][0])
        last_price_query = ("SELECT price FROM trades_crypto WHERE instrumentId = "
                            + self.id_instrument + " ORDER BY executionDate  DESC limit 1;")
        last_price = float(SqlDb.run_mysql_query(last_price_query)[0][0])
        value_instrument = round((last_price_quoted * last_price), 2)
        btc = self.browser.wait_element_presented(self.driver, self.locators.BTC_CURRENCY_NOT_SELECTED, delay)
        self.browser.click_on_element(btc)
        time.sleep(1)
        assert self.browser.wait_element_presented(self.driver,
                                                   "//li[@data-instrumentid = " + self.id_instrument_quoted
                                                   + "]//div[@class ='usdPrice']", delay)
        time.sleep(3)
        last_price_in_usd_ui = float(self.browser.execute_js(self.driver,
                                                             '''return $("[id='dx_platform'] li[data-instrumentid = '''
                                                             + self.id_instrument_quoted +
                                                             '''] div[class = 'usdPrice']").text(); ''')[2:])
        assert value_instrument == float(last_price_in_usd_ui.replace(",", ""))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        self.browser.close_browser(self.driver)
