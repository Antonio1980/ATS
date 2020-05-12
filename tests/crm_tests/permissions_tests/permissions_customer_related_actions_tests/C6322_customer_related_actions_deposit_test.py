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
class TestCustomerRelatedActionsDeposit(unittest.TestCase):
    def setUp(self):
        self.test_case = '6322'
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
        self.local_permissions_entity_name = "'Customer Related Actions - Deposit'"
        self.local_sub_module_name = "'Customer Related Actions - Deposit'"
        self.local_permissions_entity_customers = "'Customers'"
        self.local_sub_module_name_customers = "'Customers'"
        self.local_permissions_entity_name_page = "'Customer Page'"
        self.local_sub_module_name_page = "'Customer Page'"

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_customer_permission_test(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6, step7, step8, step9, step10 = False, False, False, False, False, \
                                                                                False, False, False, False, False
        try:
            # set customer menu   hasView = 1, hasEdit = 0, hasCreate = 0
            step1 = self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_customers,
                                                          self.local_sub_module_name_customers)
            # update customer menu   hasView = 1, hasEdit = 1, hasCreate = 1
            step2 = self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_customers,
                                                                       self.permissions_group_id, 2)

            # set customer Page    hasView = 1, hasEdit = 0, hasCreate = 0
            step3 = self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_name_page,
                                                          self.local_sub_module_name_page)
            # update customer Page menu   hasView = 1, hasEdit = 1, hasCreate = 1
            step4 = self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name_page,
                                                                       self.permissions_group_id, 2)
            # set entity permissions hasView = 1, hasEdit = 0, hasCreate = 0
            step5 = self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_name,
                                                          self.local_sub_module_name)
            step6 = self.home_page
            step7 = self.login_page.login(self.driver, self.username, self.password)
            customers_dropdown_button = Browser.wait_element_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            Browser.click_on_element(customers_dropdown_button)
            deposits_withdrawals_dropdown_title = Browser.wait_element_presented(self.driver,
                                                                                 self.locators.DEPOSITS_WITHDRAWALS_DROPDOWN_TITLE,
                                                                                 delay)
            Browser.click_on_element(deposits_withdrawals_dropdown_title)
            assert Browser.wait_element_presented(self.driver,
                                                  self.locators.DEPOSITS_WITHDRAWALS_TITLE_ON_DEPOSITS_WITHDRAWL_PAGE,
                                                  delay)
            assert Browser.wait_element_presented(self.driver,
                                                  self.locators.DEPOSITS_TITLE_ON_DEPOSITS_BLOCK,
                                                  delay)
            customer_id_deposit_list = Browser.find_elements(self.driver,
                                                       self.locators.CUSTOMER_ID_LIST_ON_DEPOSITS_PAGE)
            first_customer_id_deposit = customer_id_deposit_list[0]

            assert Browser.wait_element_presented(self.driver, first_customer_id_deposit, delay)
            Browser.click_on_element(first_customer_id_deposit)
            assert Browser.wait_element_presented(self.driver,
                                                  self.locators.DEPOSITS_WITHDRAWLS_TITLE_TAB_ON_CUSTOMER_PAGE,
                                                  delay)
            id_deposit = Browser.find_elements(self.driver,
                                               self.locators.NOT_EDIT_ID_DEPOSITS_ON_CUSTOMER_PAGE)
            first_customer_id_deposit = id_deposit[0]
            assert Browser.wait_element_presented(self.driver, first_customer_id_deposit, delay)
            assert Browser.check_element_not_presented(self.driver,
                                                       self.locators.EDIT_ID_DEPOSITS_LINK_ON_CUSTOMER_PAGE, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.ADD_NEW_DEPOSIT_BUTTON, delay)
            step8 = True
            # update method with  1  : hasView = 1, hasEdit = 1, hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 1)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.ADD_NEW_DEPOSIT_BUTTON, delay)
            edit_deposit_id_list = Browser.find_elements(self.driver,
                                                         self.locators.EDIT_ID_DEPOSITS_LINK_ON_CUSTOMER_PAGE)
            first_deposit_id_link = edit_deposit_id_list[0]
            Browser.click_on_element(first_deposit_id_link)
            assert Browser.wait_element_presented(self.driver, self.locators.EDIT_DEPOSIT_DETAILS_TITLE_ON_MODAL_WIN,
                                                  delay)
            close_button_for_modal_edit_deposit = Browser.wait_element_presented(self.driver,
                                                                                 self.locators.CLOSE_BUTTON_ON_MODAL_FOR_EDIT_DEPOSIT,
                                                                                 delay)
            Browser.click_on_element(close_button_for_modal_edit_deposit)
            step9 = True
            # update method with  2  : hasView = 1, hasEdit = 1, hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 2)
            Browser.refresh_page(self.driver)
            assert Browser.wait_element_presented(self.driver, first_deposit_id_link, delay)
            add_new_deposit_button = Browser.wait_element_presented(self.driver, self.locators.ADD_NEW_DEPOSIT_BUTTON,
                                                                    delay)
            Browser.click_on_element(add_new_deposit_button)
            assert Browser.wait_element_presented(self.driver, self.locators.NEW_DEPOSIT_REQUEST_TITLE_ON_MODAL_WINNEW,
                                                  delay)
            step10 = True
        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 and step10 is True:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
