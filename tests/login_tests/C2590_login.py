# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.pages.login_page import LogInPage
from tests.pages.base_page import BasePage
from tests_sources.test_utils.file_util import get_credentials_positive
from tests_sources.test_definitions import BaseConfig


@test(groups=['functional', 'smoke', 'sanity'])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        BasePage.setUpClass("chrome")

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_positive(self):
        row = 0
        column1 = 0
        column2 = 1
        credentials = get_credentials_positive(BaseConfig.W_TEST_DATA, row, column1, column2)
        username = credentials['username']
        password = credentials['password']
        LogInPage.login(username, password)

    @classmethod
    def tearDownClass(slc):
        BasePage.tearDownClass()











