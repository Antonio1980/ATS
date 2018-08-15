# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


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
        cls.results_file = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_login_logout_login(self):
        delay = 1
        step1, step2, step3 = False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.username, self.password)
            step2 = self.home_page.logout(self.driver, delay)
            step3 = self.login_page.login(self.driver, self.username, self.password)
        finally:
            if step1 and step2 and step3 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)

