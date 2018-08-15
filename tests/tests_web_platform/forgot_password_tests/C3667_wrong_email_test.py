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


@test(groups=['forgot_password_page', ])
class WrongEmailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3667'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        email_suffix = "@mailinator.com"
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results_file = cls.home_page.WTP_TESTS_RESULT
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.negative_email = cls.login_page.email_generator() + email_suffix

    @test(groups=['sanity', 'functional', 'negative', ], depends_on_groups=["smoke", ])
    def test_wrong_email(self):
        delay = 1
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay + 3)
            # Option 1- forgot password, Option 2- register link
            step2 = self.login_page.click_on_link(self.driver, 1, delay + 3)
            step3 = self.forgot_password_page.fill_email_address_form(self.driver, self.negative_email, delay + 3)
        finally:
            if step1 and step2 and step3 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
