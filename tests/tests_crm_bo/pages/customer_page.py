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

    def make_deposit(self, driver, amount=100):
        delay = 5
        try:
            assert self.get_cur_url(driver) == customer_admin_url
            self.go_to_inset_id(driver, self.locators.DEPOSIT_WITHDRAWALS_INSET_ID)
            assert customer_deposit_url == self.get_cur_url(driver)
            add_deposit_button = self.find_element_by(driver, self.locators.ADD_DEPOSIT_BUTTON_ID, "id")
            self.click_on_element(add_deposit_button)
            self.wait_element_presented(driver, self.locators.NEW_DEPOSIT_POPUP, delay)
            payment_dropdown = self.find_element(driver, self.locators.PAYMENT_METHOD_DROPDOWN)
            self.click_on_element(payment_dropdown)
            payment_option = self.find_element(driver, self.locators.CREDIT_CARD_OPTION)
            self.click_on_element(payment_option)
            bin_number_field = self.find_element_by(driver, self.locators.BIN_CARD_NUMBER_FIELD_ID, "id")
            self.click_on_element(bin_number_field)
            self.send_keys(bin_number_field, self.BIN_CARD_NUMBER)
            cc_field = self.find_element_by(driver, self.locators.CC_CARD_NUMBER_FIELD_ID, "id")
            self.click_on_element(cc_field)
            self.send_keys(cc_field, self.CC_CARD_NUMBER)
            company_dropdown = self.find_element(driver, self.locators.CLEARING_COMPANY_DROPDOWN)
            self.click_on_element(company_dropdown)
            company_option = self.find_element(driver, self.locators.ALL_CHARGE_TRANS_OPTION)
            self.click_on_element(company_option)
            status_dropdown = self.find_element(driver, self.locators.TRANSACTION_STATUS_DROPDOWN)
            self.click_on_element(status_dropdown)
            status_option = self.find_element(driver, self.locators.STATUS_OPTION)
            self.click_on_element(status_option)
            currency_dropdown = self.find_element(driver, self.locators.CURRENCY_DROPDOWN)
            self.click_on_element(currency_dropdown)
            currency_option = self.find_element(driver, self.locators.CURRENCY_OPTION)
            self.click_on_element(currency_option)
            amount_field = self.find_element_by(driver, self.locators.AMOUNT_FIELD_ID, "id")
            self.send_keys(amount_field, amount)
            ref_number_field = self.find_element_by(driver, self.locators.REFERENCE_NUMBER_FIELD_ID, "id")
            self.send_keys(ref_number_field, amount)
            comments_field = self.find_element_by(driver, self.locators.COMMENTS_FIELD_ID, "id")
            self.send_keys(comments_field, amount)
            save_button = self.find_element_by(driver, self.locators.SAVE_BUTTON_ID, "id")
            self.click_on_element(save_button)
        finally:
            if self.wait_element_presented(driver, self.locators.NEW_DEPOSIT_POPUP, delay) is None:
                return True
            else:
                return False

    def check_balance(self, driver):
        delay = 3
        try:
            self.go_to_inset_id(driver, self.locators.BALANCE_INSET_ID)
        finally:
            cur_url = self.get_cur_url(driver)
            if customer_balance_url == cur_url:
                return True
            else:
                return False

    def check_customer_icon(self, driver):
        customer_icon = self.find_element_by(driver, self.locators.CUSTOMER_ICON_ID, "id")
        icon_attribute = self.get_attribute_from_element(customer_icon, "oldtitle")
        return icon_attribute
