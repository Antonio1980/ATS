from src.base.base_exception import AutomationError
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators import users_management_page_locators
from tests.tests_crm_bo.pages import user_management_page_url, create_user_page_url


class UsersManagementPage(BasePage):
    def __init__(self):
        super().__init__()
        self.locators = users_management_page_locators

    def click_on_create_new_user(self, driver, delay):
        try:
            assert self.wait_url_contains(driver, user_management_page_url, delay)
            new_user_button = self.find_element_by(driver, self.locators.CREATE_NEW_USER_BUTTON_ID, "id")
            self.click_with_wait_and_offset(driver, new_user_button, 5, 5, delay - 3)
            return self.wait_url_contains(driver, create_user_page_url, delay)
        except AutomationError as e:
            print("{0} click_on_create_new_user failed with error: {1}".format(e.__class__.__name__, e.__cause__))
