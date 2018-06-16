# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.home_page_locators import HomePageLocators
from tests.tests_web_platform.pages import wtp_login_page_url, wtp_home_page_url, wtp_open_account_url


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()

    def open_home_page(self, driver, delay):
        self.go_to_url(driver, wtp_home_page_url)
        return self.driver_wait(driver, delay + 3)

    def open_signup_page(self, driver, delay):
        try:
            self.open_home_page(driver, delay)
            assert wtp_home_page_url == self.get_cur_url(driver)
            self.click_on_element_by_locator(driver, delay+5, HomePageLocators.SIGN_UP_BUTTON)
            self.driver_wait(driver, delay + 3)
        finally:
            if self.get_cur_url(driver) == wtp_open_account_url:
                return True
            else:
                return False

    def open_login_page(self, driver, delay):
        try:
            self.open_home_page(driver, delay)
            assert wtp_home_page_url == self.get_cur_url(driver)
            self.click_on_element_by_locator(driver, delay + 5, HomePageLocators.LOGIN_BUTTON)
            self.driver_wait(driver, delay + 3)
        finally:
            if self.get_cur_url(driver) == wtp_login_page_url:
                return True
            else:
                return False
