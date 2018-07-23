# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages import reset_password_url
from tests.tests_crm_bo.pages import new_password_url as new_url
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import write_file_result, update_test_case, write_file_user


@test(groups=['change_password_page', ])
class ChangePasswordScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3505'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.email = cls.login_page.email
        cls.username = cls.login_page.username
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_change_password_screen(self):
        delay, new_password = 5, None
        result1, result2, result3, result4 = False, False, False, False
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
            try:
                assert self.login_page.get_cur_url(self.driver) == new_url
                self.login_page.wait_element_presented(self.driver, self.login_page.locators.CURRENT_PASSWORD, delay)
                self.login_page.wait_element_presented(self.driver, self.login_page.locators.NEW_PASSWORD, delay)
                self.login_page.wait_element_presented(self.driver, self.login_page.locators.CONFIRM_PASSWORD, delay)
                if self.login_page.wait_element_clickable(self.driver,self.login_page.locators.CONFIRM_BUTTON,delay):
                    result4 = True
            except TimeoutError:
                result4 = False
        finally:
            if result1 and result2 and result3 and result4 is True:
                write_file_user(self.email + "," + new_password + "Qa" + "," + self.username + "\n", self.users)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
