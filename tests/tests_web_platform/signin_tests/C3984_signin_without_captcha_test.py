# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators

@ddt
@test(groups=['sign_in_page', ])
class LogInWithoutCaptchaTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3984'
        self.home_page = HomePage()
        self.login_page = SignInPage()
        self.email = self.login_page.email
        self.locators = SignInPageLocators()
        self.password = self.login_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['smoke', 'negative', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_in_negative(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 1
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            Browser.wait_driver(self.driver, delay + 3)
            username_field = Browser.find_element(self.driver, self.locators.USERNAME_FIELD)
            Browser.click_on_element(username_field)
            Browser.send_keys(username_field, self.email)
            password_true_field = Browser.find_element(self.driver, self.locators.PASSWORD_FIELD_TRUE)
            password_field = Browser.find_element(self.driver, self.locators.PASSWORD_FIELD)
            Browser.click_on_element(password_field)
            Browser.send_keys(password_true_field, self.password)
            login_button = Browser.find_element(self.driver, self.locators.SIGNIN_BUTTON)
            Browser.click_on_element(login_button)
            if Browser.find_element(self.driver, self.locators.CAPTCHA_ERROR):
                step2 = True
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.login_page.close_browser(self.driver)
