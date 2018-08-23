# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@ddt
@test(groups=['login_page', ])
class ForgotPasswordDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '2694'
        cls.login_page = LogInPage()
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.results_file = BaseConfig.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.FORGOT_PASSWORD_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        step1 = True
        try:
            step1 = self.login_page.forgot_password(self.driver, email)
        finally:
            if step1 is False:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        Browser.close_browser(cls.driver)
