# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from src.test_definitions import BaseConfig
from tests.crm.locators.home_page_locators import HomePageLocators
from tests.crm.locators.login_page_locators import LogInPageLocators


class LogInPage(Browser):
    @classmethod
    def login(self, delay, username, password):
        self.go_to_url(BaseConfig.CRM_BASE_URL)
        assert self.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)
        assert self.wait_element_presented(delay + 1, LogInPageLocators.FORGOT_PASSWORD_LINK)
        self.insert_text_into_element(delay + 2, username, LogInPageLocators.USERNAME_FIELD)
        self.insert_text_into_element(delay + 2, password, LogInPageLocators.PASSWORD_FIELD)
        self.click_on_element(delay + 2, LogInPageLocators.LOGIN_BUTTON)
        self.driver_wait(delay)
        assert self.wait_element_presented(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        self.driver_wait(delay)


    @classmethod
    def forgot_password(self, delay, email):
        self.go_to_url(BaseConfig.CRM_BASE_URL)
        assert self.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)
        self.click_on_element(delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert self.wait_element_presented(delay + 1, LogInPageLocators.FORGOT_POPUP)
        assert self.wait_element_presented(delay, LogInPageLocators.MESSAGE_POPUP)
        assert self.wait_element_presented(delay, LogInPageLocators.NOTE_POPUP)
        self.insert_text_into_element(delay + 3, email, LogInPageLocators.EMAIL_FIELD)
        self.click_on_element(delay + 2, LogInPageLocators.SEND_BUTTON)
        assert self.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)




