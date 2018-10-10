# !/usr/bin/env python
# -*- coding: utf8 -*-

# Import dependencies
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


# Data Driven dependency.
@ddt
# High level tests ordering - per page.
@test(groups=['login_page', ])
# LogInTest class declaration.
# Inheritance from unittest framework class.
class LogInTest(unittest.TestCase):
    # SetUp function definition (executes before test).
    def setUp(self):
        # Composition technique:
        # Local instance of the LogInPage class.
        self.login_page = LogInPage()
        # Class attributes.
        self.test_case = '2590'
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.username = self.login_page.login_username
        self.password = self.login_page.login_password
        self.results_file = BaseConfig.CRM_TESTS_RESULT

    # Low level tests ordering - per test suites.
    @test(groups=['smoke', 'positive', ])
    # Data from csv file injection (browser names).
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    # Unpacking data from csv file and passing it to test method.
    @unpack
    # Test method, name must start with "test..."
    def test_login_positive(self, browser):
        # Set up browser via WebDriverFactory class.
        self.driver = WebDriverFactory.get_browser(browser)
        # Test step result before execution (by default).
        step1 = False
        try:
            # Calling login_positive method from LogInPage class,
            # If sign_in passed successfully it will return True.
            step1 = self.login_page.login(self.driver, self.username, self.password)
        finally:
            # Result validation.
            if step1 is True:
                # Save test result into csv file (not in use).
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                # Update test rail report with "Passed".
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Save test result into csv file (not in use).
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                # Update test rail report with "Failure".
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    # CleanUp method executes after test.
    def tearDown(self):
        # Calling clean up method from Browser class.
        Browser.close_browser(self.driver)
