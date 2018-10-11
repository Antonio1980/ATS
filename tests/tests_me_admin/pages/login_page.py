from selenium.common.exceptions import TimeoutException
from tests.tests_me_admin.pages.base_page import BasePage
from tests.tests_me_admin.locators import home_page_locators
from tests.tests_me_admin.locators import login_page_locators


class LogInPage(BasePage):

    def __init__(self):
        super(LogInPage, self).__init__()
        self_url = "/xai/auth/logon"
        self.login_page_url = self.me_base_url + self_url
        self.locators = login_page_locators

    def login_positive(self, driver, username, password):
        delay = 5
        try:
            self.go_to_url(driver, self.me_base_url)
            assert self.get_cur_url(driver) == self.login_page_url
            assert self.wait_element_visible(driver, self.locators.NASDAQ_LOGO, delay)
            username_field = self.find_element_by(driver, self.locators.USERNAME_FIELD, "id")
            self.send_keys(username_field, username)
            password_field = self.find_element_by(driver, self.locators.PASSWORD_FIELD, "id")
            self.send_keys(password_field, password)
            login_button = self.search_element(driver, self.locators.LOGIN_BUTTON, delay)
            self.click_on_element(login_button)
        finally:
            try:
                self.wait_element_visible(driver, home_page_locators.HOME_PAGE_LOGO, delay)
                return True
            except TimeoutException:
                return False

