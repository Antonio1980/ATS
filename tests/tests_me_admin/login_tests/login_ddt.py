# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_me_admin.pages.home_page import HomePage
from tests.tests_me_admin.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@test(groups=['login_page', ])
@ddt
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ])
    @data(*Instruments.get_csv_data(BaseConfig.ME_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 1
        self.login_page.login(self.driver, delay, username, password)
        self.home_page.logout(self.driver, delay)
        self.login_page.login(self.driver, delay, username, password)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
