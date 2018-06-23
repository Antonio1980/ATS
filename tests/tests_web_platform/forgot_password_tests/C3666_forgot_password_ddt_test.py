# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import unpack, data, ddt
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.login_page import LogInPage
from src.test_utils.file_utils import get_csv_data, write_file_result
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@ddt
@test(groups=['forgot_password_page', ])
class ForgotPasswordTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3666'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'ddt', 'negative', ])
    @data(*get_csv_data(BaseConfig.CRM_FORGOT_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            result2 = self.login_page.click_on_forgot_password(self.driver, delay)
            self.login_page.driver_wait(self.driver, delay)
            result3 = self.forgot_password_page.fill_email_address_form_ddt(self.driver, email, delay)
        finally:
            if (result1 & result2 & result3) is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
