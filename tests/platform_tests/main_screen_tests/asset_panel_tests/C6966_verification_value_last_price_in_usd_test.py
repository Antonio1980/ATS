import time

import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.signin_page import SignInPage

test_case = '6258'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verification of Quoted/Base Currency Value", UI
    1. Open Home Page 
    2. Get last trade price instrument "BTC/EUR" as 'price_1'
    3. Get last trade price instrument "BTC/USD" as 'price_2'
    3. Get last trade price instrument "BTC/EUR" on UI as 'price_ui'
    4. Calculation conversion rate: 'price_2'/'price_1' as 'usd_rate'. Compare 'price_ui' to ('usd_rate' * 'price_2')
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification Value "Last Price USD" - FIAT to USD Conversions"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6966_verification_value_last_price_in_usd_test.py",
                 "TestVerificationQuotedBaseCurrencyValue")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.asset_panel
class TestVerificationValueLastPriceUsdFiat(object):
    browser = Browser()
    home_page = HomePage()
    sign_in_page = SignInPage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators
    instrument_id_1 = 'BTC/EUR'
    instrument_id_2 = 'BTC/USD'
    last_trade_price_1 = None
    last_trade_price_2 = None
    last_price_ui = None

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_open_home_page(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay)

    @allure.step("Proceed with: test_get_last_trade_price_instrument_1")
    @automation_logger(logger)
    def test_get_last_trade_price_instrument_1(self, web_driver):
        get_last_price_query = (
                "SELECT price FROM instruments JOIN trades_crypto ON instruments.id=trades_crypto.instrumentId"
                " WHERE instruments.name='" + str(self.instrument_id_1) + "' AND trades_crypto.direction='buy'"
                                                                          " ORDER BY executionDate DESC LIMIT 1;")
        TestVerificationValueLastPriceUsdFiat.last_trade_price_1 = Instruments.run_mysql_query(get_last_price_query)[0][
            0]
        assert self.last_trade_price_1 is not None

    @allure.step("Proceed with: test_get_last_trade_price_instrument_2")
    @automation_logger(logger)
    def test_get_last_trade_price_instrument_2(self, web_driver, ):
        get_last_price_query = (
                "SELECT price FROM instruments JOIN trades_crypto ON instruments.id=trades_crypto.instrumentId"
                " WHERE instruments.name='" + str(self.instrument_id_2) + "' AND trades_crypto.direction='buy'"
                                                                          " ORDER BY executionDate DESC LIMIT 1;")
        TestVerificationValueLastPriceUsdFiat.last_trade_price_2 = Instruments.run_mysql_query(get_last_price_query)[0][
            0]
        assert self.last_trade_price_2 is not None

    @allure.step("Proceed with: test_get_last_trade_price_ui")
    @automation_logger(logger)
    def test_get_last_trade_price_ui(self, web_driver):
        self.browser.execute_js(web_driver, self.main_screen_page.script_eur)
        time.sleep(2.0)
        last_price_locator = self.main_screen_page.generate_x_path_last_trade_price(self.instrument_id_1)
        TestVerificationValueLastPriceUsdFiat.last_price_ui = round((
            float(self.browser.find_element(web_driver, last_price_locator).get_attribute('title'))), 2)
        assert self.last_price_ui is not None

    @allure.step("Proceed with: test_check_last_trade_price_db_and_ui")
    @automation_logger(logger)
    def test_check_last_trade_price_db_and_ui(self):
        last_trade_price_db = round(((self.last_trade_price_2 / self.last_trade_price_1) * self.last_trade_price_1), 2)
        assert self.last_price_ui == float(last_trade_price_db)
