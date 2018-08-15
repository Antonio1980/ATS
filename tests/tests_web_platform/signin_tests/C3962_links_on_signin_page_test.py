# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage


@test(groups=['sign_in_page', ])
class LinksOnSignInPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3962'
        cls.home_page = HomePage()
        cls.login_page = SignInPage()
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.WTP_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['smoke', 'functional', 'positive', ])
    def test_links_on_sign_in_page(self):
        delay = 1
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            step2 = self.login_page.click_on_link(self.driver, 1, delay)
            step3 = self.login_page.go_back_and_wait(self.driver, wtp_signin_page_url)
            step4 = self.login_page.click_on_link(self.driver, 2, delay)
        finally:
            if step1 and step2 and step3 and step4 is True:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
