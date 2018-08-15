# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages import reset_password_url
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@test(groups=['login_page'])
class ForgotPasswordEmailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3438'
        cls.login_page = LogInPage()
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results_file = cls.login_page.CRM_TESTS_RESULT
        cls.forgotten_email = cls.login_page.forgotten_email
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_forgot_password_email(self):
        step1, step2 = False, False
        try:
            step1 = self.login_page.forgot_password(self.driver, self.forgotten_email)
            # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
            # 2 - click on forgot_password, 3 - ?
            content = self.login_page.get_email_updates(self.driver, self.forgotten_email, 0)
            token = content.split('/')[-1]
            new_password_url = reset_password_url + token
            step2 = self.login_page.get_email_updates(self.driver, self.forgotten_email, 2, new_password_url)
        finally:
            if step1 and step2 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)

