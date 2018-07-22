# !/usr/bin/env python
# -*- coding: utf8 -*-

# Import dependencies
import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import write_file_result, update_test_case


# High level tests ordering - per page.
@test(groups=['login_page', ])
# LogInTest class declaration.
# Inheritance from unittest framework class.
class LogInTest(unittest.TestCase):
    # Annotation for unittest framework (dependency injection).
    @classmethod
    # SetUp function definition (executes before test).
    def setUpClass(cls):
        # Composition technique:
        # Local instance of the LogInPage class.
        cls.login_page = LogInPage()
        # Class attributes.
        cls.test_case = '2590'
        cls.username = cls.login_page.username
        cls.password = cls.login_page.password
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        # Set up browser via WebDriverFactory class.
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    # Low level tests ordering - per test suites.
    @test(groups=['smoke', 'functional', 'positive', ])
    # Test method, name must start with "test..."
    def test_login_positive(self):
        # Test result before execution.
        result = False
        try:
            # Calling login_positive method from LogInPage class,
            # If sign_in passed successfully it will return True.
            result = self.login_page.login(self.driver, self.username, self.password)
        finally:
            # Result validation.
            if result is True:
                # Save test result into csv file.
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                # Update test rail report with "Passed".
                update_test_case(self.test_run, self.test_case, 1)
            else:
                # Save test result into csv file.
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                # Update test rail report with "Failure".
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    # CleanUp method executes after test.
    def tearDownClass(cls):
        # Calling clean up method from Browser via LogInPage class.
        cls.login_page.close_browser(cls.driver)
