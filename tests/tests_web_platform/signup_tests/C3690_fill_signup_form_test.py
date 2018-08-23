# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class SignUpTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3690'
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.password = self.signup_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.username = Instruments.generate_user_first_last_name()
        self.email = self.username + "@mailinator.com"
        self.results = BaseConfig.WTP_TESTS_RESULT
        self.customers = BaseConfig.WTP_TESTS_CUSTOMERS

    @test(groups=['smoke', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_up_positive(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, )
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.home_page.close_browser(self.driver)