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
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class ResendVerificationEmailTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6150'
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.password = self.signup_page.password
        self.email = self.signup_page.mailinator_email
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.locator = self.signup_page.locators.CODE_FIELD
        self.username = self.signup_page.mailinator_username
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_resend_verification_email(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            # 0 - verify email, 1 - change password, 2 - click on change_password, 3 - click on verify_email
            url = self.signup_page.get_email_updates(self.driver, self.email, 0)
            Browser.go_back(self.driver)
            self.home_page.go_back_and_wait(self.driver, self.home_page.wtp_open_account_url)
            step3 = self.signup_page.click_on_link_on_email_screen(self.driver, self.home_page.wtp_open_account_url, 3)
            url2 = self.signup_page.get_email_updates(self.driver, self.email, 0)
            if url != url2:
                Browser.go_to_url(self.driver, url2)
            time.sleep(delay)
            if Browser.find_element(self.driver, self.locator):
                step4 = True
        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
