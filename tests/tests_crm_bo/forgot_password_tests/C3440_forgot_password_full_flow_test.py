# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages import reset_password_url
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@ddt
@test(groups=['login_page'])
class ForgotPasswordFullFlowTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3440'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.users_file = BaseConfig.CRM_TESTS_USERS
        self.results_file = BaseConfig.CRM_TESTS_RESULT
        self.forgotten_email = self.login_page.forgotten_email
        self.forgotten_username = self.login_page.forgotten_username

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_forgot_password_full_flow(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay, new_password, token = 5, "", ""
        step1, step2, step3, step4, step5, step6 = False, False, False, False, False, False
        try:
            step1 = self.login_page.forgot_password(self.driver, self.forgotten_email, )
            # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
            # 2 - click on forgot_password, 3 - ?
            content = self.login_page.get_email_updates(self.driver, self.forgotten_email, 0)
            token = content.split('/')[-1]
            new_password_url = reset_password_url + token
            step2 = self.login_page.get_email_updates(self.driver, self.forgotten_email, 2, new_password_url)
            new_password = self.login_page.get_email_updates(self.driver, self.forgotten_email, 1)
            step3 = self.login_page.login(self.driver, self.forgotten_username, new_password)
            step4 = self.login_page.set_new_password(self.driver, new_password, new_password + "Qa")
            step5 = self.home_page.logout(self.driver, delay)
            step6 = self.login_page.login(self.driver, self.forgotten_username, new_password + "Qa")
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 is True:
                Instruments.write_file_user(self.forgotten_email + "," + new_password + "Qa" + "," +
                                            self.forgotten_username + "," + token + "\n", self.users_file)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
