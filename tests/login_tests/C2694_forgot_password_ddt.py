# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from tests.pages.login_page import LogInPage
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data


@test(groups=['end2end', 'functional', 'sanity'])
@ddt
class ForgotPasswordTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Browser.set_up_class("chrome")

        
    @test(groups=['login_page', 'positive'])
    @data(*get_csv_data(BaseConfig.W_TEST_FORGOT_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        LogInPage.forgot_password(delay, email)


    @classmethod
    def tearDownClass(self):
        Browser.tear_down_class()
