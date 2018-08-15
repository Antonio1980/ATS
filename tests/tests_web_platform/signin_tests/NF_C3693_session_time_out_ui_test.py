# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage


@test(groups=['sign_in_page', ])
class SessionTimeOutUITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_case = '3693'
        cls.email = cls.login_page.email
        cls.password = cls.login_page.password
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_session_time_out_ui(self):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.home_page.open_signin_page(self.driver, delay)
            result2 = self.login_page.sign_in(self.driver, self.email, self.password)
            result3 = ""
        finally:
            if result1 and result2 and result3 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
