# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
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
class SellPercentageSelectorTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '2849'
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.postman.balance_service.add_balance(int(self.customer.customer_id), 7, 1050)  # LTC currency
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_sell_percentage_selector(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6, step7 = False, False, False, False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver)
            step2 = self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1035]').click()''')
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.LTC_DXCASH_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            step3 = True
            available_for_trading_sell_jq = self.browser.execute_js(self.driver,
                                                                    self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            available_for_trading_sell = float(re.sub(',', '', available_for_trading_sell_jq))
            twenty_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_15_SELL,
                                                                         delay)
            fifty_percentage = self.browser.wait_element_presented(self.driver,
                                                                   self.locators.PERCENTAGE_SELECTOR_25_SELL, delay)
            seventy_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                          self.locators.PERCENTAGE_SELECTOR_35_SELL,
                                                                          delay)
            one_hundred_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_50_SELL,
                                                                         delay)
            self.browser.click_on_element(twenty_five_percentage)
            amount_twenty_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_twenty_five = (float(available_for_trading_sell) / 100 * 15)
            if amount_twenty_five == expected_amount_twenty_five:
                step4 = True
            self.browser.click_on_element(fifty_percentage)
            amount_fifty = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_fifty = (float(available_for_trading_sell) / 100 * 20)
            if amount_fifty == expected_amount_fifty:
                step5 = True
            self.browser.click_on_element(seventy_five_percentage)
            amount_seventy_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_seventy_five = (float(available_for_trading_sell) / 100 * 35)
            if amount_seventy_five == expected_amount_seventy_five:
                step6 = True
            self.browser.click_on_element(one_hundred_percentage)
            amount_one_hundred = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_one_hundred = float(available_for_trading_sell)
            if amount_one_hundred == expected_amount_one_hundred:
                step7 = True
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 is True:
                logger.logger.info("Test " + self.test_case + " , with CustomerID " + self.customer.customer_id +
                                   "=================TEST IS PASSED==========================")
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                logger.logger.error("Test " + self.test_case + " , with CustomerID " + self.customer.customer_id +
                                    "=================TEST IS NOT PASSED==========================")
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
