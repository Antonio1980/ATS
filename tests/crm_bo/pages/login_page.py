# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.crm_bo.pages.base_page import BasePage
from src.test_utils.file_utils import get_crm_credentials_positive
from tests.crm_bo.locators.home_page_locators import HomePageLocators
from tests.crm_bo.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    @classmethod
    def setup_login_page(cls):
        cls.setup_base_page()
        # data_file, row, column1, column2
        credentials = get_crm_credentials_positive(BaseConfig.CRM_LOGIN_DATA, 0, 0, 1)
        cls.email = BaseConfig.CRM_CUSTOMER_EMAIL
        cls.email_text = "An email has been sent to {0} which is the email address for your account. " \
                     "It includes information on changing and confirming your new password. " \
                     "Please reset your password within the next 24 hours.".format(cls.email)

        cls.login_page_url = cls.base_url + "login"
        cls.username = credentials['username']
        cls.password = credentials['password']

    @classmethod
    def go_to_login_page(cls, url):
        cls.go_to_url(url)

    @classmethod
    def login_positive(cls, delay):
        try:
            cls.go_to_login_page(cls.base_url)
            assert cls.login_page_url == cls.get_cur_url()
            username_field = cls.find_element_by(LogInPageLocators.USERNAME_FIELD_ID, "id")
            cls.send_keys(username_field, cls.username)
            password_field = cls.find_element_by(LogInPageLocators.PASSWORD_FIELD_ID, "id")
            cls.send_keys(password_field, cls.password)
            login_button = cls.find_element_by(LogInPageLocators.LOGIN_BUTTON_ID, "id")
            cls.click_on_element(login_button)
            cls.driver_wait(delay)
        finally:
            if cls.wait_element_visible(delay + 1, HomePageLocators.HOME_PAGE_LOGO):
                return True
            else:
                return False

    @classmethod
    def login(cls, delay, username, password):
        try:
            cls.go_to_login_page(cls.base_url)
            assert cls.login_page_url == cls.get_cur_url()
            username_field = cls.find_element_by(LogInPageLocators.USERNAME_FIELD_ID, "id")
            cls.send_keys(username_field, username)
            password_field = cls.find_element_by(LogInPageLocators.PASSWORD_FIELD_ID, "id")
            cls.send_keys(password_field, password)
            login_button = cls.find_element_by(LogInPageLocators.LOGIN_BUTTON_ID, "id")
            cls.click_on_element(login_button)
            cls.driver_wait(delay)
        finally:
            if cls.wait_element_visible(delay + 1, HomePageLocators.HOME_PAGE_LOGO):
                return True
            else:
                return False

    @classmethod
    def forgot_password(cls, delay, email):
        try:
            cls.go_to_login_page(cls.base_url)
            assert cls.login_page_url == cls.get_cur_url()
            cls.click_on_element_by_locator(delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
            email_field = cls.find_element_by(LogInPageLocators.POPUP_EMAIL_FIELD_ID, "id")
            cls.send_keys(email_field, email)
            send_button = cls.find_element_by(LogInPageLocators.POPUP_SEND_BUTTON_ID, "id")
            cls.click_on_element(send_button)
            cls.driver_wait(delay)
            if cls.wait_element_presented(delay + 3, LogInPageLocators.POPUP_ERROR_MESSAGE_ID) is None:
                cls.click_on_element_by_locator(delay + 1, LogInPageLocators.EMAIL_POPUP_CLOSE_BUTTON)
        finally:
            cls.driver_wait(delay)
            if cls.wait_element_presented(delay + 3, LogInPageLocators.POPUP_CHECK) is not None:
                return True
            else:
                return False
