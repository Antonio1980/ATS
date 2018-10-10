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
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@ddt
@test(groups=['forgot_password_page', ])
class ResetPasswordEmailTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3669'
        self.home_page = HomePage()
        self.login_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.forgot_password_page = ForgotPasswordPage()
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
        self.email = self.forgot_password_page.mailinator_email

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_reset_password_email(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 1
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            step2 = self.login_page.click_on_link(self.driver, 1, delay)
            step3 = self.forgot_password_page.fill_email_address_form(self.driver, self.email, delay)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            new_password_url = self.login_page.get_email_updates(self.driver, self.email, 1)
            step4 = self.login_page.get_email_updates(self.driver, self.email, 2, new_password_url)
        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
            Browser.close_browser(self.driver)
