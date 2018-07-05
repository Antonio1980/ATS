# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators.home_page_locators import HomePageLocators
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators
from tests.tests_crm_bo.locators.customer_page_locators import CustomerPageLocators
from tests.tests_crm_bo.pages import home_page_url, user_management_page_url, customer_admin_url


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()

    def logout(self, driver, delay):
        try:
            self.driver_wait(driver, delay + 3)
            assert self.find_element_by(driver, HomePageLocators.HOME_PAGE_LOGO_ID, "id")
            self.click_on_element_by_locator(driver, delay + 5, HomePageLocators.SETTINGS_DROPDOWN)
            self.click_on_element_by_locator(driver, delay + 5, HomePageLocators.LANGUAGE_ICON)
            self.click_on_element_by_locator(driver, delay + 3, HomePageLocators.LOGOUT_LINK)
        finally:
            if self.wait_element_presented(driver, delay + 1, LogInPageLocators.CRM_LOGO):
                self.driver_wait(driver, delay)
                return True
            else:
                return False

    def choose_customer_by_name(self, driver, delay):
        try:
            assert home_page_url == self.get_cur_url(driver)
            customer_field = self.find_element(driver, HomePageLocators.CUSTOMER_DROPDOWN)
            self.click_on_element(customer_field)
            self.driver_wait(driver, delay)
            customer_option = self.find_element(driver, HomePageLocators.CUSTOMER_ID_OPTION)
            self.click_on_element(customer_option)
            self.driver_wait(driver, delay)
            customer_name_field = self.find_element_by(driver, HomePageLocators.CUSTOMER_NAME_FIELD_ID, "id")
            self.click_on_element(customer_field)
            self.send_keys(customer_name_field, BaseConfig.CRM_CUSTOMER_ID)
            self.driver_wait(driver, delay)
            show_button = self.find_element_by(driver, HomePageLocators.SHOW_RESULTS_BUTTON_ID, "id")
            self.click_on_element(show_button)
            self.driver_wait(driver, delay)
            assert self.wait_element_visible(driver, delay + 1, CustomerPageLocators.CUSTOMER_ID_TEXT)
        finally:
            if customer_admin_url == self.get_cur_url(driver):
                return True
            else:
                return False

    def go_to_management_inset_with_users_option(self, driver, delay):
        try:
            assert home_page_url == self.get_cur_url(driver)
            self.driver_wait(driver, delay)
            management_dropdown = self.find_element(driver, HomePageLocators.MANAGEMENT_DROPDOWN)
            self.driver_wait(driver, delay)
            self.click_on_element(management_dropdown)
            users_option = self.find_element(driver, HomePageLocators.MANAGEMENT_USERS_OPTION)
            self.driver_wait(driver, delay)
            self.click_on_element(users_option)
            self.driver_wait(driver, delay)
        finally:
            if user_management_page_url == self.get_cur_url(driver):
                return True
            else:
                return False
