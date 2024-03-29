import unittest
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.locators import permissions_locators


@ddt
class TestManagementsPermissions(unittest.TestCase):
    def setUp(self):
        self.test_case = '6317'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.locators = permissions_locators
        self.customer_page = CustomerPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.username = self.home_page.username_permissions
        self.password = self.home_page.password_permissions
        self.customer_id = self.login_page.customer_id
        self.permissions_group_id = self.home_page.permissions_group_id
        self.local_permissions_group_name = self.home_page.local_permissions_group_name
        self.local_permissions_entity_name = "'Permissions'"
        self.local_sub_module_name = "'Permissions'"
        self.local_permissions_entity_management = "'Management'"
        self.local_sub_module_name_management = "'Management'"

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_management_permission_test(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6, step7 = False, False, False, False, False, False, False
        try:
            # set communicator menu   hasView = 1, hasEdit = 0, hasCreate = 0
            step1 = self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_management,
                                                          self.local_sub_module_name_management)
            # update communicator menu   hasView = 1, hasEdit = 1, hasCreate = 1
            step2 = self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_management,
                                                                       self.permissions_group_id, 2)
            # set entity permissions
            step3 = self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_name,
                                                          self.local_sub_module_name)
            step4 = self.login_page.login(self.driver, self.username, self.password)
            management_dropdown_button = Browser.find_element_by(self.driver, self.locators.MANAGEMENT_MENU_ID, "id")
            Browser.click_on_element(management_dropdown_button)
            users_dropdown_title = Browser.wait_element_presented(self.driver,
                                                                  self.locators.PERMISSIONS_DROPDOWN_TITLE, delay)
            Browser.click_on_element(users_dropdown_title)
            assert Browser.wait_element_presented(self.driver, self.locators.PERMISSIONS_TITLE_ON_PERMISSIONS_PAGE, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.CREATE_PERMISSIONS_GROUP_BUTTON,
                                                       delay)
            edit_permissions_group_links_list = Browser.find_elements(self.driver,
                                                                      self.locators.EDIT_LINK_FOR_PERMISSIONS)
            edit_first_link_permissioms_group = edit_permissions_group_links_list[0]
            assert Browser.wait_element_presented(self.driver, edit_first_link_permissioms_group, delay)
            Browser.click_on_element(edit_first_link_permissioms_group)
            assert Browser.wait_element_presented(self.driver, self.locators.CHECKBOX_FOR_CREATE_OPTION_OF_COMMUNICATOR_PERMISSIONS_DISABLED, delay)
            Browser.go_back(self.driver)
            step5 = True
            # update method with  1  : hasView = 1, hasEdit = 1, hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 1)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.CREATE_PERMISSIONS_GROUP_BUTTON,
                                                       delay)
            assert Browser.wait_element_presented(self.driver, edit_first_link_permissioms_group, delay)
            Browser.click_on_element(edit_first_link_permissioms_group)
            assert Browser.wait_element_presented(self.driver, self.locators.CHECKBOX_FOR_CREATE_OPTION_OF_COMMUNICATOR_PERMISSIONS, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.CHECKBOX_FOR_CREATE_OPTION_OF_COMMUNICATOR_PERMISSIONS_DISABLED,
                                                       delay)
            Browser.go_back(self.driver)
            step6 = True
            # update method with  2  : hasView = 1, hasEdit = 1, hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 2)
            Browser.refresh_page(self.driver)
            assert Browser.wait_element_presented(self.driver,  edit_first_link_permissioms_group, delay)
            create_permissions_group_button = Browser.wait_element_presented(self.driver,
                                                                           self.locators.CREATE_PERMISSIONS_GROUP_BUTTON,
                                                                           delay)
            Browser.click_on_element(create_permissions_group_button)
            assert Browser.wait_element_presented(self.driver, self.locators.CREATE_NEW_PERMISSIONS_GROUP_TITLE_ON_CREATE_NEW_PERMISSIOMS_GROUP_PAGE,
                                                  delay)
            step7 = True
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 is True:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)