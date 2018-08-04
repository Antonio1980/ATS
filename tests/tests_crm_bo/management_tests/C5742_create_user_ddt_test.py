# !/usr/bin/env python
# -*- coding: utf8 -*-

import random
import string
import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage
from src.base.instruments import write_file_result, update_test_case, get_csv_data, write_file_preconditions


@ddt
@test(groups=['create_user_page', ])
class CreateNewUserDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '5742'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.create_user_page = CreateUserPage()
        cls.user_management_page = UsersManagementPage()
        cls.login_username = cls.login_page.login_username
        cls.login_password = cls.login_page.login_password
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        write_file_preconditions(5, "@guerrillamailblock.com")
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', ])
    @data(*get_csv_data(BaseConfig.CRM_USERS_PRECONDITIONS))
    @unpack
    def test_create_new_user(self, first_last_name, phone, email, username, language, permissions, status, user_type):
        delay = 5
        user_details = {'first_last_name': first_last_name, 'phone': phone, 'username': username,
                        'language': language, 'permissions': permissions, 'status': status, 'user_type': user_type}
        result1, result2, result3, result4, result5, result6 = False, False, False, False, False, False
        try:
            result1 = self.login_page.login(self.driver, self.login_username, self.login_password)
            result2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            result3 = self.user_management_page.click_on_create_new_user(self.driver)
            result4 = self.create_user_page.fill_user_details(self.driver, email, user_details)
            result5 = self.home_page.logout(self.driver, delay)
            result6 = self.login_page.login(self.driver, username, self.login_password)
        finally:
            if result1 and result2 and result3 and result4 and result5 and result6 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
