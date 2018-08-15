# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators


@test(groups=['sign_in_page', ])
class SignInPageUITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3671'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.locators = SignInPageLocators()
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results =  cls.login_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_sign_in_page_ui(self):
        delay = 3
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            try:
                assert self.login_page.wait_url_contains(self.driver, wtp_signin_page_url, delay)
                assert self.login_page.search_element(self.driver, self.locators.SIGNIN_TITLE, delay)
                assert self.login_page.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
                assert self.login_page.search_element(self.driver, self.locators.PASSWORD_FIELD, delay)
                assert self.login_page.search_element(self.driver, self.locators.CAPTCHA_FRAME, delay)
                assert self.login_page.search_element(self.driver, self.locators.KEEP_ME_CHECKBOX, delay)
                assert self.login_page.search_element(self.driver, self.locators.SIGNIN_BUTTON, delay)
                assert self.login_page.search_element(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
                assert self.login_page.search_element(self.driver, self.locators.REGISTER_LINK, delay)
                step2 = True
            except TimeoutError:
                print("Time out occurred.")
        finally:
            if step1 and step2 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
