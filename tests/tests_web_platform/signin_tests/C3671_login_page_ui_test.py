# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages import wtp_login_page_url
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators


@test(groups=['login_page', ])
class LogInPageUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_case = '3671'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_login_page_ui(self):
        delay = 3
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            try:
                assert wtp_login_page_url == self.login_page.get_cur_url(self.driver)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.SIGNIN_TITLE)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.USERNAME_FIELD)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.PASSWORD_FIELD)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.CAPTCHA_FRAME)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.KEEP_ME_CHECKBOX)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.SIGNIN_BUTTON)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.FORGOT_PASSWORD_LINK)
                assert self.login_page.search_element(self.driver, delay, SignInPageLocators.REGISTER_LINK)
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
