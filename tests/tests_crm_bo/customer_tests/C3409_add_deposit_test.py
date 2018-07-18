# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.customer_page import CustomerPage
from src.base.engine import write_file_result, update_test_case


@test(groups=['customer_page', ])
class AddDepositTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.customer_page = CustomerPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3409'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.username = cls.login_page.username
        cls.password = cls.login_page.password

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_add_deposit(self):
        delay = 1
        amount = 100
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.login_page.login(self.driver, self.username, self.password)
            result2 = self.home_page.choose_customer_by_name(self.driver, delay)
            result3 = self.customer_page.make_deposit(self.driver, delay, amount)
            result4 = self.customer_page.check_balance(self.driver, delay)
        finally:
            if result1 and result2 is True & (result3 & result4 is True):
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
