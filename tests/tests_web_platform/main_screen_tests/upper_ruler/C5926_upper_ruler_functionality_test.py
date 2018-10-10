# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest

import selenium
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.main_screen_page import MainScreenPage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import main_screen_locators


@ddt
@test(groups=['home_page', 'upper_ruler', ])
class MainTradingScreenTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '5926'
        self.home_page = HomePage()
        self.locators = main_screen_locators
        self.signin_page = SignInPage()
        self.email = self.signin_page.email
        self.main_screen_page = MainScreenPage()
        self.password = self.signin_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['sanity', 'positive', 'ui', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_main_trading_screen(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3, step4, step5, step6 = False, True, True, False, True, True
        try:
            self.home_page.open_home_page(self.driver, delay)

            try:
                sign_up_button = Browser.find_element(self.driver, self.locators.SIGH_UP_BUTTON)
                Browser.try_click(self.driver, sign_up_button, 5)
                assert Browser.find_element(self.driver, self.locators.REGISTRATION_FORM)
                Browser.go_back(self.driver)
                sign_in_button = Browser.find_element(self.driver, self.locators.SIGH_IN_BUTTON)
                Browser.try_click(self.driver, sign_in_button, 2)
                step1 = self.signin_page.sign_in(self.driver, self.email, self.password)
                step2 = Browser.execute_js(self.driver, self.main_screen_page.script_signin_button)
                step3 = Browser.execute_js(self.driver, self.main_screen_page.script_signup_button)
                assert Browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
                user_name_on_upper_ruller_small_arrow = Browser.find_element(self.driver, self.locators.USER_NAME_ON_UPPER_RULER)
                Browser.try_click(self.driver, user_name_on_upper_ruller_small_arrow, 2)
                assert Browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
                assert Browser.wait_element_presented(self.driver, self.locators.USER_PROFILE_PANEL, delay)
                funds_button = Browser.find_element(self.driver, self.locators.FUNDS_BUTTON)
                Browser.try_click(self.driver, funds_button, 2)
                assert Browser.find_element_by(self.driver, self.locators.FUNDS_PANEL_ID, "id")
                Browser.try_click(self.driver, funds_button, 2)
                step4 = Browser.execute_js(self.driver, self.main_screen_page.script_signin_button)
                step5 = Browser.execute_js(self.driver, self.main_screen_page.script_signup_button)
                assert Browser.wait_element_presented(self.driver, self.locators.USER_NAME_ON_UPPER_RULER, delay)
                assert Browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
                assert Browser.wait_element_presented(self.driver, self.locators.TIME_ON_UPPER_RULER, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.DATE_ON_UPPER_RULER, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.LANGUAGE_FLAG, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.LOGOUT_BUTTON, delay)
                step6 = True
            except Exception as e:
                print("Exception is occurred.".format(e))

        finally:
            if step1 and step6 is True and step2 and step3 and step4 and step5 is False:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
