# !/usr/bin/env python
# -*- coding: utf8 -*-
import time

from tests.pages.browser import Browser
from tests_sources.test_definitions import BaseConfig
from tests.locators.home_page_locators import HomePageLocators
from tests.locators.login_page_locators import LogInPageLocators


class LogInPage(Browser):
    @classmethod
    def login(self, delay, username, password):
        self.go_to_page(BaseConfig.CRM_BASE_URL)
        assert self.driver_wait_element_located(delay+1, LogInPageLocators.CRM_LOGO)
        assert self.driver_wait_element_located(delay+1, LogInPageLocators.FORGOT_PASSWORD_LINK)
        self.search_and_type(delay+2, username, LogInPageLocators.USERNAME_FIELD)
        self.search_and_type(delay+2, password, LogInPageLocators.PASSWORD_FIELD)
        self.search_and_click(delay+2, LogInPageLocators.LOGIN_BUTTON)
        self.driver_wait(delay)
        assert self.driver_wait_element_located(delay+1, HomePageLocators.HOME_PAGE_LOGO)
        self.driver_wait(delay)

    @classmethod
    def logout(self, delay):
        self.driver_wait(delay)
<<<<<<< HEAD
        assert self.driver_wait_element_located(delay+1, HomePageLocators.HOME_PAGE_LOGO)
        self.search_and_click(delay+10, HomePageLocators.SETTINGS_DROPDOWN)
        #time.sleep(10)
        self.search_and_click(delay+5, HomePageLocators.LANGUAGE_ICON)
        self.search_and_click(delay+3, HomePageLocators.LOGOUT_LINK)
        assert self.driver_wait_element_located(delay+1, LogInPageLocators.CRM_LOGO)
=======
<<<<<<< HEAD
        assert self.driver_wait_element_present(delay+1, HomePageLocators.HOME_PAGE_LOGO)
        self.search_wait_click(delay+2, HomePageLocators.SETTINGS_DROPDOWN)
        self.search_wait_click(delay+2, HomePageLocators.LANGUAGE_ICON)
        self.search_wait_click(delay+2, HomePageLocators.LOGOUT_LINK)
        assert self.driver_wait_element_present(delay+1, LogInPageLocators.CRM_LOGO)
=======
        assert self.driver_wait_element_located(delay+1, HomePageLocators.HOME_PAGE_LOGO)
        self.search_and_click(delay+10, HomePageLocators.SETTINGS_DROPDOWN)
        #time.sleep(10)
        self.search_and_click(delay+5, HomePageLocators.LANGUAGE_ICON)
        self.search_and_click(delay+3, HomePageLocators.LOGOUT_LINK)
        assert self.driver_wait_element_located(delay+1, LogInPageLocators.CRM_LOGO)
>>>>>>> 1bca7f1... fixed forgot password
>>>>>>> fbcde02... fixed forgot password
        self.driver_wait(delay)


    @classmethod
    def forgot_password(self, delay, email):
        self.go_to_page(BaseConfig.CRM_BASE_URL)
<<<<<<< HEAD
=======
<<<<<<< HEAD
        assert self.driver_wait_element_present(delay, LogInPageLocators.CRM_LOGO)
        self.search_wait_click(delay, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert self.driver_wait_element_present(delay + 1, LogInPageLocators.FORGOT_POPUP)
        assert self.driver_wait_element_present(delay, LogInPageLocators.MESSAGE_POPUP)
        assert self.driver_wait_element_present(delay, LogInPageLocators.NOTE_POPUP)
        self.search_wait_click(delay + 2, LogInPageLocators.CLOSE_BUTTON)
        self.refresh_page()
        self.search_wait_click(delay, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert self.driver_wait_element_present(delay + 1, LogInPageLocators.FORGOT_POPUP)
        self.search_and_type(delay + 3, email, LogInPageLocators.EMAIL_FIELD)
        self.search_wait_click(delay + 2, LogInPageLocators.SEND_BUTTON)
        assert self.driver_wait_element_present(delay + 1, LogInPageLocators.CRM_LOGO)
        # LogInPage.forgot_password(delay, email)
=======
>>>>>>> fbcde02... fixed forgot password
        assert self.driver_wait_element_located(delay+1, LogInPageLocators.CRM_LOGO)
        self.search_and_click(delay+2, LogInPageLocators.FORGOT_PASSWORD_LINK)
        assert self.driver_wait_element_located(delay+1, LogInPageLocators.FORGOT_POPUP)
        self.search_and_type(delay+3, email, LogInPageLocators.EMAIL_FIELD)
        self.search_and_click(delay+2, LogInPageLocators.SEND_BUTTON)
        assert self.driver_wait_element_located(delay+1, LogInPageLocators.CRM_LOGO)
<<<<<<< HEAD
=======
>>>>>>> 1bca7f1... fixed forgot password
>>>>>>> fbcde02... fixed forgot password




