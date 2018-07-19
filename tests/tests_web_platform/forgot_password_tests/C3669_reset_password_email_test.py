# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage
from src.base.engine import write_file_result, update_test_case, get_account_details


@test(groups=['forgot_password_page', 'e2e', ])
class ResetPasswordEmailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3669'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.customers = cls.home_page.WTP_TESTS_CUSTOMERS
        # 1- Data file, 2- Row, 3- First column, 4- Second column, 5- Third column
        details = get_account_details(cls.customers, 3, 0, 1, 2)
        cls.email = details['email']
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        # rows = run_mysql_query(cls, "SELECT c.email FROM customers c WHERE status=1;")
        # cls.email = rows[0]

    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_reset_password_email(self):
        delay = 1
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            result2 = self.login_page.click_on_link(self.driver, 1, delay)
            result3 = self.forgot_password_page.fill_email_address_form(self.driver, self.email, delay)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            new_password_url = self.login_page.get_email_updates(self.driver, self.email, 1)
            result4 = self.login_page.get_email_updates(self.driver, self.email, 2, new_password_url)
        finally:
            if result1 and result2 and result3 and result4 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
