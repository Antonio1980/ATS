# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['sign_up_page', 'e2e', ])
class SignUpPageUITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '4431'
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.test_run = cls.home_page.TESTRAIL_RUN
        cls.results = cls.home_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'functional', 'positive', ], depends_on_groups=["smoke", ])
    def test_sign_up_page_ui(self):
        delay = 1
        step1, step2 = False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.signup_ui_test(self.driver, delay)
        finally:
            if step1 and step2 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
