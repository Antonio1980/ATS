# !/usr/bin/env python
# -*- coding: utf8 -*-
import time
import unittest
from datetime import datetime, date

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
class AddNewLeadTest(unittest.TestCase):       #before RUNNING  of test - USE "create_customer_new" precondition
    def setUp(self):
        self.test_case = '3415'
        self.login_page = LogInPage()
        self.home_page = HomePage()
        self.customer_page = CustomerPage()
        self.email = self.login_page.email
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.password = self.login_page.password
        self.results_file = BaseConfig.CRM_TESTS_RESULT

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_add_new_lead_account(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:


            step1= self.login_page.login(self.driver, self.login_page.login_username, self.login_page.login_password)
            #list_id = Instruments.run_mysql_query("SELECT id FROM customers WHERE email LIKE '%@guerrillamailblock.com' AND registrationStep < 8 ORDER BY regTime DESC")
            list_id = Instruments.get_customer_id_new_details(BaseConfig.CUSTOMER_NEW, 0, 0)
            customer_id_from_csv = list_id['customer_id']
            step2 = True
            dropdown_quick_search = Browser.wait_element_presented(self.driver, self.home_page.locators.CUSTOMER_DROPDOWN, delay)
            Browser.click_on_element(dropdown_quick_search)
            customer_id_option = Browser.wait_element_presented(self.driver, self.home_page.locators.CUSTOMER_ID_OPTION, delay)
            Browser.click_on_element(customer_id_option)
            quick_search_field = Browser.wait_element_presented(self.driver, self.home_page.locators.QUICK_SEARCH_VALUE, delay)
            Browser.send_keys(quick_search_field, customer_id_from_csv)
            quick_search_button = Browser.find_element_by(self.driver, self.home_page.locators.SHOW_RESULTS_BUTTON_ID, "id")
            Browser.click_on_element(quick_search_button)
            time.sleep(3)
            new_window = self.driver.window_handles
            Browser.switch_window(self.driver, new_window[1])
            time.sleep(3)
            customer_id_from_page = Browser.execute_js(self.driver, self.home_page.script_get_val)
            customer_id = customer_id_from_page.split()
            if (str(customer_id_from_csv) == customer_id[2]):
                step3 = True
            else:
                step3 = False



        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
