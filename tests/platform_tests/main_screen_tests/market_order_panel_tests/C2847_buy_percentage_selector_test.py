import re
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

test_case = '2847'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    UI test.
    Market Order Panel - UI verification, UI
    1.Open WTP, Market Panel
    2.Click on "15%" in the "Buy" section / Expected result: The value presented in the "amount" field can be bought 
        for 15% of customer's "Available for trading" funds 
    3.Click on "25%" in the "Buy" section / Expected result: The value presented in the "amount" field can be bought 
        for 25% of customer's "Available for trading" funds 
    4.Click on "50%" in the "Buy" section / The value presented in the "amount" field can be bought for 50%
        of customer's "Available for trading" funds 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Percentage Selector - "Buy"')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2847_buy_percentage_selector_test.py",
                 "TestBuyPercentageSelector")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.market_order
@pytest.mark.order_management
@ddt
class TestBuyPercentageSelector(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 10, 10500)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_buy_percentage_selector")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_buy_percentage_selector(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        result = 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            assert self.browser.wait_element_presented(self.driver, self.locators.MARKET_TAB, delay)
            self.browser.execute_js(self.driver, '''$("div[class='tradeType market']").click()''')
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1056]').click()''')

            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.DXCASH_JPY_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            available_buy_jq = self.browser.execute_js(self.driver,
                                                       self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_buy = float(re.sub(',', '', available_buy_jq))
            fifteen_percentage = self.browser.wait_element_presented(self.driver,
                                                                     self.locators.PERCENTAGE_SELECTOR_15_BUY,
                                                                     delay)
            twenty_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_25_BUY,
                                                                         delay)
            thirty_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_35_BUY,
                                                                         delay)
            self.browser.click_on_element(fifteen_percentage)
            estimated_price_jq_15 = self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_BUY_JQ)
            amount_fifteen = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_fifteen = round(
                (float(available_buy) / 100 * 15) / float(estimated_price_jq_15), 2)
            assert amount_fifteen == expected_fifteen

            self.browser.click_on_element(twenty_five_percentage)
            estimated_price_jq_25 = self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_BUY_JQ)
            amount_twenty_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_twenty_five = round((float(available_buy) / 100 * 25) / float(estimated_price_jq_25), 2)
            assert amount_twenty_five == expected_twenty_five

            self.browser.click_on_element(thirty_five_percentage)
            estimated_price_jq_35 = self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_BUY_JQ)
            amount_thirty_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_thirty_five = round(
                (float(available_buy) / 100 * 35) / float(estimated_price_jq_35), 2)
            assert amount_thirty_five == expected_thirty_five
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
