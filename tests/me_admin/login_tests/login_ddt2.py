# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from src.drivers.webdriver_factory import WebDriverFactory
from tests.me_admin.locators.home_page_locators import HomePageLocators
from tests.me_admin.locators.login_page_locators import LogInPageLocators



@test(groups=['end2end'])
@ddt
class LogInTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.browser = Browser
        self.browser.set_up_class("chrome")

    @test(groups=['login'])
    @data(*get_csv_data(BaseConfig.W_ME_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        by_id = "ID"
        by_xpath = "XPATH"
        delay = 3
        self.browser.go_to_url(BaseConfig.ME_BASE_URL)
        self.browser.send_keys(delay, LogInPageLocators.USERNAME_FIELD, username)
        self.browser.send_keys(delay, LogInPageLocators.PASSWORD_FIELD, password)
        self.browser.click_on_element(delay, LogInPageLocators.LOGIN_BUTTON)
        #self.browser.click_on_element(delay, LogInPageLocators.BODY)
        assert self.browser.wait_element_visible(delay, HomePageLocators.HOME_PAGE_LABEL)
        self.browser.click_on_element(delay, LogInPageLocators.BODY)
        self.browser.click_on_element(delay, HomePageLocators.SETTINGS_DROPDOWN)
        self.browser.click_on_element(delay, HomePageLocators.LOGOFF_BUTTON)
        self.browser.driver_wait(delay)
        self.browser.click_on_element(delay, HomePageLocators.LOGOFF_CONFIRM_BUTTON)
        self.browser.send_keys(delay, LogInPageLocators.USERNAME_FIELD, username)
        self.browser.send_keys(delay, LogInPageLocators.PASSWORD_FIELD, password)
        self.browser.click_on_element(delay, LogInPageLocators.LOGIN_BUTTON)
        

    @classmethod
    def tearDownClass(self):
        self.browser.tear_down_class()











