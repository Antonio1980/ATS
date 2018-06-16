# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.tests_me_admin.pages.home_page import HomePage
from tests.tests_me_admin.pages.login_page import LogInPage
from tests.drivers.webdriver_factory import WebDriverFactory


@test(groups=['end2end'])
@ddt
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['login'])
    @data(*get_csv_data(BaseConfig.ME_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 1
        self.login_page.login(self.driver, delay, username, password)
        self.home_page.logout(self.driver, delay)
        self.login_page.login(self.driver, delay, username, password)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
