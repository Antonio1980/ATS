import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '2782'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    UI test.
    "Available for trading" funds presentation , UI
    1. Open WTP
    2. Select an instrument(ETH/EUR).
    3. Check  available funds in "Buy" section are presented in quoted currency .
    4. Check  available funds in "Sell" section are presented in base currency. 
    5. Open the "Funds" section, find the base and the quoted currencies
    6. Compare available funds from Buy/Sell section to available funds from 'Funds' section 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Available for trading" funds presentation')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2782_availability_of_funds_presentation_test.py",
                 "TestAvailabilityOfFundsPresentation")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.market_order
@pytest.mark.order_management
@ddt
class TestAvailabilityOfFundsPresentation(unittest.TestCase):
    @allure.step("SetUp:  sitting new customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer.customer_registration()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 4, 10)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 10)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_availability_of_funds_presentation")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_availability_of_funds_presentation(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
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
            eur_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.EUR_OPTION_FROM_USD_DROPDOWN,
                                                                    delay)
            self.browser.click_on_element(eur_from_dropdown)

            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1013]').click()''')

            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.ETH_EUR_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            time.sleep(5)

            available_for_trading_buy = self.browser.execute_js(self.driver,
                                                                self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)

            available_for_trading_sell = self.browser.execute_js(self.driver,
                                                                 self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            funds_button = self.browser.wait_element_presented(self.driver, self.locators.FUNDS_BUTTON, delay)
            self.browser.click_on_element(funds_button)
            available_for_trading_eur_funds = self.browser.execute_js(
                self.driver, self.locators.EUR_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE_JQ)

            available_for_trading_eur_funds = available_for_trading_eur_funds[1:]
            available_for_trading_eth_funds = self.browser.execute_js(
                self.driver, self.locators.ETH_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE_JQ)
            self.assertTrue(
                available_for_trading_buy == available_for_trading_eur_funds and available_for_trading_sell
                == available_for_trading_eth_funds)

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    def tearDown(self):
        Browser.close_browser(self.driver)
