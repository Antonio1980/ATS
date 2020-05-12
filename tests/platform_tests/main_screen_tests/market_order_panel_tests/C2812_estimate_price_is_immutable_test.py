import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '2812'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    UI test.
    Verified that "Estimate Price" can't be modified manually, UI
    1. Select an instrument(ETH/EUR).
    2. Try to edit the "Estimate price" presented on the "Buy" button .
    3. Try to edit the "Estimate price" presented on the "Sell" button. 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Available for trading" funds presentation')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2812_estimate_price_is_immutable_test.py",
                 "TestEstimatePriceIsImmutable")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.market_order
@pytest.mark.order_management
@ddt
class TestEstimatePriceIsImmutable(unittest.TestCase):
    @allure.step("Starting with:SetUp:  calling registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_estimate_price_is_immutable")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_estimate_price_is_immutable(self, browser):
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
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1022]').click()''')
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.DXCASH_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            estimated_price_buy = self.browser.wait_element_presented(self.driver,
                                                                      self.locators.ESTIMATED_PRICE_FOR_BUY_MARKET,
                                                                      delay)
            estimated_price_sell = self.browser.wait_element_presented(self.driver,
                                                                       self.locators.ESTIMATED_PRICE_FOR_SELL_MARKET,
                                                                       delay)
            self.assertTrue(self.browser.possibility_to_send_keys(estimated_price_buy, "3456"))
            self.assertTrue(self.browser.possibility_to_send_keys(estimated_price_sell, "3456"))
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    def tearDown(self):
        Browser.close_browser(self.driver)
