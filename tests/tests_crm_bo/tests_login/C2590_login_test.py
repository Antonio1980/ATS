# !/usr/bin/env python
# -*- coding: utf8 -*-

# Import dependencies
import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory


# High level tests ordering - per page
@test(groups=['login_page', ])
# LogInTest class declaration
# Inheritance from unittest framework class
class LogInTest(unittest.TestCase):
    # Anotation for unittest framework
    @classmethod
    # SetUp function definition (executes before test)
    def setUpClass(cls):
        # Composition technique:
        # Local instance of the LogInPage class
        cls.login_page = LogInPage()
        # Set up browser (chrome_driver current implementation) via WebDriverFactory class
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        # Class attributes
        cls.test_case = '2590'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    # Low level tests ordering - per test suites
    @test(groups=['smoke', 'functional', 'positive', ])
    # Test method, name must start with "test..."
    def test_login_positive(self):
        # Default time out for Browser methods in seconds
        delay = 1
        # Test result befor execution
        result = False
        try:
            # Calling login_positive method from LogInPage class
            # If login passed successfully it will return True
            result = self.login_page.login(self.driver, delay)
        finally:
            # Result validation
            if result is True:
                # Save test result into csv file.
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                # Update test rail report with "Passed"
                update_test_case(self.test_run, self.test_case, 1)
            else:
                # Save test result into csv file.
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                # Update test rail report with "Failure"
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    # CleanUp method executes after test
    def tearDownClass(cls):
        # Calling clean up method from Browser via LogInPage class 
        cls.login_page.close_browser(cls.driver)
