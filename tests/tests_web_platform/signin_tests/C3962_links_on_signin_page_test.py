# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.home_page import HomePage
from src.base.instruments import write_file_result, update_test_case
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
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.home_page.open_login_page(self.driver, delay)
            # Option 1- forgot password, Option 2- register link
            result2 = self.login_page.click_on_link(self.driver, 1, delay)
            result3 = self.login_page.go_back_and_wait(self.driver, wtp_signin_page_url, delay)
            result4 = self.login_page.click_on_link(self.driver, 2, delay)
        finally:
            if result1 and result2 and result3 and result4 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)