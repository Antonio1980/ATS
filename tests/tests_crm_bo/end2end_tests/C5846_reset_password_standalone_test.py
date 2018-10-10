# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.locators import create_user_page_locators, users_management_page_locators
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage


@ddt
@test(groups=['create_user_page', ])
class ResetPasswordTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5846'
        self.phone = '123456789'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.create_user_page = CreateUserPage()
        self.locators2 = create_user_page_locators
        self.locators = users_management_page_locators
        self.results_file = BaseConfig.CRM_TESTS_RESULT
        self.user_management_page = UsersManagementPage()
        self.login_username = self.login_page.login_username
        self.login_password = self.login_page.login_password
        self.new_email = self.create_user_page.email
        self.sid_token = self.create_user_page.sid_token
        self.time_stamp = self.create_user_page.time_stamp
        self.new_username = self.create_user_page.guerrilla_username
        self.first_last_name = self.create_user_page.first_last_name

    @test(groups=['e2e', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_reset_password(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        user_details = {'first_last_name': self.first_last_name, 'phone': self.phone, 'username': self.new_username,
                        'language': "eng", 'permissions': "sup", 'status': "act", 'user_type': "Admin"}
        step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11, step12, step13 = False, False, \
            False, False, False, False, False, False, False, False, False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.login_username, self.login_password)
            step2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            step3 = self.user_management_page.click_on_create_new_user(self.driver)
            step4 = self.create_user_page.fill_user_details(self.driver, self.new_email, user_details)
            step5 = self.home_page.logout(self.driver, delay)
            time.sleep(delay * 4)
            emails_list_response = Instruments.get_guerrilla_emails(self.new_username, self.sid_token)
            sid_token = emails_list_response[1]['sid_token']
            mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.time_stamp, mail_id, sid_token)
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            new_password = parsed_html.table.find_all('td')[1].span.string
            step6 = self.login_page.login(self.driver, self.new_username, new_password)
            step7 = self.login_page.set_new_password(self.driver, new_password, new_password + "Qa1!Qa")
            step8 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            search_field = Browser.find_element(self.driver, self.locators.SEARCH_FIELD)
            Browser.click_on_element(search_field)
            Browser.send_keys(search_field, self.new_username)
            Browser.send_enter_key(search_field)
            user = Browser.find_element(self.driver, self.locators.USER)
            Browser.click_on_element(user)
            reset_button = Browser.find_element_by(self.driver, self.locators2.RESET_PASSWORD_BUTTON_ID, "id")
            Browser.click_on_element(reset_button)
            time.sleep(delay * 3)
            emails_list_response = Instruments.get_guerrilla_emails(self.new_username, sid_token)
            sid_token = emails_list_response[1]['sid_token']
            mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.time_stamp, mail_id, sid_token)
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            new_password2 = parsed_html.table.find_all('td')[1].span.string
            step9 = self.home_page.logout(self.driver, delay)
            step10 = self.login_page.login(self.driver, self.new_username, new_password2)
            step11 = self.login_page.set_new_password(self.driver, new_password2, new_password2 + "Qa!Qa1")
            step12 = self.home_page.logout(self.driver, delay)
            step13 = self.login_page.login(self.driver, self.new_username, new_password2 + "Qa!Qa1")
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 and step10 and \
                    step11 and step12 and step13 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)

    def tearDown(self):
        Browser.close_browser(self.driver)
