# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import signin_page_locators
from tests.tests_web_platform.pages import wtp_dashboard_url, signin_user_page_url, wtp_home_page_url


@ddt
@test(groups=['sign_in_page', ])
class CookieExpirationTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6121'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.email = self.signin_page.email
        self.locators = signin_page_locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.password = self.signin_page.password
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.win_details = ('Chrome', '68.0', 'Windows', '10', '2048x1536')

    @test(groups=['smoke', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_expiration_cookie(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            try:
                if Browser.wait_url_contains(self.driver, signin_user_page_url, delay):
                    username_field = Browser.find_element(self.driver, self.locators.USERNAME_FIELD)
                    Browser.click_on_element(username_field)
                    Browser.send_keys(username_field, self.email)
                    password_field_true = Browser.find_element(self.driver, self.locators.PASSWORD_FIELD_TRUE)
                    password_field = Browser.find_element(self.driver, self.locators.PASSWORD_FIELD)
                    Browser.click_on_element(password_field)
                    Browser.click_on_element(password_field_true)
                    Browser.send_keys(password_field_true, self.password)
                    Browser.execute_js(self.driver, self.home_page.script_login)
                    keep_me_checkbox = Browser.find_element(self.driver, self.locators.KEEP_ME_CHECKBOX)
                    Browser.click_on_element(keep_me_checkbox)
                    login_button = Browser.wait_element_clickable(self.driver, self.locators.SIGNIN_BUTTON, delay)
                    Browser.click_on_element(login_button)
            finally:
                if Browser.wait_url_contains(self.driver, wtp_dashboard_url, delay):
                    step2 = True
            cookie_jwt = self.driver.get_cookie('dx_jwt')
            cookie_cid = self.driver.get_cookie('dx_cid')
            Browser.close_driver(self.driver)
            time.sleep(delay * 60)
            self.driver = WebDriverFactory.get_browser(browser)
            self.home_page.open_home_page(self.driver, delay)
            self.driver.add_cookie(cookie_jwt)
            self.driver.add_cookie(cookie_cid)
            Browser.refresh_browser(self.driver)
            time.sleep(delay)
            if Browser.wait_url_contains(self.driver, wtp_home_page_url, delay):
                step3 = True
            step4 = Browser.execute_js(self.driver, self.home_page.script_is_signed)
        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)