<<<<<<< a6ac884835aaa047de5b5f6bf0e391f6806c43ed:tests/me_admin/login_tests/login_ddt.py
# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.me_admin.pages.home_page import HomePage
from tests.me_admin.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@test(groups=['end2end'])
@ddt
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls._driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['login'])
    @data(*get_csv_data(BaseConfig.ME_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 1
        self.login(self._driver, delay, username, password)
        self.logout(self._driver, delay)
        self.login(self._driver, delay, username, password)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls._driver)
=======
# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.tests_me_admin.pages.home_page import HomePage
from tests.tests_me_admin.pages.login_page import LogInPage


@test(groups=['tests_end2end'])
@ddt
class LogInTest(unittest.TestCase, LogInPage, HomePage):

    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")

    @test(groups=['login'])
    @data(*get_csv_data(BaseConfig.ME_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 1
        self.login(delay, username, password)
        self.logout(delay)
        self.login(delay, username, password)


    @classmethod
    def tearDownClass(cls):
        cls.close_browser()











>>>>>>> 46d3ea0049230292881d76fb45bbfa6fde5f95e8:tests/tests_me_admin/login_tests/login_ddt.py
