import allure
import pytest
import unittest
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
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage

test_case = '6937'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    UI test.
    Limit Order Panel - UI verification, UI
    1. Open WTP
    2.Verified that the "Buy" section contains the following :
        a. "Available for trading" funds in quoted currency
        b. Green "Buy" button with estimated price
        c. "Enter Amount" field - the default value is "0"
        d. "Amount" value converted to USD (below the "amount" field)
        e. Percentage Selector (25%, 50%, 75%, 100%)
        f. Green "Plus" and "Minus" buttons
    3. Verified that the "Sell" section contains the following :
        a. "Available for trading" funds in base currency
        b. Red "Sell" button with estimated price 
        c. "Enter Amount" field - the default value is "0"
        d. "Amount" value converted to USD (below the "amount" field)
        e. Percentage Selector (25%, 50%, 75%, 100%)
        f. Red "Plus" and "Minus" buttons
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Limit Order Panel - UI verification')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6937_limit_order_panel_ui_verification_test.py",
                 "TestLimitOrderPanelUiVerification")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestLimitOrderPanelUiVerification(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_limit_order_panel_ui_verification")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_limit_order_panel_ui_verification(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_limit_order_panel_ui_verification with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)

            assert self.browser.wait_element_presented(self.driver, self.locators.AVAILABLE_FOR_TRADING_FUNDS_BUY,
                                                       delay + 10.0)
            assert self.browser.wait_element_presented(self.driver, self.locators.BUY_BUTTON, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.ENTER_AMOUNT_WITH_DEFAULT_0_BUY,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.MIN_AMOUNT_MESSAGE_UNDER_ENTER_AMOUNT_BUY,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_25_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_50_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_75_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_100_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.SELL_BUTTON, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.ENTER_AMOUNT_WITH_DEFAULT_0_SELL,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.AVAILABLE_FOR_TRADING_FUNDS_SELL,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.MIN_AMOUNT_MESSAGE_UNDER_ENTER_AMOUNT_SELL,
                                                       delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_25_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_50_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_75_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.PERCENTAGE_SELECTOR_100_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.INCREASES_STEP_BUTTON_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.INCREASES_STEP_BUTTON_SELL, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.DECREASES_STEP_BUTTON_BUY, delay)
            assert self.browser.wait_element_presented(self.driver, self.locators.DECREASES_STEP_BUTTON_SELL, delay)
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
