# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.instruments import write_file_result, update_test_case
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['sign_up_page', 'e2e', ])
class SignUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3690'
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.email = cls.signup_page.email
        cls.password = cls.signup_page.password
        cls.username = cls.signup_page.username
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.customers = cls.home_page.WTP_TESTS_CUSTOMERS
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_sign_up_positive(self):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password)
        finally:
            if result1 and result2 is True:
                write_file_result(self.email + "," + self.password + "\n", self.customers)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
