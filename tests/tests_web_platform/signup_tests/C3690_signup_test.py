# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['open_account_page', 'e2e', ])
class SignUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.open_account_page = SignUpPage()
        cls.email = cls.open_account_page.email
        cls.password = "1Aa@<>12"
        cls.first_last_name = "QAtestQA"
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3690'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.flag = False

    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_signup_positive(self):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.open_account_page.fill_signup_form(self.driver, self.first_last_name, self.email, self.password)
        finally:
            if result1 and result2 is True:
                self.flag = True
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        if cls.flag is True:
            write_file_result(cls.first_last_name + "," + cls.email + "," + cls.password + "\n", BaseConfig.WTP_TESTS_CUSTOMERS)
        cls.home_page.close_browser(cls.driver)
