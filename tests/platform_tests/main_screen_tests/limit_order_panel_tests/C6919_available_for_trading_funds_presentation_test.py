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
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage

test_case = "6919"


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    UI test.
    "Available for trading" funds presentation , UI
    1. Open WTP
    2. Select an instrument(1023).
    3. Check  available funds in "Buy" section are presented in quoted currency .
    4. Check  available funds in "Sell" section are presented in base currency. 
    5. Open the "Funds" section, find the base and the quoted currencies
    6. Compare available funds from Buy/Sell section to available funds from 'Funds' section 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Available for trading" funds presentation')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/limit_order_panel_tests/C6919_available_for_trading_funds_presentation_test.py",
                 "TestAvailableForTradingFundsPresentation")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestAvailableForTradingFundsPresentation(unittest.TestCase):
    @allure.step("SetUp:  sitting new customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.customer.clean_up_customer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_availability_for_trading_funds_presentation")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_availability_for_trading_funds_presentation(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_availability_for_trading_funds_presentation "
                           "with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)

            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            eur_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.EUR_OPTION_FROM_USD_DROPDOWN,
                                                                    delay)
            self.browser.click_on_element(eur_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1023]').click()''')

            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.DXCASH_EUR_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 8, 100)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 1000)
            time.sleep(3)
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.EUR_CURRENCY_FOR_AVAILABLE_TRADING_BUY,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.DXCASH_CURRENCY_FOR_AVAILABLE_TRADING_SELL,
                                                       delay)
            available_for_trading_buy = self.browser.execute_js(self.driver,
                                                                self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_trading_sell = self.browser.execute_js(self.driver,
                                                                 self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            funds_button = self.browser.wait_element_presented(self.driver, self.locators.FUNDS_BUTTON, delay)
            self.browser.click_on_element(funds_button)

            available_for_trading_eur_funds = self.browser.execute_js(self.driver,
                                                                      self.locators.EUR_AVAILBLE_FUNDS_PAGE_JQ)

            available_for_trading_btc_funds = self.browser.execute_js(self.driver,
                                                                      self.locators.BTC_AVAILABLE_FUNDS_PAGE_JQ)

            assert available_for_trading_buy == available_for_trading_eur_funds[1:]
            assert available_for_trading_sell == available_for_trading_btc_funds
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    def tearDown(self):
        Browser.close_browser(self.driver)
