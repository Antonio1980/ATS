# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.engine import write_file_result, update_test_case
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators


@test(groups=['sign_in_page', ])
class SignInPageUITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.locators = SignInPageLocators()
        cls.test_case = '3671'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_sign_in_page_ui(self):
        delay = 3
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            try:
                assert wtp_signin_page_url == self.login_page.get_cur_url(self.driver)
                assert self.login_page.search_element(self.driver, self.locators.SIGNIN_TITLE, delay)
                assert self.login_page.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
                assert self.login_page.search_element(self.driver, self.locators.PASSWORD_FIELD, delay)
                assert self.login_page.search_element(self.driver, self.locators.CAPTCHA_FRAME, delay)
                assert self.login_page.search_element(self.driver, self.locators.KEEP_ME_CHECKBOX, delay)
                assert self.login_page.search_element(self.driver, self.locators.SIGNIN_BUTTON, delay)
                assert self.login_page.search_element(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
                assert self.login_page.search_element(self.driver, self.locators.REGISTER_LINK, delay)
                result2 = True
            except TimeoutError:
                print("Time out occurred.")
        finally:
            if result1 & result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
