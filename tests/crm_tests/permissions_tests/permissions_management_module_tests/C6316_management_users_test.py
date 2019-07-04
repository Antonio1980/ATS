import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage
from tests.crm_tests_base.permissions_page import PermissionsPage

test_case = '6316'


@allure.title("Permissions")
@allure.description("""
    Checking of view, edit, add options for Management Users. 
    1.
    2. 
    3. 
    4.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Management Users Permissions')
@allure.testcase(BaseConfig.GITLAB_URL_CRM +
                 "/permissions_tests/permissions_management_module_tests/C6316_management_users_test.py",
                 "TestLeadLimitations")
@pytest.mark.usefixtures("r_time_count", 'web_driver', 'r_customer')
@pytest.mark.crm_sanity
class TestManagementUsers(object):
    browser = Browser()
    home_page = HomePage()
    login_page = LogInPage()
    customer_page = CustomerPage()
    permissions_page = PermissionsPage()
    locators = permissions_page.locators
    delay = permissions_page.ui_delay
    permissions_group_id = permissions_page.permissions_group_id
    local_permissions_group_name = permissions_page.local_permissions_group_name
    local_permissions_entity_name = "'Users'"
    local_sub_module_name = "'Users'"
    local_permissions_entity_management = "'Management'"
    local_sub_module_name_management = "'Management'"

    @allure.step("Start with: test_open_homepage")
    @automation_logger(logger)
    def test_open_homepage(self, web_driver):
        assert self.login_page.login(web_driver, self.permissions_page.username, self.permissions_page.password)


    @allure.step("Proceed with: ")
    @automation_logger(logger)
    def test_set_permissions(self, web_driver):
        # set communicator menu   hasView = 1, hasEdit = 0, hasCreate = 0
        assert self.permissions_page.set_entity_permissions(self.permissions_group_id,
                                                            self.local_permissions_group_name,
                                                            self.local_permissions_entity_management,
                                                            self.local_sub_module_name_management)
        # update communicator menu   hasView = 1, hasEdit = 1, hasCreate = 1
        assert self.permissions_page.update_view_edit_create_permissions(self.local_permissions_entity_management,
                                                                         self.permissions_group_id, 2)
        # set entity permissions
        assert self.permissions_page.set_entity_permissions(self.permissions_group_id,
                                                            self.local_permissions_group_name,
                                                            self.local_permissions_entity_name,
                                                            self.local_sub_module_name)
        management_dropdown_button = Browser.find_element_by(self.driver, self.locators.MANAGEMENT_MENU_ID, "id")
        Browser.click_on_element(management_dropdown_button)
        users_dropdown_title = Browser.wait_element_presented(self.driver,
                                                              self.locators.USERS_DROPDOWN_TITLE, self.delay)
        Browser.click_on_element(users_dropdown_title)
        assert Browser.wait_element_presented(self.driver, self.locators.USERS_TITLE_ON_USER_PAGE, self.delay)
        users_list = Browser.find_elements(self.driver, self.locators.NOT_EDIT_USERS)
        first_user = users_list[0]
        assert Browser.wait_element_presented(self.driver, first_user, self.delay)
        assert Browser.check_element_not_presented(self.driver, self.locators.EDIT_LINK_FOR_USER, self.delay)
        assert Browser.check_element_not_presented(self.driver, self.locators.CREATE_USER_BUTTON_ON_USERS_PAGE,
                                                   self.delay)

        # update method with  1  : hasView = 1, hasEdit = 1, hasCreate = 0
        self.permissions_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                                  self.permissions_group_id, 1)
        Browser.refresh_page(self.driver)
        assert Browser.check_element_not_presented(self.driver, self.locators.CREATE_USER_BUTTON_ON_USERS_PAGE,
                                                   self.delay)
        edit_user_links_list = Browser.find_elements(self.driver, self.locators.EDIT_LINK_FOR_USER)
        edit_first_link_user = edit_user_links_list[0]
        assert Browser.wait_element_presented(self.driver, edit_first_link_user, self.delay)
        Browser.click_on_element(edit_first_link_user)
        assert Browser.wait_element_presented(self.driver, self.locators.EDIT_TITLE_ON_EDIT_USERS_PAGE, self.delay)
        Browser.go_back(self.driver)

        # update method with  2  : hasView = 1, hasEdit = 1, hasCreate = 1
        self.permissions_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                                  self.permissions_group_id, 2)
        Browser.refresh_page(self.driver)
        assert Browser.wait_element_presented(self.driver, edit_first_link_user, self.delay)
        create_user_button = Browser.wait_element_presented(self.driver, self.locators.CREATE_USER_BUTTON_ON_USERS_PAGE,
                                                            self.delay)
        Browser.click_on_element(create_user_button)
        assert Browser.wait_element_presented(self.driver, self.locators.CREATE_NEW_USER_TITLE_ON_USERS_PAGE,
                                              self.delay)

    @allure.step("Proceed with: ")
    @automation_logger(logger)
    def test_customer_page(self, web_driver, r_customer):
        assert self.home_page.choose_customer_by_option(web_driver, r_customer.customer_id, "Id")
        customer_id_ui = self.customer_page.get_customer_id_from_customer_page(web_driver)
        assert customer_id_ui == r_customer.customer_id

        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
