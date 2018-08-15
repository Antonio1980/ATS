# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators


@test(groups=['sign_in_page', ])
class LogInWithoutCaptchaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3984'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.email = cls.login_page.email
        cls.locators = SignInPageLocators()
        cls.password = cls.login_page.password
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'functional', 'negative', ])
    def test_sign_in_negative(self):
        delay = 1
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            self.login_page.wait_driver(,, self.driver, delay + 3
            username_field = self.login_page.find_element(self.driver, self.locators.USERNAME_FIELD)
            self.login_page.click_on_element(username_field)
            self.login_page.send_keys(username_field, self.email)
            password_true_field = self.login_page.find_element(self.driver, self.locators.PASSWORD_FIELD_TRUE)
            password_field = self.login_page.find_element(self.driver, self.locators.PASSWORD_FIELD)
            self.login_page.click_on_element(password_field)
            self.login_page.send_keys(password_true_field, self.password)
            self.login_page.driver_wait(self.driver, delay + 5)
            login_button = self.login_page.find_element(self.driver, self.locators.SIGNIN_BUTTON)
            self.login_page.click_on_element(login_button)
            self.login_page.driver_wait(self.driver, delay + 2)
            if self.login_page.find_element(self.driver, self.locators.CAPTCHA_ERROR):
                step2 = True
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
