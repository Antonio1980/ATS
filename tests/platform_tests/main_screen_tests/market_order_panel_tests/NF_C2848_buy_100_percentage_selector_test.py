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
class BuyPercentageSelectorTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '2848'
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 8, 1050)  # LTC currency
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_buy_percentage_selector(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver)
            step2 = self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1035]').click()''')

            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.LTC_DXCASH_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            step3 = True
            available_for_trading_buy_jq = self.browser.execute_js(self.driver,
                                                                   self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_trading_buy = round(((float(re.sub(',', '', available_for_trading_buy_jq))) * (1 - 0.0025)),
                                              2)
            one_hundred_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_100_BUY,
                                                                         delay)
            self.browser.click_on_element(one_hundred_percentage)
            estimated_price_jq = self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_BUY_JQ)
            amount_one_hundred = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_amount_one_hundred = round(float(available_for_trading_buy) / float(estimated_price_jq), 5)
            if amount_one_hundred == expected_amount_one_hundred:
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
