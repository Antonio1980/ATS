# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case


@test(groups=['end2end_tests', 'functional', 'sanity'])
class ForgotPasswordTest(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_login_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '2591'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password(cls):
        email = "roman@spotoption.com"
        delay = 1
        result = False
        try:
            result = cls.forgot_password(delay, email)
        finally:
            if result is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()
