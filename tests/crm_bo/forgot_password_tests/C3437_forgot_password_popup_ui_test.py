# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.base_page import BasePage
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory
from tests.crm_bo.locators.login_page_locators import LogInPageLocators


@test(groups=['end2end_tests', 'functional', 'sanity'])
class ForgotPasswordPopUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_page = BasePage()
        cls.login_page = LogInPage()
        cls._driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3437'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password_popup(cls):
        header = "Forgotten your password?"
        delay = 1
        result1, result2 = False, False
        try:
            cls.base_page.go_to_url(cls._driver, cls.base_page.crm_base_url)
            cls.base_page.driver_wait(cls._driver, delay)
            assert cls.login_page.login_page_url == cls.base_page.get_cur_url(cls._driver)
            assert cls.base_page.wait_element_visible(cls._driver, delay + 1, LogInPageLocators.FORGOT_PASSWORD_LINK)
            cls.base_page.click_on_element_by_locator(cls._driver, delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
            popup = cls.base_page.wait_element_presented(cls._driver, delay + 2, LogInPageLocators.POPUP_FORGOT_PASSWORD)
            message = cls.base_page.wait_element_presented(cls._driver, delay + 2, LogInPageLocators.POPUP_MESSAGE)
            send = cls.base_page.find_element_by(cls._driver, LogInPageLocators.POPUP_SEND_BUTTON_ID, "id")
            note = cls.base_page.wait_element_presented(cls._driver, delay + 2, LogInPageLocators.POPUP_NOTE_MESSAGE)
            close = cls.base_page.wait_element_presented(cls._driver, delay + 1, LogInPageLocators.POPUP_CLOSE_BUTTON)
            popup_html = cls.base_page.get_element_span_html(popup)
            if header in popup_html:
                if (message is not None) & (send is not None):
                    result1 = True
                    if (note is not None) & (close is not None):
                        result2 = True
        finally:
            if result1 & result2 is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.base_page.close_browser(cls._driver)
