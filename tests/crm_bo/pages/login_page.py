# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.crm_bo.pages.base_page import BasePage
from tests.crm_bo.locators.home_page_locators import HomePageLocators
from tests.crm_bo.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    @classmethod
    def login(cls, delay, username, password):
        try:
            cls.go_to_url(BaseConfig.CRM_BASE_URL)
            assert cls.wait_element_visible(delay + 1, LogInPageLocators.CRM_LOGO)
            assert cls.wait_element_visible(delay + 1, LogInPageLocators.FORGOT_PASSWORD_LINK)
            username_field = cls.find_element_by(LogInPageLocators.USERNAME_FIELD, "id")
            cls.send_keys(username_field, username)
            password_field = cls.find_element_by(LogInPageLocators.PASSWORD_FIELD, "id")
            cls.send_keys(password_field, password)
            login_button = cls.find_element_by(LogInPageLocators.LOGIN_BUTTON, "id")
            cls.click_on_element(login_button)
            cls.driver_wait(delay)
            assert cls.wait_element_visible(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
            return True
        except: Exception

    @classmethod
    def forgot_password(cls, delay, email):
        cls.go_to_url(BaseConfig.CRM_BASE_URL)
        assert cls.wait_element_visible(delay + 1, LogInPageLocators.CRM_LOGO)
        cls.click_on_element_by_locator(delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert cls.wait_element_visible(delay + 1, LogInPageLocators.FORGOT_POPUP)
        assert cls.wait_element_visible(delay + 1, LogInPageLocators.MESSAGE_POPUP)
        assert cls.wait_element_visible(delay + 1, LogInPageLocators.NOTE_POPUP)
        email_field = cls.find_element_by(LogInPageLocators.EMAIL_FIELD, "id")
        cls.send_keys(email_field, email)
        send_button = cls.find_element_by(LogInPageLocators.SEND_BUTTON, "id")
        cls.click_on_element(send_button)
        assert cls.wait_element_visible(delay + 1, LogInPageLocators.POP_UP_CHECK)




