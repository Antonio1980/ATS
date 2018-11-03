from src.base.base_exception import AutomationError
from tests.tests_web_platform.locators import forgot_password_page_locators
from tests.tests_web_platform.pages import BasePage, forgot_password_page_url, wtp_dashboard_url, wtp_open_account_url


class ForgotPasswordPage(BasePage):
    def __init__(self):
        super(ForgotPasswordPage, self).__init__()
        self.locators = forgot_password_page_locators

    def fill_email_address_form(self, driver, email, delay):
        try:
            assert self.wait_url_contains(driver, forgot_password_page_url, delay)
            email_field = self.search_element(driver, self.locators.EMAIL_TEXT_FIELD, delay)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            self.execute_js(driver, self.script_forgot)
            self.execute_js(driver, self.script_test_token)
            submit_button = self.wait_element_clickable(driver, self.locators.SUBMIT_BUTTON, delay)
            self.try_click(driver, submit_button, delay - 3)
            if self.wait_element_presented(driver, self.locators.MESSAGE, delay) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} fill_email_address_form failed with error {0}".format(e.__class__.__name__, e.__cause__))
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
            try:
                self.wait_element_clickable(driver, self.locators.CONTINUE_BUTTON, delay)
                flag = True
                continue_button = self.search_element(driver, self.locators.CONTINUE_BUTTON, delay)
                self.click_on_element(continue_button)
            except AutomationError as e:
                print("{0} set_new_password failed with error: {1}".format(e.__class__.__name__, e.__cause__))
                return False
        finally:
            if flag is True:
                return self.wait_url_contains(driver, wtp_dashboard_url, delay) or self.wait_url_contains(
                    driver, wtp_open_account_url, delay)

    def go_by_token_url(self, driver, url):
        delay = 5
        try:
            self.go_to_url(driver, url)
            if self.wait_element_clickable(driver, self.locators.CONFIRM_BUTTON, delay + 5) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} go_by_token_url failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False
