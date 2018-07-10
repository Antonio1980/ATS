import re
import time
import string
import random
from src.base.browser import Browser
from test_definitions import BaseConfig
from tests.tests_web_platform.locators.base_page_locators import BasePageLocators


class BasePage(Browser):
    def __init__(self):
        self.wtp_base_url = BaseConfig.WTP_BASE_URL
        self.base_locators = BasePageLocators()
        _self_account_url = "/openAccountDx.html"
        self.wtp_open_account_url = self.wtp_base_url + _self_account_url
        self.script_login = '$(".formContainer.formBox input.captchaCode").val("test_QA_test");'
        # self.script_signup = '$("input[name=\'captcha\']").val("test_QA_test");'
        self.script_signup = '$("#openAccountDxForm .captchaCode").val("test_QA_test");'
        self.script_forgot = '$("#dxPackageContainer_forgotPassword .captchaCode").val("test_QA_test");'

    def go_back_and_wait(self, driver, previous_url, delay=+3):
        self.driver_wait(driver, delay)
        self.go_back(driver)
        self.wait_driver(driver, delay)
        if self.get_cur_url(driver) == previous_url:
            return True
        else:
            return False

    def email_generator(self, size=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_email_updates(self, driver, email, action, *args):
        delay = 10
        self.driver_wait(driver, delay)
        pattern = r"([\w\.-]+)"
        if not isinstance(email, str):
            email, = email
        else:
            pass
        email = re.findall(pattern, email)
        email = email[0]
        mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}".format(email)
        self.go_to_url(driver, mailinator_box_url)
        time.sleep(5)
        self.driver_wait(driver, delay)
        pause_button = self.find_element_by(driver, self.base_locators.PAUSE_BUTTON_ID, "id")
        pause_button.click()
        email_item = self.find_element(driver, self.base_locators.FIRST_EMAIL)
        email_item.click()
        self.driver_wait(driver, delay)
        # 0 - get_token for verify email, 1 - get_token for forgot password, 2 - click on change_password, 3 - click on verify_email
        if action == 1 or action == 0:
            return self._get_token(driver, action)
        elif action == 2 or action == 3:
            return self._click_on(driver, action, args)

    def _get_token(self, driver, action):
        delay = 5
        button = None
        try:
            self.driver_wait(driver, delay)
            self.switch_frame(driver, self.base_locators.EMAIL_FRAME_ID)
            if action == 0:
                button = self.search_element(driver, self.base_locators.VERIFY_EMAIL_BUTTON, delay)
            else:
                button = self.search_element(driver, self.base_locators.CHANGE_PASSWORD_BUTTON, delay)
        finally:
            self.driver_wait(driver, delay)
            if button is not None:
                content = self.get_attribute_from_element(button, "href")
                return content

    def _click_on(self, driver, action, args):
        delay = 5
        new_password_url = args[0]
        try:
            self.driver_wait(driver, delay)
            self.switch_frame(driver, self.base_locators.EMAIL_FRAME_ID)
            if action == 2:
                locator = self.base_locators.CHANGE_PASSWORD_BUTTON
            else:
                locator = self.base_locators.VERIFY_EMAIL_BUTTON
            button = self.search_element(driver, locator, delay)
            button.click()
            self.driver_wait(driver, delay + 5)
            new_window = driver.window_handles
            self.switch_window(driver, new_window[1])
        finally:
            time.sleep(10)
            cur_url = self.get_cur_url(driver)
            if cur_url == self.wtp_open_account_url or cur_url == new_password_url:
                return True
            else:
                return False


# if __name__ == '__main__':
#     #RegistrationFlowTest.setUpClass()
#     url = "https://plat.dx.exchange/appProxy/forgotPasswordDx.html?validation_token=ff4a558a-2267-4443-85e8-6c5bbfef48e5&email=wovqfphw%40mailinator.com"
#     token = url.split('=')
#     token = token[1].split('&')
#     print(token, type(token))
