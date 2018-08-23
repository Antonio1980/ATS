# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators.main_screen_locators import MainScreenLocators


@ddt
@test(groups=['home_page', ])
class MainTradingScreenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5922'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.locators = MainScreenLocators()
        self.email = self.signin_page.email
        self.password = self.signin_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['sanity', 'positive', 'ui', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_main_trading_screen(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
            try:
                assert Browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
                assert Browser.wait_element_presented(self.driver, self.locators.ASSET_PANEL, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.INSTRUMENT_QUICK_INFO_PANEL, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.GRAPH_AREA, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.MARKET_ORDER_PANEL, delay)
                limit_button = Browser.find_element(self.driver, self.locators.LIMIT_BUTTON)
                Browser.try_click(self.driver, limit_button, 2)
                assert Browser.wait_element_presented(self.driver, self.locators.LIMIT_ORDER_PANEL, delay)
                assert Browser.find_element_by(self.driver, self.locators.CURRENT_PORTFOLIO_ID, "id")
                assert Browser.find_element_by(self.driver, self.locators.ORDER_BOOK_PANEL_ID, "id")
                assert Browser.wait_element_presented(self.driver, self.locators.OPEN_ORDER_TABLE, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.ORDERS_HISTORY_TABLE, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.TRADES_HISTORY_TABLE, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.LAST_TRADES_PANEL, delay)
                step3 = True
            except Exception as e:
                print(e)
        finally:
            if step1 and step2 and step3 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
