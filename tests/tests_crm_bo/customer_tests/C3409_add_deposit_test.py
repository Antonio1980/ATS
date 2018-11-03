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


@ddt
@test(groups=['customer_page', ])
class AddDepositTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3409'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.customer_page = CustomerPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.CRM_TESTS_RESULT
        self.username = self.login_page.login_username
        self.password = self.login_page.login_password
        self.customer_id = self.login_page.customer_id

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_add_deposit(self, browser):
        query = "SELECT SUM(amount) FROM deposits WHERE customerId=" + self.customer_id + " and currencyId=1"
        new_query = "SELECT SUM(amount) FROM deposits WHERE customerId=" + self.customer_id + " and currencyId=1"
        amount_before = Instruments.run_mysql_query(query)[0][0]
        if amount_before is None:
            amount_before = 0
        self.driver = WebDriverFactory.get_driver(browser)
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.login_page.login(self.driver, self.username, self.password)
            # Option 1 - ID, Option 2 - , Option 3- ;
            step2 = self.home_page.choose_customer_by_option(self.driver, self.customer_id, 1)
            step3 = self.customer_page.make_deposit(self.driver)
            amount_after = Instruments.run_mysql_query(new_query)[0][0]
            if int(amount_after) - int(amount_before) == int(100.00000000):
                step4 = True
        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
