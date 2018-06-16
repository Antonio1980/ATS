# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.tests_crm_bo.pages.base_page import BasePage
from src.test_utils.mailinator_utils import email_generator
from tests.tests_crm_bo.pages import create_user_page_url, user_index_page_url
from tests.tests_crm_bo.locators.create_user_page_locators import CreateUserPageLocators


class CreateUserPage(BasePage):
    def __init__(self):
        super(CreateUserPage, self).__init__()
        self.email_suffix = email_generator()
        self.email = self.email_suffix + "@mailinator.com"
        self.first_name = "Jason"
        self.last_name = "Born"
        self.phone = int("0549212272")

    def fill_user_details(self, driver, delay):
        try:
            assert self.get_cur_url(driver) == create_user_page_url
            first_name_field = self.find_element_by(driver, CreateUserPageLocators.FIRST_NAME_ID, "id")
            self.click_on_element(first_name_field)
            self.send_keys(first_name_field, self.first_name)
            last_name_field = self.find_element_by(driver, CreateUserPageLocators.LAST_NAME_ID, "id")
            self.click_on_element(last_name_field)
            self.send_keys(last_name_field, self.last_name)
            email_field = self.find_element_by(driver, CreateUserPageLocators.EMAIL_ID, "id")
            self.click_on_element(email_field)
            self.send_keys(email_field, self.email)
            phone_field = self.find_element_by(driver, CreateUserPageLocators.PHONE_ID, "id")
            self.click_on_element(phone_field)
            self.send_keys(phone_field, self.phone)
            username_field = self.find_element_by(driver, CreateUserPageLocators.USERNAME_ID, "id")
            self.click_on_element(username_field)
            self.send_keys(username_field, self.email_suffix)
            language_dropdown = self.find_element(driver, CreateUserPageLocators.LANGUAGE_DROPDOWN)
            self.click_on_element(language_dropdown)
            language_field = self.find_element(driver, CreateUserPageLocators.LANGUAGE_FIELD)
            self.click_on_element(language_field)
            language_text_field = self.find_element(driver, CreateUserPageLocators.LANGUAGE_TEXT_FIELD)
            self.send_keys(language_text_field, "eng")
            self.send_enter_key(language_text_field)
            permission_dropdown = self.find_element(driver, CreateUserPageLocators.PERMISSION_GROUP_DROPDOWN)
            self.click_on_element(permission_dropdown)
            permission_field = self.find_element(driver, CreateUserPageLocators.PERMISSION_GROUP_FIELD)
            self.click_on_element(permission_field)
            permission_text_field = self.find_element(driver, CreateUserPageLocators.PERMISSION_GROUP_TEXT_FIELD)
            self.send_keys(permission_text_field, "sup")
            self.send_enter_key(permission_text_field)
            status_dropdown = self.find_element(driver, CreateUserPageLocators.STATUS_DROPDOWN)
            self.click_on_element(status_dropdown)
            status_field = self.find_element(driver, CreateUserPageLocators.STATUS_FIELD)
            self.click_on_element(status_field)
            status_text_field = self.find_element(driver, CreateUserPageLocators.STATUS_TEXT_FIELD)
            self.send_keys(status_text_field, "a")
            self.send_enter_key(status_text_field)
            user_type_dropdown = self.find_element(driver, CreateUserPageLocators.USER_TYPE_DROPDOWN)
            self.click_on_element(user_type_dropdown)
            user_type_field = self.find_element(driver, CreateUserPageLocators.USER_TYPE_FIELD)
            self.click_on_element(user_type_field)
            user_type_text_field = self.find_element(driver, CreateUserPageLocators.USER_TYPE_TEXT_FIELD)
            self.send_keys(user_type_text_field, "Admin")
            self.send_enter_key(user_type_text_field)
            create_user_button = self.find_element_by(driver, CreateUserPageLocators.CREATE_USER_BUTTON_ID, "id")
            self.click_on_element(create_user_button)
            self.driver_wait(driver, delay =+ 10)
        finally:
            if self.get_cur_url(driver) == user_index_page_url:
                print(user_index_page_url)
                return True
            else:
                return False

    def fill_user_details_ddt(self, driver, first_name, last_name, email, username):
        try:
            print(user_index_page_url)
            assert self.get_cur_url(driver) == create_user_page_url
            first_name_field = self.find_element_by(driver, CreateUserPageLocators.FIRST_NAME_ID, "id")
            self.click_on_element(first_name_field)
            self.send_keys(first_name_field, first_name)
            last_name_field = self.find_element_by(driver, CreateUserPageLocators.LAST_NAME_ID, "id")
            self.click_on_element(last_name_field)
            self.send_keys(last_name_field, last_name)
            email_field = self.find_element_by(driver, CreateUserPageLocators.EMAIL_ID, "id")
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            phone_field = self.find_element_by(driver, CreateUserPageLocators.PHONE_ID, "id")
            self.click_on_element(phone_field)
            self.send_keys(phone_field, self.phone)
            username_field = self.find_element_by(driver, CreateUserPageLocators.USERNAME_ID, "id")
            self.click_on_element(username_field)
            self.send_keys(username_field, username)
            language_dropdown = self.find_element(driver, CreateUserPageLocators.LANGUAGE_DROPDOWN)
            self.click_on_element(language_dropdown)
            language_field = self.find_element(driver, CreateUserPageLocators.LANGUAGE_FIELD)
            self.click_on_element(language_field)
            language_text_field = self.find_element(driver, CreateUserPageLocators.LANGUAGE_TEXT_FIELD)
            self.send_keys(language_text_field, "eng")
            self.send_enter_key(language_text_field)
            permission_dropdown = self.find_element(driver, CreateUserPageLocators.PERMISSION_GROUP_DROPDOWN)
            self.click_on_element(permission_dropdown)
            permission_field = self.find_element(driver, CreateUserPageLocators.PERMISSION_GROUP_FIELD)
            self.click_on_element(permission_field)
            permission_text_field = self.find_element(driver, CreateUserPageLocators.PERMISSION_GROUP_TEXT_FIELD)
            self.send_keys(permission_text_field, "sup")
            self.send_enter_key(permission_text_field)
            status_dropdown = self.find_element(driver, CreateUserPageLocators.STATUS_DROPDOWN)
            self.click_on_element(status_dropdown)
            status_field = self.find_element(driver, CreateUserPageLocators.STATUS_FIELD)
            self.click_on_element(status_field)
            status_text_field = self.find_element(driver, CreateUserPageLocators.STATUS_TEXT_FIELD)
            self.send_keys(status_text_field, "a")
            self.send_enter_key(status_text_field)
            user_type_dropdown = self.find_element(driver, CreateUserPageLocators.USER_TYPE_DROPDOWN)
            self.click_on_element(user_type_dropdown)
            user_type_field = self.find_element(driver, CreateUserPageLocators.USER_TYPE_FIELD)
            self.click_on_element(user_type_field)
            user_type_text_field = self.find_element(driver, CreateUserPageLocators.USER_TYPE_TEXT_FIELD)
            self.send_keys(user_type_text_field, "Admin")
            self.send_enter_key(user_type_text_field)
            create_user_button = self.find_element_by(driver, CreateUserPageLocators.CREATE_USER_BUTTON_ID, "id")
            self.click_on_element(create_user_button)
            self.driver_wait(driver, delay =+ 10)
        finally:
            if self.get_cur_url(driver) == user_index_page_url:
                return True
            else:
                return False