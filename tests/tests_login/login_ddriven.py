# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest

from ddt import ddt, data, unpack
from proboscis import test
from tests_extensions.get_tests_context import get_csv_data
from tests_resources.locators.home_page_locators import HomePageLocators
from tests_resources.locators.login_page_locators import LogInPageLocators
from tests_extensions.tests_definitions import BaseConfig
from tests_extensions.webdriver_factory import WebDriverFactory


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
    @data(*get_csv_data(BaseConfig.W_TEST_DATA))
    @unpack
    def test_login(self, username, password):
        un = username
        ps = password
        driver = self.driver
        driver.get(BaseConfig.BASE_URL)
        user_field = driver.find_element_by_xpath(LogInPageLocators.USERNAME_FIELD)
        user_field.click()
        user_field.send_keys(un)
        password_field = driver.find_element_by_xpath(LogInPageLocators.PASSWORD_FIELD)
        password_field.click()
        password_field.send_keys(ps)
        login_button = driver.find_element_by_xpath(LogInPageLocators.LOGIN_BUTTON) 
        login_button.click()
        assert driver.find_element_by_xpath(HomePageLocators.HOME_PAGE_LOGO)


    @classmethod
    def tearDownClass(slc):
        slc.driver.delete_all_cookies()
        slc.driver.quit()
        slc.driver.close()











