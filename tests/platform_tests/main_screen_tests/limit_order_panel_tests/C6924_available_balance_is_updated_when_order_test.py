import re
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

test_case = '6924'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    UI test.
    Available Balance is Updated when Order is sent, UI
    1. Open WTP
    2. Select an instrument(1023).
    3. Check available balance for trading on the panel before trade
    4. Send Buy Order.
    5. Check available balance for trading on the panel after trade
    6. Verify that available after trade equal available calculation .
    Calculation: truncate for balance where tail digits = 2
    int((float(available_before) - (enter_amount * float(estimated_price)))*100)/100.0
    
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Available Balance" is updated when order is sent.')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/limit_order_panel_tests/C6924_available_balance_is_updated_when_order_test.py",
                 "TestAvailableBalanceIsUpdatedWhenOrderIsSent")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestAvailableBalanceIsUpdatedWhenOrderIsSent(unittest.TestCase):
    @allure.step("SetUp:  sitting new customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):

        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.customer.clean_up_customer()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()
        self.instrument_id = 1023
        self.customer.clean_instrument(self.instrument_id)
        self.customer.clean_up_customer()
        self.price_origin = Instruments.get_price_last_trade(self.instrument_id)
        Instruments.set_price_last_trade(self.instrument_id, 3)
        Instruments.set_ticker_last_price(self.instrument_id, 3)

    @allure.step("Starting with: test_available_balance_is_updated_when_order_is_sent")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_available_balance_is_updated_when_order_is_sent(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info(
            "method test_available_balance_is_updated_when_order_is_sent"
            "with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            Instruments.set_price_last_trade(self.instrument_id, 3)
            Instruments.set_ticker_last_price(self.instrument_id, 3)
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)

            eur_from_dropdown = self.browser.wait_element_presented(
                self.driver, self.locators.EUR_OPTION_FROM_USD_DROPDOWN, delay)
            self.browser.click_on_element(eur_from_dropdown)

            self.browser.execute_js(self.driver,
                                    '''$('li[data-instrumentId=''' + str(self.instrument_id) + ''']').click()''')

            assert self.browser.wait_element_presented(
                self.driver, self.locators.DXCASH_EUR_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL, delay + 5)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 2, 100)  # EUR
            time.sleep(7)
            available_before = self.browser.execute_js(self.driver,
                                                       self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_before = float(re.sub(',', '', available_before))

            enter_amount = Instruments.get_min_order_amount(self.instrument_id)
            estimated_price = Instruments.get_price_last_trade(self.instrument_id)

            self.price_origin = Instruments.get_price_last_trade(self.instrument_id)

            order_limit_buy = Order().set_order(1, self.instrument_id, enter_amount, estimated_price)
            order_response = self.customer.postman.order_service.create_order(order_limit_buy)
            time.sleep(3.0)
            order_status = order_response['result']['status']
            assert order_status is True
            time.sleep(4)

            available_after = float(self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ))
            available_calculation = round(available_before - (enter_amount * float(estimated_price)), 2)
            assert available_after == available_calculation
            logger.logger.info("available_after {0} == available_calculation{1}".format(available_after,
                                                                                        available_calculation))
            Instruments.set_price_last_trade(self.instrument_id, self.price_origin)
            Instruments.set_ticker_last_price(self.instrument_id, self.price_origin)
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
