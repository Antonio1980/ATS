# !/usr/bin/env python
# -*- coding: utf8 -*-
import os
import unittest

from ddt import ddt, data, unpack
from selenium import webdriver
from proboscis import test
from tests_extensions.get_tests_context import get_csv_data
from tests_resources.locators.home_page_locators import HomePageLocators
from tests_resources.locators.login_page_locators import LogInPageLocators
from tests_configuration.tests_definitions import BaseConfig


@test(groups=['end2end'])
@ddt
class LogInTest(unittest.TestCase):
    @classmethod
    def setUpClass(slc):
        slc.driver = webdriver.Chrome(BaseConfig.W_CHROME_PATH)
        slc.driver.implicitly_wait(1)
        slc.driver.maximize_window()

    @test(groups=['login'])
    @data(*get_csv_data(BaseConfig.W_TEST_DATA))
    @unpack
    def test_login(self, username, password):
        driver = self.driver
        driver.get(BaseConfig.BASE_URL)
        user_field = driver.find_element_by_xpath(LogInPageLocators.USERNAME_FIELD)
        user_field.click()
        #driver.implicitly_wait(3)
        user_field.send_keys(username)
        password_field = driver.find_element_by_xpath(LogInPageLocators.PASSWORD_FIELD)
        password_field.click()
        password_field.send_keys(password)
        login_button = driver.find_element_by_xpath(LogInPageLocators.LOGIN_BUTTON).click()
        homepage_label = driver.find_element_by_xpath(HomePageLocators.HOME_PAGE_LABEL)
        driver.find_element_by_xpath(HomePageLocators.SETTINGS_DROPDOWN).click()
        driver.find_element_by_xpath(HomePageLocators.LOGOFF_BUTTON).click()
        driver.find_element_by_xpath(HomePageLocators.LOGOFF_CONFIRM_BUTTON).click()
        user_field.clear()
        password_field.clear()
        user_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        assert homepage_label

    @classmethod
    def tearDownClass(slc):
        slc.driver.delete_all_cookies()
        slc.driver.quit()
        slc.driver.close()











