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
from tests.tests_web_platform.locators import main_screen_locators


@ddt
@test(groups=['home_page', ])
class MainTradingScreenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6214'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.locators = main_screen_locators
        self.email = self.signin_page.email
        self.password = self.signin_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN

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
                assert Browser.wait_element_presented(self.driver, self.locators.MAIN_MENU_ICON, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.LOGO, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.FUNDS_BUTTON, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.TIME_ON_UPPER_RULER, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.DATE_ON_UPPER_RULER, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.LANGUAGE_FLAG, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.CURRENT_PORTFOLIO, delay)
                step3 = True
            except Exception as e:
                print("Exception is occurred.".format(e))

        finally:
            if step1 and step2 and step3 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
