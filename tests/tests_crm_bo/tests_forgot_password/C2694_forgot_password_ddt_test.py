# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.tests_crm_bo.pages.login_page import LogInPage
from tests.drivers.webdriver_factory import WebDriverFactory
from src.test_utils.testrail_utils import update_test_case


@ddt
@test(groups=['tests_end2end', 'functional', 'sanity'])
class ForgotPasswordTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '2694'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['login_page', 'positive'])
    @data(*get_csv_data(BaseConfig.CRM_FORGOT_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        result = False
        try:
            result = self.login_page.forgot_password(self.driver, delay, email)
        finally:
            if result is True:
                update_test_case(self.test_run, self.test_case, 1)
            else:
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
