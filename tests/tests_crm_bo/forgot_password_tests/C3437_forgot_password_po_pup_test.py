# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages import login_page_url
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


@ddt
@test(groups=['login_page', ])
class ForgotPasswordPopUpTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '3437'
        self.login_page = LogInPage()
        self.locators = LogInPageLocators()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results_file = BaseConfig.CRM_TESTS_RESULT

    @test(groups=['sanity', 'gui', 'positive', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_forgot_password_popup(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        header = "Forgotten your password?"
        delay = 5
        step1, step2 = False, False
        try:
            self.login_page.go_to_url(self.driver, self.login_page.crm_base_url)
            assert Browser.wait_url_contains(self.driver, login_page_url, delay)
            assert Browser.wait_element_visible(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
            Browser.click_on_element_by_locator(self.driver, self.locators.FORGOT_PASSWORD_LINK, delay)
            popup = Browser.wait_element_presented(self.driver, self.locators.POPUP_FORGOT_PASSWORD, delay)
            message = Browser.wait_element_presented(self.driver, self.locators.POPUP_MESSAGE, delay)
            send = Browser.find_element_by(self.driver, self.locators.POPUP_SEND_BUTTON_ID, "id")
            note = Browser.wait_element_presented(self.driver, self.locators.POPUP_NOTE_MESSAGE, delay)
            close = Browser.wait_element_presented(self.driver, self.locators.POPUP_CLOSE_BUTTON, delay)
            popup_html = Browser.get_element_span_html(popup)
            if header in popup_html:
                if message and send:
                    step1 = True
                    if note and close:
                        step2 = True
        finally:
            if step1 and step2 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
