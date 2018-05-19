# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from tests.base.browser import Browser
from tests.pages.login_page import LogInPage
from tests_sources.test_definitions import BaseConfig
from tests_sources.test_utils.file_util import get_csv_data


@test(groups=['end2end', 'functional', 'sanity'])
@ddt
class ForgotPasswordTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Browser.setUpClass("chrome")

        
    @test(groups=['login_page', 'positive'])
    @data(*get_csv_data(BaseConfig.W_TEST_FORGOT_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        LogInPage.forgot_password(delay, email)


    @classmethod
    def tearDownClass(self):
        Browser.tearDownClass()