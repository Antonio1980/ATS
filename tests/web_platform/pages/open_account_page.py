# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.web_platform.pages.base_page import BasePage
from src.test_utils.file_utils import get_account_details
from tests.web_platform.locators.open_account_page_locators import OpenAccountPageLocators


class OpenAccountPage(BasePage):
    @classmethod
    def setup_open_account_page(cls):
        cls.set_up_base_page()
        cls.self_url = "openAccountDx.html"
        # data_file, row, column1, column2, column3, column4
        details = get_account_details(BaseConfig.OPEN_ACCOUNT_DATA, 0, 0, 1, 2, 3)
        cls.firstname = details['firstname']
        cls.lastname = details['lastname']
        cls.email = details['email']
        cls.password = details['password']
        cls.open_account_url = cls.base_url + cls.self_url
        cls.terms_url = "https://dx.exchange/terms-of-use/"
        cls.privacy_url = "https://dx.exchange/privacy-policy/"

    @classmethod
    def registration_flow_ddt(cls, firstname, lastname, email, password):
        delay = 3
        try:
            assert cls.open_account_url == cls.get_cur_url()
            cls.driver_wait(delay)
            firstname_field = cls.find_element(OpenAccountPageLocators.FIRST_NAME_FIELD)
            cls.click_on_element(firstname_field)
            cls.send_keys(firstname_field, firstname)
            lastname_field = cls.find_element(OpenAccountPageLocators.LAST_NAME_FIELD)
            cls.click_on_element(lastname_field)
            cls.send_keys(lastname_field, lastname)
            email_field = cls.find_element(OpenAccountPageLocators.EMAIL_FIELD)
            cls.click_on_element(email_field)
            cls.send_keys(email_field, email)
            password_field = cls.find_element(OpenAccountPageLocators.PASSWORD_FIELD)
            cls.click_on_element(password_field)
            cls.send_keys(password_field, password)
            captcha = cls.find_element(OpenAccountPageLocators.CAPTCHA)
            cls.click_on_element(captcha)
            certify_checkbox = cls.find_element(OpenAccountPageLocators.CERTIFY_CHECKBOX)
            cls.click_on_element(certify_checkbox)
            create_account_button = cls.find_element(OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            cls.click_on_element(create_account_button)
            cls.driver_wait(delay)
        finally:
            if cls.check_element_not_visible(OpenAccountPageLocators.OPEN_ACCOUNT_BOX):
                return True
            else:
                return False

    @classmethod
    def registration_flow(cls, delay):
        print(cls.open_account_url)
        try:
            assert cls.open_account_url == cls.get_cur_url()
            cls.driver_wait(delay + 1)
            firstname_field = cls.find_element(OpenAccountPageLocators.FIRST_NAME_FIELD)
            cls.click_on_element(firstname_field)
            cls.send_keys(firstname_field, cls.firstname)
            lastname_field = cls.find_element(OpenAccountPageLocators.LAST_NAME_FIELD)
            cls.click_on_element(lastname_field)
            cls.send_keys(lastname_field, cls.lastname)
            email_field = cls.find_element(OpenAccountPageLocators.EMAIL_FIELD)
            cls.click_on_element(email_field)
            cls.send_keys(email_field, cls.email)
            password_field = cls.find_element(OpenAccountPageLocators.PASSWORD_FIELD)
            cls.click_on_element(password_field)
            cls.send_keys(password_field, cls.password)
            cls.driver_wait(delay + 1)
            assert cls.check_element_not_visible(delay, OpenAccountPageLocators.PASSWORD_NOT_SECURE)
            cls.driver_wait(delay + 3)
            captcha_frame = cls.find_element(OpenAccountPageLocators.CAPTCHA_FRAME)
            cls.click_on_captcha(captcha_frame)
            terms_link = cls.find_element(OpenAccountPageLocators.TERM_OF_USE_LINK)
            cls.click_on_element(terms_link)
            cls.driver_wait(delay + 1)
            assert cls.get_cur_url() == cls.terms_url
            privacy_link = cls.find_element(OpenAccountPageLocators.PRIVACY_POLICY_LINK)
            cls.click_on_element(privacy_link)
            cls.driver_wait(delay + 1)
            assert cls.get_cur_url() == cls.privacy_url
            newsletters_checkbox = cls.find_element(OpenAccountPageLocators.NEWSLETTERS_CHECKBOX)
            cls.click_on_element(newsletters_checkbox)
            certify_checkbox = cls.find_element(OpenAccountPageLocators.CERTIFY_CHECKBOX)
            cls.click_on_element(certify_checkbox)
            create_account_button = cls.find_element(OpenAccountPageLocators.CREATE_ACCOUNT_BUTTON)
            cls.click_on_element(create_account_button)
            cls.driver_wait(delay + 1)
        finally:
            if cls.check_element_not_visible(OpenAccountPageLocators.OPEN_ACCOUNT_BOX):
                return True
            else:
                return False
