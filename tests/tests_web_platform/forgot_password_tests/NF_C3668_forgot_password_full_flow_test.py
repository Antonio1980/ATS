# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.db_utils import run_mysql_query
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['forgot_password_page', 'e2e'])
class ForgotPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = SignInPage()
        cls.home_page = HomePage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3668'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        rows = run_mysql_query(cls, "SELECT c.email FROM customers c WHERE status=1;")
        cls.email = rows[0]

    @test(groups=['regression', 'functional', 'positive', ], depends_on_groups=["smoke", "sanity", ])
    def test_forgot_password(self):
        delay = 1
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            result2 = self.login_page.click_on_link(self.driver, 1, delay)
            result3 = self.forgot_password_page.fill_email_address_form(self.driver, self.email, delay)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            result4 = self.home_page.get_email_updates(self.driver, self.email, 2)
        finally:
            if (result1 & result2 is True) & (result3 & result4 is True):
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
