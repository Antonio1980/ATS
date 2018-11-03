# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.customer import RegisteredCustomer
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import signin_page_locators
from tests.tests_web_platform.pages import wtp_dashboard_url, wtp_home_page_url, wtp_signin_page_url


@ddt
@test(groups=['sign_in_page', ])
class SignInCheckedTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6008'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.locators = signin_page_locators
        self.password = self.customer.password
        self.email = self.customer.pended_email
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['smoke', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_checked_sign_in(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            try:
                assert self.browser.wait_url_contains(self.driver, wtp_signin_page_url, delay)
                username_field = self.browser.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
                self.browser.click_on_element(username_field)
                self.browser.send_keys(username_field, self.email)
                password_field_true = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD_TRUE)
                password_field = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD)
                self.browser.click_on_element(password_field)
                self.browser.click_on_element(password_field_true)
                self.browser.send_keys(password_field_true, self.password)
                self.browser.execute_js(self.driver, self.customer.script_signin)
                self.browser.execute_js(self.driver, self.customer.script_test_token)
                keep_me_checkbox = self.browser.find_element(self.driver, self.locators.KEEP_ME_CHECKBOX)
                self.browser.click_on_element(keep_me_checkbox)
                login_button = self.browser.wait_element_clickable(self.driver, self.locators.SIGNIN_BUTTON, delay)
                self.browser.click_on_element(login_button)
                step2 = self.browser.wait_url_contains(self.driver, wtp_dashboard_url, delay)
            except AutomationError as e:
                print("{0} test_checked_sign_in failed with error {0}".format(e.__class__.__name__, e.__cause__))
            cookie_jwt = self.driver.get_cookie('dx_jwt')
            cookie_cid = self.driver.get_cookie('dx_cid')
            self.browser.close_driver(self.driver)
            self.driver = WebDriverFactory.get_driver(browser)
            self.home_page.open_home_page(self.driver, delay)
            self.driver.add_cookie(cookie_jwt)
            self.driver.add_cookie(cookie_cid)
            self.browser.refresh_browser(self.driver)
            time.sleep(delay)
            step3 = self.browser.wait_url_contains(self.driver, wtp_home_page_url, delay)
            step4 = self.browser.execute_js(self.driver, self.customer.script_is_signed)
        except AutomationError as e:
            print("{0} test_unchecked_sign_in failed with error {0}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
