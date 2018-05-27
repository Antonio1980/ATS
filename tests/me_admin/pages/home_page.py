# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.me_admin.locators.home_page_locators import HomePageLocators
from tests.me_admin.locators.login_page_locators import LogInPageLocators
from tests.me_admin.pages.base_page import BasePage


class HomePage(BasePage):

    @classmethod
    def logout(self, delay):
        self.wait_element_visible(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        self.click_on_element(delay + 3, HomePageLocators.SETTINGS_DROPDOWN)
        self.click_on_element(delay + 3, HomePageLocators.LOGOFF_BUTTON)
        self.click_on_element(delay + 2, HomePageLocators.LOGOFF_CONFIRM_BUTTON)
        assert self.wait_element_visible(delay + 1, LogInPageLocators.NASDAQ_LOGO)
