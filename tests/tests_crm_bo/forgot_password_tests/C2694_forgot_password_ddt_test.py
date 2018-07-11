# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.engine import write_file_result, update_test_case, get_csv_data


@ddt
@test(groups=['login_page', ])
class ForgotPasswordDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '2694'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'ddt', 'positive', ])
    @data(*get_csv_data(BaseConfig.FORGOT_PASSWORD_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        result = False
        try:
            result = self.login_page.forgot_password(self.driver, email, delay)
        finally:
            if result is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
