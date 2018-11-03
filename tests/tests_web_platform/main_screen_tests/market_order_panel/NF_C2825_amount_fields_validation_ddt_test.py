# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage


@ddt
@test(groups=['market_order_panel', ])
class AmountFieldsValidationDDTTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '2825'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.email = self.signin_page.email
        self.password = self.signin_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['functional', 'ddt', 'negative', ], depends_on_groups=["sanity", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_amount_fields_ddt(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
            time.sleep(delay)
            customer_id = Browser.execute_js(self.driver, self.signin_page.script_customer_id)
            step3 = Instruments.add_customer_balance(customer_id, '5', '20000')
            step4 = True
        finally:
            if step1 and step2 and step3 and step4 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
