# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.db_utils import run_mysql_query
from src.test_utils.file_utils import write_file_result, get_account_details
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import LogInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['forgot_password_page', 'e2e', ])
class ResetPasswordEmailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3669'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        # 1- Data file, 2- Row, 3- First column, 4- Second column, 5- Third column
        details = get_account_details(BaseConfig.WTP_TESTS_CUSTOMERS, 0, 0, 1, 2)
        cls.email = details['email']
        print(cls.email)
        #rows = run_mysql_query(cls, "SELECT c.email FROM customers c WHERE status=1;")
        #cls.email = rows[0]

    @classmethod
    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_forgot_password(cls):
        delay = 1
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = cls.home_page.open_login_page(cls.driver, delay)
            result2 = cls.login_page.click_on_forgot_password(cls.driver, delay)
            cls.login_page.driver_wait(cls.driver, delay)
            result3 = cls.forgot_password_page.fill_email_address_form(cls.driver, cls.email, delay)
            cls.login_page.wait_driver(cls.driver, delay + 5)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            result4 = cls.login_page.get_email_updates(cls.driver, cls.email, 2)
        finally:
            if (result1 & result2 is True) & (result3 & result4 is True):
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
