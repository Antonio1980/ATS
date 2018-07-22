# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import write_file_result, update_test_case
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


@test(groups=['login_page', ])
class LogInUITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3436'
        cls.login_page = LogInPage()
        cls.locators = LogInPageLocators()
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'gui', 'positive', ])
    def test_login_page(self):
        delay = 3
        result1, result2 = False, False
        try:
            self.login_page.go_to_url(self.driver, self.login_page.crm_base_url)
            assert self.login_page.wait_element_visible(self.driver, self.login_page.base_locators.CRM_LOGO, delay)
            assert self.login_page.find_element_by(self.driver, self.locators.USERNAME_FIELD_ID, "id")
            assert self.login_page.find_element_by(self.driver, self.locators.PASSWORD_FIELD_ID, "id")
            assert self.login_page.find_element_by(self.driver, self.locators.LOGIN_BUTTON_ID, "id")
            username_field_ps = int(self.driver.execute_script("return window.$(\'input[id=\"username\"]\').position()")
                                     .get('left'))
            password_field_ps = int(self.driver.execute_script("return window.$(\'input[id=\"password\"]\').position()")
                                     .get('left'))
            login_button_pos = int(self.driver.execute_script("return window.$(\'button[id=\"loginBtn\"]\').position()")
                                   .get('left'))
            if username_field_ps == 20 and password_field_ps == 20:
                result1 = True
                if login_button_pos == 215:
                    result2 = True
        finally:
            if result1 and result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
