# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.web_platform.pages.base_page import BasePage
from tests.web_platform.pages.home_page import HomePage
from src.test_utils.file_utils import get_account_details
from tests.web_platform.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    @classmethod
    def setup_login_page(cls):
        cls.set_up_base_page()
        HomePage.set_up_home_page()
        self_url = "login.html"
        cls.login_page_url = cls.wtp_base_url + self_url
        # data_file, row, column1, column2, column3, column4
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        cls.email = details['email']
        cls.password = details['password']

    @classmethod
    def login(cls, delay):
        try:
            HomePage.open_login_page(delay + 1)
            assert cls.login_page_url == cls.get_cur_url()
            username_field = cls.find_element(LogInPageLocators.USERNAME_FIELD)
            cls.send_keys(username_field, cls.email)
            password_field = cls.find_element(LogInPageLocators.PASSWORD_FIELD)
            cls.send_keys(password_field, cls.assword)
            captcha = cls.find_element(LogInPageLocators.CAPTCHA)
            cls.click_on_captcha(captcha)
            signin_button = cls.find_element(LogInPageLocators.SIGNIN_BUTTON)
            cls.click_on_element(signin_button)
            cls.driver_wait(delay + 2)
        finally:
            if cls.get_cur_url() == HomePage.wtp_home_page_url:
                return True
            else:
                return False
