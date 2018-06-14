# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


@test(groups=['tests_end2end', 'functional', 'sanity'])
class ForgotPasswordPopUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_page = BasePage()
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3437'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_forgot_password_popup(cls):
        header = "Forgotten your password?"
        delay = 1
        result1, result2 = False, False
        try:
            cls.base_page.go_to_url(cls.driver, cls.base_page.crm_base_url)
            cls.base_page.driver_wait(cls.driver, delay)
            assert cls.login_page.login_page_url == cls.base_page.get_cur_url(cls.driver)
            assert cls.base_page.wait_element_visible(cls.driver, delay + 1, LogInPageLocators.FORGOT_PASSWORD_LINK)
            cls.base_page.click_on_element_by_locator(cls.driver, delay + 2, LogInPageLocators.FORGOT_PASSWORD_LINK)
            popup = cls.base_page.wait_element_presented(cls.driver, delay + 2, LogInPageLocators.POPUP_FORGOT_PASSWORD)
            message = cls.base_page.wait_element_presented(cls.driver, delay + 2, LogInPageLocators.POPUP_MESSAGE)
            send = cls.base_page.find_element_by(cls.driver, LogInPageLocators.POPUP_SEND_BUTTON_ID, "id")
            note = cls.base_page.wait_element_presented(cls.driver, delay + 2, LogInPageLocators.POPUP_NOTE_MESSAGE)
            close = cls.base_page.wait_element_presented(cls.driver, delay + 1, LogInPageLocators.POPUP_CLOSE_BUTTON)
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
        cls.base_page.close_browser(cls.driver)
