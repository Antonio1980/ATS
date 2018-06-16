# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.test_definitions import BaseConfig
from tests.tests_web_platform.pages.base_page import BasePage
from src.test_utils.file_utils import get_account_details
from tests.tests_web_platform.pages import wtp_home_page_url, wtp_login_page_url
from tests.tests_web_platform.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    def __init__(self):
        super(LogInPage, self).__init__()
        # data_file, row, column1, column2, column3, column4
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        self.email = details['email']
        self.password = details['password']

    def login_positive(self, driver, delay):
        try:
            self.driver_wait(driver, delay + 3)
            assert wtp_login_page_url == self.get_cur_url(driver)
            username_field = self.find_element(driver, LogInPageLocators.USERNAME_FIELD)
            self.send_keys(username_field, self.email)
            password_field = self.find_element(driver, LogInPageLocators.PASSWORD_FIELD)
            self.send_keys(password_field, self.password)
            captcha = self.find_element(driver, LogInPageLocators.CAPTCHA)
            self.click_on_captcha(driver, captcha)
            signin_button = self.find_element(driver, LogInPageLocators.SIGNIN_BUTTON)
            self.click_on_element(signin_button)
            self.driver_wait(driver, delay + 2)
        finally:
            if self.get_cur_url(driver) == wtp_home_page_url:
                return True
            else:
                return False
