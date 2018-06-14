# !/usr/bin/env python
# -*- coding: utf8 -*-

<<<<<<< a6ac884835aaa047de5b5f6bf0e391f6806c43ed:tests/web_platform/pages/home_page.py
from tests.web_platform.pages.base_page import BasePage
from tests.web_platform.locators.home_page_locators import HomePageLocators
from tests.web_platform.pages.login_page import LogInPage
from tests.web_platform.pages.open_account_page import OpenAccountPage
=======
from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.home_page_locators import HomePageLocators
>>>>>>> 46d3ea0049230292881d76fb45bbfa6fde5f95e8:tests/tests_web_platform/pages/home_page.py


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()
        self.wtp_login_page_url = LogInPage().wtp_login_page_url
        self.wtp_open_account_url = OpenAccountPage().wtp_open_account_url
        self_url = "exchange.html?nr_insight=0&fullPlugin=1"
        self.wtp_home_page_url = self.wtp_base_url + self_url

    def open_home_page(self, driver, delay):
        self.go_to_url(driver, self.wtp_home_page_url)
        return self.driver_wait(driver, delay + 3)

    def open_signup_page(self, driver, delay):
        try:
            self.open_home_page(driver, delay)
            assert self.wtp_home_page_url == self.get_cur_url(driver)
            self.click_on_element_by_locator(driver, delay+5, HomePageLocators.SIGN_UP_BUTTON)
            self.driver_wait(driver, delay + 3)
        finally:
            if self.get_cur_url(driver) == self.wtp_open_account_url:
                return True
            else:
                return False

    def open_login_page(self, driver, delay):
        try:
            self.open_home_page(driver, delay)
            assert self.wtp_home_page_url == self.get_cur_url(driver)
            self.click_on_element_by_locator(driver, delay + 5, HomePageLocators.LOGIN_BUTTON)
            self.driver_wait(driver, delay + 3)
        finally:
            if self.get_cur_url(driver) == self.wtp_login_page_url:
                return True
            else:
                return False
