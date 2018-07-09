# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from tests.tests_crm_bo.pages.base_page import BasePage
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


@test(groups=['login_page', ])
class LogInUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_page = BasePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3436'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'gui', 'positive', ])
    def test_login_page(self):
        delay = 3
        result1, result2 = False, False
        try:
            self.base_page.go_to_url(self.driver, self.base_page.crm_base_url)
            assert self.base_page.wait_element_visible(self.driver, LogInPageLocators.CRM_LOGO, delay)
            assert self.base_page.find_element_by(self.driver, LogInPageLocators.USERNAME_FIELD_ID, "id")
            assert self.base_page.find_element_by(self.driver, LogInPageLocators.PASSWORD_FIELD_ID, "id")
            assert self.base_page.find_element_by(self.driver, LogInPageLocators.LOGIN_BUTTON_ID, "id")
            username_field_pos = int(self.driver.execute_script("return window.$(\'input[id=\"username\"]\').position()")
                                     .get('left'))
            password_field_pos = int(self.driver.execute_script("return window.$(\'input[id=\"password\"]\').position()")
                                     .get('left'))
            login_button_pos = int(self.driver.execute_script("return window.$(\'button[id=\"loginBtn\"]\').position()")
                                   .get('left'))
            if username_field_pos == 20 & password_field_pos == 20:
                result1 = True
                if login_button_pos == 215:
                    result2 = True
        finally:
            if result1 and result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.base_page.close_browser(cls.driver)
