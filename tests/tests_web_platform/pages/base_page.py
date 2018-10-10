import re
import time
from src.base.browser import Browser
from test_definitions import BaseConfig
from tests.tests_web_platform.locators import base_page_locators


class BasePage(Browser):
    def __init__(self):
        super(Browser, self).__init__()
        self.proxy = "appProxy"
        self.base = BaseConfig.WTP_STAGING_URL
        self.wtp_base_url = self.base + self.proxy
        self.api_base_url = BaseConfig.API_STAGING_URL
        self.base_locators = base_page_locators
        _self_account_url = "/openAccountDx.html"
        self.wtp_open_account_url = self.wtp_base_url + _self_account_url
        self.script_login = '$(".formContainer.formBox input.captchaCode").val("test_QA_test");'
        # self.script_signup = '$("input[name=\'captcha\']").val("test_QA_test");'
        self.script_signup = '$("#openAccountDxForm .captchaCode").val("test_QA_test");'
        self.script_forgot = '$("#dxPackageContainer_forgotPassword .captchaCode").val("test_QA_test");'
        self.script_customer_id = "return SO.model.Customer.getCustomerId();"
        self.script_is_signed = "return SO.model.Customer.isLoggedIn();"
        self.script_registration_step = "return SO.model.Customer.currentCustomer.registrationStep"
        self.script_document_1 = "$('.doc_1_1_0Hidden.hidden').show();"
        self.script_document_2 = "$('.doc_1_2_0Hidden.hidden').show();"
        self.script_document_3 = "$('.doc_2_1_0Hidden.hidden').show();"
        self.captcha_terms_url = "https://policies.google.com/terms?hl=en"
        self.script_input_val = '''return $("input[name='phonePrefix']").val();'''
        self.captcha_privacy_url = "https://policies.google.com/privacy?hl=en"

    def go_back_and_wait(self, driver, previous_url):
        delay = 5
        self.go_back(driver)
        if self.wait_url_contains(driver, previous_url, delay):
            return True
        else:
            return False

    def get_email_updates(self, driver, email, action, *args):
        delay = 5
        pattern = r"([\w\.-]+)"
        if not isinstance(email, str):
            email, = email
        else:
            pass
        email = re.findall(pattern, email)
        email = email[0]
        mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}".format(email)
        self.go_to_url(driver, mailinator_box_url)
        time.sleep(delay)
        pause_button = self.find_element_by(driver, self.base_locators.PAUSE_BUTTON_ID, "id")
        self.click_on_element(pause_button)
        email_item = self.search_element(driver, self.base_locators.FIRST_EMAIL, delay)
        self.click_on_element(email_item)
        # 0 - get_token for verify email, 1 - get_token for forgot password,
        # 2 - click on change_password, 3 - click on verify_email
        if action == 1 or action == 0:
            return self._get_token(driver, action)
        elif action == 2 or action == 3:
            return self._click_on(driver, action, args)

    def _get_token(self, driver, action):
        delay = 5
        button = None
        try:
            self.switch_frame(driver, self.base_locators.EMAIL_FRAME_ID)
            if action == 0:
                button = self.search_element(driver, self.base_locators.VERIFY_EMAIL_BUTTON, delay)
            else:
                button = self.search_element(driver, self.base_locators.CHANGE_PASSWORD_BUTTON, delay)
        finally:
            if button is not None:
                return self.get_attribute_from_element(button, "href")

    def _click_on(self, driver, action, args):
        delay = 5
        new_password_url = args[0]
        try:
            self.switch_frame(driver, self.base_locators.EMAIL_FRAME_ID)
            if action == 2:
                locator = self.base_locators.CHANGE_PASSWORD_BUTTON
            else:
                locator = self.base_locators.VERIFY_EMAIL_BUTTON
            button = self.search_element(driver, locator, delay + 5)
            self.click_with_offset(driver, button, 10, 10)
            new_window = driver.window_handles
            self.switch_window(driver, new_window[1])
        finally:
            if self.wait_url_contains(driver, self.wtp_open_account_url, delay) or \
                    self.wait_url_contains(driver, new_password_url, delay):
                return True
            else:
                return False

    def go_to_gmail(self, driver):
        delay = 5
        button = None
        try:
            self.go_to_url(driver, "https://gmail.com")
            email_field = self.find_element_by(driver, "identifierId", "id")
            self.click_on_element(email_field)
            self.send_keys(email_field, "qa.mailfortest@gmail.com")
            self.send_enter_key(email_field)
            password_field = self.find_element(driver, "//*[@id='password']//input")
            self.click_on_element(password_field)
            self.send_keys(password_field, "test@1248")
            self.send_enter_key(password_field)
            last_email = self.search_element(driver, "//*[@id=':3c']//span[@email='noreply@dx.exchange']", delay+5)
            self.click_on_element(last_email)
            button = self.search_element(driver, self.base_locators.VERIFY_EMAIL_BUTTON, delay)
        finally:
            if button is not None:
                content = self.get_attribute_from_element(button, "href")
                return content
