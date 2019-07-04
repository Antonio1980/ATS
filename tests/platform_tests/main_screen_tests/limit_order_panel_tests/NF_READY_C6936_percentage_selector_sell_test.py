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

# BE ATTENTION!!! IF TEST FELL - YOU WILL SEE IN CONSOLE  "TEST IS NOT PASSED!!!"
@pytest.mark.skip
@ddt
class PercentageSelectorSellTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6935'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.postman = self.customer.get_postman_access(self.customer.auth_token)
        self.postman.approve_customer(self.customer.customer_id)
        self.customer.add_credit_card_and_deposit(1000, 1)  # USD currency
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    #@test(groups=['functional', 'negative', ], depends_on_groups=["sanity", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_percentage_selector_sell(self, browser):
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
            available_for_trading_sell_jq = self.browser.execute_js(self.driver,
                                                                    self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            available_for_trading_sell = float(re.sub(',', '', available_for_trading_sell_jq))
            twenty_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_25_SELL,
                                                                         delay)
            fifty_percentage = self.browser.wait_element_presented(self.driver,
                                                                   self.locators.PERCENTAGE_SELECTOR_50_SELL, delay)
            seventy_five_percentage = self.browser.wait_element_presented(self.driver,
                                                                          self.locators.PERCENTAGE_SELECTOR_75_SELL,
                                                                          delay)
            one_hundred_percentage = self.browser.wait_element_presented(self.driver,
                                                                         self.locators.PERCENTAGE_SELECTOR_100_SELL,
                                                                         delay)
            time.sleep(1)
            self.browser.click_on_element(twenty_five_percentage)
            time.sleep(1)
            amount_twenty_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_twenty_five = (float(available_for_trading_sell) / 100 * 25)
            if amount_twenty_five == expected_amount_twenty_five:
                step4 = True
            else:
                step4 = False
            self.browser.click_on_element(fifty_percentage)
            time.sleep(1)
            amount_fifty = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_fifty = (float(available_for_trading_sell) / 100 * 50)
            if amount_fifty == expected_amount_fifty:
                step5 = True
            else:
                step5 = False
            self.browser.click_on_element(seventy_five_percentage)
            time.sleep(1)
            amount_seventy_five = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_seventy_five = (float(available_for_trading_sell) / 100 * 75)
            if amount_seventy_five == expected_amount_seventy_five:
                step6 = True
            else:
                step6 = False
            self.browser.click_on_element(one_hundred_percentage)
            time.sleep(1)
            amount_one_hundred = float(self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ))
            expected_amount_one_hundred = float(available_for_trading_sell)
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
