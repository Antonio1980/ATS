# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import time
import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer import ForgottenCustomer
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@test(groups=['forgot_password_page', ])
class ForgotPasswordStandAloneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3668'
        cls.home_page = HomePage()
        cls.signin_page = SignInPage()
        cls.signup_page = SignUpPage()
        cls.customer = ForgottenCustomer()
        cls.password = cls.customer.password
        cls.new_password = cls.password + "Qa"
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.forgot_password_page = ForgotPasswordPage()
        cls.results_file = BaseConfig.WTP_TESTS_RESULT
        cls.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
        cls.browser = cls.customer.get_browser_functionality()
        guerrilla_details = cls.customer.get_guerrilla_details()
        cls.email = guerrilla_details[0]
        cls.username = guerrilla_details[1]
        cls.sid_token = guerrilla_details[2]
        cls.time_stamp = guerrilla_details[3]
        cls.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
        cls.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(cls.email)

    @test(groups=['e2e', 'positive', ], depends_on_groups=["functional", ])
    def test_forgot_password_full_flow(self):
        delay, customer_id = 5, ""
        step1, step2, step3, step4, step5, step6, step7 = False, False, False, False, False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            customer_id = self.browser.execute_js(self.driver, self.customer.script_customer_id)
            step3 = self.signin_page.go_by_token_url(self.driver, wtp_signin_page_url)
            # Option 1- forgot password, Option 2- register link
            step4 = self.signin_page.click_on_link(self.driver, 1, delay)
            step5 = self.forgot_password_page.fill_email_address_form(self.driver, self.email, delay)
            time.sleep(delay * delay)
            emails_list_response = Instruments.get_guerrilla_emails(self.username, self.sid_token)
            self.sid_token = emails_list_response[1]['sid_token']
            mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.time_stamp, mail_id, self.sid_token)
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            new_password_url = parsed_html.center.find_all('a')[1]['href']
            # token = new_password_url.split('=')[1].split('&')[0]
            step6 = self.forgot_password_page.go_by_token_url(self.driver, new_password_url)
            step7 = self.forgot_password_page.set_new_password(self.driver, self.new_password, new_password_url)
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 is True:
                Instruments.write_file_user(self.email + "," + self.password + "," + customer_id + "," + self.sid_token
                                            + "," + self.time_stamp + "\n", self.customers_file)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close_browser(cls.driver)
