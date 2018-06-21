# !/usr/bin/env python
# -*- coding: utf8 -*-
import time

from src.test_utils.mailinator_utils import email_generator
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
        self.password = details['password']
        email_suffix = "@mailinator.com"
        self.negative_email = details['email']
        self.email = email_generator() + email_suffix
        self.terms_url = "https://dx.exchange/terms-of-use/"
        self.privacy_url = "https://dx.exchange/privacy-policy/"
        self.script = '$("input[name=\'captcha\']").val("sdfgsdfgsdfdfssdfgsdfg");'
        self.element = "//*[@class='userEmail'][contains(.,'')]"

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
            logo = self.find_element(driver, OpenAccountPageLocators.OPEN_ACCOUNT_LOGO)
            time.sleep(5)
            self.click_with_offset(driver, logo, 3, 3)
            # captcha = self.find_element(driver, OpenAccountPageLocators.CAPTCHA)
            self.execute_js(driver, self.script)
            create_account_button = self.find_element(driver, OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            self.click_on_element(create_account_button)
            self.driver_wait(driver, delay + 1)
        finally:
            if self.wait_element_presented(driver, delay, self.element):
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
            certify_checkbox = self.find_element(driver, OpenAccountPageLocators.CERTIFY_CHECKBOX)
            self.click_on_element(certify_checkbox)
            captcha_frame = self.find_element(driver, OpenAccountPageLocators.CAPTCHA_FRAME)
            self.click_with_offset(driver, captcha_frame, 10, 10)
            self.driver_wait(driver, delay + 5)
            logo = self.find_element(driver, OpenAccountPageLocators.OPEN_ACCOUNT_LOGO)
            time.sleep(4)
            self.click_with_offset(driver, logo, 5, 5)
            #captcha = self.find_element(driver, OpenAccountPageLocators.CAPTCHA)
            self.execute_js(driver, self.script)
            create_account_button = self.find_element(driver, OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            self.click_on_element(create_account_button)
            self.driver_wait(driver, delay + 1)
        finally:
            if self.wait_element_presented(driver, delay, self.element):
                return True
            else:
                return False
