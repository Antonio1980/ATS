# !/usr/bin/env python
# -*- coding: utf8 -*-
import time
import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages import reset_password_url
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage


@test(groups=['login_page'])
class ForgotPasswordFullFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3440'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.create_user_page = CreateUserPage()
        cls.phone = '123456789'
        cls.new_email = cls.create_user_page.email
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.sid_token = cls.create_user_page.sid_token
        cls.time_stamp = cls.create_user_page.time_stamp
        cls.users_file = cls.login_page.CRM_TESTS_USERS
        cls.user_management_page = UsersManagementPage()
        cls.login_username = cls.login_page.login_username
        cls.login_password = cls.login_page.login_password
        cls.results_file = cls.login_page.CRM_TESTS_RESULT
        cls.new_username = cls.create_user_page.guerrilla_username
        cls.first_last_name = cls.create_user_page.first_last_name
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_login_with_new_password(self):
        delay, new_password, sid_token = 5, "", ""
        user_details = {'first_last_name': self.first_last_name, 'phone': self.phone, 'username': self.new_username,
                        'language': "eng", 'permissions': "sup", 'status': "act", 'user_type': "Admin"}
        step1, step2, step3, step4, step5, step6, step7, step8, step9 = False, False, False, False, False, False, \
            False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.login_username, self.login_password)
            step2 = self.home_page.go_to_management_inset_with_users_option(self.driver)
            step3 = self.user_management_page.click_on_create_new_user(self.driver)
            step4 = self.create_user_page.fill_user_details(self.driver, self.new_email, user_details)
            step5 = self.home_page.logout(self.driver, delay)
            time.sleep(delay * 3)
            emails_list_response = Instruments.get_guerrilla_emails(self.new_username, self.sid_token)
            sid_token = emails_list_response[1]['sid_token']
            mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.time_stamp, mail_id, sid_token)
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            new_password = parsed_html.table.find_all('td')[1].span.string
            step6 = self.login_page.login(self.driver, self.new_username, new_password)
            step7 = self.login_page.set_new_password(self.driver, new_password, new_password + "Qa!Qa")
            step8 = self.home_page.logout(self.driver, delay)
            step9 = self.login_page.login(self.driver, self.new_username, new_password + "Qa!Qa")
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 is True:
                Instruments.write_file_user(self.forgotten_email + "," + new_password + "Qa!Qa" + "," +
                                            self.forgotten_username + "," + sid_token + "\n", self.users_file)
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
