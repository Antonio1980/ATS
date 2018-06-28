# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import string
import random
from src.base.browser import Browser
from tests.test_definitions import BaseConfig
from tests.tests_web_platform.locators.base_page_locators import BasePageLocators


class BasePage(Browser):
    def __init__(self):
        self.wtp_base_url = BaseConfig.WTP_INTEGRATION_URL
        _self_account_url = "/openAccountDx.html"
        self.wtp_open_account_url = self.wtp_base_url + _self_account_url
        self.script_login = '$(".formContainer.formBox input.captchaCode").val("test_QA_test");'
        # self.script_signup = '$("input[name=\'captcha\']").val("test_QA_test");'
        self.script_signup = '$("#openAccountDxForm .captchaCode").val("test_QA_test");'
        self.script_forgot = '$("#dxPackageContainer_forgotPassword .captchaCode").val("test_QA_test");'

    def go_back_and_wait(self, driver, previous_url, delay=3):
        self.driver_wait(driver, delay)
        self.go_back(driver)
        self.wait_driver(driver, delay)
        if self.get_cur_url(driver) == previous_url:
            return True
        else:
            return False

    def email_generator(self, size=8, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_email_updates(self, driver, email, action):
        delay = 1
        pattern = r"([\w\.-]+)"
        if not isinstance(email, str):
            email, = email
        else:
            pass
        email = re.findall(pattern, email)
        email = email[0]
        mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}".format(email)
        self.go_to_url(driver, mailinator_box_url)
        pause_button = self.find_element_by(driver, BasePageLocators.PAUSE_BUTTON_ID, "id")
        pause_button.click()
        email_item = self.find_element(driver, BasePageLocators.FIRST_EMAIL)
        email_item.click()
        self.driver_wait(driver, delay)
        # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
        if action == 1:
            return self._get_updates(driver, delay)
        elif action == 2:
            return self._click_on(driver, BasePageLocators.CHANGE_PASSWORD_BUTTON, delay)
        elif action == 3:
            return self._click_on(driver, BasePageLocators.VERIFY_EMAIL_BUTTON, delay)

    def _get_updates(self, driver, delay=1):
        try:
            self.driver_wait(driver, delay)
        finally:
            mail_content = self.find_element_by(driver, BasePageLocators.EMAIL_FRAME_ID, "id")
            self.driver_wait(driver, delay)
            if mail_content:
                return mail_content
            else:
                return False

    def _click_on(self, driver, locator, delay=1):
        try:
            self.driver_wait(driver, delay)
            element = self.find_element_by(driver, BasePageLocators.EMAIL_FRAME_ID, "id")
            self.switch_frame(driver, element)
            button = self.find_element(driver, locator)
            button.click()
            self.driver_wait(driver, delay)
        finally:
            if self.get_cur_url(driver) == self.wtp_open_account_url:
                return True
            else:
                return False
