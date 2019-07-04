import time

import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.signin_page import SignInPage

test_case = '6258'


@pytest.mark.skip
@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verification of Quoted/Base Currency Value", UI
    1. Open Home Page 
    2. Check base quoted currencies for BTC (CRYPTO, DIGITAL STOCKS/ETF)
    3. Check base quoted currencies for ETH (CRYPTO)
    4. Check base quoted currencies for USDT (CRYPTO)
    5. Check base quoted currencies for USD (CRYPTO, DIGITAL STOCKS/ETF)
    6. Check base quoted currencies for EUR (CRYPTO)
    7. Check base quoted currencies for GBP (CRYPTO)
    8. Check base quoted currencies for JPY (CRYPTO)
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification of Quoted/Base Currency Value"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6258_verification_quoted_base_currency_value_test.py",
                 "TestVerificationQuotedBaseCurrencyValue")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.asset_panel
class TestVerificationQuotedBaseCurrencyValue(object):
    browser = Browser()
    home_page = HomePage()
    sign_in_page = SignInPage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_open_home_page(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay)

    @allure.step("Proceed with: test_check_base_quoted_btc")
    @automation_logger(logger)
    def test_check_base_quoted_btc(self, web_driver):
        btc = self.browser.wait_element_presented(web_driver, self.locators.BTC_CURRENCY_NOT_SELECTED, self.delay)
        self.browser.click_on_element(btc)
        currencies_items_btc = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        list_name = self.main_screen_page.get_all_base_names(currencies_items_btc)
        digital_stocks_button = self.browser.wait_element_presented(web_driver, self.locators.DIGITAL_STOCKS_BUTTON,
                                                                    self.delay)
        self.browser.click_on_element(digital_stocks_button)
        self.browser.execute_js(web_driver, self.main_screen_page.script_stocks_btc)
        time.sleep(2.0)
        currencies_items_stocks_btc = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        list_stocks_name = self.main_screen_page.get_all_base_names(currencies_items_stocks_btc)

        self.browser.execute_js(web_driver, self.main_screen_page.script_etf_btc)
        time.sleep(2.0)
        currencies_items_etf_btc = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        list_etf_name = self.main_screen_page.get_all_base_names(currencies_items_etf_btc)
        general_name_list = sorted(list_name + list_stocks_name + list_etf_name)
        list_name_db = sorted(self.main_screen_page.get_all_base_names_db("BTC"))
        assert general_name_list == list_name_db

    @allure.step("Proceed with: ")
    @automation_logger(logger)
    def test_check_base_quoted_eth(self, web_driver):
        crypto_button = self.browser.wait_element_presented(web_driver, self.locators.CRYPTO_BUTTON_NOT_SELECTED,
                                                            self.delay)
        self.browser.click_on_element(crypto_button)
        eth = self.browser.wait_element_presented(web_driver, self.locators.ETH_CURRENCY_NOT_SELECTED, self.delay)
        self.browser.click_on_element(eth)
        time.sleep(2)
        currencies_items_eth = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        eth_list_name = sorted(self.main_screen_page.get_all_base_names(currencies_items_eth))
        eth_list_name_db = sorted(self.main_screen_page.get_all_base_names_db("ETH"))
        assert eth_list_name == eth_list_name_db

    @allure.step("Proceed with: test_check_base_quoted_usdt ")
    def test_check_base_quoted_usdt(self, web_driver):
        usdt = self.browser.wait_element_presented(web_driver, self.locators.USDT_CURRENCY_NOT_SELECTED, self.delay)
        self.browser.click_on_element(usdt)
        time.sleep(5.0)
        currencies_items_usdt = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        usdt_list_name = sorted(self.main_screen_page.get_all_base_names(currencies_items_usdt))
        usdt_list_name_db = sorted(self.main_screen_page.get_all_base_names_db("USDT"))
        assert usdt_list_name == usdt_list_name_db

    @allure.step("Proceed with: test_check_base_quoted_usd")
    def test_check_base_quoted_usd(self, web_driver):
        self.browser.execute_js(web_driver, self.main_screen_page.script_usd)
        currencies_items_usd = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        usd_list_name = self.main_screen_page.get_all_base_names(currencies_items_usd)
        digital_stocks_button = self.browser.wait_element_presented(web_driver, self.locators.DIGITAL_STOCKS_BUTTON,
                                                                    self.delay)

        self.browser.click_on_element(digital_stocks_button)
        self.browser.execute_js(web_driver, self.main_screen_page.script_stocks_usd)
        time.sleep(10.0)
        currencies_items_stocks_usd = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        list_stocks_name = self.main_screen_page.get_all_base_names(currencies_items_stocks_usd)
        self.browser.execute_js(web_driver, self.main_screen_page.script_etf_usd)
        time.sleep(10.0)
        currencies_items_etf_usd = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        list_etf_name = self.main_screen_page.get_all_base_names(currencies_items_etf_usd)
        general_name_list = sorted(usd_list_name + list_stocks_name + list_etf_name)
        usd_list_name_db = sorted(self.main_screen_page.get_all_base_names_db("USD"))
        assert general_name_list == usd_list_name_db

    @allure.step("Proceed with: test_check_base_quoted_eur ")
    def test_check_base_quoted_eur(self, web_driver):
        crypto_button = self.browser.wait_element_presented(web_driver, self.locators.CRYPTO_BUTTON_NOT_SELECTED,
                                                            self.delay)
        self.browser.click_on_element(crypto_button)
        self.browser.execute_js(web_driver, self.main_screen_page.script_eur)
        time.sleep(5.0)
        currencies_items_eur = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        eur_list_name = sorted(self.main_screen_page.get_all_base_names(currencies_items_eur))
        eur_list_name_db = sorted(self.main_screen_page.get_all_base_names_db("EUR"))
        assert eur_list_name == eur_list_name_db

    @allure.step("Proceed with: test_check_base_quoted_gbp ")
    def test_check_base_quoted_gbp(self, web_driver):
        self.browser.execute_js(web_driver, self.main_screen_page.script_gbp)
        time.sleep(5.0)
        currencies_items_gbp = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        gbp_list_name = sorted(self.main_screen_page.get_all_base_names(currencies_items_gbp))
        gbp_list_name_db = sorted(self.main_screen_page.get_all_base_names_db("GBP"))
        assert gbp_list_name == gbp_list_name_db

    @allure.step("Proceed with: test_check_base_quoted_gbp ")
    def test_check_base_quoted_jpy(self, web_driver):
        self.browser.execute_js(web_driver, self.main_screen_page.script_jpy)
        time.sleep(5.0)
        currencies_items_jpy = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        jpy_list_name = sorted(self.main_screen_page.get_all_base_names(currencies_items_jpy))
        jpy_list_name_db = sorted(self.main_screen_page.get_all_base_names_db("JPY"))
        assert jpy_list_name == jpy_list_name_db
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
