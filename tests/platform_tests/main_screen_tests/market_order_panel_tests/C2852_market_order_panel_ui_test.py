import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '2852'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    UI test.
    Market Order Panel - UI verification, UI
    1. Open WTP
    2.Verified that the "Buy" section contains the following :
        a. "Available for trading" funds in quoted currency
        b. Green "Buy" button with estimated price
        c. "Enter Amount" field - the default value is "0"
        d. "Amount" value converted to USD (below the "amount" field)
        e. Percentage Selector (15%, 25%, 35%, 50%)
    3. Verified that the "Sell" section contains the following :
        a. "Available for trading" funds in base currency
        b. Red "Sell" button with estimated price 
        c. "Enter Amount" field - the default value is "0"
        d. "Amount" value converted to USD (below the "amount" field)
        e. Percentage Selector (15%, 25%, 35%, 50%)
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Market Order Panel - UI verification')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2852_market_order_panel_ui_test.py",
                 "TestMarketOrderPanelUi")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.market_order
@pytest.mark.order_management
@ddt
class TestMarketOrderPanelUi(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer.")
    @automation_logger(logger)
    def setUp(self):

        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_market_order_panel")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_market_order_panel(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        result = 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            assert self.browser.wait_element_presented(self.driver, self.locators.MARKET_TAB, delay)
            self.browser.execute_js(self.driver, '''$("div[class='tradeType market']").click()''')
            assert self.browser.wait_element_presented(self.driver, self.locators.AVAILABLE_FOR_TRADING_FUNDS_BUY,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.BUY_BUTTON, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.ENTER_AMOUNT_WITH_DEFAULT_0_BUY,
                                                       delay)
            assert self.browser.wait_element_presented(
                self.driver, self.locators.MINIMUM_ORDER_AMOUNT_MESSAGE_UNDER_ENTER_AMOUNT_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_15_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_25_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_35_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_50_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.SELL_BUTTON, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.ENTER_AMOUNT_WITH_DEFAULT_0_SELL,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.AVAILABLE_FOR_TRADING_FUNDS_SELL,
                                                       delay)
            assert self.browser.wait_element_presented(
                self.driver, self.locators.MINIMUM_ORDER_AMOUNT_MESSAGE_UNDER_ENTER_AMOUNT_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_15_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_25_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_35_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_50_SELL, delay)
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
