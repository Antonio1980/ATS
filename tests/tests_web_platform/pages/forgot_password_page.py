from test_definitions import BaseConfig
from src.base.engine import get_account_details
from tests.tests_web_platform.pages import BasePage, forgot_password_page_url, wtp_dashboard_url
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators


class ForgotPasswordPage(BasePage):
    def __init__(self):
        super(ForgotPasswordPage, self).__init__()
        self.locators = ForgotPasswordPageLocators()
        # 1- Data file, 2- Row, 3- First column, 4- Second column, 5- Third column
        self.account_details = get_account_details(BaseConfig.WTP_TESTS_CUSTOMERS, 0, 0, 1, 2)
        self.first_last_name = self.account_details['firstname']
        self.email = self.account_details['email']
        self.password = self.account_details['password']

    def fill_email_address_form(self, driver, email, delay=+1):
        try:
            self.driver_wait(driver, delay)
            assert forgot_password_page_url == self.get_cur_url(driver)
            email_field = self.find_element(driver, self.locators.EMAIL_TEXT_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            self.wait_driver(driver, delay + 3)
            self.execute_js(driver, self.script_forgot)
            submit_button = self.find_element(driver, self.locators.SUBMIT_BUTTON)
            self.wait_driver(driver, delay + 5)
            self.click_on_element(submit_button)
            self.wait_driver(driver, delay + 5)
        finally:
            if not self.wait_element_clickable(driver, self.locators.SUBMIT_BUTTON, delay):
                return True
            else:
                return False

    def set_new_password(self, driver, password, new_password_url):
        delay, flag = 5, False
        try:
            self.driver_wait(driver, delay)
            assert self.get_cur_url(driver) == new_password_url
            password_field = self.find_element(driver, self.locators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_field, password)
            confirm_password_field = self.find_element(driver, self.locators.CONFIRM_PASSWORD_FIELD)
            self.click_on_element(confirm_password_field)
            self.send_keys(confirm_password_field, password)
            assert self.check_element_not_visible(driver, self.locators.PASSWORD_ERROR, delay)
            assert self.check_element_not_visible(driver, self.locators.CONFIRM_PASSWORD_ERROR, delay)
            confirm_button = self.find_element(driver, self.locators.CONFIRM_BUTTON)
            self.click_on_element(confirm_button)
            self.wait_driver(driver, delay + 5)
            if self.wait_element_presented(driver, self.locators.CONTINUE_BUTTON, delay):
                flag = True
                continue_button = self.find_element(driver, self.locators.CONTINUE_BUTTON)
                self.click_on_element(continue_button)
                self.driver_wait(driver, delay)
        finally:
            if flag is True and self.get_cur_url(driver) == wtp_dashboard_url:
                return True
            else:
                return False
