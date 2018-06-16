# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from ddt import data, unpack, ddt
from proboscis import test
from src.base.enums import Browsers
from src.test_utils.file_utils import get_csv_data
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from tests.drivers.webdriver_factory import WebDriverFactory
from src.test_utils.testrail_utils import update_test_case
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage


@ddt
@test(groups=['functional', 'smoke', 'sanity'])
class CreateNewUserTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.user_management_page = UsersManagementPage()
        cls.create_user_page = CreateUserPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '1132'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['login_page', 'ddt'])
    @data(*get_csv_data(BaseConfig.CRM_CREATE_USER))
    @unpack
    def test_create_new_user(self, first_name, last_name, email, username):
        delay = 3
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.login_page.login_positive(self.driver, delay)
            result2 = self.home_page.go_to_management_inset_with_users_option(self.driver, delay)
            result3 = self.user_management_page.click_on_create_new_user(self.driver, delay)
            result4 = self.create_user_page.fill_user_details_ddt(self.driver, first_name, last_name, email, username)
        finally:
            if result1 & result2 is True & result3 & result4 is True:
                update_test_case(self.test_run, self.test_case, 1)
            else:
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
