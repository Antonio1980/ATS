# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.file_utils import get_credentials_positive


@test(groups=['functional', 'smoke', 'sanity'])
class LogInTest(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_positive(cls):
        delay = 1
        # 0, 0, 1 - row, column1, column2
        credentials = get_credentials_positive(BaseConfig.CRM_LOGIN_DATA, 0, 0, 1)
        username = credentials['username']
        password = credentials['password']
        cls.login(delay, username, password)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()











