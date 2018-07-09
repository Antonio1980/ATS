# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages import login_page_url
from src.test_utils.file_utils import write_file_result
from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


@test(groups=['login_page', ])
class ForgotPasswordPopUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_page = BasePage()
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3437'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'gui', 'positive', ])
    def test_forgot_password_popup(self):
        header = "Forgotten your password?"
        delay = 1
        result1, result2 = False, False
        try:
            self.base_page.go_to_url(self.driver, self.base_page.crm_base_url)
            self.base_page.driver_wait(self.driver, delay)
            assert login_page_url == self.base_page.get_cur_url(self.driver)
            assert self.base_page.wait_element_visible(self.driver, LogInPageLocators.FORGOT_PASSWORD_LINK, delay + 1)
            self.base_page.click_on_element_by_locator(self.driver, LogInPageLocators.FORGOT_PASSWORD_LINK, delay + 2)
            popup = self.base_page.wait_element_presented(self.driver, LogInPageLocators.POPUP_FORGOT_PASSWORD,
                                                          delay + 2)
            message = self.base_page.wait_element_presented(self.driver, LogInPageLocators.POPUP_MESSAGE, delay + 2)
            send = self.base_page.find_element_by(self.driver, LogInPageLocators.POPUP_SEND_BUTTON_ID, "id")
            note = self.base_page.wait_element_presented(self.driver, LogInPageLocators.POPUP_NOTE_MESSAGE, delay + 2)
            close = self.base_page.wait_element_presented(self.driver, LogInPageLocators.POPUP_CLOSE_BUTTON, delay + 1)
            popup_html = self.base_page.get_element_span_html(popup)
            if header in popup_html:
                if (message is not None) & (send is not None):
                    result1 = True
                    if (note is not None) & (close is not None):
                        result2 = True
        finally:
            if result1 and result2 is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.base_page.close_browser(cls.driver)
