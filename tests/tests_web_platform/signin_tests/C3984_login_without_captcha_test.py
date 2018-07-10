# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.engine import write_file_result, update_test_case
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators


@test(groups=['sign_in_page', ])
class LogInWithoutCaptchaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_case = '3984'
        cls.locators = SignInPageLocators()
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.email = cls.login_page.email
        cls.password = cls.login_page.password

    @test(groups=['smoke', 'functional', 'negative', ])
    def test_sign_in_negative(self):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            self.login_page.wait_driver(self.driver, delay + 3)
            username_field = self.login_page.find_element(self.driver, self.locators.USERNAME_FIELD)
            self.login_page.click_on_element(username_field)
            self.login_page.send_keys(username_field, self.email)
            password_true_field = self.login_page.find_element(self.driver, self.locators.PASSWORD_TRUE_FIELD)
            password_field = self.login_page.find_element(self.driver, self.locators.PASSWORD_FIELD)
            self.login_page.click_on_element(password_field)
            self.login_page.send_keys(password_true_field, self.password)
            self.login_page.driver_wait(self.driver, delay + 5)
            login_button = self.login_page.find_element(self.driver, self.locators.SIGNIN_BUTTON)
            self.login_page.click_on_element(login_button)
            self.login_page.driver_wait(self.driver, delay + 2)
            if self.login_page.find_element(self.driver, self.locators.CAPTCHA_ERROR):
                result2 = True
        finally:
            if result1 and result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
