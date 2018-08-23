from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators.customer_page_locators import CustomerPageLocators
from tests.tests_crm_bo.pages import customer_admin_url, customer_deposit_url, customer_balance_url


class CustomerPage(BasePage):
    def __init__(self):
        super(CustomerPage, self).__init__()
        self.locators = CustomerPageLocators()

    def go_to_inset_id(self, driver, locator):
        deposit_inset = self.find_element_by(driver, locator, "id")
        self.click_on_element(deposit_inset)

    def make_deposit(self, driver, payment_details):
        payment_option = payment_details['payment_option']
        company_option = payment_details['company_option']
        status_option = payment_details['status_option']
        currency_option = payment_details['currency_option']
        deposit_amount = payment_details['deposit_amount']
        delay = 5
        try:
            assert self.wait_url_contains(driver, customer_admin_url, delay)
            self.go_to_inset_id(driver, self.locators.DEPOSIT_WITHDRAWALS_INSET_ID)
            assert self.wait_url_contains(driver, customer_deposit_url, delay)
            add_deposit_button = self.search_element(driver, self.locators.ADD_DEPOSIT_BUTTON, delay)
            self.hover_over_element_and_click(driver, add_deposit_button)
            self.wait_element_presented(driver, self.locators.NEW_DEPOSIT_POPUP, delay)
            self.choose_option_from_dropdown(driver, self.locators.PAYMENT_METHOD_DROPDOWN,
                                             self.locators.PAYMENT_TEXT_INPUT, payment_option, delay-2)
            bin_number_field = self.find_element_by(driver, self.locators.BIN_CARD_NUMBER_FIELD_ID, "id")
            self.click_on_element(bin_number_field)
            self.send_keys(bin_number_field, BaseConfig.BIN_CARD_NUMBER)
            cc_field = self.find_element_by(driver, self.locators.CC_CARD_NUMBER_FIELD_ID, "id")
            self.click_on_element(cc_field)
            self.send_keys(cc_field, BaseConfig.CC_CARD_NUMBER)
            self.choose_option_from_dropdown(driver, self.locators.CLEARING_COMPANY_DROPDOWN,
                                             self.locators.CLEARING_TEXT_INPUT, company_option, delay-2)
            self.choose_option_from_dropdown(driver, self.locators.TRANSACTION_STATUS_DROPDOWN,
                                             self.locators.STATUS_TEXT_INPUT, status_option, delay-2)
            self.choose_option_from_dropdown(driver, self.locators.CURRENCY_DROPDOWN,
                                             self.locators.CURRENCY_TEXT_INPUT, currency_option, delay-2)
            amount_field = self.find_element_by(driver, self.locators.AMOUNT_FIELD_ID, "id")
            self.send_keys(amount_field, deposit_amount)
            ref_number_field = self.find_element_by(driver, self.locators.REFERENCE_NUMBER_FIELD_ID, "id")
            self.send_keys(ref_number_field, deposit_amount)
            comments_field = self.find_element_by(driver, self.locators.COMMENTS_FIELD_ID, "id")
            self.send_keys(comments_field, "QA_test_QA")
            save_button = self.find_element_by(driver, self.locators.SAVE_BUTTON_ID, "id")
            self.click_on_element(save_button)
        finally:
            if self.check_element_not_presented(driver, self.locators.NEW_DEPOSIT_POPUP, delay):
                return True
            else:
                return False

    def check_balance(self, driver):
        delay = 3
        try:
            self.go_to_inset_id(driver, self.locators.BALANCE_INSET_ID)
        finally:
            if self.wait_url_contains(driver, customer_balance_url, delay):
                return True
            else:
                return False

    def check_customer_icon(self, driver):
        customer_icon = self.find_element_by(driver, self.locators.CUSTOMER_ICON_ID, "id")
        icon_attribute = self.get_attribute_from_element(customer_icon, "oldtitle")
        return icon_attribute
