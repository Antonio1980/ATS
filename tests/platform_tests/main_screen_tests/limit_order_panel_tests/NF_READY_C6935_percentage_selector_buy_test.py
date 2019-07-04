# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import time
import unittest

import pytest
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.registered_customer import RegisteredCustomer
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage
@pytest.mark.skip
@ddt
class PercentageSelectorBuyTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6935'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 1, 1000)  # USD
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_percentage_selector_buy(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6, step7 = False, False, False, False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver)
            step2 = self.signin_page.sign_in(self.driver, self.customer.email, self.customer.password)
            time.sleep(delay)
            limit_tab = self.browser.wait_element_presented(self.driver, self.locators.LIMIT_TAB, delay)
            self.browser.click_on_element(limit_tab)
            # for BUY
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            usd_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.USD_OPTION_FROM_USD_DROPDOWN,
                                                                    delay)
            self.browser.click_on_element(usd_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1013]').click()''')

            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.BTC_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            step3 = True
            available_for_trading_buy_jq = self.browser.execute_js(self.driver,
                                                                   self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            available_for_trading_buy = float(re.sub(',', '', available_for_trading_buy_jq))
            time.sleep(2)
            twenty_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_25_BUY,
                                                                         delay)
            fifty_percentage = self.browser.wait_element_presented(self.driver,
                                                                   self.locators.PERCENTAGE_SELECTOR_50_BUY, delay)
            seventy_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                          self.locators.PERCENTAGE_SELECTOR_75_BUY,
                                                                          delay)
            one_hundred_percentage = self.browser.wait_element_presented(self.driver,
                                                                          self.locators.PERCENTAGE_SELECTOR_100_BUY,
                                                                          delay)

            self.browser.click_on_element(twenty_five_percentage)
            time.sleep(1)
            enter_price_jq_25 = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            amount_twenty_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_amount_twenty_five = round(
                (float(available_for_trading_buy) / 100 * 25) / float(enter_price_jq_25), 2)
            if amount_twenty_five == expected_amount_twenty_five:
                step4 = True
            else:
                step4 = False
            time.sleep(1)
            self.browser.click_on_element(fifty_percentage)
            time.sleep(1)
            enter_price_jq_50 = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            amount_fifty = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_amount_fifty = round((float(available_for_trading_buy) / 100 * 50) / float(enter_price_jq_50),
                                          2)
            if amount_fifty == expected_amount_fifty:
                step5 = True
            else:
                step5 = False
            self.browser.click_on_element(seventy_five_percentage)
            time.sleep(1)
            enter_price_jq_75 = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            amount_seventy_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_amount_seventy_five = round(
                (float(available_for_trading_buy) / 100 * 75) / float(enter_price_jq_75), 2)
            if amount_seventy_five == expected_amount_seventy_five:
                step6 = True
            else:
                step6 = False
            self.browser.click_on_element(one_hundred_percentage)
            time.sleep(1)
            enter_price_jq_100 = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            amount_one_hundred = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ))
            expected_amount_one_hundred = round(float(available_for_trading_buy)/float(enter_price_jq_100), 2)
            if amount_one_hundred == expected_amount_one_hundred:
                step7 = True
            else:
                step7 = False
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                print("=============================TEST IS NOT PASSED=============================")
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
