# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.me_admin.pages.home_page import HomePage
from tests.me_admin.pages.login_page import LogInPage


@test(groups=['end2end'])
@ddt
class LogInTest(unittest.TestCase, LogInPage, HomePage):

    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")

    @test(groups=['login'])
    @data(*get_csv_data(BaseConfig.W_ME_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 10
        self.login(delay, username, password)
        self.logout(delay)
        self.login(delay, username, password)


    @classmethod
    def tearDownClass(cls):
        cls.close_browser()











