# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import Instruments


@ddt
@test(groups=['login_page', ])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.test_case = '2590'
        cls.username = cls.login_page.login_username
        cls.password = cls.login_page.login_password
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results_file = cls.login_page.CRM_TESTS_RESULT

    @test(groups=['smoke', 'functional', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_login_positive(self, browsers):
        driver = WebDriverFactory.get_browser(browsers)
        step1 = False
        try:
            step1 = self.login_page.login(driver, self.username, self.password)
        finally:
            if step1 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
                driver.quit()
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)
                driver.quit()
