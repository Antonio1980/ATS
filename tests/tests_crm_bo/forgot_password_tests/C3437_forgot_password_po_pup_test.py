# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.tests_crm_bo.pages import login_page_url
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.engine import write_file_result, update_test_case
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


@test(groups=['login_page', ])
class ForgotPasswordPopUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3437'
        cls.login_page = LogInPage()
        cls.locators = LogInPageLocators()
        cls.test_run = cls.login_page.TESTRAIL_RUN
        cls.results = cls.login_page.CRM_TESTS_RESULT
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)

    @test(groups=['sanity', 'gui', 'positive', ])
    def test_forgot_password_popup(self):
        header = "Forgotten your password?"
        delay = 1
        result1, result2 = False, False
        try:
            self.login_page.go_to_url(self.driver, self.login_page.crm_base_url)
            self.login_page.driver_wait(self.driver, delay)
            assert login_page_url == self.login_page.get_cur_url(self.driver)
            assert self.login_page.wait_element_visible(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay + 1)
            self.login_page.click_on_element_by_locator(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay + 2)
            popup = self.login_page.wait_element_presented(self.driver, self.locators.POPUP_FORGOT_PASSWORD, delay + 2)
            message = self.login_page.wait_element_presented(self.driver, self.locators.POPUP_MESSAGE, delay + 2)
            send = self.login_page.find_element_by(self.driver, self.locators.POPUP_SEND_BUTTON_ID, "id")
            note = self.login_page.wait_element_presented(self.driver, self.locators.POPUP_NOTE_MESSAGE, delay + 2)
            close = self.login_page.wait_element_presented(self.driver, self.locators.POPUP_CLOSE_BUTTON, delay + 1)
            popup_html = self.login_page.get_element_span_html(popup)
            if header in popup_html:
                if (message is not None) and (send is not None):
                    result1 = True
                    if (note is not None) and (close is not None):
                        result2 = True
        finally:
            if result1 and result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
