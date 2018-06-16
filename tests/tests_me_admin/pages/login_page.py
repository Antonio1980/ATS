# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.tests_me_admin.pages.base_page import BasePage
from tests.tests_me_admin.locators.home_page_locators import HomePageLocators
from tests.tests_me_admin.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):

    def __init__(self):
        super(LogInPage, self).__init__()
        self_url = "/xai/auth/logon"
        self.login_page_url = self.me_base_url + self_url

    def login(self, driver, delay, username, password):
        try:
            self.go_to_url(driver, self.me_base_url)
            assert self.get_cur_url(driver) == self.login_page_url
            assert self.wait_element_visible(driver, delay + 1, LogInPageLocators.NASDAQ_LOGO)
            username_field = self.find_element_by(driver, LogInPageLocators.USERNAME_FIELD, "id")
            self.send_keys(username_field, username)
            password_field = self.find_element_by(driver, LogInPageLocators.PASSWORD_FIELD, "id")
            self.send_keys(password_field, password)
            login_button = self.find_element(driver, LogInPageLocators.LOGIN_BUTTON)
            self.click_on_element(login_button)
        finally:
            if self.wait_element_visible(driver, delay + 1, HomePageLocators.HOME_PAGE_LOGO):
                return True
            else:
                return False

