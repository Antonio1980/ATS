# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
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
        self.zip = "45263"
        self.city = "Ashdod"
        self.test_case = '3750'
        self.birthday = "13/08/1980"
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.signin_page = SignInPage()
        self.phone = self.signup_page.phone
        self.password = self.signup_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.email = self.signup_page.guerrilla_email
        self.username = self.signup_page.username
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS

    @test(groups=['regression', 'positive', ], depends_on_groups=["sanity", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_sign_up_full_flow(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay, token, customer_id = 5, "", ""
        step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11, step12 = \
            False, False, False, False, False, False, False, False, False, False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, )
            customer_id = self.signup_page.execute_js(self.driver, self.signup_page.script_customer_id)
            # 0 - verify email, 1 - change password, 2 - click on change_password, 3 - click on verify_email
            url = self.signup_page.get_email_updates(self.driver, self.email, 0)
            token = url.split('=')[1].split('&')[0]
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
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 and step10 and \
                    step11 and step12 is True:
                Instruments.write_file_user(self.email + "," + self.password + "," + customer_id + "," + token + "\n",
                                self.customers_file)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.home_page.close_browser(self.driver)
