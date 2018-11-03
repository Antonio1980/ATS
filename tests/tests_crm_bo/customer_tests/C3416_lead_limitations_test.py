# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
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


@ddt
@test(groups=['customer_page', ])
class LeadLimitationsTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3416'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.customer_page = CustomerPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.CRM_TESTS_RESULT
        self.username = self.login_page.login_username
        self.password = self.login_page.login_password


    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_customer_status_upgrade(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5 = False, False, False, False, False
        try:
            customer_id_list = "SELECT id FROM customers WHERE registrationStep = 8 and status = 3  AND firstDepositDate = '0000-00-00 00:00:00' "
            customer_id = Instruments.run_mysql_query(customer_id_list)[0][-1]
            step1 = self.login_page.login(self.driver, self.username, self.password)
            # Option 1 - ID, Option 2 - , Option 3- ;
            step2 = self.home_page.choose_customer_by_option(self.driver, customer_id, 1)
            attribute = self.customer_page.check_customer_icon(self.driver)
            if attribute == 'Customer':
                step3 = True
            assert Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_BALANCE_FIELD)
            assert Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_ACCOUNT_INFORMATION_AREA)
            customer_admin_tab = Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_ADMIN_TAB)
            personal_information_tab = Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_PERSONAL_INFORMATION_TAB)
            Browser.click_on_element(customer_admin_tab)
            Browser.click_on_element(personal_information_tab)
            assert Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_PASSWORD_ICON)
            assert Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_BALANCE_TAB)
            assert Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_TRADES_TAB)
            assert Browser.find_element(self.driver, self.customer_page.locators.CUSTOMER_FEES_TAB)
            step3 = True
            customer_id_lead_list = "SELECT id FROM customers WHERE registrationStep < 8 and status < 3"
            customer_id_lead = Instruments.run_mysql_query(customer_id_lead_list)[0][0]
            step4 = self.home_page.choose_customer_by_option(self.driver, customer_id_lead, 1)
            Browser.wait_number_of_windows(self.driver, 3, delay)
            new_window = self.driver.window_handles[1]
            Browser.switch_window(self.driver, new_window)
            attribute1 = self.customer_page.check_customer_icon(self.driver)
            text = Browser.get_cur_url(self.driver)
            print(text)
            if attribute1 == 'Lead':
                step5 = True
            #assert Browser.check_element_not_presented(self.driver, self.customer_page.locators.CUSTOMER_BALANCE_FIELD, delay)
            assert Browser.check_element_not_presented(self.driver, self.customer_page.locators.CUSTOMER_ACCOUNT_INFORMATION_AREA, delay)
            assert Browser.check_element_not_presented(self.driver, self.customer_page.locators.CUSTOMER_BALANCE_TAB, delay)
            assert Browser.check_element_not_presented(self.driver, self.customer_page.locators.CUSTOMER_TRADES_TAB, delay)
            assert Browser.check_element_not_presented(self.driver, self.customer_page.locators.CUSTOMER_FEES_TAB, delay)
            Browser.click_on_element(customer_admin_tab)
            Browser.click_on_element(personal_information_tab)
            assert Browser.check_element_not_presented(self.driver, self.customer_page.locators.CUSTOMER_PASSWORD_ICON, delay)



        finally:
            if step1 and step2 and step3 and step4 and step5 is True:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
