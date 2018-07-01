# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.open_account_page import OpenAccountPage
from tests.tests_web_platform.pages import wtp_dashboard_url, wtp_open_account_url


@test(groups=['login_page', ])
class LinksOnVerifyEmailScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.open_account_page = OpenAccountPage()
        cls.email = cls.open_account_page.email
        cls.password = "1Aa@<>12"
        cls.first_last_name = "QAtestQA"
        cls.test_case = '3964'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @classmethod
    @test(groups=['smoke', 'functional', 'positive', ])
    def test_links_on_verify_email_screen(cls):
        delay = 1
        result1, result2, result3, result4, result5, result6 = False, False, False, False, False, False
        try:
            result1 = cls.home_page.open_signup_page(cls.driver, delay)
            result2 = cls.open_account_page.fill_signup_form(cls.driver, cls.first_last_name, cls.email, cls.password)
            # 1 - email verified link, 2 - go back link, 3 - email not sent link
            result3 = cls.open_account_page.click_on_link(cls.driver, wtp_open_account_url, 1)
            #res1 = cls.home_page.go_back_and_wait(cls.driver, wtp_open_account_url, delay)
            result4 = cls.open_account_page.click_on_link(cls.driver, wtp_dashboard_url, 2)
            res2 = cls.home_page.go_back_and_wait(cls.driver, wtp_open_account_url, delay)
            result5 = cls.open_account_page.click_on_link(cls.driver, wtp_open_account_url, 3)
            time.sleep(15)
            # Opens email box, clicks on "Very email" button and checks that redirected to OpenAccountPage url.
            result6 = cls.open_account_page.get_email_updates(cls.driver, cls.open_account_page.email, 3)
        finally:
            if result1 and result2 and result3 and result4 and result5 and result6 is True:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
