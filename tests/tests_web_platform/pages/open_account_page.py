# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.test_definitions import BaseConfig
from tests.tests_web_platform.pages import wtp_open_account_url
from tests.tests_web_platform.pages.base_page import BasePage
from src.test_utils.file_utils import get_account_details
from tests.tests_web_platform.locators.open_account_page_locators import OpenAccountPageLocators


class OpenAccountPage(BasePage):
    def __init__(self):
        super(OpenAccountPage, self).__init__()
        # data_file, row, column1, column2, column3, column4
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        self.firstname = details['firstname']
        self.lastname = details['lastname']
        self.email = details['email']
        self.password = details['password']
        self.terms_url = "https://dx.exchange/terms-of-use/"
        self.privacy_url = "https://dx.exchange/privacy-policy/"

    def registration_flow_ddt(self, driver, firstname, lastname, email, password):
        delay = 3
        try:
            assert self.get_cur_url(driver) == wtp_open_account_url
            self.driver_wait(driver, delay)
            firstname_field = self.find_element(driver, OpenAccountPageLocators.FIRST_NAME_FIELD)
            self.click_on_element(firstname_field)
            self.send_keys(firstname_field, firstname)
            lastname_field = self.find_element(driver, OpenAccountPageLocators.LAST_NAME_FIELD)
            self.click_on_element(lastname_field)
            self.send_keys(lastname_field, lastname)
            email_field = self.find_element(driver, OpenAccountPageLocators.EMAIL_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            password_field = self.find_element(driver, OpenAccountPageLocators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_field, password)
            captcha = self.find_element(driver, OpenAccountPageLocators.CAPTCHA)
            self.click_on_element(captcha)
            certify_checkbox = self.find_element(driver, OpenAccountPageLocators.CERTIFY_CHECKBOX)
            self.click_on_element(certify_checkbox)
            create_account_button = self.find_element(driver, OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            self.click_on_element(create_account_button)
            self.driver_wait(driver, delay)
        finally:
            if self.check_element_not_visible(driver, delay, OpenAccountPageLocators.OPEN_ACCOUNT_BOX):
                return True
            else:
                return False

    def registration_flow(self, driver, delay):
        try:
            assert self.get_cur_url(driver) == wtp_open_account_url
            self.driver_wait(driver, delay + 2)
            firstname_field = self.find_element(driver, OpenAccountPageLocators.FIRST_NAME_FIELD)
            self.click_on_element(firstname_field)
            self.send_keys(firstname_field, self.firstname)
            lastname_field = self.find_element(driver, OpenAccountPageLocators.LAST_NAME_FIELD)
            self.click_on_element(lastname_field)
            self.send_keys(lastname_field, self.lastname)
            email_field = self.find_element(driver, OpenAccountPageLocators.EMAIL_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, self.email)
            password_field = self.find_element(driver, OpenAccountPageLocators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_field, self.password)
            self.driver_wait(driver, delay + 1)
            assert self.check_element_not_visible(driver, delay, OpenAccountPageLocators.PASSWORD_NOT_SECURE)
            self.driver_wait(driver, delay + 3)
            #captcha_frame = self.find_element(driver, OpenAccountPageLocators.CAPTCHA_FRAME)
            #self.click_on_captcha(driver, captcha_frame)
            terms_link = self.find_element(driver, OpenAccountPageLocators.TERM_OF_USE_LINK)
            self.click_on_element(terms_link)
            self.driver_wait(driver, delay + 1)
            assert self.get_cur_url(driver) == self.terms_url
            privacy_link = self.find_element(driver, OpenAccountPageLocators.PRIVACY_POLICY_LINK)
            self.click_on_element(privacy_link)
            self.driver_wait(driver, delay + 1)
            assert self.get_cur_url(driver) == self.privacy_url
            newsletters_checkbox = self.find_element(driver, OpenAccountPageLocators.NEWSLETTERS_CHECKBOX)
            self.click_on_element(newsletters_checkbox)
            certify_checkbox = self.find_element(driver, OpenAccountPageLocators.CERTIFY_CHECKBOX)
            self.click_on_element(certify_checkbox)
            create_account_button = self.find_element(driver, OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            self.click_on_element(create_account_button)
            self.driver_wait(driver, delay + 1)
        finally:
            if self.check_element_not_visible(driver, delay, OpenAccountPageLocators.OPEN_ACCOUNT_BOX):
                return True
            else:
                return False
