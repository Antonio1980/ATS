# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from src.base.instruments import write_file_result, update_test_case, get_redis_keys, get_redis_value, write_file_user,\
     get_redis_token, parse_redis_token


@test(groups=['sign_up_page', 'e2e', ])
class SignUpFullFlowRedisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zip = "45263"
        cls.city = "Ashdod"
        cls.test_case = '3750'
        cls.birthday = "13/08/1980"
        cls.home_page = HomePage()
        cls.signin_page = SignInPage()
        cls.signup_page = SignUpPage()
        cls.email = cls.signup_page.email
        cls.phone = cls.signup_page.phone
        cls.prefix = cls.signup_page.prefix
        cls.username = cls.signup_page.username
        cls.password = cls.signup_page.password
        cls.url = cls.home_page.API_STAGING_URL
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.log_file = cls.home_page.WTP_LOG_FILE
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.customers = cls.home_page.WTP_TESTS_CUSTOMERS
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['regression', 'functional', 'positive', ], depends_on_groups=["smoke", "sanity", ])
    def test_registration_full_flow(self):
        delay = 3
        customer_id = ""
        result1, result2, result3, result4, result5, result6, result7, result8, result9, result10 = \
            False, False, False, False, False, False, False, False, False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password)
            customer_id = self.signup_page.execute_js(self.driver, self.signup_page.script_customer_id)
            keys = get_redis_keys("email_validation_token*")
            token_keys = parse_redis_token(keys, "b'")
            # tokens = parse_redis_token(keys, "b'email_validation_token_") # to get all tokens list
            token = get_redis_token(token_keys, customer_id)
            url = self.signup_page.wtp_open_account_url + "?validation_token=" + token + "&email=" + self.prefix + "%40mailinator.com"
            result3 = self.signup_page.go_by_token_url(self.driver, url)
            result4 = self.signup_page.add_phone(self.driver, self.phone)
            sms_code = get_redis_value(customer_id)
            result5 = self.signup_page.enter_phone_code(self.driver, sms_code)
            result6 = self.signup_page.fill_personal_details(self.driver, self.birthday, self.zip, self.city)
            result7 = self.signup_page.fill_client_checklist_1(self.driver, "Federation of Federations", "freestyle")
            result8 = self.signup_page.fill_client_checklist_2(self.driver, "61")
            result9 = self.signup_page.fill_client_checklist_3(self.driver)
            result10 = self.signup_page.finish_registration(self.driver)
            # result11 = self.home_page.open_login_page(self.driver, delay)
            # result12 = self.signin_page.sign_in(self.driver, self.email, self.password)
        finally:
            if result1 and result2 and result3 and result4 and result5 and result6 and result7 and result8 and result9 \
                    and result10 is True:
                write_file_user(self.email + "," + self.password + "," + customer_id + "\n", self.customers)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                response = update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                response = update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.signup_page.close_browser(cls.driver)
