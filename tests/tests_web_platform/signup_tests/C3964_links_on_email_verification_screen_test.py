# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['login_page', ])
class LinksOnVerifyEmailScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.email = cls.open_account_page.email
        cls.password = "1Aa@<>12"
        cls.first_last_name = "QAtestQA"
        cls.test_case = '3964'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'functional', 'positive', ])
    def test_links_on_verify_email_screen(self):
        delay = 1
        result1, result2, result3, result4, result5, result6 = False, False, False, False, False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, self.first_last_name, self.email, self.password)
            # 1 - email verified link, 2 - go back link, 3 - email not sent link
            result3 = self.signup_page.click_on_link_on_email_screen(self.driver, self.home_page.wtp_open_account_url, 1)
            # self.home_page.go_back_and_wait(self.driver, wtp_open_account_url, delay)
            result4 = self.signup_page.click_on_link_on_email_screen(self.driver, self.home_page.wtp_open_account_url, 2)
            self.home_page.go_back_and_wait(self.driver, self.home_page.wtp_open_account_url, delay)
            result5 = self.signup_page.click_on_link_on_email_screen(self.driver, self.home_page.wtp_open_account_url, 3)
            # Opens email box, clicks on "Very email" button and checks that redirected to OpenAccountPage url.
            result6 = self.signup_page.get_email_updates(self.driver, self.signup_page.email, 3, self.home_page.wtp_open_account_url)
        finally:
            if result1 and result2 and result3 and result5 and result6 is True and result4 is False:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
