# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from src.base.instruments import write_file_result, update_test_case, get_csv_data


@ddt
@test(groups=['sign_up_page', ])
class SignUpDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3961'
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*get_csv_data(BaseConfig.OPEN_ACCOUNT_DATA))
    @unpack
    def test_sign_up_ddt(self, first_last_name, email, password):
        delay = 1
        result1, result2 = False, True
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, first_last_name, email, password)
        finally:
            if result1 is True and result2 is False:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
