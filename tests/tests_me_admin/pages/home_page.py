<<<<<<< a6ac884835aaa047de5b5f6bf0e391f6806c43ed:tests/me_admin/pages/home_page.py
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
=======
# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.tests_me_admin.locators.home_page_locators import HomePageLocators
from tests.tests_me_admin.locators.login_page_locators import LogInPageLocators
from tests.tests_me_admin.pages.base_page import BasePage


class HomePage(BasePage):

    @classmethod
    def logout(self, delay):
        self.wait_element_visible(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        self.click_on_element(delay + 3, HomePageLocators.SETTINGS_DROPDOWN)
        self.click_on_element(delay + 3, HomePageLocators.LOGOFF_BUTTON)
        self.click_on_element(delay + 2, HomePageLocators.LOGOFF_CONFIRM_BUTTON)
        assert self.wait_element_visible(delay + 1, LogInPageLocators.NASDAQ_LOGO)
>>>>>>> 46d3ea0049230292881d76fb45bbfa6fde5f95e8:tests/tests_me_admin/pages/home_page.py
