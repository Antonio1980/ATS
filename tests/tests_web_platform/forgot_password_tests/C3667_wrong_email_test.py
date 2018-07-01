# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from src.test_utils.mailinator_utils import email_generator
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import LogInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['forgot_password_page', ])
class WrongEmailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.forgot_password_page = ForgotPasswordPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3667'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        email_suffix = "@mailinator.com"
        cls.negative_email = email_generator() + email_suffix

    @classmethod
    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_wrong_email(cls):
        delay = 1
        result1, result2, result3 = False, False, True
        try:
            result1 = cls.home_page.open_login_page(cls.driver, delay)
            result2 = cls.login_page.click_on_forgot_password(cls.driver, delay)
            cls.login_page.driver_wait(cls.driver, delay)
            result3 = cls.forgot_password_page.fill_email_address_form(cls.driver, cls.negative_email, delay)
        finally:
            if (result1 and result2 is True) and (result3 is False):
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
