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
class AddNewLeadTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3415'
        self.login_page = LogInPage()
        self.home_page = HomePage()
        self.customer_page = CustomerPage()
        self.email = self.login_page.email
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.password = self.login_page.password
        self.results = BaseConfig.CRM_TESTS_RESULT

    @test(groups=['sanity', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_add_new_lead_account(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.login_page.login(self.driver, self.login_page.email, self.login_page.password)

        finally:
            if result1 and result2 and result3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
