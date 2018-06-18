# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.test_definitions import BaseConfig
from tests.tests_web_platform.pages.base_page import BasePage
from src.test_utils.file_utils import get_account_details
from tests.tests_web_platform.pages import wtp_home_page_url, wtp_login_page_url, forgot_password_page_url
from tests.tests_web_platform.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    def __init__(self):
        super(LogInPage, self).__init__()
        # data_file, row, column1, column2, column3, column4
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        self.email = details['email']
        self.password = details['password']

    def login_positive(self, driver, delay =+ 1):
        try:
            self.driver_wait(driver, delay + 3)
            assert wtp_login_page_url == self.get_cur_url(driver)
            username_field = self.find_element(driver, LogInPageLocators.USERNAME_FIELD)
            self.click_on_element(username_field)
            self.send_keys(username_field, self.email)
            password_true_field = self.find_element(driver, LogInPageLocators.PASSWORD_TRUE_FIELD)
            password_field = self.find_element(driver, LogInPageLocators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_true_field, self.password)
            captcha = self.search_element(driver, delay +5, LogInPageLocators.CAPTCHA)
            self.click_on_captcha(driver, captcha)
            signin_button = self.find_element(driver, LogInPageLocators.SIGNIN_BUTTON)
            self.click_on_element(signin_button)
            self.driver_wait(driver, delay + 2)
        finally:
            if self.get_cur_url(driver) == wtp_home_page_url:
                return True
            else:
                return False

    def click_on_forgot_password(self, driver, delay =+ 1):
        try:
            self.driver_wait(driver, delay)
            assert wtp_login_page_url == self.get_cur_url(driver)
            forgot_link = self.find_element(driver, LogInPageLocators.FORGOT_PASSWORD_LINK)
            self.click_on_element(forgot_link)
            self.driver_wait(driver, delay)
        finally:
            if self.get_cur_url(driver) == forgot_password_page_url:
                return True
            else:
                return False
