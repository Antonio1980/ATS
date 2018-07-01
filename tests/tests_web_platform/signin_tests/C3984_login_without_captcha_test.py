# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import LogInPage
from tests.tests_web_platform.pages import wtp_login_page_url, wtp_dashboard_url
from tests.tests_web_platform.locators.login_page_locators import LogInPageLocators


@test(groups=['login_page', ])
class LogInWithoutCaptchaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home_page = HomePage()
        cls.login_page = LogInPage()
        cls.test_case = '3984'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.email = "fresh_blood_31@mailinator.com"
        cls.password = "1Aa@<>12"

    @classmethod
    @test(groups=['smoke', 'functional', 'negative', ])
    def test_login_negative(cls):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = cls.home_page.open_login_page(cls.driver, delay)
            cls.login_page.wait_driver(cls.driver, delay + 3)
            username_field = cls.login_page.find_element(cls.driver, LogInPageLocators.USERNAME_FIELD)
            cls.login_page.click_on_element(username_field)
            cls.login_page.send_keys(username_field, cls.email)
            password_true_field = cls.login_page.find_element(cls.driver, LogInPageLocators.PASSWORD_TRUE_FIELD)
            password_field = cls.login_page.find_element(cls.driver, LogInPageLocators.PASSWORD_FIELD)
            cls.login_page.click_on_element(password_field)
            cls.login_page.send_keys(password_true_field, cls.password)
            cls.login_page.driver_wait(cls.driver, delay + 5)
            login_button = cls.login_page.find_element(cls.driver, LogInPageLocators.SIGNIN_BUTTON)
            cls.login_page.click_on_element(login_button)
            cls.login_page.driver_wait(cls.driver, delay + 2)
            if cls.login_page.find_element(cls.driver, LogInPageLocators.CAPTCHA_ERROR):
                result2 = True
        finally:
            if result1 and result2 is True:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)