# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages import reset_password_url
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import write_file_result, update_test_case, write_file_user


@test(groups=['login_page', ])
class ChangePasswordForgottenUserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3504'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.email = cls.login_page.email
        cls.username = cls.login_page.username
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'negative', ])
    def test_login_with_new_password(self):
        delay, new_password = 5, None
        result1, result2, result3, result5, result6, result7, result4 = False, False, False, False, False, False, True
        try:
            result1 = self.login_page.forgot_password(self.driver, self.email, delay)
            # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
            # 2 - click on forgot_password, 3 - ?
            content = self.login_page.get_email_updates(self.driver, self.email, 0)
            token = content.split('/')[-1]
            new_password_url = reset_password_url + token
            result2 = self.login_page.get_email_updates(self.driver, self.email, 2, new_password_url)
            new_password = self.login_page.get_email_updates(self.driver, self.email, 1)
            result3 = self.login_page.login(self.driver, self.username, new_password)
            result4 = self.login_page.set_new_password(self.driver, new_password, new_password)
            result5 = self.login_page.set_new_password(self.driver, new_password, new_password + "Qa")
            result6 = self.home_page.logout(self.driver, delay)
            result7 = self.login_page.login(self.driver, self.username, new_password + "Qa")
        finally:
            if result1 and result2 and result3 and result5 and result6 and result7 is True and result4 is False:
                write_file_user(self.email + "," + new_password + "Qa" + "," + self.username + "\n", self.users)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)