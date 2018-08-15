from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.home_page_locators import HomePageLocators
from tests.tests_web_platform.pages import wtp_signin_page_url, wtp_home_page_url, user_page_url


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()
        self.locators = HomePageLocators()

    def open_home_page(self, driver, delay):
        self.go_to_url(driver, wtp_home_page_url)
        return self.wait_driver(,, driver, delay

    def open_signup_page(self, driver, delay):
        try:
            self.open_home_page(driver, delay)
            assert self.wait_url_contains(driver, wtp_home_page_url, delay)
            self.click_on_element_by_locator(driver, self.base_locators.SIGN_UP_BUTTON, delay + 5)
        finally:
            if self.wait_url_contains(driver, self.wtp_open_account_url, delay):
                return True
            else:
                return False

    def open_signin_page(self, driver, delay):
        try:
            self.open_home_page(driver, delay)
            assert self.wait_url_contains(driver, wtp_home_page_url, delay)
            self.click_on_element_by_locator(driver, self.base_locators.LOGIN_BUTTON, delay + 5)
        finally:
            if self.wait_url_contains(driver, wtp_signin_page_url, delay):
                return True
            else:
                return False

    def sign_out(self, driver):
        delay = 5
        try:
            log_out_button = self.find_element(driver, self.locators.LOG_OUT_BUTTON)
            self.click_on_element(log_out_button)
        finally:
            if self.wait_url_contains(driver, user_page_url, delay):
                return True
            else:
                return False
