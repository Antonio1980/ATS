# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer import RegisteredCustomer
from src.base.base_exception import AutomationError
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import main_screen_locators


@ddt
@test(groups=['home_page', ])
class MainTradingScreenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5922'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.locators = main_screen_locators
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.email = self.customer.pended_email
        self.results = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['sanity', 'positive', 'ui', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_main_trading_screen(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
            try:
                assert self.browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
                assert self.browser.wait_element_presented(self.driver, self.locators.ASSET_PANEL, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.INSTRUMENT_QUICK_INFO_PANEL, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.GRAPH_AREA, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.MARKET_ORDER_PANEL, delay)
                limit_button = self.browser.find_element(self.driver, self.locators.LIMIT_BUTTON)
                self.browser.try_click(self.driver, limit_button, 2)
                assert self.browser.wait_element_presented(self.driver, self.locators.LIMIT_ORDER_PANEL, delay)
                assert self.browser.find_element_by(self.driver, self.locators.CURRENT_PORTFOLIO_ID, "id")
                assert self.browser.find_element_by(self.driver, self.locators.ORDER_BOOK_PANEL_ID, "id")
                assert self.browser.wait_element_presented(self.driver, self.locators.OPEN_ORDER_TABLE, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.ORDERS_HISTORY_TABLE, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.TRADES_HISTORY_TABLE, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.LAST_TRADES_PANEL, delay)
                step3 = True
            except AutomationError as e:
                print("{0} test_main_trading_screen failed with error: {1}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 and step3 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
