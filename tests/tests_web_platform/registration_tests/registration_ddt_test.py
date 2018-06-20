# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.open_account_page import OpenAccountPage


@ddt
@test(groups=['open_account_page', ])
class RegistrationTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.open_account_page = OpenAccountPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = ''
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'ddt', 'negative', ])
    @data(*get_csv_data(BaseConfig.OPEN_ACCOUNT_DATA))
    @unpack
    def test_registration_ddt(self, firstname, lastname, email, password):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = self.open_signup_page(self.driver, delay)
            result2 = self.registration_flow_ddt(self.driver, firstname, lastname, email, password)
        finally:
            if (result1 & result2) is True:
                update_test_case(self.test_run, self.test_case, 1)
            else:
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
