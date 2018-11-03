# !/usr/bin/env python
# -*- coding: utf8 -*-
import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer import RegisteredCustomer
from src.base.base_exception import AutomationError
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import signin_page_locators


@ddt
@test(groups=['sign_in_page', ])
class SignInWithoutCaptchaTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3984'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.password = self.customer.password
        self.email = self.customer.pended_email
        self.locators = signin_page_locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['smoke', 'negative', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_in_without_captcha(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2 = False, True
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            self.browser.wait_driver(self.driver, delay)
            username_field = self.browser.find_element(self.driver, self.locators.USERNAME_FIELD)
            self.browser.click_on_element(username_field)
            self.browser.send_keys(username_field, self.email)
            password_true_field = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD_TRUE)
            password_field = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD)
            self.browser.click_on_element(password_field)
            self.browser.send_keys(password_true_field, self.password)
            self.browser.execute_js(self.driver, self.customer.script_signin)
            login_button = self.browser.find_element(self.driver, self.locators.SIGNIN_BUTTON)
            self.browser.click_on_element(login_button)
            assert self.browser.search_element(self.driver, self.locators.CAPTCHA_ERROR, delay)
            time.sleep(delay)
            captcha_error_text = self.browser.execute_js(self.driver, '''return $("[class='errorMessage hidden'] span[class='errorText']").text();''')
            if captcha_error_text != "":
                step2 = False
        except AutomationError as e:
            print("{0} test_sign_in_negative failed with error {0}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 is True and step2 is False:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
