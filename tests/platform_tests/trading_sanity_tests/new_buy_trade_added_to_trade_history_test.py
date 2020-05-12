import time
import unittest

import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.enums import Browsers
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage
from tests.platform_tests_base.signin_page import SignInPage


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST 'TS- 9'")
@allure.description("""
    Verify that new created trades are presented in Trades History.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_sanity_tests/new_buy_trade_added_to_trade_history_test.py",
                 "TestNewBuyTradeIsAddedToTradeHistory")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.trading_sanity
class TestNewBuyTradeIsAddedToTradeHistory(unittest.TestCase):
    test_case = "TS- 9"

    @allure.step("SetUp: calling registered customer and adding EUR and BTC to balance.")
    @automation_logger(logger)
    def setUp(self):
        self.instrument_id = 1012
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 80000)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 10)
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_new_buy_trades_is_added_to_trade_history")
    @automation_logger(logger)
    def test_new_sell_trade_is_added_to_trade_history(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(self.test_case))
        logger.logger.info("method test_new_buy_trade_is_added_to_trade_history")
        delay = 10.0
        result = 0
        price_1 = Instruments.get_price_last_trade(self.instrument_id)
        quantity = Instruments.get_min_order_amount(self.instrument_id)
        order_limit_1 = Order().set_order(2, self.instrument_id, quantity, price_1)
        order_response_1 = self.customer.postman.order_service.create_order_sync(order_limit_1)
        assert order_response_1['error'] is None
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)

            price_buy = float(Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 1)[0])
            order_limit_buy = Order().set_order(1, self.instrument_id, quantity, price_buy)
            order_response_buy = self.customer.postman.order_service.create_order_sync(order_limit_buy)
            assert order_response_buy['error'] is None
            order_id_buy = order_response_buy['result']['orderId']

            time.sleep(10.0)
            trade_id = \
                Instruments.run_mysql_query("SELECT id FROM trades_crypto WHERE orderId = " + order_id_buy + ";")[0][0]
            self.browser.execute_js(self.driver,
                                    '''$("[id='dxPackageContainer_dx_positions'] div[class='positionsTab_tradesHistory last'] div[class='bgStart']").click()''')
            time.sleep(3.0)
            expand_button = self.browser.wait_element_presented(self.driver,
                                                                LimitOrderPanelPage().locators.EXPAND_BUTTON, delay)
            self.browser.click_on_element(expand_button)
            time.sleep(5)

            price_from_ui_buy = self.browser.wait_element_presented(self.driver,
                                                                    "//*[@id ='tradesHistoryPosition_" + str(trade_id) +
                                                                    "_0']/td[@class ='price']/span",
                                                                    delay).get_attribute('innerText').replace(',', '')
            assert self.browser.wait_element_presented(self.driver, "//span[contains(.,'" + order_id_buy + "')]",
                                                       delay), "Order Id is not on the UI"
            assert self.browser.wait_element_presented(self.driver, "//span[contains(.,'" + str(trade_id) + "')]",
                                                       delay), "Trade Id is not on the UI"
            assert price_buy == float(price_from_ui_buy)

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
