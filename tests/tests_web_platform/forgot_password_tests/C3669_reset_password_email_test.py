# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer import ForgottenCustomer
from src.base.base_exception import AutomationError
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


@ddt
@test(groups=['forgot_password_page', ])
class ResetPasswordEmailTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3669'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = ForgottenCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.forgot_password_page = ForgotPasswordPage()
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.password = self.customer.password
        self.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
        self.email = self.customer.forgotten_email
        self.customer_id = self.customer.forgotten_customer_id
        self.sid_token = self.customer.forgotten_guerrilla_token
        self.time_stamp = self.customer.forgotten_guerrilla_timestamp
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_reset_password_email(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay, token, customer_id, sid_token, time_stamp = 5, "", "", "", ""
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            step2 = self.signin_page.click_on_link(self.driver, 1, delay)
            step3 = self.forgot_password_page.fill_email_address_form(self.driver, self.email, delay)
            time.sleep(delay * delay)
            check_email_response = Instruments.check_guerrilla_email(self.time_stamp, self.sid_token)
            # emails_list_response = Instruments.get_guerrilla_emails(self.username, self.sid_token)
            self.sid_token = check_email_response[1]['sid_token']
            mail_id = str(check_email_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.time_stamp, mail_id, self.sid_token)
            sid_token = fetch_email_response[1]['sid_token']
            time_stamp = fetch_email_response[1]['mail_timestamp']
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            new_password_url = parsed_html.center.find_all('a')[1]['href']
            step4 = self.forgot_password_page.go_by_token_url(self.driver, new_password_url)
        except AutomationError as e:
            print("{0} test_reset_password_email failed with error {0}".format(e.__class__.__name__, e.__cause__))
        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_user(self.email + "," + self.password + "," + self.customer_id + "," + sid_token +
                #                            "," + time_stamp + "\n", self.customers_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
            self.browser.close_browser(self.driver)
