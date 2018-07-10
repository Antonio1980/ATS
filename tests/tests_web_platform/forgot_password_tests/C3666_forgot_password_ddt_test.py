# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import unpack, data, ddt
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from src.base.engine import write_file_result, get_csv_data, update_test_case
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@ddt
@test(groups=['forgot_password_page', ])
class ForgotPasswordTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = SignInPage()
        cls.home_page = HomePage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3666'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*get_csv_data(BaseConfig.FORGOT_PASSWORD_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        result1, result2, result3 = False, False, True
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            result2 = self.login_page.click_on_link(self.driver, 1, delay)
            result3 = self.forgot_password_page.fill_email_address_form(self.driver, email, delay)
        finally:
            if (result1 and result2 is True) and (result3 is False):
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                #update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                #update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
