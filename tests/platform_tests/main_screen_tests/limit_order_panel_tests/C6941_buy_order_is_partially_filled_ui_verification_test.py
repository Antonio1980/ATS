import time
import unittest

import allure
import pytest
from ddt import ddt, data, unpack

from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage
from tests.platform_tests_base.signin_page import SignInPage

test_case = '6941'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    Pre - condition: Market Makers need to be stopped
    UI test.  
    "Buy" Order Is Partially Filled - UI Verification
    1. Open WTP
    2. Select an instrument(1014).
    3. Place a new "Buy" order with price between the first and the second price from Order Book .
    4. Verify that Order is presented in UI
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Buy" Order Is Partially Filled - UI Verification')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6941_buy_order_is_partially_filled_ui_verification_test.py",
    "TestBuyOrderIsPartiallyFilledUiVerification")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestBuyOrderIsPartiallyFilledUiVerification(unittest.TestCase):
    @allure.step("SetUp:  sitting new customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.instrument_id = 1014
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 800000)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_buy_order_is_partially_filled_ui_verification")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_buy_order_is_partially_filled_ui_verification(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info(
            "method test_buy_order_is_partially_filled_ui_verification"
            "with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            self.price_origin = Instruments.get_price_last_trade(self.instrument_id)
            Instruments.set_price_last_trade(self.instrument_id, 5)
            Instruments.set_ticker_last_price(self.instrument_id, 5)
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            assert self.browser.wait_element_presented(self.driver, self.locators.USD, delay+10.0)
            self.browser.execute_js(self.driver,
                                    '''$('li[data-instrumentId=''' + str(self.instrument_id) + ''']').click()''')
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.XRP_EUR_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            time.sleep(5)

            quantity_tail_digits = Instruments.get_quantity_tail_digits(self.instrument_id)
            price_tail_digits = Instruments.get_price_tail_digits(self.instrument_id)

            price_1 = Instruments.get_price_last_trade(self.instrument_id)
            quantity = Instruments.get_min_order_amount(self.instrument_id)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 6, quantity + 6)
            order_limit_1 = Order().set_order(2, self.instrument_id, quantity + 5, price_1)
            order_response_1 = self.customer.postman.order_service.create_order(order_limit_1)
            order_status_1 = order_response_1['result']['status']
            assert order_status_1

            price_2 = round((price_1 + (price_1 * 0.2)), price_tail_digits)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 6, quantity + 20)
            order_limit_2 = Order().set_order(2, self.instrument_id, quantity + 16, price_2)
            order_response_2 = self.customer.postman.order_service.create_order(order_limit_2)
            order_status_2 = order_response_2['result']['status']
            assert order_status_2

            price_and_quantity = Instruments.get_orders_best_price_and_quantity(self.instrument_id, "buy", 2)
            if quantity_tail_digits == 0:
                quantity = round((price_and_quantity[0][1] + price_and_quantity[1][1]) / 2)
            else:
                quantity = round((price_and_quantity[0][1] + price_and_quantity[1][1]) / 2,
                                 quantity_tail_digits)
            price = round((price_and_quantity[0][0] + price_and_quantity[1][0]) / 2, price_tail_digits)
            order_buy = Order().set_order(1, self.instrument_id, quantity, price)
            order_response = self.customer.postman.order_service.create_order(order_buy)
            order_status = order_response['result']['status']
            assert order_status
            time.sleep(3)
            data_query = ("SELECT id, price FROM orders WHERE customerId = " + str(self.customer.customer_id) +
                          " and direction = 'buy' ORDER BY orders.dateInserted DESC limit 1;")
            data_order = Instruments.run_mysql_query(data_query)
            order_id = str(data_order[0][0])
            price_db = float(data_order[0][1])
            self.browser.execute_js(self.driver,
                                    '''$("[id='dxPackageContainer_dx_positions'] div[class='positionsTab_ordersHistory'] div[class='bgStart']").click()''')
            time.sleep(2)
            expand_button = self.browser.wait_element_presented(self.driver, self.locators.EXPAND_BUTTON, delay)
            self.browser.click_on_element(expand_button)
            time.sleep(10)
            assert self.browser.wait_element_presented(self.driver, "//span[contains(.,'" + order_id + "')]", delay)
            price_from_ui = self.browser.wait_element_presented(self.driver,
                                                                "//*[@id ='ordersHistoryPosition_" + order_id + "_0']/td[@class ='price']/span",
                                                                delay).get_attribute('innerText')
            filled_quantity_ui = self.browser.find_element(self.driver,
                                                           "//*[@id ='ordersHistoryPosition_" + order_id + "_0']/td[@class ='filled']/span").get_attribute(
                'innerText')
            filled_quantity = round((price_and_quantity[0][1] / quantity) * 100, 2)
            assert price_db == float(price_from_ui)
            assert float(filled_quantity_ui[:-1]) == filled_quantity
            Instruments.set_price_last_trade(self.instrument_id, self.price_origin)
            Instruments.set_ticker_last_price(self.instrument_id, self.price_origin)
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    def tearDown(self):
        Browser.close_browser(self.driver)
