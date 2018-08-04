# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import write_file_result, update_test_case


@test(groups=['login_page', ])
class ForgotPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '2591'
        cls.login_page = LogInPage()
        cls.email = cls.login_page.email
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_forgot_password(self):
        delay = 1
        result = False
        try:
            result = self.login_page.forgot_password(self.driver, self.email)
        finally:
            if result is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
