# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.pages import wtp_open_account_url
from tests.tests_web_platform.locators.open_account_page_locators import OpenAccountPageLocators


class OpenAccountPage(BasePage):
    def __init__(self):
        super(OpenAccountPage, self).__init__()
        email_suffix = "@mailinator.com"
        self.email = self.email_generator() + email_suffix
        self.terms_url = "https://dx.exchange/terms-of-use/"
        self.privacy_url = "https://dx.exchange/privacy-policy/"
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)
        self.email_verified_locator = OpenAccountPageLocators.EMAIL_ALREADY_VERIFIED
        self.go_back_locator = OpenAccountPageLocators.GO_BACK_TO_DX
        self.email_not_arrived_locator = OpenAccountPageLocators.EMAIL_NOT_ARRIVED

    def fill_signup_form(self, driver, first_last_name, email, password):
        delay = 3
        try:
            self.driver_wait(driver, delay)
            assert self.get_cur_url(driver) == wtp_open_account_url
            firstname_field = self.find_element(driver, OpenAccountPageLocators.FIRST_NAME_FIELD)
            self.click_on_element(firstname_field)
            self.send_keys(firstname_field, first_last_name)
            lastname_field = self.find_element(driver, OpenAccountPageLocators.LAST_NAME_FIELD)
            self.click_on_element(lastname_field)
            self.send_keys(lastname_field, first_last_name)
            email_field = self.find_element(driver, OpenAccountPageLocators.EMAIL_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            password_field = self.find_element(driver, OpenAccountPageLocators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_field, password)
            self.driver_wait(driver, delay)
            assert self.check_element_not_visible(driver, delay, OpenAccountPageLocators.PASSWORD_NOT_SECURE)
            self.driver_wait(driver, delay)
            certify_checkbox = self.find_element(driver, OpenAccountPageLocators.CERTIFY_CHECKBOX)
            self.click_on_element(certify_checkbox)
            newsletters_checkbox = self.find_element(driver, OpenAccountPageLocators.NEWSLETTERS_CHECKBOX)
            self.click_on_element(newsletters_checkbox)
            self.execute_js(driver, self.script_signup)
            create_account_button = self.find_element(driver, OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            self.click_on_element(create_account_button)
            self.driver_wait(driver, delay + 1)
        finally:
            if (self.find_element(driver, self.element) and self.check_element_not_visible(driver, delay, OpenAccountPageLocators.EMAIL_ERROR)) \
                    or self.check_element_not_visible(driver, delay, OpenAccountPageLocators.EMAIL_ERROR2):
                return True
            else:
                return False

    def verify_email_screen_test(self, driver, delay=1):
        assert self.get_cur_url(driver) == wtp_open_account_url
        self.driver_wait(driver, delay + 2)
        assert self.wait_element_presented(driver, delay, OpenAccountPageLocators.EMAIL_NOT_ARRIVED)
        assert self.wait_element_presented(driver, delay, OpenAccountPageLocators.EMAIL_ALREADY_VERIFIED)
        assert self.wait_element_presented(driver, delay, self.go_back_locator)
        return True

    def click_on_link(self, driver, url_to_check, option):
        delay = 3
        try:
            self.wait_driver(driver, delay)
            assert wtp_open_account_url == self.get_cur_url(driver)
            if option == 1:
                element = self.find_element(driver, self.email_verified_locator)
            elif option == 2:
                element = self.find_element(driver, self.go_back_locator)
            else:
                element = self.find_element(driver, self.email_not_arrived_locator)
            self.click_on_element(element)
            self.driver_wait(driver, delay + 1)
        finally:
            if self.get_cur_url(driver) == url_to_check:
                return True
            else:
                return False
