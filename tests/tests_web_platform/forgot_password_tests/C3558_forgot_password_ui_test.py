# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages import forgot_password_page_url
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators


@test(groups=['forgot_password_page', ])
class ForgotPasswordUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = SignInPage()
        cls.home_page = HomePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3558'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_forgot_password_page_ui(self):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay + 3)
            # Option 1- forgot password, Option 2- register link
            result2 = self.login_page.click_on_link(self.driver, 1, delay + 1)
            assert forgot_password_page_url == self.login_page.get_cur_url(self.driver)
            self.login_page.wait_driver(self.driver, delay + 3)
            if self.login_page.wait_element_presented(self.driver, delay, ForgotPasswordPageLocators.FORGOT_PASSWORD_TITLE):
                if self.login_page.wait_element_presented(self.driver, delay, ForgotPasswordPageLocators.EMAIL_TEXT_FIELD):
                    result3 = True
        finally:
            if result1 and result2 and result3 is True:
                if self.login_page.wait_element_presented(self.driver, delay, ForgotPasswordPageLocators.SUBMIT_BUTTON):
                    write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                    update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
