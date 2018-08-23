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


@test(groups=['login_page'])
class UpdateDefaultPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3412'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.forgotten_email = cls.login_page.forgotten_email
        cls.forgotten_username = cls.login_page.forgotten_username
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.users_file = cls.login_page.CRM_TESTS_USERS
        cls.results_file = cls.login_page.CRM_TESTS_RESULT

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_update_default_password_chrome(self):
        driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        delay, new_password = 5, None
        step1, step2, step3, step4, step5 = False, False, False, False, False
        try:
            step1 = self.login_page.forgot_password(driver, self.forgotten_email)
            # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
            # 2 - click on forgot_password, 3 - ?
            content = self.login_page.get_email_updates(driver, self.forgotten_email, 0)
            token = content.split('/')[-1]
            new_password_url = reset_password_url + token
            step2 = self.login_page.get_email_updates(driver, self.forgotten_email, 2, new_password_url)
            new_password = self.login_page.get_email_updates(driver, self.forgotten_email, 1)
            step3 = self.login_page.login(driver, self.forgotten_username, new_password)
            step4 = self.login_page.set_new_password(driver, new_password, new_password + "Qa")
            step5 = self.home_page.logout(driver, delay)
        finally:
            if step1 and step2 and step3 and step4 and step5 is True:
                Instruments.write_file_user(self.forgotten_email + "," + new_password + "Qa" + "," +
                                            self.forgotten_username + "\n", self.users_file)
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
                driver.quit()
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)
                driver.quit()

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_update_default_password_firefox(self):
        driver = WebDriverFactory.get_browser(Browsers.FIREFOX.value)
        delay, new_password = 5, None
        step1, step2, step3, step4, step5 = False, False, False, False, False
        try:
            step1 = self.login_page.forgot_password(driver, self.forgotten_email)
            # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
            # 2 - click on forgot_password, 3 - ?
            content = self.login_page.get_email_updates(driver, self.forgotten_email, 0)
            token = content.split('/')[-1]
            new_password_url = reset_password_url + token
            step2 = self.login_page.get_email_updates(driver, self.forgotten_email, 2, new_password_url)
            new_password = self.login_page.get_email_updates(driver, self.forgotten_email, 1)
            step3 = self.login_page.login(driver, self.forgotten_username, new_password)
            step4 = self.login_page.set_new_password(driver, new_password, new_password + "Qa")
            step5 = self.home_page.logout(driver, delay)
        finally:
            if step1 and step2 and step3 and step4 and step5 is True:
                Instruments.write_file_user(self.forgotten_email + "," + new_password + "Qa" + "," +
                                            self.forgotten_username + "\n", self.users_file)
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
                driver.quit()
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)
                driver.quit()