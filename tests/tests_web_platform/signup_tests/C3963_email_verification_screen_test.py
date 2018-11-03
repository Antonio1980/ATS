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
from tests.tests_web_platform.pages import wtp_open_account_url
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class EmailVerificationScreenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3963'
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.email = self.customer.email
        self.username = self.customer.username
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_email_verification_screen(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            try:
                assert self.browser.wait_url_contains(self.driver, wtp_open_account_url, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.EMAIL_NOT_ARRIVED, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.EMAIL_ALREADY_VERIFIED, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.GO_BACK_LINK, delay)
                step3 = True
            except AutomationError as e:
                print("{0} test_email_verification_screen failed with error: {1}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
