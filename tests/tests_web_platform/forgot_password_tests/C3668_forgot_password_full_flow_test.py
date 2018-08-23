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
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@ddt
@test(groups=['forgot_password_page', ])
class ForgotPasswordFullFlowTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3668'
        self.home_page = HomePage()
        self.login_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.forgot_password_page = ForgotPasswordPage()
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.email = self.forgot_password_page.mailinator_email
        self.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
        self.new_password = self.forgot_password_page.password + "Qa"
        self.first_last_name = self.forgot_password_page.first_last_name

    @test(groups=['regression', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_forgot_password_full_flow(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay, customer_id, token = 5, "", ""
        step1, step2, step3, step4, step5 = False, False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            step2 = self.login_page.click_on_link(self.driver, 1, delay)
            step3 = self.forgot_password_page.fill_email_address_form(self.driver, self.email, delay)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            new_password_url = self.login_page.get_email_updates(self.driver, self.email, 1)
            token = new_password_url.split('=')[1].split('&')[0]
            step4 = self.login_page.get_email_updates(self.driver, self.email, 2, new_password_url)
            step5 = self.forgot_password_page.set_new_password(self.driver, self.new_password, new_password_url)
        finally:
            if step1 and step2 and step3 and step4 and step5 is True:
                Instruments.write_file_user(self.email + "," + self.password + "," + token + "\n", self.customers_file)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.home_page.close_browser(self.driver)
