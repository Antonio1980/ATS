# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from src.base.customer import RegisteredCustomer
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.market_order_panel_page import MarketOrderPanelPage


@ddt
@test(groups=['market_order_panel', ])
class EstimatePriceIsImmutableTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '2812'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.email = self.customer.pended_email
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['functional', 'positive', ], depends_on_groups=["sanity", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_estimate_price_is_immutable(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
            time.sleep(delay)
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            usd_from_dropdown = self.browser.wait_element_presented(self.driver, self.locators.USD_OPTION_FROM_USD_DROPDOWN, delay)
            self.browser.click_on_element(usd_from_dropdown)
            dxcash_usd_instrument = self.browser.wait_element_presented(self.driver, self.locators.DXCASH_USD_INSTRUMENT, delay + 5)
            self.browser.click_on_element(dxcash_usd_instrument)
            assert self.browser.wait_element_presented(self.driver, self.locators.DXCASH_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL, delay + 5)
            estimated_price_buy = self.browser.wait_element_presented(self.driver, self.locators.ESTIMATED_PRICE_FOR_BUY_MARKET, delay)
            estimated_price_sell = self.browser.wait_element_presented(self.driver, self.locators.ESTIMATED_PRICE_FOR_SELL_MARKET, delay)
            step3 = self.browser.check_not_send_key(estimated_price_buy, "3456")
            step4 = self.browser.check_not_send_key(estimated_price_sell, "3456")

        finally:
            if step1 and step2 and step3 and step4 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
