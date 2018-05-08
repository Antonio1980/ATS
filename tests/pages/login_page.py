# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.pages.page_base import BasePage
from tests_extensions.tests_definitions import BaseConfig
from tests_resources.locators.home_page_locators import HomePageLocators
from tests_resources.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    @classmethod
    def login(self, username, password):
        self.go_to_page(BaseConfig.CRM_BASE_URL)
        assert self.driver_wait_element_present(2, LogInPageLocators.CRM_LOGO)
        assert self.driver_wait_element_present(2, LogInPageLocators.FORGOT_PASSWORD_LINK)
        self.search_and_type(3, username, LogInPageLocators.USERNAME_FIELD)
        self.search_and_type(3, password, LogInPageLocators.PASSWORD_FIELD)
        self.search_and_click(3, LogInPageLocators.LOGIN_BUTTON)
        self.driver_wait(2)
        assert self.driver_wait_element_present(2, HomePageLocators.HOME_PAGE_LOGO)
        self.driver_wait(1)

    @classmethod
    def logout(self):
        self.driver_wait(1)
        self.driver_wait_element_present(2, HomePageLocators.HOME_PAGE_LOGO)
        self.search_and_click(3, HomePageLocators.SETTINGS_DROPDOWN)
        self.search_wait_click(3, HomePageLocators.LANGUAGE_ICON)
        self.search_and_click(10, HomePageLocators.LOGOUT_LINK)
        self.driver_wait_element_present(2, LogInPageLocators.CRM_LOGO)
        self.driver_wait(1)




