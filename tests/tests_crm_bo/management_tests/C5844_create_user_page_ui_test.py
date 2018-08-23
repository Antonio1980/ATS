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
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage
from tests.tests_crm_bo.locators.create_user_page_locators import CreateUserPageLocators


@ddt
@test(groups=['create_user_page', ])
class CreateNewUserUITest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5844'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = CreateUserPageLocators()
        self.message = CreateUserPage.password_message
        self.results_file = BaseConfig.CRM_TESTS_RESULT
        self.user_management_page = UsersManagementPage()
        self.login_username = self.login_page.login_username
        self.login_password = self.login_page.login_password

    @test(groups=['sanity', 'gui', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_ui_create_new_user(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.login_username, self.login_password)
            step2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            step3 = self.user_management_page.click_on_create_new_user(self.driver)
            try:
                assert Browser.find_element(self.driver, self.locators.PAGE_TITLE_1)
                assert Browser.find_element(self.driver, self.locators.PAGE_TITLE_2)
                assert Browser.find_element_by(self.driver, self.locators.FIRST_NAME_ID, "id")
                assert Browser.find_element_by(self.driver, self.locators.LAST_NAME_ID, "id")
                assert Browser.find_element_by(self.driver, self.locators.EMAIL_ID, "id")
                assert Browser.find_element_by(self.driver, self.locators.PHONE_ID, "id")
                assert Browser.find_element_by(self.driver, self.locators.USERNAME_ID, "id")
                password_message = Browser.find_element(self.driver, self.locators.PASSWORD_MESSAGE)
                assert self.message ==  password_message.text
                Browser.find_element(self.driver, self.locators.LANGUAGE_DROPDOWN)
                Browser.find_element(self.driver, self.locators.PERMISSION_GROUP_DROPDOWN)
                Browser.find_element(self.driver, self.locators.STATUS_DROPDOWN)
                Browser.choose_option_from_dropdown(self.driver, self.locators.USER_TYPE_DROPDOWN,
                                                    self.locators.USER_TYPE_TEXT_FIELD, "regular", delay - 3)
                Browser.find_element(self.driver, self.locators.DESKS_DROPDOWN)
                create_user_button = Browser.search_element(self.driver, self.locators.CREATE_USER_BUTTON, delay)
                Browser.click_with_wait_and_offset(self.driver, create_user_button, 5, 5, delay - 3)
                Browser.wait_element_presented(self.driver, self.locators.FIRST_NAME_ERROR, delay)
                Browser.wait_element_presented(self.driver, self.locators.LAST_NAME_ERROR, delay)
                Browser.wait_element_presented(self.driver, self.locators.EMAIL_ERROR, delay)
                Browser.wait_element_presented(self.driver, self.locators.PHONE_ERROR, delay)
                Browser.wait_element_presented(self.driver, self.locators.USERNAME_ERROR, delay)
                step4 = True
            except Exception as e:
                print(e)
        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
