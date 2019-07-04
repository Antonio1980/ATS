import time
import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.data_bases.redis_db import RedisDb
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST 'TS- 10'")
@allure.description("""
    Verify after trade is created it updates quick instrument panel.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_sanity_tests/quick_instrument_panel_updated_after_trade_test.py",
                 "TestQuickInstrumentPanelUpdatedAfterTrade")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.trading_sanity
@ddt
class TestQuickInstrumentPanelUpdatedAfterTrade(unittest.TestCase):
    test_case = "TS- 10"

    @allure.step("SetUp: calling registered customer and adding USD to balance.")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id = 1011
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.locators = MainScreenPage().locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 7, 5)  # LTC
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 10000.0)  # USD

    @allure.step("Starting with: test_quick_instrument_panel_updated_after_trade")
    @automation_logger(logger)
    def test_quick_instrument_panel_updated_after_trade(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(self.test_case))
        delay = 10.0
        logger.logger.info("method test_quick_instrument_panel_updated_after_trade , with browser {0}".format(self.browser))
        result = 0

        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)

            usd_title_menu = self.browser.wait_element_presented(self.driver, LimitOrderPanelPage().locators.USD,
                                                                 delay)
            self.browser.click_on_element(usd_title_menu)
            usd_from_dropdown = self.browser.wait_element_presented(
                self.driver, MarketOrderPanelPage().locators.USD_OPTION_FROM_USD_DROPDOWN, delay)
            self.browser.click_on_element(usd_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1011]').click()''')
            time.sleep(5.0)
            assert self.browser.wait_element_presented(
                self.driver, MarketOrderPanelPage().locators.LTC_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL, delay + 5)

            price_1 = Instruments.get_price_last_trade(self.instrument_id)
            quantity = Instruments.get_min_order_amount(self.instrument_id)
            order_limit_1 = Order().set_order(2, self.instrument_id, quantity, price_1)
            order_response_1 = self.customer.postman.order_service.create_order_sync(order_limit_1)
            assert order_response_1['error'] is None

            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 1)
            price = best_price_and_quantity[0]
            order_limit_buy = Order().set_order(1, self.instrument_id, quantity, price)
            order_response = self.customer.postman.order_service.create_order(order_limit_buy)
            order_status = order_response['result']['status']

            assert order_status

            time.sleep(10.0)
            base_rate_quick_panel = self.browser.wait_element_presented(
                self.driver, self.locators.BASE_RATE_QUICK_PANEL, delay).get_attribute('innerText')
            emphasis_rate_quick_panel = self.browser.wait_element_presented(
                self.driver, self.locators.EMPHASIS_RATE_QUICK_PANEL, delay).get_attribute('innerText')
            price_quick_panel = base_rate_quick_panel + emphasis_rate_quick_panel
            base_rate_order_book = self.browser.wait_element_presented(
                self.driver, self.locators.BASE_RATE_ORDER_BOOK, delay).get_attribute('innerText')
            emphasis_rate = self.browser.wait_element_presented(
                self.driver, self.locators.EMPHASIS_RATE, delay).get_attribute('innerText')
            price_order_book = base_rate_order_book + emphasis_rate
            prise_from_last_trades = self.browser.find_elements(
                self.driver, self.locators.PRICES_FROM_LAST_TRADES_LIST)[0].get_attribute('innerText')
            price_last_trade_redis = RedisDb.get_price_last_trade(self.instrument_id)
            volume_24_quick_panel_after_trade = float(self.browser.wait_element_presented(
                self.driver, self.locators.VOLUME_24_QUICK_PANEL, delay).get_attribute('innerText'))
            change_24_quick_panel = (self.browser.wait_element_presented(
                self.driver, self.locators.CHANGE_24_QUICK_PANEL, delay).get_attribute('innerText'))
            high_24_quick_panel = (self.browser.wait_element_presented(
                self.driver, self.locators.HIGH_24_QUICK_PANEL, delay).get_attribute('innerText'))
            low_24_quick_panel = (self.browser.wait_element_presented(
                self.driver, self.locators.LOW_24_QUICK_PANEL, delay).get_attribute('innerText'))

            assert price == float(price_quick_panel) == float(price_order_book) == float(
                prise_from_last_trades) == price_last_trade_redis
            assert change_24_quick_panel != "..."
            assert high_24_quick_panel != "..."
            assert low_24_quick_panel != "..."
            assert volume_24_quick_panel_after_trade != "..."

            logger.logger.info("Test {0}, with CustomerID {1}".format(self.test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, self.test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
