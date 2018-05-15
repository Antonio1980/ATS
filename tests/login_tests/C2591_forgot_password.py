# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.pages.browser import Browser
from tests.pages.login_page import LogInPage


@test(groups=['end2end', 'functional', 'sanity'])
class ForgotPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Browser.setUpClass("chrome")

        
    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password(self):
        email = "roman@spotoption.com"
        delay = 10
        LogInPage.forgot_password(delay, email)


    @classmethod
    def tearDownClass(self):
        Browser.tearDownClass()
