# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from src.base.engine import * #write_file_result, update_test_case, get_redis_keys, get_redis_value, parse_redis_token, get_redis_token


@test(groups=['sign_up_page', 'e2e', ])
class RegistrationFullFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = BaseConfig.API_STAGING_URL
        cls.signup_page = SignUpPage()
        cls.home_page = HomePage()
        cls.test_case = '3750'
        cls.phone = cls.signup_page.phone
        cls.prefix = cls.signup_page.prefix
        cls.email = cls.signup_page.email
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.password = cls.signup_page.password
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.first_last_name = cls.signup_page.first_last_name

    @test(groups=['regression', 'functional', 'positive', ], depends_on_groups=["smoke", "sanity", ])
    def test_registration_full_flow(self):
        delay = 1
        result0, result1, result2, result3, result4, result5, result6, result7, result8 = False, False, False, False, False, False, False, False, False
        try:
            result0 = self.home_page.open_signup_page(self.driver, delay)
            result1 = self.signup_page.fill_signup_form(self.driver, self.first_last_name, self.email, self.password)
            customer_id = self.signup_page.execute_js(self.driver, 'return SO.model.Customer.getCustomerId();')
            keys = get_redis_keys("email_validation_token*")
            token_keys = parse_redis_token(keys, "b'")
            # tokens = parse_redis_token(keys, "b'email_validation_token_")
            token = get_redis_token(token_keys, customer_id)
            url = self.signup_page.wtp_open_account_url + "?validation_token=" + token + "&email=" + self.prefix + "%40mailinator.com"
            result2 = self.signup_page.go_by_token_url(self.driver, url)
            result3 = self.signup_page.add_phone(self.driver, self.phone)
            sms_code = get_redis_value(customer_id)
            result4 = self.signup_page.enter_phone_code(self.driver, sms_code)
            # birthday, zip, city
            result5 = self.signup_page.fill_personal_details(self.driver, "13/08/1980", "45263", "Ashdod")
            result6 = self.signup_page.fill_client_checklist_1(self.driver, "Federation of Federations", "freestyle")
            result7 = self.signup_page.fill_client_checklist_2(self.driver, "61")
            result8 = self.signup_page.fill_client_checklist_3(self.driver)
        finally:
            if result0 and result1 and result2 and result3 and result4 and result5 and result6 and result7 and result8 is True:
                write_file_result(self.first_last_name + "," + self.email + "," + self.password + "," + token + "\n",
                                  BaseConfig.WTP_TESTS_CUSTOMERS)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                response = update_test_case(self.test_run, self.test_case, 1)
                write_file_result(str(response), BaseConfig.WTP_LOG_FILE)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                response = update_test_case(self.test_run, self.test_case, 0)
                write_file_result(str(response), BaseConfig.WTP_LOG_FILE)

    @classmethod
    def tearDownClass(cls):
        cls.signup_page.close_browser(cls.driver)

