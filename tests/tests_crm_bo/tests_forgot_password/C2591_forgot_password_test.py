# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory


@test(groups=['login_page', ])
class ForgotPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '2591'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['sanity', 'functional', 'positive', ])
    def test_forgot_password(cls):
        email = "roman@spotoption.com"
        delay = 1
        result = False
        try:
            result = cls.login_page.forgot_password(cls.driver, delay, email)
        finally:
            if result is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
