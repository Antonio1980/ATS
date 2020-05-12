import time
import allure
import pytest
import unittest
from src.base import logger
from src.base.enums import Browsers
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST 'TS- 15'")
@allure.description("""
    Verify that unmatched order presented into Open Orders.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_sanity_tests/unmatched_order_added_to_open_orders_test.py",
                 "TestUnmatchedOrderAddedToOpenOrders")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.trading_sanity
class TestUnmatchedOrderAddedToOpenOrders(unittest.TestCase):
    test_case = "TS- 15"

    @allure.step("SetUp: calling registered customer and adding USD and LTC to balance.")
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
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 1000)  # USD
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 7, 5)  # LTC

    @allure.step("Starting with: test_unmatched_order_added_to_open_orders")
    @automation_logger(logger)
    def test_unmatched_order_added_to_open_orders(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(self.test_case))
        delay = 5
        result = 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)

            price_1 = Instruments.get_price_last_trade(self.instrument_id)
            quantity = Instruments.get_min_order_amount(self.instrument_id)
            order_limit_1 = Order().set_order(2, self.instrument_id, quantity, price_1)
            order_response_1 = self.customer.postman.order_service.create_order_sync(order_limit_1)
            assert order_response_1['error'] is None

            order_limit_1 = Order().set_order(1, self.instrument_id, quantity, price_1-1.0)
            order_response_1 = self.customer.postman.order_service.create_order_sync(order_limit_1)
            assert order_response_1['error'] is None

            # for BUY
            best_price_from_order_book_buy = float(
                round(Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 1)[0]))
            price_buy = best_price_from_order_book_buy - best_price_from_order_book_buy * 0.10
            quantity = 1
            order_limit_buy = Order().set_order(1, self.instrument_id, quantity, price_buy)
            order_response_buy = self.customer.postman.order_service.create_order(order_limit_buy)
            order_status_buy = order_response_buy['result']['status']

            assert order_status_buy
            external_order_id_buy = order_response_buy['result']['externalOrderId']

            time.sleep(3)
            open_orders_buy = self.customer.postman.order_service.get_open_orders()
            order_id_buy = open_orders_buy['result']['orders'][-1]['id']
            external_order_id_buy_ = open_orders_buy['result']['orders'][-1]['externalOrderId']
            expand_button = self.browser.wait_element_presented(
                self.driver, LimitOrderPanelPage().locators.EXPAND_BUTTON, delay)
            self.browser.click_on_element(expand_button)

            time.sleep(5)
            price_from_ui_buy = self.browser.wait_element_presented(
                self.driver, "//*[@id ='ordersOpenPosition_" + order_id_buy + "_0']/td[@class ='price']/span",
                delay).get_attribute('innerText')

            assert self.browser.wait_element_presented(self.driver, "//span[contains(.,'" + order_id_buy + "')]", delay)
            assert external_order_id_buy == external_order_id_buy_ and price_buy == float(price_from_ui_buy)

            # for BUY
            best_price_from_order_book_sell = float(
                round(Instruments.get_orders_best_price_and_quantity(self.instrument_id, "sell", 1)[0]))
            price_sell = best_price_from_order_book_sell + best_price_from_order_book_sell * 0.10
            quantity = 1
            order_limit_sell = Order().set_order(2, self.instrument_id, quantity, price_sell)
            order_response_sell = self.customer.postman.order_service.create_order(order_limit_sell)
            order_status_sell = order_response_sell['result']['status']

            assert order_status_sell

            external_order_id_sell_ = order_response_sell['result']['externalOrderId']

            time.sleep(3)
            open_orders_sell = self.customer.postman.order_service.get_open_orders()
            order_id_sell = open_orders_sell['result']['orders'][-1]['id']
            external_order_id_sell = open_orders_sell['result']['orders'][-1]['externalOrderId']

            time.sleep(2)
            price_from_ui_sell = self.browser.wait_element_presented(
                self.driver, "//*[@id ='ordersOpenPosition_" + order_id_sell + "_0']/td[@class ='price']/span",
                delay).get_attribute('innerText')

            assert self.browser.wait_element_presented(self.driver, "//span[contains(.,'" + order_id_sell + "')]",
                                                       delay)
            assert external_order_id_sell == external_order_id_sell_
            assert price_sell == float(price_from_ui_sell)

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
