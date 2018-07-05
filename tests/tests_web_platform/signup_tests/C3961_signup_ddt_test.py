# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from src.test_utils.file_utils import get_csv_data, write_file_result
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['open_account_page', ])
class RegistrationTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.open_account_page = SignUpPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3961'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*get_csv_data(BaseConfig.OPEN_ACCOUNT_DATA))
    @unpack
    def test_registration_ddt(self, first_last_name, email, password):
        delay = 1
        result1, result2 = False, True
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.open_account_page.fill_signup_form(self.driver, first_last_name, email, password)
        finally:
            if result1 is True and result2 is False:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
