# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.pages.page_base import BasePage
from tests_extensions.tests_definitions import BaseConfig
from tests_resources.locators.login_page_locators import LogInPageLocators


@test(groups=['end2end','smoke','sanity'])
class ForgotPassword(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        BasePage.setUpClass("chrome")

        
    @classmethod
    def test_logout(self):
        BasePage.go_to_page(BaseConfig.CRM_BASE_URL)
        assert BasePage.driver_wait_element_present(2, LogInPageLocators.CRM_LOGO)
        BasePage.search_and_click(3, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert BasePage.driver_wait_element_present(2, LogInPageLocators.FORGOT_POPUP)
        BasePage.search_and_click(3, LogInPageLocators.CLOSE_BUTTON)
        assert BasePage.driver_wait_element_present(2, LogInPageLocators.CRM_LOGO)
        BasePage.search_wait_click(10, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert BasePage.driver_wait_element_present(2, LogInPageLocators.FORGOT_POPUP)
        BasePage.search_and_type(1, "roman@spotoption.com", LogInPageLocators.EMAIL_FIELD)
        BasePage.search_and_click(3, LogInPageLocators.SEND_BUTTON)
        assert BasePage.driver_wait_element_present(2, LogInPageLocators.CRM_LOGO)


    @classmethod
    def tearDownClass(self):
        BasePage.tearDownClass()
