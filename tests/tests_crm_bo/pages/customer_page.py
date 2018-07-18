from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators.customer_page_locators import CustomerPageLocators
from tests.tests_crm_bo.pages import customer_admin_url, customer_deposit_url, customer_balance_url


class CustomerPage(BasePage):
    def __init__(self):
        super(CustomerPage, self).__init__()
        self.locators = CustomerPageLocators()

    def go_to_inset_id(self, driver, locator, delay=1):
        deposit_inset = self.find_element_by(driver, locator, "id")
        self.click_on_element(deposit_inset)
        return self.driver_wait(driver, delay)

    def make_deposit(self, driver, delay=1, amount=100):
        try:
            assert customer_admin_url == self.get_cur_url(driver)
            self.go_to_inset_id(driver, self.locators.DEPOSIT_WITHDRAWALS_INSET_ID, delay)
            assert customer_deposit_url == self.get_cur_url(driver)
            add_deposit_button = self.find_element_by(driver, self.locators.ADD_DEPOSIT_BUTTON_ID, "id")
            self.click_on_element(add_deposit_button)
            self.wait_element_presented(driver, self.locators.NEW_DEPOSIT_POPUP, delay)
            payment_dropdown = self.find_element(driver, self.locators.PAYMENT_METHOD_DROPDOWN)
            self.click_on_element(payment_dropdown)
            self.driver_wait(driver, delay)
            payment_option = self.find_element(driver, self.locators.CREDIT_CARD_OPTION)
            self.click_on_element(payment_option)
            self.driver_wait(driver, delay)
            bin_number_field = self.find_element_by(driver, self.locators.BIN_CARD_NUMBER_FIELD_ID, "id")
            self.click_on_element(bin_number_field)
            self.driver_wait(driver, delay)
            self.send_keys(bin_number_field, BaseConfig.BIN_CARD_NUMBER)
            cc_field = self.find_element_by(driver, self.locators.CC_CARD_NUMBER_FIELD_ID, "id")
            self.click_on_element(cc_field)
            self.driver_wait(driver, delay)
            self.send_keys(cc_field, BaseConfig.CC_CARD_NUMBER)
            company_dropdown = self.find_element(driver, self.locators.CLEARING_COMPANY_DROPDOWN)
            self.click_on_element(company_dropdown)
            self.driver_wait(driver, delay)
            company_option = self.find_element(driver, self.locators.ALL_CHARGE_TRANS_OPTION)
            self.click_on_element(company_option)
            self.driver_wait(driver, delay)
            status_dropdown = self.find_element(driver, self.locators.TRANSACTION_STATUS_DROPDOWN)
            self.click_on_element(status_dropdown)
            self.driver_wait(driver, delay)
            status_option = self.find_element(driver, self.locators.STATUS_OPTION)
            self.click_on_element(status_option)
            self.driver_wait(driver, delay)
            currency_dropdown = self.find_element(driver, self.locators.CURRENCY_DROPDOWN)
            self.click_on_element(currency_dropdown)
            currency_option = self.find_element(driver, self.locators.CURRENCY_OPTION)
            self.click_on_element(currency_option)
            self.driver_wait(driver, delay)
            amount_field = self.find_element_by(driver, self.locators.AMOUNT_FIELD_ID, "id")
            self.send_keys(amount_field, amount)
            ref_number_field = self.find_element_by(driver, self.locators.REFERENCE_NUMBER_FIELD_ID, "id")
            self.send_keys(ref_number_field, amount)
            comments_field = self.find_element_by(driver, self.locators.COMMENTS_FIELD_ID, "id")
            self.send_keys(comments_field, amount)
            save_button = self.find_element_by(driver, self.locators.SAVE_BUTTON_ID, "id")
            self.click_on_element(save_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_presented(driver, self.locators.NEW_DEPOSIT_POPUP, delay) is None:
                return True
            else:
                return False

    def check_balance(self, driver, delay=+1):
        try:
            self.go_to_inset_id(driver, self.locators.BALANCE_INSET_ID, delay)
        finally:
            self.driver_wait(driver, delay)
            if customer_balance_url == self.get_cur_url(driver) is True:
                return True
            else:
                return False

    def check_customer_icon(self, driver):
        customer_icon = self.find_element_by(driver, self.locators.CUSTOMER_ICON_ID, "id")
        icon_attribute = self.get_attribute_from_element(customer_icon, "oldtitle")
        return icon_attribute
