from src.base.instruments import Instruments
from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators
from tests.tests_web_platform.pages import wtp_signin_page_url, forgot_password_page_url, wtp_dashboard_url, \
    user_page_url, logged_user_page_url


class SignInPage(BasePage):
    def __init__(self):
        super(SignInPage, self).__init__()
        self.locators = SignInPageLocators()
        rows = Instruments.run_mysql_query("SELECT email FROM customers WHERE status = 2 AND email LIKE '%guerrillamailblock%';")
        self.email = rows[1][0]
        self.username = self.email.split('@')[0]
        self.password = '1Aa@<>12'

    def sign_in(self, driver, email, password):
        delay = 5
        try:
            if self.wait_url_contains(driver, user_page_url, delay) or self.wait_url_contains(driver, logged_user_page_url, delay):
                username_field = self.find_element(driver, self.locators.USERNAME_FIELD)
                self.click_on_element(username_field)
                self.send_keys(username_field, email)
                password_field_true = self.find_element(driver, self.locators.PASSWORD_FIELD_TRUE)
                password_field = self.find_element(driver, self.locators.PASSWORD_FIELD)
                self.click_on_element(password_field)
                self.click_on_element(password_field_true)
                self.send_keys(password_field_true, password)
                self.execute_js(driver, self.script_login)
                login_button = self.wait_element_clickable(driver, self.locators.SIGNIN_BUTTON, delay)
                self.click_on_element(login_button)
        finally:
            if self.wait_url_contains(driver, wtp_dashboard_url, delay):
                return True
            else:
                return False

    def click_on_link(self, driver, option, delay=+3):
        # Option 1- forgot password, Option 2- register link
        try:
            assert self.wait_url_contains(driver, wtp_signin_page_url, delay)
            if option == 1:
                link = self.find_element(driver, self.locators.FORGOT_PASSWORD_LINK)
            else:
                link = self.find_element(driver, self.locators.REGISTER_LINK)
            self.click_on_element(link)
        finally:
            if option == 1:
                if self.wait_url_contains(driver, forgot_password_page_url, delay):
                    return True
                else:
                    return False
            else:
                if self.wait_url_contains(driver, self.wtp_open_account_url, delay):
                    return True
                else:
                    return False

    def go_by_token_url(self, driver, url):
        delay = 5
        if url is not None:
            try:
                self.go_to_url(driver, url)
            finally:
                if self.wait_element_clickable(driver, self.locators.SIGNIN_BUTTON, delay + 5):
                    return True
                else:
                    return False
