from src.base.base_exception import AutomationError
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators import home_page_locators
from tests.tests_crm_bo.pages import home_page_url, user_management_page_url, customer_admin_url


class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        self.locators = home_page_locators
        self.customer_id_locator = "//*[@class='customerIdtext'][contains(text(),'Customer ID {0}')]"
        self.username_permissions = "Christina K"
        self.password_permissions = "qwerty12345"
        self.permissions_group_id = '20'
        self.local_permissions_group_name = "'Christina'"

    def logout(self, driver, delay):
        try:
            assert self.find_element_by(driver, self.locators.HOME_PAGE_LOGO_ID, "id")
            self.click_on_element_by_locator(driver, self.locators.SETTINGS_DROPDOWN, delay + 5)
            self.click_on_element_by_locator(driver, self.locators.LANGUAGE_ICON, delay + 5)
            self.click_on_element_by_locator(driver, self.locators.LOGOUT_LINK, delay + 3)
        finally:
            if self.wait_element_presented(driver, self.base_locators.CRM_LOGO, delay + 3):
                return True
            else:
                return False

    def choose_customer_by_option(self, driver, customer, option):
        delay = 5
        customer_option = None
        try:
            assert self.wait_url_contains(driver, home_page_url, delay)
            customer_field = self.find_element(driver, self.locators.CUSTOMER_DROPDOWN)
            self.click_on_element(customer_field)
            if option == 1:
                customer_option = self.find_element(driver, self.locators.CUSTOMER_ID_OPTION)
            elif option == 2:
                customer_option = self.find_element(driver, self.locators.CUSTOMER_ID_OPTION)
            elif option == 3:
                customer_option = self.find_element(driver, self.locators.CUSTOMER_ID_OPTION)
            if customer_option is not None:
                self.click_on_element(customer_option)
            customer_name_field = self.find_element_by(driver, self.locators.CUSTOMER_NAME_FIELD_ID, "id")
            self.click_on_element(customer_field)
            self.send_keys(customer_name_field, customer)
            show_button = self.find_element_by(driver, self.locators.SHOW_RESULTS_BUTTON_ID, "id")
            self.click_on_element(show_button)
            self.wait_number_of_windows(driver, 2, delay)
            new_window = driver.window_handles[1]
            self.switch_window(driver, new_window)
            x = self.wait_element_visible(driver, self.customer_id_locator.format(customer), delay + 5)
        finally:
            if self.wait_url_contains(driver, str(customer_admin_url), delay + 5):
                return True
            else:
                return False

    def go_to_management_inset_with_users_option(self, driver):
        delay = 5
        try:
            assert self.wait_url_contains(driver, home_page_url, delay)
            management_dropdown = self.find_element(driver, self.locators.MANAGEMENT_DROPDOWN)
            self.click_on_element(management_dropdown)
            users_option = self.find_element(driver, self.locators.MANAGEMENT_USERS_OPTION)
            self.click_on_element(users_option)
        finally:
            if self.wait_url_contains(driver, user_management_page_url, delay):
                return True
            else:
                return False

    def set_entity_permissions(self, permissions_group_id, local_permissions_group_name,
                                        local_permissions_entity_name, local_sub_module_name):
        query_entity_name = "SELECT * FROM local_permission_entities WHERE permissionGroupId = " + permissions_group_id + " and name = " + local_permissions_entity_name + ""
        query_insert_view = "INSERT INTO local_permission_entities " \
                            "('brokerId', 'name', 'moduleId', 'hasView', 'hasEdit', 'hasCreate', 'enableEdit', 'enableCreate', 'permissionGroupId', 'submoduleId') " \
                            "VALUES(100001, " + local_permissions_entity_name + ", (SELECT id FROM local_modules WHERE name = " + local_permissions_entity_name + "), 1, 0, 0, 0, 0, " \
                            "(SELECT id FROM local_permission_groups WHERE name = " + local_permissions_group_name + "), " \
                            " (SELECT id FROM local_sub_modules WHERE name = " + local_sub_module_name + "))"
        query_update_view = "UPDATE local_permission_entities SET hasView = 1, hasEdit = 0, hasCreate = 0" \
                            " WHERE name = " + local_permissions_entity_name + " AND permissionGroupId = " + permissions_group_id + ""

        try:
            query_entity_name_result = Instruments.run_mysql_query(query_entity_name)
            if query_entity_name_result is None:
                Instruments.run_mysql_query(query_insert_view)
                return True
            else:
                Instruments.run_mysql_query(query_update_view)
                return True
        except AutomationError as e:
            print("{0} set_entity_permissions failed with error. {1}".format(e.__class__.__name__,
                                                                                      e.__cause__))
            return False


    def update_view_edit_create_permissions(self, local_permissions_entity_name, permissions_group_id, flag = 0):
        # flag = 1 : update permissions  to view and edit,
        # flag = 2 : update permissions to view , edit and create
        if flag == 0:
            part = "hasView = 0, hasEdit = 0, hasCreate = 0"
        elif flag == 1:
            part = "hasView = 1, hasEdit = 1, hasCreate = 0"
        elif flag == 2:
            part = "hasView = 1, hasEdit = 1, hasCreate = 1"
        query_update_view_edit = "UPDATE local_permission_entities SET " + part + " WHERE name = " + local_permissions_entity_name + " AND permissionGroupId = " + permissions_group_id + ""
        try:
            Instruments.run_mysql_query(query_update_view_edit)
            return True
        except AutomationError as e:
            print("{0} update_view_edit_permissions failed with error. {1}".format(e.__class__.__name__,
                                                                          e.__cause__))
        return False


    # def update_view_edit_create_permissions(self, local_permissions_entity_name, permissions_group_id):
    #     query_update_view_edit_create = "UPDATE local_permission_entities SET hasView = 1, hasEdit = 1, hasCreate = 1" \
    #                                     " WHERE name = " + local_permissions_entity_name + " AND permissionGroupId = " + permissions_group_id + ""
    #     try:
    #         Instruments.run_mysql_query(query_update_view_edit_create)
    #         return True
    #     except AutomationError as e:
    #         print("{0} update_view_edit_create_permissions failed with error. {1}".format(e.__class__.__name__,
    #                                                                       e.__cause__))
    #     return False