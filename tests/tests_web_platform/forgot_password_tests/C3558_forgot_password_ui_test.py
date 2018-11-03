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
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import forgot_password_page_locators


@ddt
@test(groups=['forgot_password_page', ])
class ForgotPasswordUITest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3558'
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = forgot_password_page_locators
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_forgot_password_page_ui(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            step2 = self.signin_page.click_on_link(self.driver, 1, delay)
            try:
                self.browser.wait_element_presented(self.driver, self.locators.FORGOT_PASSWORD_TITLE, delay)
                self.browser.wait_element_presented(self.driver, self.locators.EMAIL_TEXT_FIELD, delay)
                self.browser.wait_element_presented(self.driver, self.locators.SUBMIT_BUTTON, delay)
                step3 = True
            except AutomationError as e:
                print("{0} test_forgot_password_page_ui failed with error {0}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
