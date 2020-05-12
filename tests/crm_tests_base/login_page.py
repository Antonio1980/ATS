import time
from src.base import logger
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.base_page import BasePage
from selenium.webdriver.remote.webelement import WebElement
from tests.crm_tests_base.locators import home_page_locators
from tests.crm_tests_base.locators import login_page_locators
from tests.crm_tests_base import login_page_url, new_password_url, home_page_url


class LogInPage(BasePage):

    def __init__(self):
        super(LogInPage, self).__init__()
        self.locators = login_page_locators

    @automation_logger(logger)
    def go_to_login_page(self, driver, url):
        self.go_to_url(driver, url)
        return self.wait_url_contains(driver, login_page_url, self.ui_delay)

    @automation_logger(logger)
    def login(self, driver, username, password):
        try:
            if self.go_to_login_page(driver, self.crm_base_url):
                username_field = self.find_element_by(driver, self.locators.USERNAME_FIELD_ID, "id")
                self.send_keys(username_field, username)
                password_field = self.find_element_by(driver, self.locators.PASSWORD_FIELD_ID, "id")
                self.send_keys(password_field, password)
                login_button = self.find_element_by(driver, self.locators.LOGIN_BUTTON_ID, "id")
                self.click_on_element(login_button)
                time.sleep(2.0)
                if not self.find_element_by(driver, home_page_locators.HOME_PAGE_LOGO_ID, "id"):
                    return self.wait_url_contains(driver, new_password_url, self.ui_delay)
                else:
                    return True
        except Exception as e:
            logger.logger.error("{0} login failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    @automation_logger(logger)
    def forgot_password(self, driver, email):
        try:
            if self.go_to_login_page(driver, self.crm_base_url):
                forgot_password_link = self.wait_element_clickable(driver, self.locators.FORGOT_PASSWORD_LINK,
                                                                   self.ui_delay)
                self.click_on_element(forgot_password_link)
                email_field = self.wait_element_clickable(driver, self.locators.POPUP_EMAIL_FIELD, self.ui_delay)
                self.send_keys(email_field, email)
                send_button = self.find_element_by(driver, self.locators.POPUP_SEND_BUTTON_ID, "id")
                self.click_on_element(send_button)
                if self.check_element_not_visible(driver, self.locators.POPUP_CHECK, self.ui_delay):
                    time.sleep(2.0)
                    if self.check_element_not_visible(driver, self.locators.POPUP_ERROR_MESSAGE_CLOSE_BUTTON,
                                                      self.ui_delay):
                        self.click_on_element_by_locator(driver, self.locators.EMAIL_POPUP_CLOSE_BUTTON, self.ui_delay)
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} forgot_password failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    @automation_logger(logger)
    def set_new_password(self, driver, password, new_password):
        try:
            assert self.wait_url_contains(driver, new_password_url, self.ui_delay)
            cur_password_field = self.find_element_by(driver, self.locators.CURRENT_PASSWORD_ID, "id")
            self.click_on_element(cur_password_field)
            self.send_keys(cur_password_field, password)
            new_password_field = self.find_element_by(driver, self.locators.NEW_PASSWORD_ID, "id")
            self.click_on_element(new_password_field)
            self.send_keys(new_password_field, new_password)
            confirm_password_field = self.find_element_by(driver, self.locators.CONFIRM_PASSWORD_ID, "id")
            self.click_on_element(confirm_password_field)
            self.send_keys(confirm_password_field, new_password)
            confirm_button = self.find_element(driver, self.locators.CONFIRM_BUTTON)
            self.click_on_element(confirm_button)
            return self.wait_url_contains(driver, home_page_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} set_new_password failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    @automation_logger(logger)
    def go_by_token_url(self, driver, _new_password_url):
        try:
            self.go_to_url(driver, _new_password_url)
            if isinstance(self.check_element_not_visible(driver, self.locators.PASSWORD_TOKEN_WARNING, self.ui_delay),
                          WebElement):
                return False
            else:
                return True
        except Exception as e:
            logger.logger.error("{0} go_by_token_url failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False
