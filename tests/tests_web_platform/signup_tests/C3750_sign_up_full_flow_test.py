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
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class SignUpFullFlowTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3750'
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.signin_page = SignInPage()
        self.zip = self.customer.zip
        self.city = self.customer.city
        self.phone = self.customer.phone
        self.birthday = self.customer.birthday
        self.password = self.customer.password
        self.browser = self.customer.get_browser_functionality()
        # Return tuple of 0- guerrilla_email, 1- guerrilla_username, 2- sid_token, 3- time_stamp
        guerrilla_details = self.customer.get_guerrilla_details()
        self.email = guerrilla_details[0]
        self.username = guerrilla_details[1]
        self.sid_token = guerrilla_details[2]
        self.time_stamp = guerrilla_details[3]
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    @test(groups=['regression', 'positive', ], depends_on_groups=["sanity", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_up_full_flow(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay, sid_token, time_stamp, customer_id = 5, "", "", ""
        step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11, step12, step13 = \
            False, False, False, False, False, False, False, False, False, False, False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            customer_id = self.browser.execute_js(self.driver, self.customer.script_customer_id)
            time.sleep(delay * delay)
            emails_list_response = Instruments.get_guerrilla_emails(self.username, self.sid_token)
            sid_token = emails_list_response[1]['sid_token']
            mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.time_stamp, mail_id, sid_token)
            sid_token = fetch_email_response[1]['sid_token']
            time_stamp = fetch_email_response[1]['mail_timestamp']
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            url = parsed_html.center.find_all('a')[1]['href']
            # token = url.split('=')[1].split('&')[0]
            step3 = self.signup_page.go_by_token_url(self.driver, url)
            step4 = self.signup_page.add_phone(self.driver, self.phone)
            step5 = self.signup_page.enter_phone_code(self.driver, "592031", delay)
            step6 = self.signup_page.fill_personal_details(self.driver, self.birthday, self.zip, self.city)
            step7 = self.signup_page.fill_client_checklist_1(self.driver, "Federation of Federations", "freestyle", delay)
            step8 = self.signup_page.fill_client_checklist_2(self.driver, delay)
            step9 = self.signup_page.fill_client_checklist_3(self.driver, delay)
            step10 = self.signup_page.finish_registration(self.driver, delay)
            step11 = self.home_page.sign_out(self.driver, delay)
            step12 = self.home_page.open_signin_page(self.driver, delay)
            step13 = self.signin_page.sign_in(self.driver, self.email, self.password)
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 and step10 and \
                    step11 and step12 and step13 is True:
                Instruments.write_file_user(self.email + "," + self.password + "," + customer_id + "," + sid_token +
                                            "," + time_stamp + "\n", self.customers_file)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
