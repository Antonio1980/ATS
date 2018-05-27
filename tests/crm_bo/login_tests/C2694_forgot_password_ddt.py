# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.file_utils import get_csv_data


@test(groups=['end2end', 'functional', 'sanity'])
@ddt
class ForgotPasswordTestDDT(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")

    @test(groups=['login_page', 'positive'])
    @data(*get_csv_data(BaseConfig.CRM_FORGOT_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        self.forgot_password(delay, email)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()
