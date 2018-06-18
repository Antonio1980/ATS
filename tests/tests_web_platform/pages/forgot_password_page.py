# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import get_account_details
from src.test_utils.mailinator_utils import email_generator
from tests.tests_web_platform.pages import BasePage, forgot_password_page_url
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators


class ForgotPasswordPage(BasePage):
    def __init__(self):
        super(ForgotPasswordPage, self).__init__()
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        email_suffix = "@mailinator"
        self.email = details['email']
        self.negative_email = email_generator() + email_suffix

    def fill_email_address_form(self, driver, delay =+ 1):
        try:
            self.driver_wait(driver, delay)
            assert forgot_password_page_url == self.get_cur_url(driver)
            email_field = self.find_element(driver, ForgotPasswordPageLocators.EMAIL_TEXT_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, self.email)
            submit_button = self.find_element(driver, ForgotPasswordPageLocators.SUBMIT_BUTTON)
            self.click_on_element(submit_button)
        finally:
            if self.get_cur_url(driver) ==  forgot_password_page_url:
                return True
            else:
                return False

    def fill_email_address_form_ddt(self, driver, email, delay =+ 1):
        try:
            self.driver_wait(driver, delay)
            assert forgot_password_page_url == self.get_cur_url(driver)
            email_field = self.find_element(driver, ForgotPasswordPageLocators.EMAIL_TEXT_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            submit_button = self.find_element(driver, ForgotPasswordPageLocators.SUBMIT_BUTTON)
            self.click_on_element(submit_button)
        finally:
            if self.get_cur_url(driver) ==  forgot_password_page_url:
                return True
            else:
                return False

    def fill_email_address_form_negative(self, driver, delay =+ 1):
        try:
            self.driver_wait(driver, delay)
            assert forgot_password_page_url == self.get_cur_url(driver)
            email_field = self.find_element(driver, ForgotPasswordPageLocators.EMAIL_TEXT_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, self.negative_email)
            submit_button = self.find_element(driver, ForgotPasswordPageLocators.SUBMIT_BUTTON)
            self.click_on_element(submit_button)
        finally:
            if self.get_cur_url(driver) ==  forgot_password_page_url:
                return True
            else:
                return False
