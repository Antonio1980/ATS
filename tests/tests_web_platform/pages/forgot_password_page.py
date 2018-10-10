from src.base.instruments import Instruments
from tests.tests_web_platform.locators import forgot_password_page_locators
from tests.tests_web_platform.pages import BasePage, forgot_password_page_url, wtp_dashboard_url


class ForgotPasswordPage(BasePage):
    def __init__(self):
        super().__init__()
        self.password = "1Aa@<>12"
        self.locators = forgot_password_page_locators
        self.first_last_name = Instruments.generate_user_first_last_name()
        self.guerrilla_email = \
            Instruments.run_mysql_query("SELECT email FROM customers WHERE email LIKE '%@guerrillamail%' AND status=2;")[0]
        self.mailinator_email = \
            Instruments.run_mysql_query("SELECT email FROM customers WHERE email LIKE '%@mailinator.com%' AND status=2;")[0]

    def fill_email_address_form(self, driver, email, delay=+1):
        try:
            assert self.wait_url_contains(driver, forgot_password_page_url, delay + 3)
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
            assert self.wait_url_contains(driver, new_password_url, delay)
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
            if flag is True and self.wait_url_contains(driver, wtp_dashboard_url, delay) or \
                    self.wait_url_contains(driver, self.wtp_open_account_url + "?lang=en", delay):
                return True
            else:
                return False

    def go_by_token_url(self, driver, url):
        delay = 5
        if url is not None:
            try:
                self.go_to_url(driver, url)
            finally:
                if self.wait_element_clickable(driver, self.locators.CONFIRM_BUTTON, delay + 5):
                    return True
                else:
                    return False
