# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.crm.pages.login_page import LogInPage


@test(groups=['end2end', 'functional', 'sanity'])
class ForgotPasswordTest(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password(cls):
        email = "roman@spotoption.com"
        delay = 1
        cls.forgot_password(delay, email)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()
