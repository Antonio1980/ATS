# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage


@ddt
@test(groups=['market_order_panel', ])
class BuyMatchedWithTwoOrdersTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '2808'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.email = self.signin_page.email
        self.password = self.signin_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['functional', 'positive', ], depends_on_groups=["sanity", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_buy_matched_with_two_orders(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
            step3 = ""
        finally:
            if step1 and step2 and step3 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.signin_page.close_browser(self.driver)
