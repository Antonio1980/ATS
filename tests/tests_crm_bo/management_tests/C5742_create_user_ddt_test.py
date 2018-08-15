# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage


@ddt
@test(groups=['create_user_page', ])
class CreateNewUserDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '5742'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.create_user_page = CreateUserPage()
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.user_management_page = UsersManagementPage()
        cls.login_username = cls.login_page.login_username
        cls.login_password = cls.login_page.login_password
        cls.results_file = cls.login_page.CRM_TESTS_RESULT
        Instruments.write_file_preconditions(5, "@guerrillamailblock.com")
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative'])
    @data(*Instruments.get_csv_data(BaseConfig.CRM_USERS_PRECONDITIONS))
    @unpack
    def test_create_new_user(self, first_last_name, phone, email, username, language, permissions, status, user_type):
        delay = 5
        user_details = {'first_last_name': first_last_name, 'phone': phone, 'username': username,
                        'language': language, 'permissions': permissions, 'status': status, 'user_type': user_type}
        step1, step2, step3, step4, step5 = False, False, False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.login_username, self.login_password)
            step2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            step3 = self.user_management_page.click_on_create_new_user(self.driver)
            step4 = self.create_user_page.fill_user_details(self.driver, email, user_details)
            step5 = self.home_page.logout(self.driver, delay)
        finally:
            if step1 and step2 and step3 and step4 and step5 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
