import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '7322'


@pytest.mark.skip(reason="no way of currently testing this")
@allure.title("API BALANCE")
@allure.description("""
    Functional test. UI.
    Validation of 'frozen' balance after matched "Sell" Limit order via UI.
    1. Checking of 'frozen' balance before orders.
    2. Place 'Sell' Limit order.      
    4. Checking of'frozen' balances after orders. 
    Calculation: frozen_balance = frozen_balance_before
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + '/index.php?/cases/view/' + test_case,
             name='Market Sell Order Matched - Balance Unfrozen')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7322_market_sell_order_matched_balance_unfrozen_test.py",
                 "TestMarketSellOrderMatchedBalanceUnfrozen")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
@ddt
class MarketSellOrderMatchedBalanceUnfrozenTest(unittest.TestCase):
    @allure.step("SetUp: sitting new customer and adding EUR to balance.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 4, 200)
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()
        self.instrument_id = 1013

    @allure.step("Starting with: test_market_sell_order_matched_balance_unfrozen_ui")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_market_sell_order_matched_balance_unfrozen_ui(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_market_sell_order_matched_balance_unfrozen with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        result = 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in.sign_in(self.driver, self.customer.email, self.customer.password)
            time.sleep(delay)
            order_quantity = float(
                Instruments.run_mysql_query(
                    "SELECT minOrderQuantity FROM instruments WHERE id=" + str(self.instrument_id) + ";")[0][0])
            funds_button = self.browser.wait_element_presented(self.driver, self.locators.FUNDS_BUTTON, delay)
            self.browser.click_on_element(funds_button)
            time.sleep(5)
            frozen_balance_before = self.browser.execute_js(self.driver, self.locators.EUR_FROZEN_BALANS_FUNDS_PAGE_JQ)
            order_market_buy = Order().set_order(2, self.instrument_id, order_quantity)

            for i in range(30):
                time_ = time.time() + 250
                order_response = self.customer.postman.order_service.create_order(order_market_buy)
                order_status = order_response['result']['status']
                assert order_status is True

                time.sleep(delay - 2)
                frozen_balance = self.browser.execute_js(self.driver,
                                                         self.locators.EUR_FROZEN_BALANS_FUNDS_PAGE_JQ)
                while frozen_balance != frozen_balance_before and time_ > time.time():
                    frozen_balance = self.browser.execute_js(self.driver, self.locators.EUR_FROZEN_BALANS_FUNDS_PAGE_JQ)
                assert frozen_balance == frozen_balance_before

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
