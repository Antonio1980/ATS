# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.crm.pages.base_page import BasePage
from tests.crm.locators.home_page_locators import HomePageLocators
from tests.crm.locators.login_page_locators import LogInPageLocators


class HomePage(BasePage):
    @classmethod
    def logout(cls, delay):
        cls.driver_wait(delay)
        assert cls.wait_element_presented(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        cls.click_on_element(delay + 5, HomePageLocators.SETTINGS_DROPDOWN)
        cls.click_on_element(delay + 5, HomePageLocators.LANGUAGE_ICON)
        cls.click_on_element(delay + 3, HomePageLocators.LOGOUT_LINK)
        assert cls.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)
        cls.driver_wait(delay)
