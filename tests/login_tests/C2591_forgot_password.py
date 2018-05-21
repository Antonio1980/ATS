# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.browser import Browser
from tests.pages.login_page import LogInPage


@test(groups=['end2end', 'functional', 'sanity'])
class ForgotPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Browser.set_up_class("chrome")

        
    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password(self):
        email = "roman@spotoption.com"
        delay = 10
        LogInPage.forgot_password(delay, email)


    @classmethod
    def tearDownClass(self):
        Browser.tear_down_class()
