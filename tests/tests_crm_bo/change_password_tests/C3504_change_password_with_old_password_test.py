# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages import reset_password_url
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@test(groups=['login_page', ])
class ChangePasswordForgottenUserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3504'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.forgotten_email = cls.login_page.forgotten_email
        cls.forgotten_username = cls.login_page.forgotten_username
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.users_file = cls.login_page.CRM_TESTS_USERS
        cls.results_file = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'negative', ])
    def test_login_with_new_password(self):
        delay, new_password = 5, None
        step1, step2, step3, step5, step6, step7, step4 = False, False, False, False, False, False, True
        try:
            step1 = self.login_page.forgot_password(self.driver, self.forgotten_email)
            # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
            # 2 - click on forgot_password, 3 - ?
            content = self.login_page.get_email_updates(self.driver, self.forgotten_email, 0)
            token = content.split('/')[-1]
            new_password_url = reset_password_url + token
            step2 = self.login_page.get_email_updates(self.driver, self.forgotten_email, 2, new_password_url)
            new_password = self.login_page.get_email_updates(self.driver, self.forgotten_email, 1)
            step3 = self.login_page.login(self.driver, self.forgotten_username, new_password)
            step4 = self.login_page.set_new_password(self.driver, new_password, new_password)
            step5 = self.login_page.set_new_password(self.driver, new_password, new_password + "Qa")
            step6 = self.home_page.logout(self.driver, delay)
            step7 = self.login_page.login(self.driver, self.forgotten_username, new_password + "Qa")
        finally:
            if step1 and step2 and step3 and step5 and step6 and step7 is True and step4 is False:
                Instruments.write_file_user(self.forgotten_email + "," + new_password + "Qa" + "," +
                                            self.forgotten_username + "\n", self.users_file)
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)