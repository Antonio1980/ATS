from test_definitions import BaseConfig
from src.base.engine import get_account_details
from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.signin_page_locators import SignInPageLocators
from tests.tests_web_platform.pages import wtp_login_page_url, forgot_password_page_url, wtp_dashboard_url


class SignInPage(BasePage):
    def __init__(self):
        super(SignInPage, self).__init__()
        self.locators = SignInPageLocators()
        # 1- Data file, 2- Row, 3- First column, 4- Second column, 5- Third column
        self.account_details = get_account_details(BaseConfig.WTP_TESTS_CUSTOMERS, 0, 0, 1, 2)
        self.first_last_name = self.account_details['firstname']
        self.email = self.account_details['email']
        self.password = self.account_details['password']

    def login(self, driver, email, password):
        delay = 1
        try:
            self.wait_driver(driver, delay + 3)
            assert wtp_login_page_url == self.get_cur_url(driver)
            username_field = self.find_element(driver, self.locators.USERNAME_FIELD)
            self.click_on_element(username_field)
            self.send_keys(username_field, email)
            password_true_field = self.find_element(driver, self.locators.PASSWORD_TRUE_FIELD)
            password_field = self.find_element(driver, self.locators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_true_field, password)
            self.driver_wait(driver, delay + 5)
            self.execute_js(driver, self.script_login)
            login_button = self.find_element(driver, self.locators.SIGNIN_BUTTON)
            self.click_on_element(login_button)
            self.driver_wait(driver, delay + 3)
        finally:
            if self.get_cur_url(driver) == wtp_dashboard_url:
                return True
            else:
                return False

    def click_on_link(self, driver, option, delay=1):
        # Option 1- forgot password, Option 2- register link
        try:
            self.wait_driver(driver, delay)
            assert wtp_login_page_url == self.get_cur_url(driver)
            if option == 1:
                link = self.find_element(driver, self.locators.FORGOT_PASSWORD_LINK)
            else:
                link = self.find_element(driver, self.locators.REGISTER_LINK)
            self.click_on_element(link)
            self.driver_wait(driver, delay + 3)
        finally:
            if option == 1:
                if self.get_cur_url(driver) == forgot_password_page_url:
                    return True
                else:
                    return False
            else:
                if self.get_cur_url(driver) == self.wtp_open_account_url:
                    return True
                else:
                    return False
