# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from src.base.engine import write_file_result, update_test_case, get_redis_value


@test(groups=['sign_up_page', 'e2e', ])
class SignUpFullFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3750'
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.email = cls.signup_page.email
        cls.phone = cls.signup_page.phone
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.password = cls.signup_page.password
        cls.first_last_name = cls.signup_page.first_last_name
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['regression', 'functional', 'positive', ], depends_on_groups=["smoke", "sanity", ])
    def test_sign_up_full_flow(self):
        delay = 1
        result1, result2, result3, result4, result5, result6, result7, result8, result9 = False, False, False, False, False, False, False, False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, self.first_last_name, self.email, self.password)
            # 0 - verify email, 1 - change password, 2 - click on change_password, 3 - click on verify_email
            url = self.signup_page.get_email_updates(self.driver, self.email, 0)
            self.token = url.split('=')[1].split('&')[0]
            result3 = self.signup_page.go_by_token_url(self.driver, url)
            customer_id = self.signup_page.execute_js(self.driver, 'return SO.model.Customer.getCustomerId();')
            result4 = self.signup_page.add_phone(self.driver, self.phone)
            sms_code = get_redis_value(customer_id)
            result5 = self.signup_page.enter_phone_code(self.driver, sms_code)
            # birthday, zip, city
            result6 = self.signup_page.fill_personal_details(self.driver, "13/08/1980", "45263", "Ashdod")
            result7 = self.signup_page.fill_client_checklist_1(self.driver, "Federation of Federations", "freestyle")
            result8 = self.signup_page.fill_client_checklist_2(self.driver, "61")
            result9 = self.signup_page.fill_client_checklist_3(self.driver)
        finally:
            if result1 and result2 and result3 and result4 and result5 and result6 and result7 and result8 and result9 is True:
                write_file_result(self.first_last_name + "," + self.email + "," + self.password + "," + self.token+"\n",
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
        cls.home_page.close_browser(cls.driver)

