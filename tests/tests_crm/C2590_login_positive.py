# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.pages.login_page import LogInPage
from tests.pages.page_base import BasePage
from tests_extensions.get_tests_context import get_credentials_positive
from tests_extensions.tests_definitions import BaseConfig


@test(groups=['end2end','smoke','sanity'])
class LogInTestPositive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        BasePage.setUpClass("chrome")

    @classmethod
    @test(groups=['login'])
    def test_login_logout_login(self):
        row = 0
        column1 = 0
        column2 = 1
        credentials = get_credentials_positive(BaseConfig.W_TEST_DATA, row, column1, column2)
        username = credentials['username']
        password = credentials['password']
        LogInPage.login(username, password)
        LogInPage.logout()
        LogInPage.login(username, password)

    @classmethod
    def tearDownClass(slc):
        BasePage.tearDownClass()











