# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from tests.tests_crm_bo.pages import login_page, home_page
from tests.drivers.webdriver_factory import WebDriverFactory


@test(groups=['login_page', ])
class LogInLogOutLogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = login_page.LogInPage()
        cls.home_page = home_page.HomePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '2598'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['sanity', 'functional', 'positive', ])
    def test_login_logout_login(cls):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.login_page.login_positive(cls.driver, delay)
            result2 = cls.home_page.logout(cls.driver, delay)
            result3 = cls.login_page.login_positive(cls.driver, delay)
        finally:
            if (result1 & result2 & result3) is True:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)

