# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from src.base.customer import Customer
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class EnterCodeScreenDDTTest(unittest.TestCase):
    def setUp(self):
        self.test_case = "6309"
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        # 0- email, 1- username, 2- sid_token, 3- time_stamp
        customer_details = self.customer.get_guerrilla_details()
        self.browser = self.customer.get_browser_functionality()
        self.password = self.customer.password
        self.email = customer_details[0]
        self.username = customer_details[1]
        self.sid_token = customer_details[2]
        self.time_stamp = customer_details[3]
        self.phone = self.customer.phone
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.PHONE_CODES))
    @unpack
    def test_enter_code_screen_ddt(self, code):
        delay = 5
        step1, step2, step3, step4, step5, step6 = False, False, False, False, False, True
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            time.sleep(delay * delay)
            emails_list_response = Instruments.get_guerrilla_emails(self.username, self.sid_token)
            self.sid_token = emails_list_response[1]['sid_token']
            mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.time_stamp, mail_id, self.sid_token)
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            url = parsed_html.center.find_all('a')[1]['href']
            step3 = self.signup_page.go_by_token_url(self.driver, url)
            time.sleep(delay)
            step4 = self.signup_page.add_phone(self.driver, self.phone)
            try:
                submit_button = self.browser.wait_element_clickable(self.driver, self.locators.SUBMIT_BUTTON, delay + 5)
                self.browser.click_on_element(submit_button)
                if self.browser.wait_element_presented(self.driver, self.locators.FIELD_ERROR, delay) is not False:
                    step5 = True
            except AutomationError as e:
                print("{0} test_enter_code_screen_ddt failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            step6 = self.signup_page.enter_phone_code(self.driver, code, delay)
        finally:
            if step1 and step2 and step3 and step4 and step5 is True and step6 is False:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close_browser(cls.driver)
