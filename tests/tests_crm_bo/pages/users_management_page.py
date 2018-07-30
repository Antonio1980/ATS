from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators.users_page_locators import UsersPageLocators
from tests.tests_crm_bo.pages import user_management_page_url, create_user_page_url


class UsersManagementPage(BasePage):
    def __init__(self):
        super(UsersManagementPage, self).__init__()
        self.locators = UsersPageLocators()

    def click_on_create_new_user(self, driver):
        try:
            assert user_management_page_url == self.get_cur_url(driver)
            new_user_button = self.find_element_by(driver, self.locators.CREATE_NEW_USER_BUTTON_ID, "id")
            self.click_on_element(new_user_button)
        finally:
            cur_url = self.get_cur_url(driver)
            if cur_url == create_user_page_url:
                return True
            else:
                return False
