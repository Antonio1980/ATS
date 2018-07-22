# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import unpack, ddt, data
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from src.base.instruments import write_file_result, update_test_case, get_csv_data


@ddt
@test(groups=['sign_in_page', ])
class SignInDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3966'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ])
    @data(*get_csv_data(BaseConfig.WTP_LOGIN_DATA))
    @unpack
    def test_sign_in_ddt(self, email, password):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            result2 = self.login_page.sign_in(self.driver, email, password)
        finally:
            if result1 and result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
