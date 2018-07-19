# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.engine import write_file_result, update_test_case
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages import forgot_password_page_url
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators


@test(groups=['forgot_password_page', ])
class ForgotPasswordUITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3558'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.locators = ForgotPasswordPageLocators()
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

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
            if self.login_page.wait_element_presented(self.driver, self.locators.FORGOT_PASSWORD_TITLE, delay):
                if self.login_page.wait_element_presented(self.driver, self.locators.EMAIL_TEXT_FIELD, delay):
                    result3 = True
        finally:
            if result1 and result2 and result3 is True:
                if self.login_page.wait_element_presented(self.driver, self.locators.SUBMIT_BUTTON, delay):
                    write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                    update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
