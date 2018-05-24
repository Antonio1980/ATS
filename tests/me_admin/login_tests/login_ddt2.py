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
        self.browser.go_to_url(BaseConfig.ME_BASE_URL)
        user_field = self.browser.find_element_by(LogInPageLocators.USERNAME_FIELD, by_id)
        user_field.clear()
        user_field.send_keys(username)
        password_field = self.browser.find_element_by(LogInPageLocators.PASSWORD_FIELD, by_id)
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(3)
        login_button = self.browser.click_on_element(LogInPageLocators.LOGIN_BUTTON)
        self.browser.click_on_element(LogInPageLocators.BODY)
        assert self.browser.wait_element_visible(HomePageLocators.HOME_PAGE_LABEL)
        time.sleep(3)
        self.browser.click_on_element(LogInPageLocators.BODY)
        dropdown = self.browser.click_on_element(HomePageLocators.SETTINGS_DROPDOWN)
        dropdown.click()
        time.sleep(3)
        logoff = driver.find_element_by_xpath(HomePageLocators.LOGOFF_BUTTON)
        logoff.click()
        time.sleep(3)
        logoff_conf = driver.find_element_by_xpath(HomePageLocators.LOGOFF_CONFIRM_BUTTON)
        logoff_conf.click()
        user_field.clear()
        password_field.clear()
        user_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        assert homepage_label

    @classmethod
    def tearDownClass(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
        self.driver.close()











