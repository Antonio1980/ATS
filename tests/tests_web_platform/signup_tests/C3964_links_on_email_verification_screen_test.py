# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.engine import write_file_result, update_test_case, get_redis_keys, parse_redis_token, get_redis_token
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['sign_up_page', ])
class LinksOnVerifyEmailScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3964'
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.email = cls.signup_page.email
        cls.password = cls.signup_page.password
        cls.username = cls.signup_page.username
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'functional', 'positive', ])
    def test_links_on_verify_email_screen(self):
        token = ""
        delay = 1
        result1, result2, result3, result4, result5, result6 = False, False, False, True, False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password)
            customer_id = self.signup_page.execute_js(self.driver, self.signup_page.script_customer_id)
            # # 0 - verify email, 1 - change password, 2 - click on change_password, 3 - click on verify_email
            # url = self.signup_page.get_email_updates(self.driver, self.email, 0)
            # token = url.split('=')[1].split('&')[0]
            # self.signup_page.go_to_url(self.driver, self.signup_page.wtp_open_account_url)
            # 1 - Email verified link, 2 - Go back link, 3 - Resend email
            keys = get_redis_keys("email_validation_token*")
            token_keys = parse_redis_token(keys, "b'")
            token = get_redis_token(token_keys, customer_id)
            result3 = self.signup_page.click_on_link_on_email_screen(self.driver, self.home_page.wtp_open_account_url, 1)
            #result4 = self.signup_page.click_on_link_on_email_screen(self.driver, self.home_page.wtp_open_account_url, 2)
            #self.home_page.go_back_and_wait(self.driver, self.home_page.wtp_open_account_url, delay)
            result5 = self.signup_page.click_on_link_on_email_screen(self.driver, self.home_page.wtp_open_account_url, 3)
            # Opens email box, clicks on "Very email" button and checks that redirected to OpenAccountPage url.
            result6 = self.signup_page.get_email_updates(self.driver, self.signup_page.email, 3, self.home_page.wtp_open_account_url)
        finally:
            if result1 and result2 and result3 and result4 and result5 and result6 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
