# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory


@test(groups=['functional', 'smoke', 'sanity'])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls._driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '2590'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    #@classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_positive(cls):
        delay = 1
        result = False
        try:
            result = cls.login_page.login_positive(cls._driver, delay)
        finally:
            if result is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls._driver)
