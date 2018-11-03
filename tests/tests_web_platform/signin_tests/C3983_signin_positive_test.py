# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.customer import RegisteredCustomer
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage


@ddt
@test(groups=['sign_in_page', ])
class SignInTestPositive(unittest.TestCase):
    def setUp(self):
        self.test_case = '3983'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.password = self.customer.password
        self.email = self.customer.pended_email
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['smoke', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_in_positive(self, browser):
        # test_token = {'name': 'Test-Token', 'value': self.test_token}
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
