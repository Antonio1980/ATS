# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.me_admin.pages.base_page import BasePage
from tests.crm.locators.home_page_locators import HomePageLocators
from tests.me_admin.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    @classmethod
    def login(cls, delay, username, password):
        by_id = "ID"
        cls.go_to_url(BaseConfig.ME_BASE_URL)
        assert cls.wait_element_visible(delay + 1, LogInPageLocators.NASDAQ_LOGO)
        un = cls.find_element_by(LogInPageLocators.USERNAME_FIELD, by_id)
        un.clear()
        un.send_keys(username)
        ps = cls.find_element_by(LogInPageLocators.PASSWORD_FIELD, by_id)
        ps.clear()
        ps.send_keys(password)
        cls.click_on_element(delay + 2, LogInPageLocators.LOGIN_BUTTON)
        cls.wait_element_visible(delay + 1, HomePageLocators.HOME_PAGE_LOGO)

