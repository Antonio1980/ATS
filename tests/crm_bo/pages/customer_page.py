# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.test_definitions import BaseConfig
from tests.crm_bo.pages.base_page import BasePage
from tests.crm_bo.locators.customer_page_locators import CustomerPageLocators


class CustomerPage(BasePage):
    @classmethod
    def setup_customer_page(cls):
        cls.setup_base_page()
        cls.self_url = cls.base_url + "customers/page/"
        cls.customer_admin_url = cls.self_url + "{0}#customer_admin_status".format(BaseConfig.CRM_CUSTOMER_ID)
        cls.customer_deposit_url = cls.self_url + "{0}#customer_dw".format(BaseConfig.CRM_CUSTOMER_ID)
        cls.customer_balance_url = cls.self_url + "{0}#customer_balance".format(BaseConfig.CRM_CUSTOMER_ID)

    @classmethod
    def go_to_inset_id(cls, locator, delay=1):
        deposit_inset = cls.find_element_by(locator, "id")
        cls.click_on_element(deposit_inset)
        return cls.driver_wait(delay)

    @classmethod
    def make_deposit(cls, delay=1, amount=100):
        try:
            assert cls.customer_admin_url == cls.get_cur_url()
            cls.go_to_inset_id(CustomerPageLocators.DEPOSIT_WITHDRAWALS_INSET_ID, delay)
            assert cls.customer_deposit_url == cls.get_cur_url()
            add_deposit_button = cls.find_element_by(CustomerPageLocators.ADD_DEPOSIT_BUTTON_ID, "id")
            cls.click_on_element(add_deposit_button)
            cls.wait_element_presented(delay, CustomerPageLocators.NEW_DEPOSIT_POPUP)
            #new_deposit_popup_title = cls.find_element_by(CustomerPageLocators.NEW_DEPOSIT_POPUP_TITLE_ID, "id")
            payment_dropdown = cls.find_element(CustomerPageLocators.PAYMENT_METHOD_DROPDOWN)
            cls.click_on_element(payment_dropdown)
            cls.driver_wait(delay)
            payment_option = cls.find_element(CustomerPageLocators.CREDIT_CARD_OPTION)
            cls.click_on_element(payment_option)
            cls.driver_wait(delay)
            bin_number_field = cls.find_element_by(CustomerPageLocators.BIN_CARD_NUMBER_FIELD_ID, "id")
            cls.click_on_element(bin_number_field)
            cls.driver_wait(delay)
            cls.send_keys(bin_number_field, BaseConfig.BIN_CARD_NUMBER)
            cc_field = cls.find_element_by(CustomerPageLocators.CC_CARD_NUMBER_FIELD_ID, "id")
            cls.click_on_element(cc_field)
            cls.driver_wait(delay)
            cls.send_keys(cc_field, BaseConfig.CC_CARD_NUMBER)
            company_dropdown = cls.find_element(CustomerPageLocators.CLEARING_COMPANY_DROPDOWN)
            cls.click_on_element(company_dropdown)
            cls.driver_wait(delay)
            company_option = cls.find_element(CustomerPageLocators.ALL_CHARGE_TRANS_OPTION)
            cls.click_on_element(company_option)
            cls.driver_wait(delay)
            status_dropdown = cls.find_element(CustomerPageLocators.TRANSACTION_STATUS_DROPDOWN)
            cls.click_on_element(status_dropdown)
            cls.driver_wait(delay)
            status_option = cls.find_element(CustomerPageLocators.STATUS_OPTION)
            cls.click_on_element(status_option)
            cls.driver_wait(delay)
            currency_dropdown = cls.find_element(CustomerPageLocators.CURRENCY_DROPDOWN)
            cls.click_on_element(currency_dropdown)
            currency_option = cls.find_element(CustomerPageLocators.CURRENCY_OPTION)
            cls.click_on_element(currency_option)
            cls.driver_wait(delay)
            amount_field = cls.find_element_by(CustomerPageLocators.AMOUNT_FIELD_ID, "id")
            cls.send_keys(amount_field, amount)
            ref_number_field = cls.find_element_by(CustomerPageLocators.REFERENCE_NUMBER_FIELD_ID, "id")
            cls.send_keys(ref_number_field, amount)
            comments_field = cls.find_element_by(CustomerPageLocators.COMMENTS_FIELD_ID, "id")
            cls.send_keys(comments_field, amount)
            save_button = cls.find_element_by(CustomerPageLocators.SAVE_BUTTON_ID, "id")
            cls.click_on_element(save_button)
            cls.driver_wait(delay)
        finally:
            cls.driver_wait(delay)
            if cls.wait_element_presented(delay, CustomerPageLocators.NEW_DEPOSIT_POPUP) is None:
                return True
            else:
                return False

    @classmethod
    def check_balance(cls, delay=1):
        try:
            cls.go_to_inset_id(CustomerPageLocators.BALANCE_INSET_ID, delay)
        finally:
            cls.driver_wait(delay)
            if cls.customer_balance_url == cls.get_cur_url() is True:
                return True
            else:
                return False

    @classmethod
    def check_customer_icon(cls):
        customer_icon = cls.find_element_by(CustomerPageLocators.CUSTOMER_ICON_ID, "by")
        icon_attribute = cls.get_attribute_from_element(customer_icon, "oldtitle")
        return icon_attribute
