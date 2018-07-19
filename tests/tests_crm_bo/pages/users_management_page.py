from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators.users_page_locators import UsersPageLocators
from tests.tests_crm_bo.pages import user_management_page_url, create_user_page_url


class UsersManagementPage(BasePage):
    def __init__(self):
        super(UsersManagementPage, self).__init__()
        self.locators = UsersPageLocators()

    def click_on_create_new_user(self, driver):
        delay = 3
        try:
            self.driver_wait(driver, delay + 5)
            assert self.get_cur_url(driver) == user_management_page_url
            new_user_button = self.find_element_by(driver, self.locators.CREATE_NEW_USER_BUTTON_ID, "id")
            self.click_on_element(new_user_button)
            self.driver_wait(driver, delay + 5)
        finally:
            if self.get_cur_url(driver) == create_user_page_url:
                return True
            else:
                return False
