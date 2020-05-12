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

test_case = '8089'


@allure.title("Upper Ruler")
@allure.description("""
    UI test.
    "Funds Filtering Verification against DB", UI
    1. Log In to the web platform  (homepage)
    2. Open Funds panel
    3. Filter the Funds by currency on UI
    4. Generate list of filtered funds from UI
    5. Get list of filtered funds from DB
    6. Compare list from from UI with list from DB
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Funds Filters Verification Against DB"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/upper_ruler_tests/C8089_funds_filters_verification_against_db_test.py",
                 "TestFilteringFunds")
@pytest.mark.usefixtures("r_time_count", "web_driver", "r_customer")
@pytest.mark.ui
@pytest.mark.upper_ruler
class TestFilteringFunds(object):
    browser = Browser()
    home_page = HomePage()
    sign_in_page = SignInPage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators
    filtered_funds = None
    funds = False

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_sign_in_page(self, web_driver, r_customer):
        self.home_page.open_signin_page(web_driver)
        time.sleep(3.0)
        self.sign_in_page.sign_in(web_driver, r_customer.email, r_customer.password)
        time.sleep(3.0)

    @allure.step("Proceed with: test_open_funds_screen ")
    @automation_logger(logger)
    def test_open_funds_screen(self, web_driver):
        funds_button = self.browser.wait_element_presented(web_driver, self.locators.FUNDS_BUTTON, self.delay)
        self.browser.click_on_element(funds_button)
        assert self.browser.wait_element_presented(web_driver, self.locators.FUNDS_PANEL_VISIBLE, self.delay)

    @allure.step("Proceed with: test_funds_filtering ")
    @automation_logger(logger)
    def test_funds_crypto_filtering(self, web_driver):

        currency_type = 'Cryptocurrencies'
        crypto_button = self.browser.execute_js(web_driver, self.locators.CRYPTO_BUTTON_JQ)
        if crypto_button:
            ui_name = self.browser.get_attribute_from_locator(web_driver, self.locators.FILTER_CRYPTO, "innerText")
            assert ui_name == "Crypto"
            filter_crypto = self.browser.wait_element_presented(web_driver, self.locators.FILTER_CRYPTO, self.delay)
            self.browser.click_on_element(filter_crypto)
            filtered_list = self.browser.find_elements(web_driver, self.locators.CURRENCY_NAME_BY_FILTER)
            TestFilteringFunds.filtered_funds = self.main_screen_page.get_filtered_currencies(filtered_list)
            assert self.filtered_funds is not None
            get_currencies_from_db = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert sorted(self.filtered_funds) == sorted(
                get_currencies_from_db), "Funds from UI are not according to funds from DB"
        else:
            db_list = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert db_list is None
        logger.logger.info("=======test_funds_crypto_filtering is passed=======")

    @allure.step("Proceed with: test_funds_filtering ")
    @automation_logger(logger)
    def test_funds_stocks_filtering(self, web_driver):
        currency_type = 'DigitalStocks'
        crypto_button = self.browser.execute_js(web_driver, self.locators.STOCKS_BUTTON_JQ)
        if crypto_button:
            ui_name = self.browser.get_attribute_from_locator(web_driver, self.locators.FILTER_STOCKS, "innerText")
            assert ui_name == "Stocks"
            filter_crypto = self.browser.wait_element_presented(web_driver, self.locators.FILTER_STOCKS, self.delay)
            self.browser.click_on_element(filter_crypto)
            filtered_list = self.browser.find_elements(web_driver, self.locators.CURRENCY_NAME_BY_FILTER)
            TestFilteringFunds.filtered_funds = self.main_screen_page.get_filtered_currencies(filtered_list)
            assert self.filtered_funds is not None
            get_currencies_from_db = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert sorted(self.filtered_funds) == sorted(
                get_currencies_from_db), "Funds from UI are not according to funds from DB"
        else:
            db_list = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert db_list is None
        logger.logger.info("=========test_funds_stocks_filtering is passed=========")

    @allure.step("Proceed with: test_funds_filtering ")
    @automation_logger(logger)
    def test_funds_etf_filtering(self, web_driver):
        currency_type = 'ETF'
        crypto_button = self.browser.execute_js(web_driver, self.locators.ETFS_BUTTON_JQ)
        if crypto_button:
            ui_name = self.browser.get_attribute_from_locator(web_driver, self.locators.FILTER_ETFS, "innerText")
            assert ui_name == "ETFs"
            filter_crypto = self.browser.wait_element_presented(web_driver, self.locators.FILTER_ETFS, self.delay)
            self.browser.click_on_element(filter_crypto)
            filtered_list = self.browser.find_elements(web_driver, self.locators.CURRENCY_NAME_BY_FILTER)
            TestFilteringFunds.filtered_funds = self.main_screen_page.get_filtered_currencies(filtered_list)
            assert self.filtered_funds is not None
            get_currencies_from_db = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert sorted(self.filtered_funds) == sorted(
                get_currencies_from_db), "Funds from UI are not according to funds from DB"
        else:
            db_list = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert db_list is None
        logger.logger.info("=======test_funds_etf_filtering is passed=======")

    @allure.step("Proceed with: test_funds_filtering ")
    @automation_logger(logger)
    def test_funds_sto_filtering(self, web_driver):
        currency_type = 'STO'
        crypto_button = self.browser.execute_js(web_driver, self.locators.STO_BUTTON_JQ)
        if crypto_button:
            ui_name = self.browser.get_attribute_from_locator(web_driver, self.locators.FILTER_STO, "innerText")
            assert ui_name == "STO"
            filter_crypto = self.browser.wait_element_presented(web_driver, self.locators.FILTER_STO, self.delay)
            self.browser.click_on_element(filter_crypto)
            filtered_list = self.browser.find_elements(web_driver, self.locators.CURRENCY_NAME_BY_FILTER)
            TestFilteringFunds.filtered_funds = self.main_screen_page.get_filtered_currencies(filtered_list)
            assert self.filtered_funds is not None
            get_currencies_from_db = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert sorted(self.filtered_funds) == sorted(
                get_currencies_from_db), "Funds from UI are not according to funds from DB"
        else:
            db_list = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert db_list is None
        logger.logger.info("=======test_funds_sto_filtering is passed=======")

    @allure.step("Proceed with: test_funds_filtering ")
    @automation_logger(logger)
    def test_funds_fiat_filtering(self, web_driver):
        currency_type = 'Fiat'
        crypto_button = self.browser.execute_js(web_driver, self.locators.FIAT_BUTTON_JQ)
        if crypto_button:
            ui_name = self.browser.get_attribute_from_locator(web_driver, self.locators.FILTER_FIAT, "innerText")
            assert ui_name == "Fiat"
            filter_crypto = self.browser.wait_element_presented(web_driver, self.locators.FILTER_FIAT, self.delay)
            self.browser.click_on_element(filter_crypto)
            filtered_list = self.browser.find_elements(web_driver, self.locators.CURRENCY_NAME_BY_FILTER)
            TestFilteringFunds.filtered_funds = self.main_screen_page.get_filtered_currencies(filtered_list)
            assert self.filtered_funds is not None
            get_currencies_from_db = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert sorted(self.filtered_funds) == sorted(
                get_currencies_from_db), "Funds from UI are not according to funds from DB"
        else:
            db_list = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert db_list is None
        logger.logger.info("=======test_funds_fiat_filtering is passed=======")

    @allure.step("Proceed with: test_funds_filtering ")
    @automation_logger(logger)
    def test_funds_all_filtering(self, web_driver):
        currency_type = 'All'
        crypto_button = self.browser.execute_js(web_driver, self.locators.ALL_CURRENCIES_BUTTON_JQ)
        if crypto_button:
            ui_name = self.browser.get_attribute_from_locator(web_driver, self.locators.FILTER_ALL, "innerText")
            assert ui_name == "All"
            filter_crypto = self.browser.wait_element_presented(web_driver, self.locators.FILTER_ALL, self.delay)
            self.browser.click_on_element(filter_crypto)
            filtered_list = self.browser.find_elements(web_driver, self.locators.CURRENCY_NAME_BY_FILTER)
            TestFilteringFunds.filtered_funds = self.main_screen_page.get_filtered_currencies(filtered_list)
            assert self.filtered_funds is not None
            get_currencies_from_db = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert sorted(self.filtered_funds) == sorted(
                get_currencies_from_db), "Funds from UI are not according to funds from DB"
        else:
            db_list = self.main_screen_page.get_list_of_specific_type_currencies_db(currency_type)
            assert db_list is None
        logger.logger.info("=======test_funds_all_filtering is passed=======")