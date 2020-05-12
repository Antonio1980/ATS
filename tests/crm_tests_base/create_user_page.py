from src.base import logger
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.base_page import BasePage
from tests.crm_tests_base.locators import create_user_page_locators
from tests.crm_tests_base import create_user_page_url, user_index_page_url


class CreateUserPage(BasePage):
    password_message = "A temporary password will be created and an email will be send to the user with instructions to change it"

    def __init__(self):
        super(CreateUserPage, self).__init__()
        self.locators = create_user_page_locators

    @automation_logger(logger)
    def fill_user_details(self, driver, email, user_details):
        first_last_name, phone, username, language, permissions, status, user_type = user_details['first_last_name'], \
                                          "35435456456", user_details['username'], user_details['language'], \
                                          user_details['permissions'], user_details['status'], user_details['user_type']
        try:
            assert self.wait_url_contains(driver, create_user_page_url, self.ui_delay)
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
            # self.choose_option_from_dropdown(driver, self.locators.LANGUAGE_DROPDOWN,
                                             # self.locators.LANGUAGE_TEXT_FIELD, language)
            self.choose_option_from_dropdown(driver, self.locators.PERMISSION_GROUP_DROPDOWN,
                                             self.locators.PERMISSION_GROUP_TEXT_FIELD, permissions)
            # self.choose_option_from_dropdown(driver, self.locators.STATUS_DROPDOWN,
                                             # self.locators.STATUS_TEXT_FIELD, status)
            self.choose_option_from_dropdown(driver, self.locators.USER_TYPE_DROPDOWN,
                                             self.locators.USER_TYPE_FIELD, user_type)
            create_user_button = self.search_element(driver, self.locators.CREATE_USER_BUTTON, self.ui_delay)
            self.click_on_element(create_user_button)
            return self.wait_url_contains(driver, user_index_page_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} fill_user_details failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False
