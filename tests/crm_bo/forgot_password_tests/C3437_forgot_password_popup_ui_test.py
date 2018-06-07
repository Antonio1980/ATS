# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.crm_bo.locators.login_page_locators import LogInPageLocators
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case


@test(groups=['end2end_tests', 'functional', 'sanity'])
class ForgotPasswordPopUpTest(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_login_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '3437'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password_popup(cls):
        header = "Forgotten your password?"
        delay = 1
        result1, result2 = False, False
        try:
            cls.go_to_url(cls.base_url)
            assert cls.login_page_url == cls.get_cur_url()
            assert cls.wait_element_visible(delay + 1, LogInPageLocators.FORGOT_PASSWORD_LINK)
            cls.click_on_element_by_locator(delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
            popup = cls.wait_element_presented(delay + 2, LogInPageLocators.POPUP_FORGOT_PASSWORD)
            message = cls.wait_element_presented(delay + 2, LogInPageLocators.POPUP_MESSAGE)
            send = cls.find_element_by(LogInPageLocators.POPUP_SEND_BUTTON_ID, "id")
            note = cls.wait_element_presented(delay + 2, LogInPageLocators.POPUP_NOTE_MESSAGE)
            close = cls.wait_element_presented(delay + 1, LogInPageLocators.POPUP_CLOSE_BUTTON)
            popup_html = cls.get_element_span_html(popup)
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
        cls.close_browser()
