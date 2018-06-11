# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.web_platform.pages.base_page import BasePage
from tests.web_platform.pages.home_page import HomePage
from src.test_utils.file_utils import get_account_details
from tests.web_platform.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    def __init__(self):
        super(LogInPage, self).__init__()
        self.wtp_home_page_url = HomePage().wtp_home_page_url
        self_url = "login.html"
        self.wtp_login_page_url = self.wtp_base_url + self_url
        # data_file, row, column1, column2, column3, column4
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        self.email = details['email']
        self.password = details['password']

    def login(self, driver, delay):
        try:
            self.home_page.open_login_page(driver, delay + 1)
            assert self.wtp_login_page_url == self.get_cur_url(driver)
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
            if self.get_cur_url(driver) == self.wtp_home_page_url:
                return True
            else:
                return False
