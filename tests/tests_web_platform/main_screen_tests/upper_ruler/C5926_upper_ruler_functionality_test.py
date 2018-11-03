# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer import RegisteredCustomer
from src.base.base_exception import AutomationError
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import main_screen_locators
from tests.tests_web_platform.pages.main_screen_page import MainScreenPage


@ddt
@test(groups=['home_page', 'upper_ruler', ])
class UpperRulerFunctionalTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5926'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.locators = main_screen_locators
        self.password = self.customer.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.main_screen_page = MainScreenPage()
        self.email = self.customer.pended_email
        self.results = BaseConfig.WTP_TESTS_RESULT
        self.browser = self.customer.get_browser_functionality()

    @test(groups=['sanity', 'positive', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_upper_ruler_functional(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6 = False, True, True, False, True, True
        try:
            self.home_page.open_home_page(self.driver, delay)
            try:
                sign_up_button = self.browser.find_element(self.driver, self.locators.SIGH_UP_BUTTON)
                self.browser.try_click(self.driver, sign_up_button, 5)
                assert self.browser.find_element(self.driver, self.locators.REGISTRATION_FORM)
                self.browser.go_back(self.driver)
                sign_in_button = self.browser.find_element(self.driver, self.locators.SIGH_IN_BUTTON)
                self.browser.try_click(self.driver, sign_in_button, 2)
                step1 = self.signin_page.sign_in(self.driver, self.email, self.password)
                step2 = self.browser.execute_js(self.driver, self.main_screen_page.script_signin_button)
                step3 = self.browser.execute_js(self.driver, self.main_screen_page.script_signup_button)
                assert self.browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
                user_name_on_upper_ruller_small_arrow = self.browser.find_element(self.driver, self.locators.USER_NAME_ON_UPPER_RULER)
                self.browser.try_click(self.driver, user_name_on_upper_ruller_small_arrow, 2)
                assert self.browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
                assert self.browser.wait_element_presented(self.driver, self.locators.USER_PROFILE_PANEL, delay)
                funds_button = self.browser.find_element(self.driver, self.locators.FUNDS_BUTTON)
                self.browser.try_click(self.driver, funds_button, 2)
                assert self.browser.find_element_by(self.driver, self.locators.FUNDS_PANEL_ID, "id")
                self.browser.try_click(self.driver, funds_button, 2)
                step4 = self.browser.execute_js(self.driver, self.main_screen_page.script_signin_button)
                step5 = self.browser.execute_js(self.driver, self.main_screen_page.script_signup_button)
                assert self.browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
                assert self.browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
                assert self.browser.wait_element_presented(self.driver, self.locators.TIME_ON_UPPER_RULER, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.DATE_ON_UPPER_RULER, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.LANGUAGE_FLAG, delay)
                assert self.browser.wait_element_presented(self.driver, self.locators.LOGOUT_BUTTON, delay)
                step6 = True
            except AutomationError as e:
                print("{0} test_upper_ruler_functional failed with error: {1}".format(e.__class__.__name__, e.__cause__))

        finally:
            if step1 and step6 is True and step2 and step3 and step4 and step5 is False:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        self.browser.close_browser(self.driver)
