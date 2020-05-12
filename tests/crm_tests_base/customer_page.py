import time
from src.base import logger
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.base_page import BasePage
from selenium.webdriver.remote.webelement import WebElement
from tests.crm_tests_base.locators import customer_page_locators
from tests.crm_tests_base import customer_balance_url


class CustomerPage(BasePage):

    def __init__(self):
        super(CustomerPage, self).__init__()
        self.locators = customer_page_locators

    @automation_logger(logger)
    def go_to_inset_id(self, driver, locator):
        deposit_inset = self.find_element_by(driver, locator, "id")
        self.click_on_element(deposit_inset)

    @automation_logger(logger)
    def make_deposit(self, driver, currency_name, amount, status):
        try:
            self.go_to_inset_id(driver, self.locators.DEPOSIT_WITHDRAWALS_INSET_ID)
            time.sleep(2.0)
            add_deposit_button = self.search_element(driver, self.locators.ADD_DEPOSIT_BUTTON, self.ui_delay)
            self.hover_over_element_and_click(driver, add_deposit_button)
            self.wait_element_presented(driver, self.locators.NEW_DEPOSIT_POPUP, self.ui_delay)
            payment_method_dropdown = self.search_element(driver, self.locators.PAYMENT_METHOD_DROPDOWN, self.ui_delay)
            self.click_on_element(payment_method_dropdown)
            payment_input = self.find_element(driver, self.locators.PAYMENT_TEXT_INPUT)
            self.input_data(payment_input, "Wire Transfer")
            status_dropdown = self.find_element(driver, self.locators.TRANSACTION_STATUS_DROPDOWN)
            self.click_on_element(status_dropdown)
            status_input = self.find_element(driver, self.locators.STATUS_TEXT_INPUT)
            self.input_data(status_input, status)
            currency_dropdown = self.find_element(driver, self.locators.CURRENCY_DROPDOWN)
            self.click_on_element(currency_dropdown)
            currency_input = self.find_element(driver, self.locators.CURRENCY_TEXT_INPUT)
            self.input_data(currency_input, currency_name)
            amount_input = self.find_element_by(driver, self.locators.AMOUNT_FIELD_ID, "id")
            self.input_data(amount_input, str(amount))
            reference_number_input = self.find_element_by(driver, self.locators.REFERENCE_NUMBER_FIELD_ID, "id")
            self.input_data(reference_number_input, "8930405")
            comments_input = self.find_element_by(driver, self.locators.COMMENTS_FIELD_ID, "id")
            self.input_data(comments_input, "Hello World")
            if status == "Approved":
                value_data = self.find_element_by(driver, self.locators.VALUE_DATA_ID, "id")
                self.input_data(value_data, "2020-03-01")
            name_on_bank_account = self.find_element_by(driver, self.locators.NAME_ON_BANK_ACCOUNT_FIELD_ID, "id")
            self.input_data(name_on_bank_account, "FGFGFG HJHJH")
            iban = self.find_element_by(driver, self.locators.IBAN_FIELD_ID, "id")
            self.input_data(iban, "CH56048350123477778009")
            bank_name = self.find_element_by(driver, self.locators.BANK_NAME_FIELD_ID, "id")
            self.input_data(bank_name, "LIMUKJJHH")
            bic = self.find_element_by(driver, self.locators.BIC_FIELD_ID, "id")
            self.input_data(bic, "KJKKGHGHGHG")
            bank_address = self.find_element_by(driver, self.locators.BANK_ADDRESS_ID, "id")
            self.input_data(bank_address, "7678687   khjhjkhkj jh8hkjhkjh")
            description_by_customer = self.find_element_by(driver, self.locators.DESCRIPTION_BY_CUSTOMER_ID, "id")
            self.input_data(description_by_customer, "iuewj,d  ekc;oli; lkkjkjsdfoidsmdl  fdklfks;kfsdf fsd")
            save_button = self.find_element_by(driver, self.locators.SAVE_BUTTON_ID, "id")
            self.click_on_element(save_button)
            if isinstance(self.check_element_not_presented(driver, self.locators.NEW_DEPOSIT_POPUP, self.ui_delay),
                          WebElement):
                return False
            else:
                return True
        except Exception as e:
            logger.logger.error("{0} make_deposit failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    @automation_logger(logger)
    def go_to_balance_inset(self, driver):
        try:
            self.go_to_inset_id(driver, self.locators.BALANCE_INSET_ID)
            return self.wait_url_contains(driver, customer_balance_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} check_balance failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    @automation_logger(logger)
    def check_icon(self, driver, locator):
        icon = self.find_element(driver, locator)
        icon_attribute = self.get_attribute_from_element(icon, "data-original-title")
        return icon_attribute

    @automation_logger(logger)
    def get_all_deposits_id_from_deposits_result(self, all_id):
        id_list = []
        for i in all_id:
            deposit_id = i.get_attribute('innerText')
            id_list.append(deposit_id)
        return id_list

    @automation_logger(logger)
    def get_customer_id_from_customer_page(self, driver):
        customer_id = self.get_attribute_from_locator(driver, self.locators.CUSTOMER_ID_TEXT, 'innerText')
        assert 'Customer ID' in customer_id
        return customer_id.split(' ')[-1]
