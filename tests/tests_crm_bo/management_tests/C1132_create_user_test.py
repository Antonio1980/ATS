# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage
from src.base.engine import write_file_result, update_test_case, write_file_user


@test(groups=['create_user_page', ])
class CreateNewUserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '1132'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.create_user_page = CreateUserPage()
        cls.user_management_page = UsersManagementPage()
        cls.username = cls.login_page.username
        cls.password = cls.login_page.password
        cls.password_new = cls.password + "Az"
        cls.email_new = cls.create_user_page.email
        cls.test_run = cls.create_user_page.TESTRAIL_RUN
        cls.username_new = cls.create_user_page.email_prefix
        cls.first_last_name = cls.create_user_page.first_last_name
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_create_new_user(self):
        details = {'first_last_name': self.first_last_name, 'phone': '0547324546', 'username': self.username_new}
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.login_page.login(self.driver, self.username, self.password)
            result2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            result3 = self.user_management_page.click_on_create_new_user(self.driver)
            result4 = self.create_user_page.fill_user_details(self.driver, self.email_new, details)
        finally:
            if result1 and result2 and result3 and result4 is True:
                # write_file_user(self.email_new + "," + self.password_new + "," + self.username_new + " \n", BaseConfig.CRM_TESTS_USERS)
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
