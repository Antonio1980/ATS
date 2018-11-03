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
class CustomerRelatedActionsSendEmail(unittest.TestCase):
    def setUp(self):
        self.test_case = '6323'
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
        self.local_permissions_entity_name = "'Customer Related Actions - Send Email'"
        self.local_sub_module_name = "'Customer Related Actions - Send Email'"
        self.local_permissions_entity_customers = "'Customers'"
        self.local_sub_module_name_customers = "'Customers'"
        self.local_permissions_entity_name_page = "'Customer Page'"
        self.local_sub_module_name_page = "'Customer Page'"

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_customer_permission_test(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6, step7, step8, step9, step10 = \
            False, False, False, False, False, False, False, False, False, False
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
            # set entity permissions : hasView = 1, hasEdit = 0, hasCreate = 0
            step5 = self.home_page.set_entity_permissions(self.permissions_group_id,
                                                          self.local_permissions_group_name,
                                                          self.local_permissions_entity_name,
                                                          self.local_sub_module_name)
            step6 = self.home_page
            step7 = self.login_page.login(self.driver, self.username, self.password)
            customers_dropdown_button = Browser.wait_element_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            Browser.click_on_element(customers_dropdown_button)
            quick_customers_approval_title = Browser.wait_element_presented(self.driver,
                                                                     self.locators.QUICK_CUSTOMER_APPROVAL_DROPDOWN_TITLE, delay)
            Browser.click_on_element(quick_customers_approval_title)
            assert Browser.wait_element_presented(self.driver, self.locators.QUICK_CUSTOMER_APPROVAL_TITLE_ON_QUICK_CUSTOMER_APPROVAL_PAGE, delay)
            assert Browser.check_element_not_presented(self.driver, self.locators.EDIT_MAIL_ON_QUICK_CUSTOMERS_APPROVAL, delay)
            step8 = True
            # update method with  1  : hasView = 1, hasEdit = 1, hasCreate = 0
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 1)
            Browser.refresh_page(self.driver)
            assert Browser.check_element_not_presented(self.driver, self.locators.EDIT_MAIL_ON_QUICK_CUSTOMERS_APPROVAL,
                                                       delay)
            step9 = True
            # update method with  2  : hasView = 1, hasEdit = 1, hasCreate = 1
            self.home_page.update_view_edit_create_permissions(self.local_permissions_entity_name,
                                                               self.permissions_group_id, 2)
            Browser.refresh_page(self.driver)
            send_email_button = Browser.wait_element_presented(self.driver, self.locators.EDIT_MAIL_ON_QUICK_CUSTOMERS_APPROVAL, delay)
            Browser.click_on_element(send_email_button)
            Browser.wait_element_presented(self.driver, self.locators.SEND_EMAIL_TITLE_ON_MODAL_WIN, delay)
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
