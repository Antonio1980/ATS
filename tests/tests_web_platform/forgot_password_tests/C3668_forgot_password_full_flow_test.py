# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from src.base.engine import write_file_result, update_test_case
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['forgot_password_page', 'e2e', ])
class ForgotPasswordFullFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = SignInPage()
        cls.home_page = HomePage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3668'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.email = cls.forgot_password_page.email
        cls.new_password = cls.login_page.email_generator() + "A"
        # rows = run_mysql_query(cls, "SELECT c.email FROM customers c WHERE status=1;")
        # cls.email = rows[0]

    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_forgot_password_full_flow(self):
        delay = 1
        result1, result2, result3, result4, result5 = False, False, False, False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            result2 = self.login_page.click_on_link(self.driver, 1, delay)
            result3 = self.forgot_password_page.fill_email_address_form(self.driver, self.email, delay)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            new_password_url = self.forgot_password_page.get_email_updates(self.driver, self.email, 1)
            time.sleep(10)
            result4 = self.forgot_password_page.get_email_updates(self.driver, self.email, 2, new_password_url)
            result5 = self.forgot_password_page.set_new_password(self.driver, self.new_password, new_password_url)
        finally:
            if result1 and result2 and result3 and result4 and result5 is True:
                write_file_result(self.first_last_name + "," + self.email + "," + self.new_password + "\n",
                                  BaseConfig.WTP_TESTS_CUSTOMERS)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
