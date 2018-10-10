# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@ddt
@test(groups=['sign_up_page', ])
class EmailVerifiedUITest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6164'
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.password = self.signup_page.password
        self.email = self.signup_page.mailinator_email
        self.results_file = BaseConfig.WTP_TESTS_RESULT
        self.username = self.signup_page.mailinator_username
        self.locators = self.signup_page.locators
        self.base_locators = self.signup_page.base_locators
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    @test(groups=['smoke', 'gui', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_ui_verified_email(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.open_signup_page(self.driver, delay)
            step2 = self.signup_page.fill_signup_form(self.driver, self.username, self.email, self.password, self.element)
            try:
                mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}".format(self.username)
                Browser.go_to_url(self.driver, mailinator_box_url)
                time.sleep(delay)
                pause_button = Browser.find_element_by(self.driver, self.base_locators.PAUSE_BUTTON_ID, "id")
                Browser.click_on_element(pause_button)
                email_item = Browser.search_element(self.driver, self.base_locators.FIRST_EMAIL, delay)
                Browser.click_on_element(email_item)
                mail_frame = Browser.find_element(self.driver, "//iframe[@id='msg_body']")
                Browser.switch_frame(self.driver, mail_frame)
                button = Browser.find_element(self.driver, self.base_locators.VERIFY_EMAIL_BUTTON)
                Browser.click_with_offset(self.driver, button, 10, 10)
                new_window = self.driver.window_handles
                Browser.switch_window(self.driver, new_window[1])
                assert Browser.find_element(self.driver, self.locators.CONTINUE_BUTTON)
                # assert Browser.find_element(self.driver, self.locators.GO_BACK_LINK_V)
                step3 = True
            except Exception as e:
                print("Exception is occurred. ".format(e))
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
