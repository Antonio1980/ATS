# !/usr/bin/env python
# -*- coding: utf8 -*-
import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.customer import Customer
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages import wtp_open_account_url
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class LinksOnVerifyEmailScreenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3964'
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.email = self.customer.email
        self.username = self.customer.username
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    @test(groups=['smoke', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_links_on_verify_email_screen(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5 = False, False, False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            # 1 - Email verified link, 2 - Go back link, 3 - Resend email
            step3 = self.signup_page.click_on_link_on_email_screen(self.driver, wtp_open_account_url, 1)
            step4 = self.signup_page.click_on_link_on_email_screen(self.driver, wtp_open_account_url, 2)
            self.browser.go_back(self.driver)
            time.sleep(delay)
            step5 = self.signup_page.click_on_link_on_email_screen(self.driver, wtp_open_account_url, 3)
        finally:
            if step1 and step2 and step3 and step4 and step5 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
