# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.web_platform.pages.home_page import HomePage
from tests.web_platform.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from src.test_utils.mailinator_utils import get_mailinator_updates


@test(groups=['end2end_tests', 'functional', 'sanity'])
class ForgotPasswordUiTest(unittest.TestCase, LogInPage, HomePage):
    @classmethod
    def setUpClass(cls):
        cls.setup_login_page()
        cls.get_browser(Browsers.CHROME.value)
        cls._driver = cls.driver
        cls.test_case = '3558'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password_page_ui(cls):
        delay = 1
        result1 = False
        try:
            cls.open_login_page(delay)
            data = get_mailinator_updates(cls.driver, cls.email)
            print(data)
        finally:
            if result1 is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()
