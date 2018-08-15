# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['forgot_password_page', 'e2e', ])
class ResetPasswordEmailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3669'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.forgot_password_page = ForgotPasswordPage()
        cls.results_file = cls.home_page.WTP_TESTS_RESULT
        cls.customers_file = cls.home_page.WTP_TESTS_CUSTOMERS
        cls.email = cls.forgot_password_page.mailinator_email
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_reset_password_email(self):
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
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
