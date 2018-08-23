# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import unpack, ddt, data
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage


@ddt
@test(groups=['sign_in_page', ])
class SignInDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3966'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.results = BaseConfig.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.WTP_LOGIN_DATA))
    @unpack
    def test_sign_in_ddt(self, email, password):
        delay = 1
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.login_page.sign_in(self.driver, email, password)
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
