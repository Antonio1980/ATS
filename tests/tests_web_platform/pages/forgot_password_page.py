# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests.tests_web_platform.pages import BasePage, forgot_password_page_url
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators


class ForgotPasswordPage(BasePage):
    def __init__(self):
        super(ForgotPasswordPage, self).__init__()

    def fill_email_address_form(self, driver, email, delay =+ 1):
        try:
            self.driver_wait(driver, delay)
            assert forgot_password_page_url == self.get_cur_url(driver)
            email_field = self.find_element(driver, ForgotPasswordPageLocators.EMAIL_TEXT_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            self.wait_driver(driver, delay + 3)
            self.execute_js(driver, self.script_forgot)
            submit_button = self.find_element(driver, ForgotPasswordPageLocators.SUBMIT_BUTTON)
            self.click_on_element(submit_button)
        finally:
            if self.check_element_not_visible(driver, delay, ForgotPasswordPageLocators.EMAIL_ERROR_MESSAGE) or not self.wait_element_clickable(driver, delay, ForgotPasswordPageLocators.SUBMIT_BUTTON):
                return True
            else:
                return False

