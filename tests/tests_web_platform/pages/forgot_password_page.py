import time

from src.base.instruments import get_account_details
from tests.tests_web_platform.pages import BasePage, forgot_password_page_url, wtp_dashboard_url
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators


class ForgotPasswordPage(BasePage):
    def __init__(self):
        super(ForgotPasswordPage, self).__init__()
        self.locators = ForgotPasswordPageLocators()
        # 1- Data file, 2- Row, 3- First column, 4- Second column, 5- Third column
        self.account_details = get_account_details(self.WTP_TESTS_CUSTOMERS, 16, 0, 1, 2)
        self.first_last_name = self.account_details['customer_username']
        self.email = self.account_details['email']
        self.password = self.account_details['password']

    def fill_email_address_form(self, driver, email, delay=+1):
        try:
            assert forgot_password_page_url == self.get_cur_url(driver)
            email_field = self.find_element(driver, self.locators.EMAIL_TEXT_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            self.wait_element_presented(driver, self.locators.CAPTCHA, delay + 5)
            self.execute_js(driver, self.script_forgot)
            submit_button = self.wait_element_clickable(driver, self.locators.SUBMIT_BUTTON, delay + 5)
            self.click_with_offset(driver, submit_button, 10, 20)
        finally:
            if self.wait_element_presented(driver, self.locators.MESSAGE, delay + 5):
                return True
            else:
                return False

    def set_new_password(self, driver, password, new_password_url):
        delay, flag = 5, False
        try:
            time.sleep(3)
            assert self.get_cur_url(driver) == new_password_url
            password_field = self.find_element(driver, self.locators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_field, password)
            confirm_password_field = self.find_element(driver, self.locators.CONFIRM_PASSWORD_FIELD)
            self.click_on_element(confirm_password_field)
            self.send_keys(confirm_password_field, password)
            assert self.wait_element_presented(driver, self.locators.PASSWORD_ERROR, delay)
            assert self.wait_element_presented(driver, self.locators.CONFIRM_PASSWORD_ERROR, delay)
            confirm_button = self.search_element(driver, self.locators.CONFIRM_BUTTON, delay)
            self.click_with_offset(driver, confirm_button, 10, 20)
            if self.wait_element_clickable(driver, self.locators.CONTINUE_BUTTON, delay):
                flag = True
                continue_button = self.search_element(driver, self.locators.CONTINUE_BUTTON, delay)
                self.click_on_element(continue_button)
        finally:
            if flag is True and self.get_cur_url(driver) == wtp_dashboard_url:
                return True
            else:
                return False
