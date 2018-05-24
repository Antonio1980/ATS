# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.crm.pages.login_page import LogInPage


@test(groups=['functional', 'smoke', 'sanity'])
@ddt
class LogInTestDDT(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")

    @test(groups=['login_page', 'ddt'])
    @data(*get_csv_data(BaseConfig.W_CRM_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 3
        self.login(delay, username, password)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()

