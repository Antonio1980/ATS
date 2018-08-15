# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['sign_up_page', ])
class EmailVerificationScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3963'
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.email = cls.signup_page.email
        cls.password = cls.signup_page.password
        cls.username = cls.signup_page.username
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_email_verification_screen(self):
        delay = 1
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, )
            step3 = self.signup_page.verify_email_screen_test(self.driver, delay)
        finally:
            if step1 and step2 and step3 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
