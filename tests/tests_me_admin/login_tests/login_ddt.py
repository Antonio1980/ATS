# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError
from tests.tests_me_admin.pages.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_me_admin.pages.login_page import LogInPage


@ddt
@test(groups=['login_page', ])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ])
    @data(*Instruments.get_csv_data(BaseConfig.ME_LOGIN_DATA))
    @unpack
    def test_login_ddt(self, username, password):
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.login_page.login_positive(self.driver, username, password)
            step2 = self.home_page.logout(self.driver, delay)
            step3 = self.login_page.login_positive(self.driver, username, password)
        except AutomationError as e:
            print("{0} method test_login_ddt failed with error. {1}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)

    @classmethod
    def tearDownClass(cls):
        Browser.close_browser(cls.driver)
