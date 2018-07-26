# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.instruments import write_file_result, update_test_case, write_file_user
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['forgot_password_page', 'e2e', ])
class ForgotPasswordFullFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3668'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.forgot_page = ForgotPasswordPage()
        cls.email = cls.forgot_page.email
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.customers = cls.home_page.WTP_TESTS_CUSTOMERS
        cls.new_password = cls.forgot_page.password + "Qa"
        cls.first_last_name = cls.forgot_page.first_last_name
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
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
            result3 = self.forgot_page.fill_email_address_form(self.driver, self.email, delay)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            new_password_url = self.forgot_page.get_email_updates(self.driver, self.email, 1)
            result4 = self.forgot_page.get_email_updates(self.driver, self.email, 2, new_password_url)
            result5 = self.forgot_page.set_new_password(self.driver, self.new_password, new_password_url)
        finally:
            if result1 and result2 and result3 and result4 and result5 is True:
                write_file_user(self.email + "," + self.new_password + "," + self.first_last_name + "\n", self.customers)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
