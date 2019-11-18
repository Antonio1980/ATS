from tests.me_tests_base.base_page import BasePage
from tests.me_tests_base.locators.home_page_locators import *
from tests.me_tests_base.locators.login_page_locators import *


class LogInPage(BasePage):

    def __init__(self):
        super(LogInPage, self).__init__()
        self_url = "/xai/auth/logon"
        self.login_page_url = self.me_base_url + self_url

    def login(self, driver, delay, username, password):
        try:
            self.go_to_url(driver, self.me_base_url)
            assert self.get_cur_url(driver) == self.login_page_url
            assert self.wait_element_visible(driver, NASDAQ_LOGO, delay + 1)
            username_field = self.find_element_by(driver, USERNAME_FIELD, "id")
            self.send_keys(username_field, username)
            password_field = self.find_element_by(driver, PASSWORD_FIELD, "id")
            self.send_keys(password_field, password)
            login_button = self.find_element(driver, LOGIN_BUTTON)
            self.click_on_element(login_button)
        finally:
            if self.wait_element_visible(driver, HOME_PAGE_LOGO, delay + 1):
                return True
            else:
                return False
