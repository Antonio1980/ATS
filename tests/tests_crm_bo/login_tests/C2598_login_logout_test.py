# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import write_file_result, update_test_case


@test(groups=['login_page', ])
class LogInLogOutLogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '2598'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.username = cls.login_page.login_username
        cls.password = cls.login_page.login_password
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_login_logout_login(self):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.login_page.login(self.driver, self.username, self.password)
            result2 = self.home_page.logout(self.driver, delay)
            result3 = self.login_page.login(self.driver, self.username, self.password)
        finally:
            if result1 and result2 and result3 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)

