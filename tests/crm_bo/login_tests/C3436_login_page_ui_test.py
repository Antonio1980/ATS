# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from src.test_utils.js_utils import get_element_position
from tests.crm_bo.locators.login_page_locators import LogInPageLocators


@test(groups=['functional', 'smoke', 'sanity'])
class LogInUiTest(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_login_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '3436'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_page(cls):
        delay = 1
        result1, result2 = False, False
        try:
            cls.go_to_url(cls.base_url)
            assert cls.wait_element_visible(delay, LogInPageLocators.CRM_LOGO)
            assert cls.find_element_by(LogInPageLocators.USERNAME_FIELD_ID, "id")
            assert cls.find_element_by(LogInPageLocators.PASSWORD_FIELD_ID, "id")
            assert cls.find_element_by(LogInPageLocators.LOGIN_BUTTON_ID, "id")
            username_field_pos = int(cls.driver.execute_script("return window.$(\'input[id=\"username\"]\').position()").get('left'))
            password_field_pos = int(cls.driver.execute_script("return window.$(\'input[id=\"password\"]\').position()").get('left'))
            login_button_pos = int(cls.driver.execute_script("return window.$(\'button[id=\"loginBtn\"]\').position()").get('left'))
            if username_field_pos == 20 & password_field_pos == 20:
                result1 = True
                if login_button_pos == 215:
                    result2 = True
        finally:
            if result1 & result2 is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()











