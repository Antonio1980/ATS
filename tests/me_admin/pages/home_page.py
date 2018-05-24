# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.me_admin.locators.home_page_locators import HomePageLocators
from tests.me_admin.locators.login_page_locators import LogInPageLocators
from tests.me_admin.pages.base_page import BasePage


class HomePage(BasePage):

    @classmethod
    def logout(self, delay):
        #self.find_element_by(HomePageLocators.SETTINGS_DROPDOWN, "XPATH")
        self.wait_element_visible(delay, HomePageLocators.HOME_PAGE_LOGO)
        self.click_on_element(delay, HomePageLocators.SETTINGS_DROPDOWN)
        self.click_on_element(delay, HomePageLocators.LOGOFF_BUTTON)
        self.click_on_element(delay, HomePageLocators.LOGOFF_CONFIRM_BUTTON)
        assert self.wait_element_visible(delay, LogInPageLocators.NASDAQ_LOGO)
