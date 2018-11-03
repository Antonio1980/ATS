# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import arrow
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.customer import RegisteredCustomer
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import signin_page_locators


@ddt
@test(groups=['sign_in_page', ])
class CookieCreatedTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6121'
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
    def test_created_cookie(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
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
            time.sleep(delay)
            step2 = self.browser.execute_js(self.driver, self.customer.script_is_signed)
            cookie_jwt = self.driver.get_cookie('dx_jwt')
            cookie_cid = self.driver.get_cookie('dx_cid')
            time_stamp_jwt = arrow.get(cookie_jwt['expiry']).format('YYYY-MM-DD')
            time_stamp_cid = arrow.get(cookie_cid['expiry']).format('YYYY-MM-DD')
            time_stamp_cur = arrow.utcnow().shift(days=+30).format('YYYY-MM-DD')
            if time_stamp_cur == time_stamp_jwt and time_stamp_cur == time_stamp_cid:
                step3 = True
        except AutomationError as e:
            print("{0} test_created_cookie failed with error {0}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
