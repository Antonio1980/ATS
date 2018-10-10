# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@ddt
@test(groups=['login_page', ])
class LogInLogOutLogInTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '2598'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.username = self.login_page.login_username
        self.password = self.login_page.login_password
        self.results_file = BaseConfig.CRM_TESTS_RESULT

    @test(groups=['smoke', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_login_logout_login(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 1
        step1, step2, step3 = False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.username, self.password)
            step2 = self.home_page.logout(self.driver, delay)
            step3 = self.login_page.login(self.driver, self.username, self.password)
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)

