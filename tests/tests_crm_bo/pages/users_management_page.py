from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators.users_page_locators import UsersPageLocators
from tests.tests_crm_bo.pages import user_management_page_url, create_user_page_url


class UsersManagementPage(BasePage):
    def __init__(self):
        super(UsersManagementPage, self).__init__()
        self.locators = UsersPageLocators()

    def click_on_create_new_user(self, driver):
        delay = 5
        try:
            assert self.wait_url_contains(driver, user_management_page_url, delay)
            new_user_button = self.find_element_by(driver, self.locators.CREATE_NEW_USER_BUTTON_ID, "id")
            self.click_on_element(new_user_button)
        finally:
            if self.wait_url_contains(driver, create_user_page_url, delay):
                return True
            else:
                return False
