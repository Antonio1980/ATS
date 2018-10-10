import random

from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators import home_page_locators
from tests.tests_crm_bo.locators import login_page_locators
from tests.tests_crm_bo.pages import login_page_url, new_password_url, home_page_url


class LogInPage(BasePage):
    def __init__(self):
        super().__init__()
        self.login_username = "admin"
        self.login_password = "password1"
        self.login_email = "roman@spotoption.com"
        self.locators = login_page_locators
        # data_file, row, column1, column2, column3
        self.account_details = Instruments.get_account_details(BaseConfig.WTP_TESTS_CUSTOMERS, 40, 0, 1, 2)
        self.email = self.account_details['email']
        self.password = self.account_details['password']
        self.username = self.account_details['customer_username']
        rows = Instruments.run_mysql_query("SELECT email, username FROM local_users WHERE status = 'Active' AND email LIKE '%@guerrillamailblock.com';")
        index = random.randrange(len(rows))
        self.forgotten_email = rows[index][0]
        self.forgotten_username = rows[index][1]
        self.email_text = "An email has been sent to {0} which is the email address for your account. " \
                          "It includes information on changing and confirming your new password. " \
                          "Please reset your password within the next 24 hours.".format(self.email)

    def go_to_login_page(self, driver, url):
        delay = 5
        self.go_to_url(driver, url)
        if self.wait_url_contains(driver, login_page_url, delay):
            return True
        else:
            return False

    def login(self, driver, username, password):
        delay = 5
        try:
            result = self.go_to_login_page(driver, self.crm_base_url)
            if result is True:
                username_field = self.find_element_by(driver, self.locators.USERNAME_FIELD_ID, "id")
                self.send_keys(username_field, username)
                password_field = self.find_element_by(driver, self.locators.PASSWORD_FIELD_ID, "id")
                self.send_keys(password_field, password)
                login_button = self.find_element_by(driver, self.locators.LOGIN_BUTTON_ID, "id")
                self.click_on_element(login_button)
        finally:
            if self.find_element_by(driver, home_page_locators.HOME_PAGE_LOGO_ID, "id") or self.wait_url_contains(driver, new_password_url, delay):
                return True
            else:
                return False

    def forgot_password(self, driver, email):
        delay = 5
        try:
            result = self.go_to_login_page(driver, self.crm_base_url)
            if result is True:
                forgot_password_link = self.wait_element_clickable(driver, self.locators.FORGOT_PASSWORD_LINK, delay)
                self.click_on_element(forgot_password_link)
                email_field = self.wait_element_clickable(driver, self.locators.POPUP_EMAIL_FIELD, delay)
                self.send_keys(email_field, email)
                send_button = self.find_element_by(driver, self.locators.POPUP_SEND_BUTTON_ID, "id")
                self.click_on_element(send_button)
        finally:
            if self.check_element_not_visible(driver, self.locators.POPUP_CHECK, delay + 3):
                if self.check_element_not_visible(driver, self.locators.POPUP_ERROR_MESSAGE_CLOSE_BUTTON, delay + 3):
                    self.click_on_element_by_locator(driver, self.locators.EMAIL_POPUP_CLOSE_BUTTON, delay + 3)
                    return True
                else:
                    return False
            else:
                return False

    def set_new_password(self, driver, password, new_password):
        delay = 5
        try:
            assert self.wait_url_contains(driver, new_password_url, delay)
            cur_password_field = self.find_element_by(driver, self.locators.CURRENT_PASSWORD_ID, "id")
            self.click_on_element(cur_password_field)
            self.send_keys(cur_password_field, password)
            new_password_field = self.find_element_by(driver, self.locators.NEW_PASSWORD_ID, "id")
            self.click_on_element(new_password_field)
            self.send_keys(new_password_field, new_password)
            confirm_password_field = self.find_element_by(driver, self.locators.CONFIRM_PASSWORD_ID, "id")
            self.click_on_element(confirm_password_field)
            self.send_keys(confirm_password_field, new_password)
            confirm_button = self.find_element(driver, self.locators.CONFIRM_BUTTON)
            self.click_on_element(confirm_button)
        finally:
            if self.wait_url_contains(driver, home_page_url, delay):
                return True
            else:
                return False

    def go_by_token_url(self, driver, _new_password_url):
        delay = 5
        if _new_password_url is not None:
            try:
                self.go_to_url(driver, _new_password_url)
            finally:
                if self.check_element_not_visible(driver, self.locators.PASSWORD_TOKEN_WARNING, delay + 5):
                    return True
                else:
                    return False
