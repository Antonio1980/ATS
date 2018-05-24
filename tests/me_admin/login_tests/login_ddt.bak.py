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
        self.browser_name = "chrome"
        self.driver = WebDriverFactory.get_browser(self.browser_name)
        self.driver.implicitly_wait(1)
        self.driver.maximize_window()

    @test(groups=['login'])
    @data(*get_csv_data(BaseConfig.W_ME_LOGIN_DATA))
    @unpack
    def test_login(self, username, password):
        driver = self.driver
        driver.get(BaseConfig.ME_BASE_URL)
        user_field = driver.find_element_by_id(LogInPageLocators.USERNAME_FIELD)
        user_field.clear()
        user_field.send_keys(username)
        password_field = driver.find_element_by_id(LogInPageLocators.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(3)
        login_button = driver.find_element_by_xpath(LogInPageLocators.LOGIN_BUTTON)
        driver.find_element_by_xpath(LogInPageLocators.BODY).click()
        login_button.click()
        #time.sleep(10)
        homepage_label = driver.find_element_by_xpath(HomePageLocators.HOME_PAGE_LABEL)
        time.sleep(3)
        driver.find_element_by_xpath(LogInPageLocators.BODY).click()
        dropdown = driver.find_element_by_xpath(HomePageLocators.SETTINGS_DROPDOWN)
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











