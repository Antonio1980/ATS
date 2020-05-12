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

test_case = '6923'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    UI test.
    Amount verification against Available Funds Negative, UI
    1. Open WTP
    2. Select an instrument(1049).
    3. Enter an amount of based currency - "Estimate Price" * "Amount" must exceed the available funds 
       and try to send order. 
    4. Verify that order is rejected.
    5. Enter an amount of quoted currency - it must exceed the available funds and try to send order
    6. Verify that order is rejected.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Amount verification against Available Funds (Negative)')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6923_amount_verification_against_available_funds_test.py",
    "TestAmountVerificationAgainstAvailableFunds")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestAmountVerificationAgainstAvailableFunds(unittest.TestCase):
    @allure.step("SetUp:  sitting new customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.instrument_id = 1049
        self.customer.clean_instrument(self.instrument_id)
        self.price_origin = Instruments.get_price_last_trade(self.instrument_id)
        Instruments.set_price_last_trade(self.instrument_id, 5)
        Instruments.set_ticker_last_price(self.instrument_id, 5)
        self.customer.clean_up_customer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_amount_verification_against_available_funds")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_amount_verification_against_available_funds(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info(
            "method test_amount_verification_against_available_funds , "
            "with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            enter_amount = Instruments.get_min_order_amount(self.instrument_id)
            estimated_price = Instruments.get_price_last_trade(self.instrument_id)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 2000)
            order_limit_buy = Order().set_order(1, self.instrument_id, enter_amount, estimated_price - 1)
            order_response_buy = self.customer.postman.order_service.create_order_sync(order_limit_buy)
            time.sleep(3.0)
            assert order_response_buy['error'] is None

            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 16, 2000)
            order_limit_sell = Order().set_order(2, self.instrument_id, enter_amount, estimated_price + 1)
            order_response = self.customer.postman.order_service.create_order_sync(order_limit_sell)
            time.sleep(3.0)
            assert order_response['error'] is None
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            time.sleep(delay)

            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1049]').click()''')
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.ENG_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 16, 200)
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 2000)
            time.sleep(delay)
            available_for_buy_before = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_buy_before = float(re.sub(',', '', available_for_buy_before))
            enter_price_buy = float(self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ))
            enter_amount = round((available_for_buy_before / enter_price_buy) + (
                    (available_for_buy_before / enter_price_buy) * 0.1))
            enter_amount_buy_field = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_BUY,
                                                                         delay)
            self.browser.send_keys(enter_amount_buy_field, enter_amount)
            buy_button = self.browser.wait_element_presented(self.driver, self.locators.BUY_BUTTON, delay)
            self.browser.click_on_element(buy_button)
            time.sleep(5)

            available_for_buy_after = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_buy_after = float(re.sub(',', '', available_for_buy_after))
            available_for_sell_before = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            available_for_sell_before = float(re.sub(',', '', available_for_sell_before))
            enter_amount_sell = str(
                round(available_for_sell_before + (available_for_sell_before * 0.11)))
            enter_amount_sell_field = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_SELL,
                                                                          delay)
            self.browser.send_keys(enter_amount_sell_field, enter_amount_sell)
            sell_button = self.browser.wait_element_presented(self.driver, self.locators.SELL_BUTTON, delay)
            self.browser.click_on_element(sell_button)
            time.sleep(3)

            available_for_sell_after = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            available_for_sell_after = float(re.sub(',', '', available_for_sell_after))
            assert available_for_buy_before == available_for_buy_after
            assert available_for_sell_before == available_for_sell_after
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            Instruments.set_price_last_trade(self.instrument_id, self.price_origin)
            Instruments.set_ticker_last_price(self.instrument_id, self.price_origin)
            result = 1

        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
