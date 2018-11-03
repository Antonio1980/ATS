# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.customer import Customer
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError
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
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.locators = signin_page_locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_in_page_ui(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            try:
                assert self.browser.wait_url_contains(self.driver, wtp_signin_page_url, delay)
                assert self.browser.search_element(self.driver, self.locators.SIGNIN_TITLE, delay)
                assert self.browser.search_element(self.driver, self.locators.USERNAME_FIELD, delay)
                assert self.browser.search_element(self.driver, self.locators.PASSWORD_FIELD, delay)
                assert self.browser.search_element(self.driver, self.locators.CAPTCHA_FRAME, delay)
                assert self.browser.search_element(self.driver, self.locators.KEEP_ME_CHECKBOX, delay)
                assert self.browser.search_element(self.driver, self.locators.SIGNIN_BUTTON, delay)
                assert self.browser.search_element(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
                assert self.browser.search_element(self.driver, self.locators.REGISTER_LINK, delay)
                step2 = True
            except AutomationError as e:
                print("{0} test_sign_in_page_ui failed with error {0}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
