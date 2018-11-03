# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import unpack, data, ddt
from src.base.enums import Browsers
from src.base.customer import Customer
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@ddt
@test(groups=['forgot_password_page', ])
class ForgotPasswordDDTTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3666'
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.forgot_password_page = ForgotPasswordPage()
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.FORGOT_PASSWORD_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 5
        step1, step2, step3 = False, False, True
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            step2 = self.signin_page.click_on_link(self.driver, 1, delay)
            step3 = self.forgot_password_page.fill_email_address_form(self.driver, email, delay)
        finally:
            if step1 and step2 is True and step3 is False:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_driver(self.driver)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close_browser(cls.driver)
