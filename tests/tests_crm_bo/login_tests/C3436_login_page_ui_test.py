# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages import login_page_url
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.locators import login_page_locators


@ddt
@test(groups=['login_page', ])
class LogInUITest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3436'
        self.login_page = LogInPage()
        self.locators = login_page_locators
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.CRM_TESTS_RESULT

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_ui_login_page(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2 = False, False
        try:
            Browser.go_to_url(self.driver, self.login_page.crm_base_url)
            assert Browser.wait_url_contains(self.driver, login_page_url, delay)
            assert Browser.wait_element_visible(self.driver, self.login_page.base_locators.CRM_LOGO, delay)
            assert Browser.find_element_by(self.driver, self.locators.USERNAME_FIELD_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.PASSWORD_FIELD_ID, "id")
            assert Browser.find_element_by(self.driver, self.locators.LOGIN_BUTTON_ID, "id")
            username_field_ps = int(self.driver.execute_script("return window.$(\'input[id=\"username\"]\').position()")
                                    .get('left'))
            password_field_ps = int(self.driver.execute_script("return window.$(\'input[id=\"password\"]\').position()")
                                    .get('left'))
            login_button_pos = int(self.driver.execute_script("return window.$(\'button[id=\"loginBtn\"]\').position()")
                                   .get('left'))
            if username_field_ps == 20 and password_field_ps == 20:
                step1 = True
                if login_button_pos == 215:
                    step2 = True
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
