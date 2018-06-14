# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.base_page import BasePage
from src.test_utils.file_utils import get_crm_credentials_positive
from tests.tests_crm_bo.locators.home_page_locators import HomePageLocators
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    self_url = "/dx/login"
    login_page_url = BasePage.crm_base_url + self_url
    # data_file, row, column1, column2
    credentials = get_crm_credentials_positive(BaseConfig.CRM_LOGIN_DATA, 0, 0, 1)
    email = BaseConfig.CRM_CUSTOMER_EMAIL
    email_text = "An email has been sent to {0} which is the email address for your account. " \
                      "It includes information on changing and confirming your new password. " \
                      "Please reset your password within the next 24 hours.".format(email)
    username = credentials['username']
    password = credentials['password']

    def __init__(self):
        super(LogInPage, self).__init__()

    def go_to_login_page(self, driver, url):
        self.go_to_url(driver, url)

    def login_positive(self, driver, delay):
        try:
            self.go_to_login_page(driver, self.crm_base_url)
            assert self.login_page_url == self.get_cur_url(driver)
            username_field = self.find_element_by(driver, LogInPageLocators.USERNAME_FIELD_ID, "id")
            self.send_keys(username_field, self.username)
            password_field = self.find_element_by(driver, LogInPageLocators.PASSWORD_FIELD_ID, "id")
            self.send_keys(password_field, self.password)
            login_button = self.find_element_by(driver, LogInPageLocators.LOGIN_BUTTON_ID, "id")
            self.click_on_element(login_button)
            self.driver_wait(driver, delay)
        finally:
            if self.find_element_by(driver, HomePageLocators.HOME_PAGE_LOGO_ID, "id"):
                return True
            else:
                return False

    def login(self, driver, delay, username, password):
        try:
            self.go_to_login_page(driver, self.crm_base_url)
            assert self.login_page_url == self.get_cur_url(driver)
            username_field = self.find_element_by(driver, LogInPageLocators.USERNAME_FIELD_ID, "id")
            self.send_keys(username_field, username)
            password_field = self.find_element_by(driver, LogInPageLocators.PASSWORD_FIELD_ID, "id")
            self.send_keys(password_field, password)
            login_button = self.find_element_by(driver, LogInPageLocators.LOGIN_BUTTON_ID, "id")
            self.click_on_element(login_button)
            self.driver_wait(driver, delay)
        finally:
            if self.find_element_by(driver, HomePageLocators.HOME_PAGE_LOGO_ID, "id"):
                return True
            else:
                return False

    def forgot_password(self, driver, delay, email):
        try:
            self.go_to_login_page(driver, self.crm_base_url)
            assert self.login_page_url == self.get_cur_url(driver)
            self.click_on_element_by_locator(driver, delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
            email_field = self.find_element_by(driver, LogInPageLocators.POPUP_EMAIL_FIELD_ID, "id")
            self.send_keys(email_field, email)
            send_button = self.find_element_by(driver, LogInPageLocators.POPUP_SEND_BUTTON_ID, "id")
            self.click_on_element(send_button)
            self.driver_wait(driver, delay)
            if self.wait_element_presented(driver, delay + 3, LogInPageLocators.POPUP_ERROR_MESSAGE_ID) is None:
                self.click_on_element_by_locator(driver, delay + 1, LogInPageLocators.EMAIL_POPUP_CLOSE_BUTTON)
        finally:
            self.driver_wait(driver, delay)
            if self.wait_element_presented(driver, delay + 3, LogInPageLocators.POPUP_CHECK) is not None:
                return True
            else:
                return False
