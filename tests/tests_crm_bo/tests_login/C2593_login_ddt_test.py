# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from src.test_utils.file_utils import get_csv_data, write_file_result


@ddt
@test(groups=['login_page', ])
class LogInTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '2593'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'ddt', 'positive', ])
    @data(*get_csv_data(BaseConfig.CRM_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.login_page.login(self.driver, delay, username, password)
            result2 = self.home_page.logout(self.driver, delay)
        finally:
            if result1 & result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
