# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.pages.base_page import BasePage
from tests_sources.test_definitions import BaseConfig
from tests.locators.login_page_locators import LogInPageLocators


@test(groups=['end2end', 'functional', 'sanity'])
class ForgotPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        BasePage.setUpClass("chrome")

        
    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password(self):
        email = "roman@spotoption.com"
        wait_element = 2
        wait_click = 3
        try:
            BasePage.go_to_page(BaseConfig.CRM_BASE_URL)
            assert BasePage.driver_wait_element_present(wait_element, LogInPageLocators.CRM_LOGO)
            BasePage.search_and_click(wait_click, LogInPageLocators.FORGOT_PASSWORD_LINK)
            assert BasePage.driver_wait_element_present(wait_element, LogInPageLocators.FORGOT_POPUP)
            BasePage.search_and_click(wait_click, LogInPageLocators.CLOSE_BUTTON)
            assert BasePage.driver_wait_element_present(wait_element, LogInPageLocators.CRM_LOGO)
            BasePage.search_wait_click(wait_click, LogInPageLocators.FORGOT_PASSWORD_LINK)
            assert BasePage.driver_wait_element_present(wait_element, LogInPageLocators.FORGOT_POPUP)
            BasePage.search_and_type(wait_click, email, LogInPageLocators.EMAIL_FIELD)
            BasePage.search_and_click(wait_click, LogInPageLocators.SEND_BUTTON)
            assert BasePage.driver_wait_element_present(wait_element, LogInPageLocators.CRM_LOGO)
        finally:
            raise Exception


    @classmethod
    def tearDownClass(self):
        BasePage.tearDownClass()
