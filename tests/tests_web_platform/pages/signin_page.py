from src.base.base_exception import AutomationError
from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators import signin_page_locators
from tests.tests_web_platform.pages import wtp_signin_page_url, forgot_password_page_url, wtp_dashboard_url, \
    wtp_open_account_url


class SignInPage(BasePage):
    def __init__(self):
        super(SignInPage, self).__init__()
        self.locators = signin_page_locators

    def sign_in(self, driver, email, password):
        delay = 5
        try:
            username_field = self.search_element(driver, self.locators.USERNAME_FIELD, delay)
            self.click_on_element(username_field)
            self.send_keys(username_field, email)
            password_field_true = self.find_element(driver, self.locators.PASSWORD_FIELD_TRUE)
            password_field = self.find_element(driver, self.locators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.click_on_element(password_field_true)
            self.send_keys(password_field_true, password)
            self.execute_js(driver, self.script_signin)
            keep_me_checkbox = self.find_element(driver, self.locators.KEEP_ME_CHECKBOX)
            self.click_on_element(keep_me_checkbox)
            login_button = self.wait_element_clickable(driver, self.locators.SIGNIN_BUTTON, delay)
            self.execute_js(driver, self.script_test_token)
            self.click_on_element(login_button)
            return self.wait_url_contains(driver, wtp_dashboard_url, delay)
        except AutomationError as e:
            print("{0} sign_in failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def click_on_link(self, driver, option, delay):
        delay =+ delay
        # Option 1- forgot password, Option 2- register link
        try:
            self.wait_url_contains(driver, wtp_signin_page_url, delay)
            if option == 1:
                link = self.search_element(driver, self.locators.FORGOT_PASSWORD_LINK, delay)
            else:
                link = self.search_element(driver, self.locators.REGISTER_LINK, delay)
            self.click_on_element(link)
            if option == 1:
                return self.wait_url_contains(driver, forgot_password_page_url, delay)
            else:
                return self.wait_url_contains(driver, wtp_open_account_url, delay)
        except AutomationError as e:
            print("{0} click_on_link failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def go_by_token_url(self, driver, url):
        delay = 5
        try:
            self.go_to_url(driver, url)
            if self.wait_element_clickable(driver, self.locators.SIGNIN_BUTTON, delay + 5) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} go_by_token_url failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False
