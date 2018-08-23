# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage


@ddt
@test(groups=['sign_in_page', ])
class SessionTimeOutUITest(unittest.TestCase):
    def setUp(self):
        self.home_page = HomePage()
        self.login_page = SignInPage()
        self.test_case = '3693'
        self.email = self.login_page.email
        self.password = self.login_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_session_time_out_ui(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.home_page.open_signin_page(self.driver, delay)
            result2 = self.login_page.sign_in(self.driver, self.email, self.password)
            result3 = ""
        finally:
            if result1 and result2 and result3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.login_page.close_browser(self.driver)
