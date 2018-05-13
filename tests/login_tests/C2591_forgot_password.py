# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.pages.browser import Browser
from tests.pages.login_page import LogInPage
from tests_sources.test_definitions import BaseConfig
from tests.locators.login_page_locators import LogInPageLocators


@test(groups=['end2end', 'functional', 'sanity'])
class ForgotPasswordTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Browser.setUpClass("chrome")

        
    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password(self):
        email = "roman@spotoption.com"
        delay = 1
        try:
            Browser.go_to_page(BaseConfig.CRM_BASE_URL)
            assert Browser.driver_wait_element_present(delay, LogInPageLocators.CRM_LOGO)
            Browser.search_and_click(delay, LogInPageLocators.FORGOT_PASSWORD_LINK)
            assert Browser.driver_wait_element_present(delay, LogInPageLocators.FORGOT_POPUP)
            Browser.search_and_click(delay, LogInPageLocators.CLOSE_BUTTON)
            LogInPage.forgot_password(delay, email)
        finally:
            raise Exception


    @classmethod
    def tearDownClass(self):
        Browser.tearDownClass()
