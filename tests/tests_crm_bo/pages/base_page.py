import re
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.locators import base_page_locators


class BasePage(Browser):
    def __init__(self):
        super().__init__()
        self.base_locators = base_page_locators
        self.crm_base_url = BaseConfig.CRM_STAGING_URL
        # data_file, row, column1, column2, column3
        self.account_details = Instruments.get_account_details(BaseConfig.WTP_TESTS_CUSTOMERS, 38, 0, 1, 2)
        self.customer_id = self.account_details['customer_username']

    def go_back_and_wait(self, driver, previous_url):
        delay = 5
        self.go_back(driver)
        return self.wait_url_contains(driver, previous_url, delay)

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
        pause_button = self.find_element_by(driver, self.base_locators.PAUSE_BUTTON_ID, "id")
        self.wait_driver(driver, delay)
        self.click_on_element(pause_button)
        email_item = self.search_element(driver, self.base_locators.FIRST_EMAIL, delay)
        self.click_on_element(email_item)
        # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
        # 2 - click on forgot_password, 3 - click on verify_email
        if action == 0 or action == 1:
            return self._get_token(driver, action)
        elif action == 2 or action == 3:
            return self._click_on(driver, action, args)

    def _get_token(self, driver, action):
        delay = 5
        link = None
        try:
            self.switch_frame(driver, self.base_locators.EMAIL_FRAME_ID)
            if action == 0:
                link = self.search_element(driver, self.base_locators.FORGOT_PASSWORD_LINK, delay)
            else:
                link = self.search_element(driver, self.base_locators.REGENERATE_PASSWORD, delay)
        finally:
            if link is not None and action == 0:
                content = self.get_attribute_from_element(link, "href")
                return content
            elif link is not None and action == 1:
                content = self.get_element_span_html(link)
                return content

    def _click_on(self, driver, action, args):
        delay = 5
        url_to_check = args[0]
        try:
            self.switch_frame(driver, self.base_locators.EMAIL_FRAME_ID)
            if action == 2:
                locator = self.base_locators.FORGOT_PASSWORD_LINK
            else:
                locator = self.base_locators.CHANGE_PASSWORD_LINK
            link = self.search_element(driver, locator, delay)
            self.click_on_element(link)
            new_window = driver.window_handles
            self.switch_window(driver, new_window[1])
        finally:
            if self.wait_url_contains(driver, url_to_check, delay):
                return True
            else:
                return False
