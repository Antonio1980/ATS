# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.crm.pages.login_page import LogInPage
from src.base.browser import Browser
from src.test_utils.file_utils import get_credentials_positive
from src.test_definitions import BaseConfig


@test(groups=['functional', 'smoke', 'sanity'])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Browser.set_up_class("chrome")

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_positive(self):
        delay = 1
        # 0, 0, 1 - row, column1, column2
        credentials = get_credentials_positive(BaseConfig.W_CRM_LOGIN_DATA, 0, 0, 1)
        username = credentials['username']
        password = credentials['password']
        LogInPage.login(delay, username, password)

    @classmethod
    def tearDownClass(slc):
        Browser.tear_down_class()











