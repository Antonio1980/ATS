# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.customer_page import CustomerPage
from tests.tests_crm_bo.locators import users_permissions_checking_locators


@ddt
@test(groups=['customer_page', ])
class CustomersQuickSearch(unittest.TestCase):
    def setUp(self):
        self.test_case = '6306'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.locators = users_permissions_checking_locators
        self.customer_page = CustomerPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.CRM_TESTS_RESULT
        self.username = self.home_page.username_permissions
        self.password = self.home_page.password_permissions
        self.customer_id = self.login_page.customer_id
        self.permissions_group_id = self.home_page.permissions_group_id
        self.local_permissions_group_name = self.home_page.local_permissions_group_name
        self.local_permissions_entity_name = "'Customers - Search'"
        self.local_sub_module_name = "'Customers - Quick Search'"
        self.local_permissions_entity_customers = "'Customers'"
        self.local_sub_module_name_customers = "'Customers'"
        self.local_permissions_entity_communicator = "'Communicator'"
        self.local_sub_module_name_communicator = "'Communicator'"
        self.local_permissions_entity_reports = "'Reports'"
        self.local_sub_module_name_reports = "'Reports'"
        self.local_permissions_entity_management = "'Management'"
        self.local_sub_module_name_management = "'Management'"

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_customers_permission_test(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11, step12, step13, step14\
            = False, False, False, False, False, False, False, False, False, False, False, False, False, False
        try:

            # set customer menu hasView = 1, hasEdit = 0, hasCreate = 0
            self.home_page.set_entity_permissions(self.permissions_group_id,
                                                            self.local_permissions_group_name,
                                                            self.local_permissions_entity_customers,
                                                            self.local_sub_module_name_customers)
            # update customer menu   hasView = 1, hasEdit = 1 , hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_customers,
                                                                         self.permissions_group_id, 2)
            step1 = True

            # set communicator menu hasView = 1, hasEdit = 0, hasCreate = 0
            self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_communicator,
                                                          self.local_sub_module_name_communicator)
            # update communicator   hasView = 1, hasEdit = 1 , hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_communicator,
                                                                       self.permissions_group_id, 2)
            step2 = True

            # set reports menu hasView = 1, hasEdit = 0, hasCreate = 0
            self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_reports,
                                                          self.local_sub_module_name_reports)
            # update reports menu   hasView = 1, hasEdit = 1 , hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_reports,
                                                                       self.permissions_group_id, 2)

            step3 = True

            # set management menu hasView = 1, hasEdit = 0, hasCreate = 0
            self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_management,
                                                          self.local_sub_module_name_management)
            # update management menu   hasView = 1, hasEdit = 1 , hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_management,
                                                                       self.permissions_group_id, 2)
            step4 = True


            # set entity permissions_view
            step5 = self.home_page.set_entity_permissions(self.permissions_group_id,
                                                            self.local_permissions_group_name,
                                                            self.local_permissions_entity_name,
                                                            self.local_sub_module_name)

            step6 = self.login_page.login(self.driver, self.username, self.password)
            assert Browser.wait_element_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.REPORTS_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.COMMUNICATOR_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step7 = True
            # update method with  1  : hasView = 1, hasEdit = 1, hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name, self.permissions_group_id, 1)
            Browser.refresh_page(self.driver)
            assert Browser.wait_element_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.REPORTS_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.COMMUNICATOR_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step8 = True
            # update method with  2  : hasView = 1, hasEdit = 1, hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 2)
            Browser.refresh_page(self.driver)
            assert Browser.wait_element_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.REPORTS_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.COMMUNICATOR_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step9 = True

            # remove customer from menu   hasView = 0, hasEdit = 0 , hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_customers,
                                                                       self.permissions_group_id, 0)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.REPORTS_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.COMMUNICATOR_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step10 = True

            # remove communicator  from menu  hasView = 0, hasEdit = 0 , hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_communicator,
                                                                       self.permissions_group_id, 0)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.REPORTS_MENU, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.COMMUNICATOR_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step11 = True
            # remove reports from menu   hasView = 0, hasEdit = 0 , hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_reports,
                                                                       self.permissions_group_id, 0)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.REPORTS_MENU, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.COMMUNICATOR_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step12 = True
            # remove management from menu   hasView = 0, hasEdit = 0 , hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_management,
                                                                       self.permissions_group_id, 0)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.REPORTS_MENU, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.COMMUNICATOR_MENU, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step13 = True
            # remove quick search from page   hasView = 0, hasEdit = 0 , hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 0)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.QUICK_SEARCH_DROPDOWN_BUTTON, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.QUICK_SEARCH_VALUE_FIELD, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.QUICK_SEARCH_BUTTON, delay)
            step14 = True

        finally:
            if step1 and step2 and step3 and step4 and step5 and step6 and step7 \
                   and step8 and step9 and step10 and step11 and step12 and step13 and step14 is True:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
