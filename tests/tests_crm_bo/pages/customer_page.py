from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators import customer_page_locators
from tests.tests_crm_bo.pages import customer_admin_url, customer_deposit_url, customer_balance_url


class CustomerPage(BasePage):
    def __init__(self):
        super().__init__()
        self.locators = customer_page_locators

    def go_to_inset_id(self, driver, locator):
        deposit_inset = self.find_element_by(driver, locator, "id")
        self.click_on_element(deposit_inset)

    def make_deposit(self, driver):
        delay = 5
        try:
            assert self.wait_url_contains(driver, customer_admin_url, delay)
            self.go_to_inset_id(driver, self.locators.DEPOSIT_WITHDRAWALS_INSET_ID)
            assert self.wait_url_contains(driver, customer_deposit_url, delay)
            add_deposit_button = self.search_element(driver, self.locators.ADD_DEPOSIT_BUTTON, delay)
            self.hover_over_element_and_click(driver, add_deposit_button)
            self.wait_element_presented(driver, self.locators.NEW_DEPOSIT_POPUP, delay)
            payment_method_dropdown = self.search_element(driver, self.locators.PAYMENT_METHOD_DROPDOWN, delay)
            self.click_on_element(payment_method_dropdown)
            payment_input = self.find_element(driver, self.locators.PAYMENT_TEXT_INPUT)
            self.input_data(payment_input, "Wire Transfer")
            status_dropdown = self.find_element(driver, self.locators.TRANSACTION_STATUS_DROPDOWN)
            self.click_on_element(status_dropdown)
            status_input = self.find_element(driver, self.locators.STATUS_TEXT_INPUT)
            self.input_data(status_input, "Approved")
            currency_dropdown = self.find_element(driver, self.locators.CURRENCY_DROPDOWN)
            self.click_on_element(currency_dropdown)
            currency_input = self.find_element(driver, self.locators.CURRENCY_TEXT_INPUT)
            self.input_data(currency_input, "USD")
            amount_input = self.find_element_by(driver, self.locators.AMOUNT_FIELD_ID, "id")
            self.input_data(amount_input, "100")
            reference_number_input = self.find_element_by(driver, self.locators.REFERENCE_NUMBER_FIELD_ID, "id")
            self.input_data(reference_number_input, "8930405")
            comments_input = self.find_element_by(driver, self.locators.COMMENTS_FIELD_ID, "id")
            self.input_data(comments_input, "Hello World")
            value_data = self.find_element_by(driver, self.locators.VALUE_DATA_ID, "id")
            self.input_data(value_data, "2020-03-01")
            name_on_bank_account = self.find_element_by(driver, self.locators.NAME_ON_BANK_ACCOUNT_FIELD_ID, "id")
            self.input_data(name_on_bank_account, "FGFGFG HJHJH")
            iban = self.find_element_by(driver, self.locators.IBAN_FIELD_ID, "id")
            self.input_data(iban, "CH56048350123477778009")
            bank_name = self.find_element_by(driver, self.locators.BANK_NAME_FIELD_ID, "id")
            self.input_data(bank_name, "LIMUKJJHH")
            bic = self.find_element_by(driver, self.locators.BIC_FIELD_ID, "id")
            self.input_data(bic, "WHYTHJHA")
            bank_address = self.find_element_by(driver, self.locators.BANK_ADDRESS_ID, "id")
            self.input_data(bank_address, "7678687   khjhjkhkj jh8hkjhkjh")
            description_by_customer = self.find_element_by(driver, self.locators.DESCRIPTION_BY_CUSTOMER_ID, "id")
            self.input_data(description_by_customer, "iuewj,d  ekc;oli; lkkjkjsdfoidsmdl  fdklfks;kfsdf fsd")
            #wallet_address = self.find_element_by(driver, self.locators.WALLET_ADDRESS_ID, "id")
            #self.input_data(wallet_address, "uy454yu4yh45uy5h4hb54h")
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

    def check_depositor_icon(self, driver):
        depositor_icon = self.find_element_by(driver, self.locators.DEPOSITOR_ICON_ID, "id")
        icon_attribute = self.get_attribute_from_element(depositor_icon, "oldtitle")
        return icon_attribute
