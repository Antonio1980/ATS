import time
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.pages import create_user_page_url, user_index_page_url
from tests.tests_crm_bo.locators.create_user_page_locators import CreateUserPageLocators


class CreateUserPage(BasePage):
    def __init__(self):
        super(CreateUserPage, self).__init__()
        self.first_last_name = "QA_test_QA"
        self.locators = CreateUserPageLocators()
        self.email_prefix = self.email_generator()
        self.email = self.email_prefix + "@mailinator.com"

    def fill_user_details(self, driver, email, details):
        first_last_name, phone, username = details['first_last_name'], details['phone'], details['username']
        try:
            assert self.get_cur_url(driver) == create_user_page_url
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
            language_dropdown = self.find_element(driver, self.locators.LANGUAGE_DROPDOWN)
            self.click_on_element(language_dropdown)
            language_field = self.find_element(driver, self.locators.LANGUAGE_FIELD)
            self.click_on_element(language_field)
            language_text_field = self.find_element(driver, self.locators.LANGUAGE_TEXT_FIELD)
            self.send_keys(language_text_field, "eng")
            self.send_enter_key(language_text_field)
            permission_dropdown = self.find_element(driver, self.locators.PERMISSION_GROUP_DROPDOWN)
            self.click_on_element(permission_dropdown)
            permission_field = self.find_element(driver, self.locators.PERMISSION_GROUP_FIELD)
            self.click_on_element(permission_field)
            permission_text_field = self.find_element(driver, self.locators.PERMISSION_GROUP_TEXT_FIELD)
            self.send_keys(permission_text_field, "sup")
            self.send_enter_key(permission_text_field)
            status_dropdown = self.find_element(driver, self.locators.STATUS_DROPDOWN)
            self.click_on_element(status_dropdown)
            status_field = self.find_element(driver, self.locators.STATUS_FIELD)
            self.click_on_element(status_field)
            status_text_field = self.find_element(driver, self.locators.STATUS_TEXT_FIELD)
            self.send_keys(status_text_field, "a")
            self.send_enter_key(status_text_field)
            user_type_dropdown = self.find_element(driver, self.locators.USER_TYPE_DROPDOWN)
            self.click_on_element(user_type_dropdown)
            user_type_field = self.find_element(driver, self.locators.USER_TYPE_FIELD)
            self.click_on_element(user_type_field)
            user_type_text_field = self.find_element(driver, self.locators.USER_TYPE_TEXT_FIELD)
            self.send_keys(user_type_text_field, "Admin")
            self.send_enter_key(user_type_text_field)
            create_user_button = self.find_element_by(driver, self.locators.CREATE_USER_BUTTON_ID, "id")
            self.click_on_element(create_user_button)
        finally:
            cur_url = self.get_cur_url(driver)
            if cur_url == user_index_page_url:
                return True
            else:
                return False
