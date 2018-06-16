# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.test_definitions import BaseConfig
from tests.tests_web_platform.pages.home_page import HomePage
from src.test_utils.testrail_utils import update_test_case
from src.test_utils.mailinator_utils import get_mailinator_updates
from tests.tests_web_platform.pages.open_account_page import OpenAccountPage


@test(groups=['end2end_tests', 'functional', 'sanity'])
class ForgotPasswordUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.email = OpenAccountPage().email
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3558'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password_page_ui(cls):
        delay = 1
        result1 = False
        try:
            cls.home_page.open_login_page(cls.driver, delay)
            data = get_mailinator_updates(cls.driver, cls.email)
            print(data)
        finally:
            if result1 is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
