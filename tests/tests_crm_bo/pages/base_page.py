import re
import string
import random
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import get_account_details
from tests.tests_crm_bo.locators.base_page_locators import BasePageLocators


class BasePage(Browser, BaseConfig):
    def __init__(self):
        super(BasePage, self).__init__()
        self.base_locators = BasePageLocators()
        self.crm_base_url = self.CRM_STAGING_URL
        # data_file, row, column1, column2, column3
        self.account_details = get_account_details(self.WTP_TESTS_CUSTOMERS, 0, 0, 1, 2)
        self.customer_id = self.account_details['customer_username']

    def email_generator(self, size=8, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

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
        # 2 - click on forgot_password, 3 - ?
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
            cur_url = self.get_cur_url(driver)
            if cur_url == url_to_check:
                return True
            else:
                return False
