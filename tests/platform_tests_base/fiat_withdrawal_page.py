from src.base import logger
from tests.platform_tests_base.base_page import BasePage
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.locators import fiat_withdrawal_locators


class FiatWithdrawalPage(BasePage):

    def __init__(self):
        super(FiatWithdrawalPage, self).__init__()
        self.locators = fiat_withdrawal_locators

    @automation_logger(logger)
    def withdrawal_input_data(self, driver, amount):
        try:
            input_withdrawal_amount = self.wait_element_presented(driver, self.locators.INPUT_WITHDRAWAL_AMOUNT, self.ui_delay)
            self.input_data(input_withdrawal_amount, amount)
            description = self.wait_element_presented(driver, self.locators.INPUT_DESCRIPTION, self.ui_delay)
            self.send_keys(description, "Withdrawal of EUR")
            name_on_account = self.wait_element_presented(driver, self.locators.INPUT_NAME_ON_ACCOUNT_INPUT, self.ui_delay)
            self.send_keys(name_on_account, "Name Name")
            iban = self.wait_element_presented(driver, self.locators.INPUT_IBAN, self.ui_delay)
            self.send_keys(iban, "CH56048350123477778009")
            bank_name = self.wait_element_presented(driver, self.locators.INPUT_BANK_NAME, self.ui_delay)
            self.send_keys(bank_name, "Sberbank")
            bic = self.wait_element_presented(driver, self.locators.INPUT_BIC, self.ui_delay)
            self.send_keys(bic, "WHYTHJHA")
            address = self.wait_element_presented(driver, self.locators.INPUT_ADDRESS, self.ui_delay)
            self.send_keys(address, "Israel, Tel Aviv")
            submit_button = self.wait_element_presented(driver, self.locators.SUBMIT_BUTTON_WITHDRAWAL, self.ui_delay)
            a = self.find_elements(driver, self.locators.LIST_OF_ERRORS_IF_NO_INPUT_FOR_WITHDRAWAL)
            b = []
            if isinstance(a, list) and a == b:
                self.click_on_element(submit_button)
                return True
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} withdrawal input failed with error: {1}".format(e.__class__.__name__,
                                                                                           e.__cause__), e)
            return False
