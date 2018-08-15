# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.customer_page import CustomerPage
from src.base.instruments import Instruments


@test(groups=['customer_page', ])
class AddDepositTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3409'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.customer_page = CustomerPage()
        cls.username = cls.login_page.login_username
        cls.password = cls.login_page.login_password
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.home_page.CRM_TESTS_RESULT
        cls.customer_id = cls.login_page.customer_id
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_add_deposit(self):
        payment_details = {'payment_option': 'Credit', 'company_option': 'DX', 'status_option': 'Approved',
                           'currency_option': 'USD', 'deposit_amount': 100}
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.login_page.login(self.driver, self.username, self.password)
            # Option 1 - ID, Option 2 - , Option 3- ;
            result2 = self.home_page.choose_customer_by_option(self.driver, self.customer_id, 1)
            result3 = self.customer_page.make_deposit(self.driver, payment_details)
            result4 = self.customer_page.check_balance(self.driver)
        finally:
            if result1 and result2 is True & (result3 & result4 is True):
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
