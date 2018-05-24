# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.browser import Browser
from tests.crm.pages.home_page import HomePage
from tests.crm.pages.login_page import LogInPage
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_credentials_positive


@test(groups=['functional','smoke','sanity'])
class LogInLogOutLogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Browser.set_up_class("chrome")

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_logout_login(self):
        delay = 1
        credentials = get_credentials_positive(BaseConfig.W_CRM_LOGIN_DATA, 0, 0, 1)
        username = credentials['username']
        password = credentials['password']
        LogInPage.login(delay, username, password)
        HomePage.logout(delay)
        LogInPage.login(delay, username, password)

    @classmethod
    def tearDownClass(slc):
        Browser.tear_down_class()











