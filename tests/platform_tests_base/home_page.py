from src.base import logger
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.base_page import BasePage
from tests.platform_tests_base.locators import home_page_locators
from tests.platform_tests_base import wtp_home_page_url, wtp_signin_page_url, wtp_dashboard_url, \
    wtp_open_account_url


class HomePage(BasePage):

    def __init__(self):
        super(HomePage, self).__init__()
        self.locators = home_page_locators

    @automation_logger(logger)
    def open_home_page(self, driver):
        try:
            self.go_to_url(driver, wtp_home_page_url)
            return self.wait_url_contains(driver, wtp_home_page_url, self.ui_delay) or \
                   self.wait_url_contains(driver, wtp_dashboard_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} open_home_page failed with error: {1}".format(e.__class__.__name__,
                                                                                   e.__cause__), e)
            return False

    @automation_logger(logger)
    def open_signup_page(self, driver):
        try:
            if self.open_home_page(driver):
                self.click_on_element_by_locator(driver, self.locators.SIGN_UP_BUTTON, self.ui_delay)
            return self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} open_signup_page failed with error: {1}".format(e.__class__.__name__,
                                                                                     e.__cause__), e)
            return False

    @automation_logger(logger)
    def open_signin_page(self, driver):
        try:
            if self.open_home_page(driver):

                self.click_on_element_by_locator(driver, self.locators.SIGNIN_BUTTON, self.ui_delay)
            return self.wait_url_contains(driver, wtp_signin_page_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} open_signin_page failed with error: {1}".format(e.__class__.__name__,
                                                                                     e.__cause__), e)
            return False

    @automation_logger(logger)
    def sign_out(self, driver):
        try:
            self.wait_element_clickable(driver, self.locators.LOG_OUT_BUTTON, self.ui_delay)
            self.click_on_element_by_locator(driver, self.locators.LOG_OUT_BUTTON, self.ui_delay)
            return self.wait_url_contains(driver, wtp_dashboard_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} sign_out failed with error: {1}".format(e.__class__.__name__,
                                                                             e.__cause__), e)
            return False
