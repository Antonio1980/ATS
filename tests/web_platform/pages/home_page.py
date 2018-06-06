# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.web_platform.pages.base_page import BasePage
from tests.web_platform.pages.open_account_page import OpenAccountPage
from tests.web_platform.locators.home_page_locators import HomePageLocators


class HomePage(BasePage):
    @classmethod
    def set_up_home_page(cls):
        cls.set_up_base_page()
        cls.self_url = "exchange.html?nr_insight=0&fullPlugin=1"
        cls.wtp_home_page_url = cls.base_url + cls.self_url

    @classmethod
    def go_to_home_page(cls):
        cls.go_to_url(cls.wtp_home_page_url)

    @classmethod
    def click_on_sign_up(cls, delay):
        try:
            assert cls.wtp_home_page_url == cls.get_cur_url()
            signup_button = cls.find_element_by(HomePageLocators.SIGN_UP_BUTTON_CLS, "class_name")
            cls.driver_wait(delay + 3)
            cls.click_on_element(signup_button)
            cls.driver_wait(delay + 10)
        finally:
            if cls.get_cur_url() == cls.open_account_url:
                return True
            else:
                return False
            