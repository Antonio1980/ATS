import re
import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.registered_customer import RegisteredCustomer
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '2824'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    UI test.
    Amount verification against Available Funds Negative, UI
    1. Open WTP
    2. Select an instrument(1007).
    3. Enter an amount of based currency - "Estimate Price" * "Amount" must exceed the available funds 
       and try to send order. 
    4. Verify that order is rejected.
    5. Enter an amount of quoted currency - it must exceed the available funds and try to send order
    6. Verify that order is rejected.
    7. Check "Trades History". No new trades.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Amount verification against Available Funds Negative')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2824_amount_verification_against_funds_negative_test.py",
    "TestAmountVerificationAgainstFundsNegative")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.market_order
@pytest.mark.order_management
@ddt
class TestAmountVerificationAgainstFundsNegative(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 2000)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 10)
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_amount_verification_against_funds")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_amount_verification_against_funds(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        result = 0
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver))
            self.assertTrue(self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password))
            assert self.browser.wait_element_presented(self.driver, self.locators.MARKET_TAB, delay)
            self.browser.execute_js(self.driver, '''$("div[class='tradeType market']").click()''')
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            usd_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.USD_OPTION_FROM_USD_DROPDOWN, delay)
            self.browser.click_on_element(usd_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1007]').click()''')
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.BTC_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay)
            amount_buy = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_BUY, delay)
            time.sleep(3)
            available_for_trading_buy = self.browser.execute_js(self.driver,
                                                                self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_trading_buy = float(re.sub(',', '', available_for_trading_buy))
            estimated_price_buy = float(self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_BUY_JQ))
            amount_sell = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_SELL, delay)
            available_for_trading_sell = self.browser.execute_js(self.driver,
                                                                 self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            available_for_trading_sell = float(re.sub(',', '', available_for_trading_sell))
            if available_for_trading_buy < estimated_price_buy or available_for_trading_buy == 0:
                self.browser.send_keys(amount_buy, 6)
            else:
                amount_more_available_for_trading_buy = int((available_for_trading_buy / estimated_price_buy) + (
                        (available_for_trading_buy / estimated_price_buy) / 100 * 20))
                self.browser.send_keys(amount_buy, amount_more_available_for_trading_buy)
            buy_button = self.browser.wait_element_presented(self.driver, self.locators.BUY_BUTTON, delay)
            self.browser.click_on_element(buy_button)
            available_for_trading_buy_after_click_buy_button = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_trading_buy_after_click_buy_button = float(
                re.sub(',', '', available_for_trading_buy_after_click_buy_button))
            self.assertTrue(available_for_trading_buy == available_for_trading_buy_after_click_buy_button)
            if available_for_trading_sell == 0:
                self.browser.send_keys(amount_sell, 7)
            else:
                amount_more_available_for_trading_sell = int(
                    available_for_trading_sell + available_for_trading_sell / 100 * 10)
                self.browser.send_keys(amount_sell, amount_more_available_for_trading_sell)
            sell_button = self.browser.wait_element_presented(self.driver, self.locators.SELL_BUTTON, delay)
            self.browser.click_on_element(sell_button)
            available_for_trading_sell_after_click_sell_button = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            available_for_trading_sell_after_click_sell_button = float(
                re.sub(',', '', available_for_trading_sell_after_click_sell_button))
            self.assertTrue(available_for_trading_sell == available_for_trading_sell_after_click_sell_button)
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    def tearDown(self):
        Browser.close_browser(self.driver)
