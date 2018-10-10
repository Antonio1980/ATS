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
from tests.tests_web_platform.pages import user_open_account_url
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class BrokenTokenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6149'
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.password = self.signup_page.password
        self.email = self.signup_page.mailinator_email
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.username = self.signup_page.mailinator_username
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_broken_token(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay, token, customer_id = 5, "", ""
        invalid_token = "3!*5"
        step1, step2, step3 = False, False, True
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            # 0 - verify email, 1 - change password, 2 - click on change_password, 3 - click on verify_email
            url = self.signup_page.get_email_updates(self.driver, self.email, 0)
            token = url.split('=')[2].split('&')[0] + invalid_token
            broken_url = user_open_account_url + "&validation_token=" + token + "&email=" + self.username + "%40mailinator.com"
            step3 = self.signup_page.go_by_token_url(self.driver, broken_url)
        finally:
            if step1 and step2 is True and step3 is False:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)