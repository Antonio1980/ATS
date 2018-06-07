# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case


@ddt
@test(groups=['end2end_tests', 'functional', 'sanity'])
class ForgotPasswordTestDDT(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_login_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '2694'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['login_page', 'positive'])
    @data(*get_csv_data(BaseConfig.CRM_FORGOT_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        result = False
        try:
            result = self.forgot_password(delay, email)
        finally:
            if result is True:
                # server_url, test_case, status
                update_test_case(self.test_run, self.test_case, 1)
            else:
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()
