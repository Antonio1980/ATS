# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.crm.pages.base_page import BasePage
from tests.crm.locators.home_page_locators import HomePageLocators
from tests.crm.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    @classmethod
    def login(cls, delay, username, password):
        cls.go_to_url(BaseConfig.CRM_BASE_URL)
        assert cls.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)
        assert cls.wait_element_presented(delay + 1, LogInPageLocators.FORGOT_PASSWORD_LINK)
        cls.insert_text_into_element(delay + 2, username, LogInPageLocators.USERNAME_FIELD)
        cls.insert_text_into_element(delay + 2, password, LogInPageLocators.PASSWORD_FIELD)
        cls.click_on_element(delay + 2, LogInPageLocators.LOGIN_BUTTON)
        cls.driver_wait(delay)
        assert cls.wait_element_presented(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        cls.driver_wait(delay)

    @classmethod
    def forgot_password(cls, delay, email):
        cls.go_to_url(BaseConfig.CRM_BASE_URL)
        assert cls.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)
        cls.click_on_element(delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert cls.wait_element_presented(delay + 1, LogInPageLocators.FORGOT_POPUP)
        assert cls.wait_element_presented(delay, LogInPageLocators.MESSAGE_POPUP)
        assert cls.wait_element_presented(delay, LogInPageLocators.NOTE_POPUP)
        cls.insert_text_into_element(delay + 3, email, LogInPageLocators.EMAIL_FIELD)
        cls.click_on_element(delay + 2, LogInPageLocators.SEND_BUTTON)
        assert cls.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)




