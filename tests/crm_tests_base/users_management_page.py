from src.base import logger
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.base_page import BasePage
from tests.crm_tests_base.locators import users_management_page_locators
from tests.crm_tests_base import user_management_page_url, create_user_page_url


class UsersManagementPage(BasePage):

    def __init__(self):
        super(UsersManagementPage, self).__init__()
        self.locators = users_management_page_locators

    @automation_logger(logger)
    def click_on_create_new_user(self, driver):
        try:
            assert self.wait_url_contains(driver, user_management_page_url, self.ui_delay)
            new_user_button = self.find_element_by(driver, self.locators.CREATE_NEW_USER_BUTTON_ID, "id")
            self.click_with_wait_and_offset(driver, new_user_button, 5, 5)
            return self.wait_url_contains(driver, create_user_page_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} click_on_create_new_user failed with error: {1}".format(e.__class__.__name__,
                                                                                             e.__cause__))
            return False
