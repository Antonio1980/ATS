# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import unpack, ddt, data
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.login_page import LogInPage
from src.test_utils.file_utils import write_file_result, get_csv_data


@ddt
@test(groups=['open_account_page', ])
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.test_case = '3832'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ])
    @data(*get_csv_data(BaseConfig.WTP_LOGIN_DATA))
    @unpack
    def test_login_positive(self, email, password):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            result2 = self.login_page.login_ddt(self.driver, email, password)
        finally:
            if result1 & result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)