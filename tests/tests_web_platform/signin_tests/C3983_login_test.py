# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.engine import write_file_result, update_test_case
from tests.tests_web_platform.pages.signin_page import SignInPage


@test(groups=['sign_in_page', ])
class SignInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_case = '3983'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.email = cls.login_page.email
        cls.password = cls.login_page.password

    @test(groups=['smoke', 'functional', 'positive', ])
    def test_sign_in_positive(self):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            result2 = self.login_page.sign_in(self.driver, self.email, self.password)
        finally:
            if result1 & result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
