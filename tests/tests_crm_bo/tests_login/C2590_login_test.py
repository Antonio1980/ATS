# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory


@test(groups=['functional', 'smoke', 'sanity'])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '2590'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['login_page', 'positive'])
    def test_login_positive(self):
        delay = 1
        result = False
        try:
            result = self.login_page.login_positive(self.driver, delay)
        finally:
            if result is True:
                update_test_case(self.test_run, self.test_case, 1)
            else:
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
