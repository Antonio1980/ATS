# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages import user_index_page_url, create_user_page_url
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from src.base.engine import write_file_result, update_test_case, get_csv_data
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage


@ddt
@test(groups=['create_user_page', ])
class CreateNewUserDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '1132'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.create_user_page = CreateUserPage()
        cls.user_management_page = UsersManagementPage()
        cls.username = cls.login_page.username
        cls.password = cls.login_page.password
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', ])
    @data(*get_csv_data(BaseConfig.CRM_CREATE_USER))
    @unpack
    def test_create_new_user(self, first_name, last_name, email, username):
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.login_page.login(self.driver, self.username, self.password)
            result2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            result3 = self.user_management_page.click_on_create_new_user(self.driver)
            try:
                print(user_index_page_url)
                assert self.get_cur_url(self.driver) == create_user_page_url
                first_name_field = self.find_element_by(self.driver, self.locators.FIRST_NAME_ID, "id")
                self.click_on_element(first_name_field)
                self.send_keys(first_name_field, first_name)
                last_name_field = self.find_element_by(self.driver, self.locators.LAST_NAME_ID, "id")
                self.click_on_element(last_name_field)
                self.send_keys(last_name_field, last_name)
                email_field = self.find_element_by(self.driver, self.locators.EMAIL_ID, "id")
                self.click_on_element(email_field)
                self.send_keys(email_field, email)
                phone_field = self.find_element_by(self.driver, self.locators.PHONE_ID, "id")
                self.click_on_element(phone_field)
                self.send_keys(phone_field, self.phone)
                username_field = self.find_element_by(self.driver, self.locators.USERNAME_ID, "id")
                self.click_on_element(username_field)
                self.send_keys(username_field, username)
                language_dropdown = self.find_element(self.driver, self.locators.LANGUAGE_DROPDOWN)
                self.click_on_element(language_dropdown)
                language_field = self.find_element(self.driver, self.locators.LANGUAGE_FIELD)
                self.click_on_element(language_field)
                language_text_field = self.find_element(self.driver, self.locators.LANGUAGE_TEXT_FIELD)
                self.send_keys(language_text_field, "eng")
                self.send_enter_key(language_text_field)
                permission_dropdown = self.find_element(self.driver, self.locators.PERMISSION_GROUP_DROPDOWN)
                self.click_on_element(permission_dropdown)
                permission_field = self.find_element(self.driver, self.locators.PERMISSION_GROUP_FIELD)
                self.click_on_element(permission_field)
                permission_text_field = self.find_element(self.driver, self.locators.PERMISSION_GROUP_TEXT_FIELD)
                self.send_keys(permission_text_field, "sup")
                self.send_enter_key(permission_text_field)
                status_dropdown = self.find_element(self.driver, self.locators.STATUS_DROPDOWN)
                self.click_on_element(status_dropdown)
                status_field = self.find_element(self.driver, self.locators.STATUS_FIELD)
                self.click_on_element(status_field)
                status_text_field = self.find_element(self.driver, self.locators.STATUS_TEXT_FIELD)
                self.send_keys(status_text_field, "a")
                self.send_enter_key(status_text_field)
                user_type_dropdown = self.find_element(self.driver, self.locators.USER_TYPE_DROPDOWN)
                self.click_on_element(user_type_dropdown)
                user_type_field = self.find_element(self.driver, self.locators.USER_TYPE_FIELD)
                self.click_on_element(user_type_field)
                user_type_text_field = self.find_element(self.driver, self.locators.USER_TYPE_TEXT_FIELD)
                self.send_keys(user_type_text_field, "Admin")
                self.send_enter_key(user_type_text_field)
                create_user_button = self.find_element_by(self.driver, self.locators.CREATE_USER_BUTTON_ID, "id")
                self.click_on_element(create_user_button)
                self.driver_wait(self.driver, delay=+ 10)
            except Exception:
                if self.get_cur_url(self.driver) == user_index_page_url:
                    result4 = True
                else:
                    result4 = False
        finally:
            if result1 and result2 and result3 and result4 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
