# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.crm_bo.pages.home_page import HomePage
from tests.crm_bo.pages.login_page import LogInPage


@test(groups=['functional', 'smoke', 'sanity'])
@ddt
class LogInTestDDT(unittest.TestCase, LogInPage, HomePage):
    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")

    @test(groups=['login_page', 'ddt'])
    @data(*get_csv_data(BaseConfig.CRM_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 1
        self.login(delay, username, password)
        self.logout(delay)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()

