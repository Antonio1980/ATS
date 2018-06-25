# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages import wtp_login_page_url
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.login_page import LogInPage
from tests.tests_web_platform.locators.login_page_locators import LogInPageLocators


@test(groups=['login_page', ])
class LogInPageUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.test_case = '3671'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @classmethod
    @test(groups=['smoke', 'gui', 'positive', ])
    def test_login_page_ui(cls):
        delay = 3
        result1, result2 = False, False
        try:
            result1 = cls.home_page.open_login_page(cls.driver, delay)
            try:
                assert wtp_login_page_url == cls.login_page.get_cur_url(cls.driver)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.SIGNIN_TITLE)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.USERNAME_FIELD)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.PASSWORD_FIELD)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.CAPTCHA_FRAME)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.KEEP_ME_CHECKBOX)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.SIGNIN_BUTTON)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.FORGOT_PASSWORD_LINK)
                assert cls.login_page.search_element(cls.driver, delay, LogInPageLocators.REGISTER_LINK)
                result2 = True
            except TimeoutError:
                print("Time out occurred.")
        finally:
            if result1 & result2 is True:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)