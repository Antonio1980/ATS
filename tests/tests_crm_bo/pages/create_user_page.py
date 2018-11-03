import re
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators import create_user_page_locators
from tests.tests_crm_bo.pages import create_user_page_url, user_index_page_url


class CreateUserPage(BasePage):
    password_message = "A temporary password will be created and an email will be send to the user with instructions to change it"

    def __init__(self):
        super().__init__()
        self.locators = create_user_page_locators
        self.response = Instruments.get_guerrilla_email()
        self.email = self.response[1]['email_addr']
        self.guerrilla_username = re.findall(r"([\w.-]+)", self.email)[0]
        self.sid_token = self.response[1]['sid_token']
        self.phone = Instruments.generate_phone_number()
        self.time_stamp = str(self.response[1]['email_timestamp'])
        self.username = Instruments.generate_username()
        self.first_last_name = Instruments.generate_user_first_last_name()

    def fill_user_details(self, driver, email, user_details):
        delay = 5
        first_last_name, phone, username, language, permissions, status, user_type = user_details['first_last_name'], \
                                          "35435456456", user_details['username'], user_details['language'], \
                                          user_details['permissions'], user_details['status'], user_details['user_type']
        try:
            assert self.wait_url_contains(driver, create_user_page_url, delay)
            first_name_field = self.find_element_by(driver, self.locators.FIRST_NAME_ID, "id")
            self.click_on_element(first_name_field)
            self.send_keys(first_name_field, first_last_name)
            last_name_field = self.find_element_by(driver, self.locators.LAST_NAME_ID, "id")
            self.click_on_element(last_name_field)
            self.send_keys(last_name_field, first_last_name)
            email_field = self.find_element_by(driver, self.locators.EMAIL_ID, "id")
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            phone_field = self.find_element_by(driver, self.locators.PHONE_ID, "id")
            self.click_on_element(phone_field)
            self.send_keys(phone_field, phone)
            username_field = self.find_element_by(driver, self.locators.USERNAME_ID, "id")
            self.click_on_element(username_field)
            self.send_keys(username_field, username)
            # self.choose_option_from_dropdown(driver, self.locators.LANGUAGE_DROPDOWN, self.locators.LANGUAGE_TEXT_FIELD, language, delay - 3)
            self.choose_option_from_dropdown(driver, self.locators.PERMISSION_GROUP_DROPDOWN,
                                             self.locators.PERMISSION_GROUP_TEXT_FIELD, permissions, delay - 3)
            # self.choose_option_from_dropdown(driver, self.locators.STATUS_DROPDOWN, self.locators.STATUS_TEXT_FIELD, status, delay - 3)
            self.choose_option_from_dropdown(driver, self.locators.USER_TYPE_DROPDOWN,
                                             self.locators.USER_TYPE_TEXT_FIELD, user_type, delay - 3)
            create_user_button = self.search_element(driver, self.locators.CREATE_USER_BUTTON, delay)
            self.click_on_element(create_user_button)
            return self.wait_url_contains(driver, user_index_page_url, delay)
        except AutomationError as e:
            print("{0} fill_user_details failed with error: {1}".format(e.__class__.__name__, e.__cause__))
