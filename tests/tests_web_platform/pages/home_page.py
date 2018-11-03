from src.base.base_exception import AutomationError
from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators import home_page_locators
from tests.tests_web_platform.pages import wtp_home_page_url, wtp_signin_page_url, wtp_dashboard_url, \
    wtp_open_account_url


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()
        self.locators = home_page_locators

    def open_home_page(self, driver, delay):
        try:
            # self.wait_driver(driver, delay)
            self.go_to_url(driver, wtp_home_page_url)
            return self.wait_url_contains(driver, wtp_home_page_url, delay) or self.wait_url_contains(driver, wtp_dashboard_url, delay)
        except AutomationError as e:
            print("{0} open_home_page failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def open_signup_page(self, driver, delay):
        try:
            if self.open_home_page(driver, delay):
                self.click_on_element_by_locator(driver, self.locators.SIGN_UP_BUTTON, delay)
            return self.wait_url_contains(driver, wtp_open_account_url, delay)
        except AutomationError as e:
            print("{0} open_signup_page failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def open_signin_page(self, driver, delay):
        try:
            if self.open_home_page(driver, delay):
                self.click_on_element_by_locator(driver, self.locators.SIGNIN_BUTTON, delay)
            return self.wait_url_contains(driver, wtp_signin_page_url, delay)
        except AutomationError as e:
            print("{0} open_signin_page failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def sign_out(self, driver, delay):
        try:
            self.wait_element_clickable(driver, self.locators.LOG_OUT_BUTTON, delay)
            self.click_on_element_by_locator(driver, self.locators.LOG_OUT_BUTTON, delay)
            return self.wait_url_contains(driver, wtp_dashboard_url, delay)
        except AutomationError as e:
            print("{0} sign_out failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False
