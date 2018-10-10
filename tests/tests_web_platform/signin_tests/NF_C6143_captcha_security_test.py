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
class CaptchaUsabilityUITest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3671'
        self.home_page = HomePage()
        self.login_page = SignInPage()
        self.locators = signin_page_locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_captcha_usability_ui(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 3
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            assert Browser.wait_url_contains(self.driver, wtp_signin_page_url, delay)
            captcha_frame = Browser.search_element(self.driver, self.locators.CAPTCHA_FRAME, delay)
            Browser.switch_frame(self.driver, captcha_frame)
            captcha_terms = Browser.search_element(self.driver, self.locators.CAPTCHA_TERMS, delay)
            Browser.click_on_element(captcha_terms)
            windows = self.driver.window_handles
            self.switch_window(self.driver, windows[1])
            assert Browser.wait_url_contains(self.driver, self.home_page.captcha_terms_url, delay)
            self.switch_window(self.driver, windows[0])
            captcha_privacy = Browser.search_element(self.driver, self.locators.CAPTCHA_PRIVACY, delay)
            Browser.click_on_element(captcha_privacy)
            windows = self.driver.window_handles
            self.switch_window(self.driver, windows[1])
            assert Browser.wait_url_contains(self.driver, self.home_page.captcha_privacy_url, delay)
            step2 = True
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)


def tearDown(self):
    Browser.close_browser(self.driver)
