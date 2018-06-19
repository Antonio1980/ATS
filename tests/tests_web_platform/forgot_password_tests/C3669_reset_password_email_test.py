# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import get_account_details
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.login_page import LogInPage
from src.test_utils.mailinator_utils import get_email_updates
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['end2end_tests', 'functional', 'sanity'])
class ResetPasswordEmailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3669'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        # data_file, row, column1, column2, column3, column4
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        cls.email = details['email']

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_reset_password_email(cls):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.home_page.open_login_page(cls.driver, delay)
            result2 = cls.login_page.click_on_forgot_password(cls.driver, delay)
            cls.login_page.driver_wait(cls.driver, delay)
            result3 = cls.forgot_password_page.fill_email_address_form(cls.driver, delay)
            cls.login_page.driver_wait(cls.driver, delay)
            data = get_email_updates(cls.driver, cls.email)
            print(data)
        finally:
            if (result1 & result2 & result3) is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
