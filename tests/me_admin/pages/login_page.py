# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.me_admin.pages.base_page import BasePage
from tests.crm_bo.locators.home_page_locators import HomePageLocators
from tests.me_admin.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    def __init__(self):
        super(LogInPage, self).__init__()
        self_url = ""
        self.me_login_page_url = self.me_base_url + self_url

    def login(self, driver, delay, username, password):
        by_id = "ID"
        self.go_to_url(driver, self.me_base_url)
        assert self.wait_element_visible(driver, delay + 1, LogInPageLocators.NASDAQ_LOGO)
        username_field = self.find_element_by(driver, LogInPageLocators.USERNAME_FIELD_ID, by_id)
        username_field.clear()
        username_field.send_keys(username)
        password_field = self.find_element_by(driver, LogInPageLocators.PASSWORD_FIELD_ID, by_id)
        password_field.clear()
        password_field.send_keys(password)
        login_button = self.find_element(driver, LogInPageLocators.LOGIN_BUTTON)
        self.click_on_element(login_button)
        self.wait_element_visible(driver, delay + 1, HomePageLocators.HOME_PAGE_LOGO)
