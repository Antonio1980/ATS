# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.locators.create_user_page_locators import CreateUserPageLocators
from tests.tests_crm_bo.locators.users_management_page_locators import UsersManagementPageLocators


@ddt
@test(groups=['create_user_page', ])
class EditNewUserUITest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5845'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators2 = CreateUserPageLocators()
        self.locators = UsersManagementPageLocators()
        self.results_file = BaseConfig.CRM_TESTS_RESULT
        self.username = self.login_page.forgotten_username
        self.login_username = self.login_page.login_username
        self.login_password = self.login_page.login_password

    @test(groups=['sanity', 'gui', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_ui_edit_new_user(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        step1, step2, step3 = False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.login_username, self.login_password)
            step2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            try:
                search_field = Browser.find_element(self.driver, self.locators.SEARCH_FIELD)
                Browser.click_on_element(search_field)
                Browser.send_keys(search_field, self.username)
                Browser.send_enter_key(search_field)
                user = Browser.find_element(self.driver, self.locators.USER)
                Browser.click_on_element(user)
                first_name_field = Browser.find_element_by(self.driver, self.locators2.FIRST_NAME_ID, "id")
                Browser.clear_field(first_name_field)
                Browser.send_keys(first_name_field, "QAtestQA")
                last_name_field = Browser.find_element_by(self.driver, self.locators2.LAST_NAME_ID, "id")
                Browser.clear_field(last_name_field)
                Browser.send_keys(last_name_field, "__QA__TEST__QA__")
                email_field = Browser.find_element_by(self.driver, self.locators2.EMAIL_ID, "id")
                Browser.clear_field(email_field)
                Browser.send_keys(email_field, "qa_test_qa@gmail.com")
                phone_field = Browser.find_element_by(self.driver, self.locators2.PHONE_ID, "id")
                Browser.clear_field(phone_field)
                Browser.send_keys(phone_field, "0528234546")
                username_field = Browser.find_element_by(self.driver, self.locators2.USERNAME_ID, "id")
                Browser.clear_field(username_field)
                Browser.send_keys(username_field, "32874238hgsdha#42!")
                step3 = True
            except Exception as e:
                print(e)
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
