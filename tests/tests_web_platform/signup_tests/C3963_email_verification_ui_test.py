# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['login_page', ])
class EmailVerificationScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.open_account_page = SignUpPage()
        cls.email = cls.open_account_page.email
        cls.password = "1Aa@<>12"
        cls.first_last_name = "QAtestQA"
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3963'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_email_verification_screen(self):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.open_account_page.fill_signup_form(self.driver, self.first_last_name, self.email, self.password)
            result3 = self.open_account_page.verify_email_screen_test(self.driver, delay)
        finally:
            if result1 and result2 and result3 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
