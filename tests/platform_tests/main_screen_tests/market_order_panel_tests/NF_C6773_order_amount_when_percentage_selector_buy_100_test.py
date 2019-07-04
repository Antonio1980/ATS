# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import time
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage


@ddt
class VerificationOfOrderAmountWhenPercentageSelectorTest(unittest.TestCase):
    test_case = '6773'

    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 8, 50)  # LTC
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_verification_of_order_amount_when_percentage_selector_buy(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver)
            step2 = self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1011]').click()''')
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.LTC_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            time.sleep(2)
            step3 = True
            available_for_trading_buy_jq = self.browser.execute_js(self.driver,
                                                                   self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_trading_buy = round(((float(re.sub(',', '', available_for_trading_buy_jq))) * (1 - 0.0025)),
                                              2)
            one_hundred_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_50_BUY,
                                                                         delay)
            self.browser.click_on_element(one_hundred_percentage)
            available_for_trading_without_buffer_jq = float(
                self.browser.execute_js(self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_AFTER_BUFFER))
            if available_for_trading_buy == available_for_trading_without_buffer_jq:
                step4 = True
        finally:
            if step1 and step2 and step3 and step4 is True:
                logger.logger.info("Test " + self.test_case + " , with CustomerID " + self.customer.customer_id +
                                   "=================TEST IS PASSED==========================")
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                logger.logger.error("Test " + self.test_case + " , with CustomerID " + self.customer.customer_id +
                                    "=================TEST IS NOT PASSED==========================")
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
