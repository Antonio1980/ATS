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
class CustomerUpgradeStatusTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3408'
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.customer_page = CustomerPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.CRM_TESTS_RESULT
        self.username = self.login_page.login_username
        self.password = self.login_page.login_password
        self.customer_id = self.login_page.customer_id

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_customer_status_upgrade(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        customer_status = 'Depositor'
        payment_details = {'payment_option': 'Credit', 'company_option': 'DX', 'status_option': 'Approved',
                           'currency_option': 'USD', 'deposit_amount': 100}
        result1, result2, result3, result4 = False, False, False, None
        try:
            result1 = self.login_page.login(self.driver, self.username, self.password)
            # Option 1 - ID, Option 2 - , Option 3- ;
            result2 = self.home_page.choose_customer_by_option(self.driver, self.customer_id, 1)
            result3 = self.customer_page.make_deposit(self.driver, payment_details)
            result4 = self.customer_page.check_customer_icon(self.driver)
        finally:
            if result1 and result2 and result3 is True and result4 == customer_status:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
