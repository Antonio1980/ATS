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
from tests.tests_web_platform.locators import main_screen_locators


@ddt
@test(groups=['home_page', 'upper_ruler', ])
class MainTradingScreenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5923'
        self.home_page = HomePage()
        self.locators = main_screen_locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['sanity', 'positive', 'ui', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_main_trading_screen(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1 = False
        try:
            self.home_page.open_home_page(self.driver, delay)
            assert Browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
            assert Browser.wait_element_presented(self.driver, self.locators.SIGH_UP_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.SIGH_IN_BUTTON, delay)
            # assert Browser.wait_element_presented(self.driver, self.locators.ABOUT, delay)
            # assert Browser.wait_element_presented(self.driver, self.locators.HELP, delay)
            # assert Browser.wait_element_presented(self.driver, self.locators.FAQ, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.LOGO, delay)
            # assert Browser.check_element_not_visible(self.driver, self.locators.MAIN_MENU_ICON, delay)
            # assert Browser.check_element_not_visible(self.driver, self.locators.LANGUAGE_FLAG, delay)
            step1 = True
        finally:
            if step1 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
