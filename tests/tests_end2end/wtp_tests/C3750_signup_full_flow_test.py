# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['sign_up_page', ])
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
        cls.phone = cls.signup_page.phone
        cls.username = Instruments.generate_user_first_last_name()
        cls.email = cls.username + "@mailinator.com"
        cls.password = cls.signup_page.password
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.results_file = BaseConfig.WTP_TESTS_RESULT
        cls.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['e2e', 'positive', ], depends_on_groups=["functional", ])
    def test_registration_full_flow_with_redis(self):
        delay, token, customer_id = 5, "", ""
        step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11, step12 = \
            False, False, False, False, False, False, False, False, False, False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, )
            customer_id = Browser.execute_js(self.driver, self.signup_page.script_customer_id)
            keys = Instruments.get_redis_keys("email_validation_token*")
            token_keys = Instruments.parse_redis_token(keys, "b'")
            # tokens = parse_redis_token(keys, "b'email_validation_token_") # to get all tokens list
            token = Instruments.get_redis_token(token_keys, customer_id)
            url = self.signup_page.wtp_open_account_url + "?validation_token=" + token + "&email=" + self.username + "%40mailinator.com"
            step3 = self.signup_page.go_by_token_url(self.driver, url)
            step4 = self.signup_page.add_phone(self.driver, self.phone)
            sms_code = Instruments.get_redis_value(customer_id)
            step5 = self.signup_page.enter_phone_code(self.driver, sms_code)
            step6 = self.signup_page.fill_personal_details(self.driver, self.birthday, self.zip, self.city)
            step7 = self.signup_page.fill_client_checklist_1(self.driver, "Federation of Federations", "freestyle")
            step8 = self.signup_page.fill_client_checklist_2(self.driver)
            step9 = self.signup_page.fill_client_checklist_3(self.driver)
            step10 = self.signup_page.finish_registration(self.driver)
            step11 = self.home_page.sign_out(self.driver)
            step12 = self.signin_page.sign_in(self.driver, self.email, self.password)
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 and step10 \
                    and step11 and step12 is True:
                Instruments.write_file_user(self.email + "," + self.password + "," + customer_id + "," + token + "\n",
                                self.customers_file)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        Browser.close_browser(cls.driver)
