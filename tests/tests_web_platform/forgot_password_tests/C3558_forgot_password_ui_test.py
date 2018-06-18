# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.test_definitions import BaseConfig
from tests.tests_web_platform.locators.forgot_password_page_locators import ForgotPasswordPageLocators
from tests.tests_web_platform.pages import forgot_password_page_url
from tests.tests_web_platform.pages.home_page import HomePage
from src.test_utils.testrail_utils import update_test_case
from tests.tests_web_platform.pages.login_page import LogInPage


@test(groups=['end2end_tests', 'functional', 'sanity'])
class ForgotPasswordUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3558'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password_page_ui(cls):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = cls.home_page.open_login_page(cls.driver, delay)
            result2 = cls.login_page.click_on_forgot_password(cls.driver, delay)
            cls.login_page.driver_wait(cls.driver, delay)
            assert forgot_password_page_url == cls.login_page.get_cur_url(cls.driver)
            assert cls.login_page.wait_element_presented(cls.driver, delay, ForgotPasswordPageLocators.FORGOT_PASSWORD_TITLE)
            cls.login_page.wait_element_presented(cls.driver, delay, ForgotPasswordPageLocators.EMAIL_TEXT_FIELD)
        finally:
            if result1 & result2 is True:
                if cls.login_page.wait_element_presented(cls.driver, delay, ForgotPasswordPageLocators.SUBMIT_BUTTON):
                    update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls.driver)
