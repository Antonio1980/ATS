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
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import signin_page_locators


@ddt
@test(groups=['sign_in_page', ])
class SignInPageUITest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3671'
        self.home_page = HomePage()
        self.login_page = SignInPage()
        self.locators = signin_page_locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file =  BaseConfig.WTP_TESTS_RESULT

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_in_page_ui(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 3
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            try:
                assert Browser.wait_url_contains(self.driver, wtp_signin_page_url, delay)
                assert Browser.search_element(self.driver, self.locators.SIGNIN_TITLE, delay)
                assert Browser.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
                assert Browser.search_element(self.driver, self.locators.PASSWORD_FIELD, delay)
                assert Browser.search_element(self.driver, self.locators.CAPTCHA_FRAME, delay)
                assert Browser.search_element(self.driver, self.locators.KEEP_ME_CHECKBOX, delay)
                assert Browser.search_element(self.driver, self.locators.SIGNIN_BUTTON, delay)
                assert Browser.search_element(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
                assert Browser.search_element(self.driver, self.locators.REGISTER_LINK, delay)
                step2 = True
            except Exception as e:
                print("Exception is occurred.".format(e))
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
