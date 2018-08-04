# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.customer_page import CustomerPage
from src.base.instruments import write_file_result, update_test_case, get_csv_data


@ddt
@test(groups=['customer_page', ])
class CustomerUpgradeStatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3408'
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.customer_page = CustomerPage()
        cls.username = cls.login_page.login_username
        cls.password = cls.login_page.login_password
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.CRM_TESTS_RESULT
        cls.customer_id = cls.login_page.customer_id
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', ])
    @data(*get_csv_data(BaseConfig.CRM_DEPOSIT_DETAILS))
    @unpack
    def test_customer_status_upgrade(self, payment_option, company_option, status_option, currency_option, deposit_amount):
        customer_status = 'Depositor'
        payment_details = {'payment_option': payment_option, 'company_option': company_option, 'status_option': status_option,
                           'currency_option': currency_option, 'deposit_amount': deposit_amount}
        result1, result2, result3, result4 = False, False, False, None
        try:
            result1 = self.login_page.login(self.driver, self.username, self.password)
            result2 = self.home_page.choose_customer_by_option(self.driver, self.customer_id, 1)
            result3 = self.customer_page.make_deposit(self.driver, payment_details)
            result4 = self.customer_page.check_customer_icon(self.driver)
        finally:
            if result1 and result2 and result3 is True and result4 == customer_status:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDown(cls):
        cls.login_page.close_browser(cls.driver)
