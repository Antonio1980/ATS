# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages import forgot_password_page_url
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators


@test(groups=['forgot_password_page', ])
class ForgotPasswordUITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3558'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.locators = ForgotPasswordPageLocators()
        cls.results_file = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'gui', 'positive', ])
    def test_forgot_password_page_ui(self):
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay + 3)
            # Option 1- forgot password, Option 2- register link
            step2 = self.login_page.click_on_link(self.driver, 1, delay + 5)
            assert self.login_page.wait_url_contains(self.driver, forgot_password_page_url, delay)
            if self.login_page.wait_element_presented(self.driver, self.locators.FORGOT_PASSWORD_TITLE, delay):
                if self.login_page.wait_element_presented(self.driver, self.locators.EMAIL_TEXT_FIELD, delay):
                    step3 = True
        finally:
            if step1 and step2 and step3 is True:
                if self.login_page.wait_element_presented(self.driver, self.locators.SUBMIT_BUTTON, delay):
                    Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                    Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
