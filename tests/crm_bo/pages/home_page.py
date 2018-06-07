# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.crm_bo.pages.base_page import BasePage
from tests.crm_bo.pages.customer_page import CustomerPage
from tests.crm_bo.locators.home_page_locators import HomePageLocators
from tests.crm_bo.locators.login_page_locators import LogInPageLocators
from tests.crm_bo.locators.customer_page_locators import CustomerPageLocators


class HomePage(BasePage):
    @classmethod
    def setup_home_page(cls):
        CustomerPage.setup_customer_page()
        cls.customer_page_url = CustomerPage.customer_page_url
        cls.home_page_url = cls.base_url + "dashboard" 

    @classmethod
    def logout(cls, delay):
        try:
            cls.driver_wait(delay)
            assert cls.wait_element_presented(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
            cls.click_on_element_by_locator(delay + 5, HomePageLocators.SETTINGS_DROPDOWN)
            cls.click_on_element_by_locator(delay + 5, HomePageLocators.LANGUAGE_ICON)
            cls.click_on_element_by_locator(delay + 3, HomePageLocators.LOGOUT_LINK)
        finally:
            if cls.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO):
                cls.driver_wait(delay)
                return True
            else:
                return False

    @classmethod
    def choose_customer_by_name(cls, delay):
        try:
            assert cls.home_page_url == cls.get_cur_url()
            customer_field = cls.find_element(HomePageLocators.CUSTOMER_DROPDOWN)
            cls.click_on_element(customer_field)
            cls.driver_wait(delay)
            customer_option = cls.find_element(HomePageLocators.CUSTOMER_ID_OPTION)
            cls.click_on_element(customer_option)
            cls.driver_wait(delay)
            customer_name_field = cls.find_element_by(HomePageLocators.CUSTOMER_NAME_FIELD_ID, "id")
            cls.click_on_element(customer_field)
            cls.send_keys(customer_name_field, BaseConfig.CRM_CUSTOMER_ID)
            cls.driver_wait(delay)
            show_button = cls.find_element_by(HomePageLocators.SHOW_RESULTS_BUTTON_ID, "id")
            cls.click_on_element(show_button)
            cls.driver_wait(delay)
            assert cls.wait_element_visible(delay + 1, CustomerPageLocators.CUSTOMER_ID_TEXT)
        finally:
            if cls.customer_page_url == cls.get_cur_url():
                return True
            else:
                return False
