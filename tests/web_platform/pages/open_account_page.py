# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.web_platform.locators.open_account_page_locators import OpenAccountPageLocators
from tests.web_platform.pages.base_page import BasePage


class OpenAccountPage(BasePage):
    @classmethod
    def setup_open_account_page(cls):
        cls.set_up_base_page()
        cls.self_url = "openAccountDx.html"
        cls.open_account_url = cls.base_url + cls.self_url

    @classmethod
    def registration(cls, firstname, lastname, email, password):
        delay = 3
        try:
            assert cls.open_account_url == cls.get_cur_url()
            cls.driver_wait(delay)
            firstname_field = cls.find_element(OpenAccountPageLocators.FIRST_NAME_FIELD)
            cls.click_on_element(firstname_field)
            cls.send_keys(firstname_field, firstname)
            lastname_field = cls.find_element(OpenAccountPageLocators.LAST_NAME_FIELD)
            cls.click_on_element(lastname_field)
            cls.send_keys(lastname_field, lastname)
            email_field = cls.find_element(OpenAccountPageLocators.EMAIL_FIELD)
            cls.click_on_element(email_field)
            cls.send_keys(email_field, email)
            password_field = cls.find_element(OpenAccountPageLocators.PASSWORD_FIELD)
            cls.click_on_element(password_field)
            cls.send_keys(password_field, password)
            captcha = cls.find_element(OpenAccountPageLocators.CAPTCHA)
            cls.click_on_element(captcha)
            newsletters_checkbox = cls.find_element(OpenAccountPageLocators.NEWSLETTERS_CHECKBOX)
            cls.click_on_element(newsletters_checkbox)
            certify_checkbox = cls.find_element(OpenAccountPageLocators.CERTIFY_CHECKBOX)
            cls.click_on_element(certify_checkbox)
            create_account_button = cls.find_element(OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            cls.click_on_element(create_account_button)
            cls.driver_wait(delay)
        finally:
            if cls.check_element_not_visible(OpenAccountPageLocators.PASSWORD_NOT_SECURE):
                return True
            else:
                return False
