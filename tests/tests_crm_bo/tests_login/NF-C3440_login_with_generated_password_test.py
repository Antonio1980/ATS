# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.customer_page import CustomerPage


@test(groups=['login_page', ])
class LogInGeneratePasswordTest(unittest.TestCase, LogInPage, HomePage, CustomerPage):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.customer_page = CustomerPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3440'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['sanity', 'functional', 'positive', ])
    def test_login_with_generated_password(cls):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.login_page.login(cls.driver, delay)

        finally:
            if (result1 & result2 & result3) is True:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDown(cls):
        cls.login_page.close_browser(cls.driver)
