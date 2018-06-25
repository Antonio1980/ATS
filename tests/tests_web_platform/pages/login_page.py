# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.pages import wtp_login_page_url, forgot_password_page_url, wtp_dashboard_url
from tests.tests_web_platform.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    def __init__(self):
        super(LogInPage, self).__init__()
        self.email = "fresh_blood_31@mailinator.com"
        self.password = "1Aa@<>12"

    def login(self, driver, email, password):
        delay = 1
        try:
            self.wait_driver(driver, delay + 3)
            assert wtp_login_page_url == self.get_cur_url(driver)
            username_field = self.find_element(driver, LogInPageLocators.USERNAME_FIELD)
            self.click_on_element(username_field)
            self.send_keys(username_field, email)
            password_true_field = self.find_element(driver, LogInPageLocators.PASSWORD_TRUE_FIELD)
            password_field = self.find_element(driver, LogInPageLocators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_true_field, password)
            self.driver_wait(driver, delay + 5)
            self.execute_js(driver, self.script_login)
            login_button = self.find_element(driver, LogInPageLocators.SIGNIN_BUTTON)
            self.click_on_element(login_button)
            self.driver_wait(driver, delay + 2)
        finally:
            if self.get_cur_url(driver) == wtp_dashboard_url:
                return True
            else:
                return False

    def click_on_forgot_password(self, driver, delay =+ 1):
        try:
            self.wait_driver(driver, delay)
            assert wtp_login_page_url == self.get_cur_url(driver)
            forgot_link = self.find_element(driver, LogInPageLocators.FORGOT_PASSWORD_LINK)
            self.click_on_element(forgot_link)
            self.driver_wait(driver, delay)
        finally:
            if self.get_cur_url(driver) == forgot_password_page_url:
                return True
            else:
                return False
