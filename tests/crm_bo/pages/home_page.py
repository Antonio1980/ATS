# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.crm_bo.pages.base_page import BasePage
from tests.crm_bo.pages.customer_page import CustomerPage
from tests.crm_bo.locators.home_page_locators import HomePageLocators
from tests.crm_bo.locators.login_page_locators import LogInPageLocators
from tests.crm_bo.locators.customer_page_locators import CustomerPageLocators


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()
        self.customer_admin_url = CustomerPage().customer_admin_url
        self_url = "dashboard"
        self.home_page_url = self.crm_base_url + self_url

    def logout(self, driver, delay):
        try:
            self.driver_wait(driver, delay)
            assert self.wait_element_presented(driver, delay + 1, HomePageLocators.HOME_PAGE_LOGO)
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
            assert self.home_page_url == self.get_cur_url(driver)
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
            if self.customer_admin_url == self.get_cur_url(driver):
                return True
            else:
                return False
