# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
import requests
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.signup_page import SignUpPage
from src.base.engine import write_file_result, update_test_case, get_redis_keys, get_redis_value


@test(groups=['sign_up_page', 'e2e', ])
class RegistrationFullFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = BaseConfig.API_STAGING_URL
        cls.signup_page = SignUpPage()
        cls.test_case = '3750'
        cls.prefix = cls.signup_page.prefix
        cls.email = cls.signup_page.email
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.password = cls.signup_page.password
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.first_last_name = cls.signup_page.first_last_name
        cls.headers = {'Content-Type': "application/json"}
        cls.payload = "{\n\t\"jsonrpc\": \"2.0\",\n\t\"method\": \"Authorization.SignUp\"," \
                      "\n\t\"params\": [{\n\t\t\"FirstName\": \"%s\",\n\t\t\"LastName\": \"%s\"," \
                      "\n\t\t\"Email\": \"%s\",\n\t\t\"Password\": \"%s\"," \
                      "\n\t\t\"receivePromoEmail\": false,\n\t\t\"AcceptTerms\": true," \
                      "\n\t\t\"Captcha\": \"test_test\",\n\t\t\"siteLanguage\": \"en\"," \
                      "\n\t\t\"EmailValidationUrl\": \"http://staging-plat.dx.exchange:30010/appProxy/openAccountDx.html\"," \
                      "\n\t\t\"receivePromoSMS\": false,\n\t\t\"receivePromoPushToMobile\": false," \
                      "\n\t\t\"receiveTradingEmail\": false \n\t}],\n\t\"id\": \"1\"\n}" % (cls.first_last_name, cls.first_last_name, cls.email, cls.password)

    @test(groups=['regression', 'functional', 'positive', ], depends_on_groups=["smoke", "sanity", ])
    def test_registration_full_flow(self):
        temp, temp2, temp3 = [], [], []
        delay = 1
        result1, result2, result3, result4, result5, result6, result7, result8 = False, False, False, False, False, False, False, False
        try:
            result1 = requests.request("POST", self.signup_page.api_base_url, data=self.payload, headers=self.headers)
            json_body = result1.json()
            authorization_token = json_body['result']['authToken']
            customer_id = json_body['result']['customerId']
            keys = get_redis_keys("email_validation_token*")
            for i in keys:
                i = str(i)
                temp.append(i.split("b'email_validation_token_"))
            for j in temp:
                for k in j[::1]:
                    temp2.append(k)
            while '' in temp2:
                temp2.remove('')
            for x in temp2:
                temp3.append(x[:-1])
            print(temp3)
            url = self.signup_page.wtp_open_account_url + "?validation_token=" + temp3[0] + "&email=" + self.prefix + "%40mailinator.com"
            print(url)
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
            if result1 and result2 and result3 and result4 and result5 and result6 and result7 and result8 is True:
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
        cls.signup_page.close_browser(cls.driver)

