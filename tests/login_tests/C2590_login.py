# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.pages.login_page import LogInPage
from tests.base.browser import Browser
from tests_sources.test_utils.file_util import get_credentials_positive
from tests_sources.test_definitions import BaseConfig


@test(groups=['functional', 'smoke', 'sanity'])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Browser.setUpClass("chrome")

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_positive(self):
        delay = 1
        # 0, 0, 1 - row, column1, column2
        credentials = get_credentials_positive(BaseConfig.W_TEST_LOGIN_DATA, 0, 0, 1)
        username = credentials['username']
        password = credentials['password']
        LogInPage.login(delay, username, password)

    @classmethod
    def tearDownClass(slc):
        Browser.tearDownClass()











