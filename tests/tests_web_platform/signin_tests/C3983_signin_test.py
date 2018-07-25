# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.instruments import write_file_result, update_test_case
from tests.tests_web_platform.pages.signin_page import SignInPage


@test(groups=['sign_in_page', ])
class SignInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3983'
        cls.home_page = HomePage()
        cls.signin_page = SignInPage()
        cls.email = cls.signin_page.email
        cls.password = cls.signin_page.password
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'functional', 'positive', ])
    def test_sign_in_positive(self):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            result2 = self.signin_page.sign_in(self.driver, self.email, self.password)
        finally:
            if result1 & result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.signin_page.close_browser(cls.driver)
