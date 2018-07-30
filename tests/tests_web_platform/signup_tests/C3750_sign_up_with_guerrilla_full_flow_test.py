# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import time
import unittest
from proboscis import test
from bs4 import BeautifulSoup
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from src.base.instruments import write_file_result,update_test_case,get_redis_value,write_file_user,get_guerrilla_email


@test(groups=['sign_up_page', 'e2e', ])
class SignUpFullFlowGuerrillaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zip = "45263"
        cls.city = "Ashdod"
        cls.test_case = '3750'
        cls.birthday = "13/08/1980"
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.signin_page = SignInPage()
        cls.phone = cls.signup_page.phone
        cls.password = cls.signup_page.password
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.log_file = cls.home_page.WTP_LOG_FILE
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.customers = cls.home_page.WTP_TESTS_CUSTOMERS
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        response = get_guerrilla_email("get_email_address")
        cls.time_stamp = str(response['email_timestamp'])
        cls.email = response['email_addr']
        cls.sid_token = response['sid_token']
        cls.username = re.findall(r"([\w.-]+)", cls.email)[0]
        cls.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(cls.email)

    @test(groups=['regression', 'functional', 'positive', ], depends_on_groups=["smoke", "sanity", ])
    def test_sign_up_full_flow_with_guerrilla(self):
        delay = 3
        customer_id = ""
        result1, result2, result3, result4, result5, result6, result7, result8, result9, result10, result11, result12 =\
            False, False, False, False, False, False, False, False, False, False, False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password,
                                                        self.element)
            customer_id = self.signup_page.execute_js(self.driver, self.signup_page.script_customer_id)
            time.sleep(5)
            response1 = get_guerrilla_email("get_email_list&offset=0&site=guerrillamail.com&_=" + self.username,
                                            self.sid_token)
            email_id = str(response1['list'][0]['mail_id'])
            response2 = get_guerrilla_email("fetch_email&email_id=mr_" + email_id + "&site=guerrillamail.com&_=",
                                            self.sid_token)
            html = response2['mail_body']
            parsed_html = BeautifulSoup(html, 'html.parser')
            url = parsed_html.center.find_all('a')[1]['href']
            # token = url.split('=')[1].split('&')[0]
            result3 = self.signup_page.go_by_token_url(self.driver, url)
            result4 = self.signup_page.add_phone(self.driver, self.phone)
            sms_code = get_redis_value(customer_id)
            result5 = self.signup_page.enter_phone_code(self.driver, sms_code)
            result6 = self.signup_page.fill_personal_details(self.driver, self.birthday, self.zip, self.city)
            result7 = self.signup_page.fill_client_checklist_1(self.driver, "Federation of Federations", "freestyle")
            result8 = self.signup_page.fill_client_checklist_2(self.driver, "61")
            result9 = self.signup_page.fill_client_checklist_3(self.driver)
            result10 = self.signup_page.finish_registration(self.driver)
            result11 = self.home_page.open_login_page(self.driver, delay)
            result12 = self.signin_page.sign_in(self.driver, self.email, self.password)
        finally:
            if result1 and result2 and result3 and result4 and result5 and result6 and result7 \
                    and result8 and result9 and result10 and result11 and result12 is True:
                write_file_user(self.email + "," + self.password + "," + customer_id + "\n", self.customers)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                response = update_test_case(self.test_run, self.test_case, 1)
                write_file_result(str(response), self.log_file)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                response = update_test_case(self.test_run, self.test_case, 0)
                write_file_result(str(response), self.log_file)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)