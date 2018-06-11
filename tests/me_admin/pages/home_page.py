# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.me_admin.pages.base_page import BasePage
from tests.me_admin.locators.home_page_locators import HomePageLocators
from tests.me_admin.locators.login_page_locators import LogInPageLocators


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()

    def logout(self, driver, delay):
        self.wait_element_visible(driver, delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        self.find_element(driver, HomePageLocators.SETTINGS_DROPDOWN)
        self.find_element(driver, HomePageLocators.LOGOFF_BUTTON)
        self.find_element(driver, HomePageLocators.LOGOFF_CONFIRM_BUTTON)
        assert self.wait_element_visible(driver, delay + 1, LogInPageLocators.NASDAQ_LOGO)
